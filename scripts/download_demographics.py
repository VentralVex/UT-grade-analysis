"""Download the external (non-grade) data used by grade_analysis.ipynb.

Sources
- UT Austin "Trends in Student Data" dashboard (reports.utexas.edu/spotlight-data/students): Fall headcount by
  classification and by federal gender category, via the dashboard's public Tableau CSV export.
- IPEDS (NCES) via the Urban Institute Education Data API: full-time instructional staff (faculty) and
  full-time non-instructional staff for UT Austin (unitid 228778).
- U.S. Census Bureau Vintage 2025 population estimates (July 1, 2025): Texas counties and states.
- World Bank WDI SP.POP.TOTL (2025): national populations and the list of economies.
- UNESCO Institute for Statistics indicator 25053: enrolment in tertiary education, all programmes (latest year since 2005);
  Taiwan (not in UIS): Ministry of Education, Education in Taiwan 2025-2026, SY2022 (1,140,089 students).
- UT course catalog "Courses A-Z": course prefix -> full name (data/reference/course_prefixes.csv).
- Map outlines (GeoJSON): Plotly's Census county file, PublicaMundi US states, Natural Earth 110m countries.
- UT Graduate School "Admissions & Enrollment Statistics" dashboard (graduate.utexas.edu), S/Fall 2025 cycle:
  selectivity & yield, average GPA and average GRE tabs.
"""
import io, json, os, re, urllib.parse
import pandas as pd
import requests

ROOT = os.path.join(os.path.dirname(__file__), '..', 'data')
DEMO, REF, GRAD = f'{ROOT}/demographics', f'{ROOT}/reference', f'{ROOT}/grad school'
for d in (DEMO, REF, f'{REF}/geo', GRAD):
    os.makedirs(d, exist_ok=True)
TABLEAU = 'https://iq-analytics.austin.utexas.edu'
UT_UNITID = 228778


