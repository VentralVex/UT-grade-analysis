# UT-grade-analysis

An analysis of course grade distributions at the University of Texas at Austin from Summer 2011 through Summer 2026, together with context on UT's students, degrees and graduate admissions.

All results, figures and notes are in [`grade_analysis.ipynb`](grade_analysis.ipynb). The saved PNGs are in [`figures/`](figures/).

## What's in the notebook

| Part | Topics |
|---|---|
| **0. Data and preparation** | Sources and caveats, merging 46 semesters, section-level grade averages, course-type dummies (intro, honors, lab, I/II/III, web-based, …) |
| **1. UT at a glance** | Population over time; degrees conferred by college; where students come from (Texas counties, U.S. states, countries: tables, scatterplots and side-by-side maps); graduate program selectivity, yield, and applicant GPA/GRE; enrollment and course offerings by prefix; course size |
| **2. Grades in 2025–26** | Mean grade by course prefix and by field group, the grade distribution, section averages, course-type comparisons |
| **3. Grade trends by major** | Grade trends 2011–2026 for core and engineering prefixes; highest- and lowest-graded courses overall and within each prefix; foreign-language classes |
| **4. COVID and online instruction** | Grades in the COVID year vs Fall 2019; the rise of web-based courses and their grades (including a fixed pool of courses followed through COVID) |
| **5. Same course, different terms** | Fall vs spring vs summer grades for the same courses (2025–26 and every year since 2011); "I" vs "II" course sequences, with a regression |
| **6. Does UT weed students out?** | Following Computer Science (C S 312 → 314 → 429 → 439) and Economics (ECO 304K → … → 320L) cohorts through their core sequences |

## Selected findings

- **Grades rose over the period.** 15 of the 16 prefixes tracked in Part 3 grade higher in 2025–26 than in 2011–12; Chemical Engineering is the exception. Mathematics, for example, rose from 2.85 to 3.33. Grades spiked in Spring 2020, when instruction moved online.
- **COVID raised grades.** Of 1,755 courses offered in both periods, 71% had higher grades in 2020–21 than in Fall 2019 (82% weighted by course size).
- **Online courses grew permanently.** Web-based sections jumped from under 2% of fall/spring sections before 2020 to about 75% during COVID. They settled at about 4% of fall/spring and more than half of summer sections. The 10 largest sections in 2025–26 are all web-based.
- **Weed-out attrition.** On average, cohort enrollment fell 18.5% from C S 314 to C S 439 and 14.2% from ECO 329 to ECO 320L across six cohorts. These are enrollment counts, not tracked students; see the caveats in Part 6.
- **Grades differ by field.** Weighted by course size in 2025–26, the average course grade ranges from 3.46 in natural science to 3.72 in fine arts and design.

## Data sources

| Data | Source |
|---|---|
| Course grade distributions, Summer 2011–Summer 2026 | [UT Course Grade Distributions](https://reports.utexas.edu/spotlight-data/ut-course-grade-distributions) (public Tableau dashboard) |
| Student headcount by classification and gender; degrees conferred; enrollment by county, state and country | [UT Trends in Student Data](https://reports.utexas.edu/spotlight-data/students) |
| Faculty and staff counts | IPEDS, via the [Urban Institute Education Data API](https://educationdata.urban.org) |
| County and state populations (July 2025) | U.S. Census Bureau, Vintage 2025 population estimates |
| National populations (2025) | World Bank WDI; Taiwan from its Ministry of the Interior |
| College enrollment by country | UNESCO Institute for Statistics; Taiwan from its Ministry of Education |
| Graduate applications, admissions, GPA and GRE by program | [UT Graduate School admissions & enrollment statistics](https://graduate.utexas.edu/about/statistics-surveys/admissions-enrollment) |
| Course prefix names | [UT catalog, Courses A–Z](https://catalog.utexas.edu/general-information/coursesatoz/) |
| Map outlines | Census county boundaries (Plotly GeoJSON), PublicaMundi US states, Natural Earth 1:110m countries |

**Caveats.**
- The grade dashboard redacts small sections and sections where everyone (or all but one) received the same grade, and it counts unique students per section.
- "Other" grades (W, Q, CR/NC, incomplete, etc.) are excluded from grade averages but included in course size.
- The notebook lists every judgment call it makes, such as field groupings and language prefixes.

## Reproducing the results

The `data/` folder is not in the repository (it is git-ignored, about 260 MB). To rebuild it:

1. **Install dependencies** (tested with Python 3.9):
   ```bash
   pip install pandas numpy matplotlib scipy statsmodels requests beautifulsoup4 nbformat nbconvert ipykernel
   ```
2. **Download the grade data** (all semesters; takes about 45 minutes):
   ```bash
   python3 scripts/download_grades.py
   ```
3. **Download everything else** (student and staff counts, populations, college enrollment, map outlines, graduate admissions, prefix names):
   ```bash
   python3 scripts/download_demographics.py
   ```
4. **Export four files by hand** from the [Trends in Student Data](https://reports.utexas.edu/spotlight-data/students) dashboard (Download → Crosstab) into `data/demographics/`:
   - `county_enrollment.csv`, `state_enrollment.csv` and `nation_enrollment.csv` (Maps tab, Fall 2025)
   - `degrees_conferred.csv` (Degrees conferred tab, 2024–25)

   These tabs have no scriptable export.
5. **Run the notebook** (about 5 minutes):
   ```bash
   python3 -m nbconvert --to notebook --execute --inplace grade_analysis.ipynb
   ```

The task specification the analysis follows is in [`instructions.md`](instructions.md).

## License

[MIT](LICENSE)