def tableau_csv(view, params):
    r = requests.get(f'{TABLEAU}/views/{view}.csv?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote), timeout=300)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), thousands=',')


def ut_students():
    # Empty "c.dynamic year range" removes the dashboard's default 2017+ window (data then starts Fall 2009).
    base = {'c.dynamic year range': '', 'p.select third column': 'Leave empty'}
    for label, col in [('classification', 'Classification'), ('gender', 'Federal gender categories')]:
        d = tableau_csv('Spotlightondata/Stathandbook', {**base, 'p.select second column': col})
        d = d.rename(columns={'c.select second column': label, 'c.semester first day year': 'fall_year',
                              'Number of Records': 'students'})[['fall_year', label, 'students']]
        d.to_csv(f'{DEMO}/ut_students_by_{label}.csv', index=False)
        print(label, d.fall_year.min(), d.fall_year.max(), len(d))


def ipeds_staff():
    api = 'https://educationdata.urban.org/api/v1/college-university/ipeds'
    rows = []
    for year in range(2009, 2026):
        ins = requests.get(f'{api}/salaries-instructional-staff/{year}/', params={'unitid': UT_UNITID}, timeout=120).json().get('results', [])
        non = requests.get(f'{api}/salaries-noninstructional-staff/{year}/', params={'unitid': UT_UNITID}, timeout=120).json().get('results', [])
        # contract-length codes change over the years; the all-contracts total is always the largest count (-1 = missing)
        fac = [max(r['instruc_staff_count'] for r in ins if r['academic_rank'] == 99 and r['sex'] == 99)] if ins else []
        stf = [r['noninstruc_staff_count'] for r in non if r['staff_category'] == 99]
        if fac or stf:
            rows.append({'fall_year': year, 'ft_instructional_faculty': fac[0] if fac else None,
                         'ft_noninstructional_staff': stf[0] if stf else None})
    d = pd.DataFrame(rows)
    d.to_csv(f'{DEMO}/ut_faculty_staff_ipeds.csv', index=False)
    print('ipeds', d.fall_year.min(), d.fall_year.max())


def census():
    url = 'https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv'
    d = pd.read_csv(url, encoding='latin1', dtype={'STATE': str, 'COUNTY': str})
    tx = d[(d.SUMLEV == 50) & (d.STNAME == 'Texas')]
    tx = pd.DataFrame({'fips': tx.STATE + tx.COUNTY, 'county': tx.CTYNAME.str.replace(' County', '', regex=False),
                       'population_2025': tx.POPESTIMATE2025})
    tx.to_csv(f'{REF}/tx_county_population_2025.csv', index=False)
    st = d[d.SUMLEV == 40][['STATE', 'STNAME', 'POPESTIMATE2025']]
    st.columns = ['fips', 'state', 'population_2025']
    st.to_csv(f'{REF}/state_population_2025.csv', index=False)
    print('census', len(tx), len(st))


def world_bank():
    econ = requests.get('https://api.worldbank.org/v2/country?format=json&per_page=400', timeout=120).json()[1]
    econ = {e['id']: e for e in econ if e['region']['id'] != 'NA'}          # drop regional aggregates
    pop = requests.get('https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&mrv=1&per_page=400',
                       timeout=120).json()[1]
    d = pd.DataFrame([{'iso3': p['countryiso3code'], 'country': p['country']['value'], 'year': int(p['date']),
                       'population': p['value']} for p in pop if p['countryiso3code'] in econ])
    # Taiwan is not in World Bank data: Ministry of the Interior household registration, end of September 2025.
    d = pd.concat([d, pd.DataFrame([{'iso3': 'TWN', 'country': 'Taiwan', 'year': 2025, 'population': 23_317_031}])])
    d.to_csv(f'{REF}/world_population.csv', index=False)
    print('world bank', len(d), d.year.value_counts().to_dict())


def tertiary_enrollment():
    """College enrollment per country (UNESCO UIS 25053), latest available year since 2005."""
    r = requests.get('https://api.uis.unesco.org/api/public/data/indicators', timeout=300,
                     params={'indicator': '25053', 'start': 2005, 'end': 2025, 'geoUnitType': 'NATIONAL'})
    d = pd.DataFrame(r.json()['records']).dropna(subset=['value'])
    d = d.sort_values('year').groupby('geoUnit').tail(1)
    d = d.rename(columns={'geoUnit': 'iso3', 'value': 'tertiary_students'})[['iso3', 'year', 'tertiary_students']]
    d = pd.concat([d, pd.DataFrame([{'iso3': 'TWN', 'year': 2022, 'tertiary_students': 1_140_089}])])
    d.to_csv(f'{REF}/tertiary_enrollment_uis.csv', index=False)
    print('uis tertiary', len(d), d.year.value_counts().sort_index().to_dict())



def course_prefixes():
    """Course prefix -> name from the UT catalog's Courses A-Z page."""
    import html
    page = requests.get('https://catalog.utexas.edu/general-information/coursesatoz/', timeout=120).text
    rows = {}
    for text in re.findall(r'<a href="/general-information/coursesatoz/[^"]+/">([^<]+)</a>', page):
        prefix, _, name = html.unescape(text).replace('\u200b', '').partition(' -')
        rows[prefix.strip()] = name.strip()
    pd.Series(rows, name='Prefix Name').rename_axis('Course Prefix').sort_index().to_csv(f'{REF}/course_prefixes.csv')
    print('course prefixes', len(rows))


def geojson():
    src = {
        'tx_counties.geojson': 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json',
        'us_states.geojson': 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json',
        'world_countries.geojson': 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson',
    }
    for name, url in src.items():
        g = requests.get(url, timeout=120).json()
        if name == 'tx_counties.geojson':
            g['features'] = [f for f in g['features'] if f['id'].startswith('48')]
        json.dump(g, open(f'{REF}/geo/{name}', 'w'))
        print(name, len(g['features']))


def tableau_text_table(wb, view):
    """Rebuild a dashboard text table (School x Program x measures) from the Tableau bootstrap payload (no export button)."""
    s = requests.Session()
    s.get(f'{TABLEAU}/views/{wb}/{view}', params={':embed': 'y', ':showVizHome': 'no'}, timeout=120)
    r = s.post(f'{TABLEAU}/vizql/w/{wb}/v/{view}/startSession/viewing', params={':embed': 'y', ':showVizHome': 'no'}, timeout=120)
    sid, sheet = r.headers['X-Session-Id'], r.json()['sheetId']
    r = s.post(f'{TABLEAU}/vizql/w/{wb}/v/{view}/bootstrapSession/sessions/{sid}', timeout=300, data={
        'sheet_id': sheet, 'worksheetPortSize': '{"w":1000,"h":850}', 'dashboardPortSize': '{"w":1000,"h":850}',
        'clientDimension': '{"w":1200,"h":800}', 'renderMapsClientSide': 'true', 'isBrowserRendering': 'true',
        'browserRenderingThreshold': '100', 'formatDataValueLocally': 'false', 'language': 'en', 'locale': 'en_US'})
    t, parts, i = r.text, [], 0
    while i < len(t):                                   # response = "<len>;<json><len>;<json>"
        m = re.match(r'(\d+);', t[i:])
        start = i + len(m.group(0))
        parts.append(json.loads(t[start:start + int(m.group(1))]))
        i = start + int(m.group(1))
    info = parts[1]['secondaryInfo']['presModelMap']
    values = info['dataDictionary']['presModelHolder']['genDataDictionaryPresModel']['dataSegments']['0']['dataColumns'][0]['dataValues']
    ws = next(iter(info['vizData']['presModelHolder']['genPresModelMapPresModel']['presModelMap'].values()))
    pane = ws['presModelHolder']['genVizDataPresModel']['paneColumnsData']['paneColumnsList'][0]['vizPaneColumns']
    decode = lambda idx: [values[k] if k >= 0 else values[-k - 1] for k in idx]
    long = pd.DataFrame({'School': decode(pane[1]['aliasIndices']), 'Program': decode(pane[2]['aliasIndices']),
                         'Measure': decode(pane[3]['aliasIndices']), 'Value': decode(pane[4]['aliasIndices'])})
    d = long.pivot_table(index=['School', 'Program'], columns='Measure', values='Value', aggfunc='first')
    d.columns = d.columns.str.strip()
    return d.drop(index='All', level='School')


def grad_admissions():
    """Selectivity & Yield, Average GPA and Average GRE tabs (S/Fall 2025 cycle), merged by program.
    GPA and GRE averages are over applicants who reported them ("n" columns)."""
    num = lambda c: pd.to_numeric(c.str.replace(',', '').str.rstrip('%'), errors='coerce')   # blank → NaN
    wb = 'AdmissionsEnrollmentStatistics'
    sy = tableau_text_table(wb, 'SelectivityYield')[['Applied', 'Admitted', 'Enrolled', 'Selectivity', 'Yield']]
    gpa = tableau_text_table(wb, 'AverageGPA').rename(columns={'Average GPA': 'Avg GPA', 'Included in Avg': 'GPA n'})[['Avg GPA', 'GPA n']]
    gre = tableau_text_table(wb, 'AverageGRE').rename(columns={'Avg GRE Verbal': 'Avg GRE Verbal', 'Avg GRE Quant': 'Avg GRE Quant',
                                                               'Avg GRE Writing': 'Avg GRE Writing', 'Included in Avg': 'GRE n'})
    gre = gre[['Avg GRE Verbal', 'Avg GRE Quant', 'Avg GRE Writing', 'GRE n']]
    d = sy.join(gpa).join(gre).apply(num).reset_index()
    for c in ['Applied', 'Admitted', 'Enrolled']:
        d[c] = d[c].astype(int)
    d.insert(0, 'Admissions Cycle', 'S/Fall 2025')
    d.to_csv(f'{GRAD}/admissions_enrollment_sfall2025.csv', index=False)
    print('grad programs', len(d), 'with GPA', d['Avg GPA'].notna().sum(), 'with GRE', d['Avg GRE Quant'].notna().sum())

if __name__ == '__main__':
    import sys
    for step in (sys.argv[1:] or ['course_prefixes', 'ut_students', 'ipeds_staff', 'census', 'world_bank', 'tertiary_enrollment', 'geojson', 'grad_admissions']):
        globals()[step]()
