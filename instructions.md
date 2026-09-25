## General notes/preprocessing
- Combine results into a .ipynb notebook. The notebook should be divided into collapsable sections as you see fit. It should include all code that can be used to reproduce the results. It should display the figures and include some descriptions/notes.
- Exclude "Other" grade frequency when computing a course's grade average.  
- Try to format visualizations similarly
- The term "letter grade" refers to a grade that wasn't "Other".
- Save all figures in the "figures" folder
- Include figure notes where relevant
- When I refer to a major or field of study (e.g., mathematics), I'm referring to courses aggregated by the corresponding course prefix. 
- Include sanity checks where relevant
- Include correlation coefficient, r^2, line of best fit, and p-value for any scatterplot
- Describe the data sourcing and caveats using this description from the website: "The UT Austin grade distribution displays grade distributions for all courses since summer 2011. The dashboard displays grade distributions based on a unique student headcount for each class, semester and year; it is not representative of enrollment counts or instances of registration. The dashboard was last updated with Summer 2026 grades. In order to maintain student confidentiality, courses are not displayed if they satisfy one of the following conditions:
    1. The course is graduate level and there are less than 5 students of record.
    2. The course is undergraduate level and there are less than 10 students of record.
    3. All students received the same grade.
    4. All students except one received the same grade.
    5. None of the students received a letter grade.
	- Graduate student instructors' names will not be displayed due to FERPA restrictions.
	- The 'Other' grade category includes all non-standard letter grades, including: In Progress, Incomplete, Permanent Incomplete, Obit, Q-Drop, Withdrawn, Credit, No Credit, Satisfactory, Unsatisfactory, and Registered on CR/F or CR/NC basis.
	- Courses that appear in the filters but are not displayed in the table are redacted according to IRRIS student confidentiality guidelines."
    
- I have the grade data for the Fall 2025, Spring 2026, and Summer 2026 semesters. Please download it for the other available semesters to the "data/grades" folder. If you think this would burn through my token limit, please feel free to skip this and skip any steps that would require non-downloaded semesters. Make note of what was skipped Format the file names consistently. You can download the files from here: "distributionshttps://reports.utexas.edu/spotlight-data/ut-course-grade-distributions"
- Please merge the semesters into one dataset

- For each observation, create an average grade column. This contains the grade average for the course according to UT's GPA computation standards. Here are the letter grade-number pairs: A: 4, A-: 3.67, B+: 3.33, B: 3, B-: 2.67, C+: 2.33, C: 2, C-, 1.67, D+: 1.33, D: 1, D-: .67, F: 0
- Create dummies for course type. These dummies are for whether the normalized text contains the strings "intro", "intermediate", "advanced", "principles", " I" (there's a space before because this is supposed to be the roman numeral), "II", "III", "honors", and "lab"
- Create a course size variable. This is the quantity of grades in the course, including both letter grades and "Other".
- Course prefixes and there full names can be found here: https://catalog.utexas.edu/general-information/coursesatoz/?utm_source=chatgpt.com 
## Analysis

1. Generate a rotated bar graph. It's one of those where the categorical data is on the vertical axis and the quantitative data is horizontal. This should show mean course grade by course prefix in the 2025-2026 school year. This means that for a given course prefix, you take the arithmetic mean of the course grade averages from the Fall 2025 and Spring 2026 semesters (exclude summer). Please stack them in descending order. The title should be "Mean Course Grade By Course Prefix". Instead of displaying this for each course prefix (there are over 150), let's do it for course prefixes where enrollment was at least 100 across the Fall 2025 and Spring 2026 semesters. By enrollment, I mean the course size summed within a course prefix. If the graph is too tall, you can raise the minimum enrollment to 150, 200, etc.

2. Generate a line graph of mean course grade by semester, excluding summer semesters. There should be multiple lines. One line should weight each course equally when computing a semester's course grade average. The second should weight each course by the number of letter grades. There should be lines for math, physics, chemistry, biology, psychology, english, history, computer science, economics, The title should be "Mean Course Grade Over Time (By Course Prefix)". The graph should have a legend distinguishing the lines. Make sure the vertical scale and graph are large enough not to feel cluttered. Feel free to trim the bottom of the vertical scale, since I doubt any entire department has course grade averages below 2.5 for a given semester. The figure note should caveat that this is based on aggregated department course data. It should be interpreted as average course grades for a given department, not a measure of course difficulty or the average GPA of students in the corresponding major. Also note that not all courses were offered during every semester.

3. Display a histogram of grades for the 2025-2026 school year. Aggregate the data from the Fall 2025 and Spring 2026 semesters (exclude summer). Have vertical dashed lines for the mean and median. The horizontal axis should be categorical, including both letter grades and the "Other" category. Display the letter grades as letters on the horizontal axis labels, not their numerical equivalents. 

4. Display this same histogram for Fall 2020-Spring 2021 (aggregated). This was during COVID. Take note of that. 

5. Show the scatterplot of COVID period grades versus 2025-2026 academic year (Fall 2025 and Spring 2026) grades for course numbers present at least once in both periods. If a course appears twice within a given period, take the average across both semesters within the period. Please weight the correlation and dot sizes by course size. If a course is present across both semesters, sum its course sizes across both semesters.

6. Display a histogram of average course grades for the 2025-2026 school year by course section. Reminder not to use the "Other" grades. Overlay a kdensity curve. The horizontal axis may need to be trimmed. You may want to scale of the increments not to be constant, meaning the distance from 2.5 to 3.0 isn't the same as the distance from 3.0 to 3.5. Let me make this decision of rescaling after informing me of the results.

7. Display in a rotated bar graph, as above, the top 10 largest course prefixes by enrollment across Fall 2025 and Spring 2026. The bars should have exact numbers.

8. Of course prefixes with at least 200 enrollment for a given year, show the top 10 highest percentage increase and top 10 highest percentage decrease course prefixes. The beginning period should be Fall 2010 and Spring 2011 pooled together. The end period should be Fall 2025 and Spring 2026 pooled together. Normalize for the change in UT's student body size. That is, the enrollment for courses in the most recent year should be adjusted for the percentage growth in UT's student population. Note in the figure that this isn't a percentage change in enrollment by major. 

9. Display the top 10 course prefixes with the most and least number of distinct course numbers in the pooled Fall 2025 and Spring 2026. This should be a rotated bar graph. Include numbers next to the bar for their height (the number of distinct courses). The top 10 most and top 10 least should be two different colors, as indicated in a legend. There should be a bar of a third color for the mean number of distinct course numbers in the same time period across course prefixes, not weighted by enrollment. The bars for both top 10 categories should also show the number of courses for a course prefix divided by its enrollment for the period, rounded to some amount of decimal places. The bar size is not normalized for enrollment, however.

10. Display the top 10 highest and lowest grade average courses in Fall 2025 and Spring 2026 (pooled) on a rotated bar graph for courses that had enrollment of at least 50. If there are multiple sections of the same course prefix + number in the same semester, they should be included in the pooling for that class. For example, if ACC 100 appears once in Fall 2025 and twice in Spring 2026, you should take the arithmetic mean of these three course grade averages. There should be different colors for the two categories. The vertical axis should represent the median course grade, with this exact number displayed. The top 10 highest will jut to the right, while the top 10 lowest will jut to the left. The labels for the bars will be on the right for the 10 highest and the left for the 10 lowest. Bars should be accompanied by the exact grade average. The labels should be the course prefix and its course number. 

11. In a table, show the grade averages by course for the 20 courses from the previous step. Columns should show relevant information, most notably the actual course title, which I believe comes under the "Course" column in the data. Make sure there's a column for both the course prefix and the course prefix's full name.

12. Display a scatterplot of fall and spring grades for courses of a prefix + number present in both Fall 2025 and Spring 2026. If there are multiple sections in a semester, combine their distributions the get the average course grade. This is effectively weighting by relative course size. Weight dot size and correlation by mean course size between Fall 2025 and Spring 2026.

13. Do the same as above, but for Fall 2025-Spring 2026 versus Summer 2026. 

14. To the same scatterplot as number 12, but for I and II courses. By this, I mean courses that have the same normalized course name, except that one has the roman numeral I while the other has II. Please use the semesters Fall 2024, Spring 2025, Fall 2025, and Spring 2026. If a course prefix + number appears multiple times, simply aggregate as above. 

15. Show the results of regressing II grades on I grades in a regression table. In this case, the observation is a course sequence (course with I and II). Use robust standard errors.

16. Display a descriptive stats table for each of the course dummies generated earlier (I, II, honors, lab, etc.). These should be based on Fall 2025 and Spring 2026. As earlier, if a prefix + number appears multiple times, just aggregate the grade distributions for each section.

## Conclusion

I will go through your results and let you know whether to stage, commit, and push to the original repo.

## Revisions 1.0

I would like to make some additions/revisions.

General notes:
- Please rearrange the results in the notebook to flow more organically. Some visualizations make sense to be grouped together, such as those related to COVID.
- Steps 1-6 can probably be grouped together at the beginning because they provide an overview of UT's demographics
- Steps 7-8 can be grouped with COVID stuff
- You can group 10-11 with the major grade trends
- Please generate a dummy that indicates whether a course was web-based. This is based on the course title. Typically, it will contain the string "WB" or "(WB)" or "-WB". Include this dummy in the descriptive stats table of the dummy variables.

1. When loading the data, please also find data on the UT student population over time. Produce a line graph of the university's population over time. There should be separate lines for the overall population, student population, faculty population, and staff population. Then show another line graph with male student population and female student population. Then show one with lines for each "type" of student: bachelors, master's, doctoral, law, medical, etc. Please clarify where this data comes from. 

2. Produce a rotated bar graph of the number of degrees conferred in the 2024-2025 academic year, as contained in "data/demographics/degrees_conferred.csv". It should be grouped into vertical "chunks" for the degree type. Please preserve the vertical ordering of the bachelors' chunk for the other chunks. For example, if the college of natural science conferred more bachelors' degrees than the college of liberal arts, this should be preserved for the masters' degree ordering. Please color each chunk differently. This visual will show the number of degrees conferred by school. The bars should have exact numbers as well. 

3. You'll need to obtain data on Texas counties as of Fall 2025 for this. Show a table of the top 10 Texas counties with the greatest number of students enrolled as of Fall 2025, shown as "Number of Records" in county_enrollment.csv. The table should show country name, number of students, and county population. Then, display a table of the counties with zero number of students, along with how many of them there are. These tables should be grouped with the texas_map.pdf file in figures. Specify that obtained this visualization from this website: https://reports.utexas.edu/spotlight-data/students. Clarify that Fall 2025 was the most recent data I could find. Then, display a scatterplot of the relationship between county population and enrollment. You might want to do log of the county population, though I'm not sure. Weight counties equally in the correlation and line of best fit. Then, produce a table of the top 10 Texas counties by enrollment, adjusted for country population as of Fall 2025. This table should show county name, adjusted enrollment, number of students, and population. Finally, generate a choropleth map of Texas and its counties with the color gradient based on enrollment divided by population (perhaps multiplied by some factor to avoid lots of decimal places). 

4. Repeat the previous step, but use data on US state populations as of Fall 2025. Data on enrollment by state comes from state_enrollment.csv. The only change from above is that instead of showing a top 10 table and a count of states with zero enrollment, just do a population adjusted and population un-adjusted table in descending order by their key quantity. These tables will each contain every state, since there are only 50. You might want to use log of the state population in the scatterplot.

5. Repeat step 3, but for countries. Use data on nation populations as of Fall 2025. I doubt we'd have population data as of Fall 2025 exactly, so just choose the closest period. You can use the nation_enrollment.csv file for student enrollment data. In the scatterplot, use log of the nation population. Weight nations equally. For the tables, do top 20 nations by enrollment. Then, do a top 20 adjusted for population size. I want to do another top 20 where we adjust for "educated" population. I'm not sure how to quantify this. Let me know if you have a suggestion and we can add a top 20 table that adjusts for "educated population size". 

6. Extract the table from this website into a .csv file in "data/grad school": https://graduate.utexas.edu/about/statistics-surveys/admissions-enrollment. Then display this table for the top 20 most competitive graduate programs (lowest selectivity in descending order). This would show for each program its school, name, applied, admitted, enrolled, selectivity, yield, etc. Please restrict to programs where at least 50 people applied. Then, show the same table, but for the top 20 most enrolled programs. In addition to tables, generate the rotated bar graphs for these with the key quantities included. 

7. Produce a line graph of the number of web-based courses offered by semester (including summer) as a fraction of the courses offered in that semester. You might want to multiply these by some factor of ten if there are too many decimal places (definitely clarify any multiplication). Include a "gray region" for when the COVID pandemic occurred. 

8. Produce a line graph of the average course grade of web-based courses by semester (including summer). Make one line weighted by course size and the other not. Indicate the COVID pandemic region. Produce the same graph, but for web-based courses present from some arbitrary period before COVID (maybe fall 2018) through some arbitrary period after it. This is supposed to follow the same pool of courses since it's possible that more web-based courses were added and the new courses were easier, artifically driving up the average. The reason I say arbitrary periods instead of the full duration is that I want a sufficiently large sample of courses.

9. Produce a histogram of course size in 2025-2026, along with an overlaid kdensity. You might want the horizontal axis to be log of course size. Alternatively, you might want to divide into course size buckets. The histogram should have vertical lines for mean and median with their respective numerical quantities. Produce a line graph with average course size over time (semester), excluding summer semesters. The line graph should come with exact quantities for each period. You can decide where to put them, perhaps near the nodes of the line or below the graph. Finally, show a table of the top 10 largest courses in 2025-2026 (including summer).

10. Remember that section with line graphs showing the average course grade over time for multiple course prefixes? I want to add some more prefixes to that. Namely, ASE, BME, C E, CHE, ECE, E M, and M E. You can group the engineering prefixes separately.

11. Generate a table with the top 3 highest/lowest average grade courses for each of the prefixes for which you generated a line graph. Limited to courses with at least 50 enrollment across both semesters. Columns include, but are not limited to, course prefix, ranking (top 1, top 2, bottom 3, etc.), course number, average grade, etc. In addition to the table, generate a rotated bar graph formatted like the one that shows the top 10 highest/lowest grade courses.

12. Generate a rotated bar graphs for language popularity (enrollment in fall 2025, spring 2026, and summer 2026) and for average grade in language classes (excluding English). Read the course prefixes to determine which ones are associated with foreign languages. The popularity bar graph should be in descending order. The average grade bar graph should also be in descending order. Finally, create a pie chart of language popularity. Make the pie chart "ordered" by slice size. You may want to keep the slice labels outside of the slices themselves. You may want to group languages that account for a miniscule share together to minimize clutter. Make sure the slice labels include exact percentages.

13. You remember when you did those scatterplots for fall vs. spring vs. summer grades for the same courses? I actually want you to extend this to all years instead of just last year. I want you to compare the mean course grade across all three. 

## Revisions 2.0

I'm going to make more revisions.

General notes:
- Line graphs should show a vertical dotted line for the date of public release of ChatGPT. I believe this is November 30, 2022. 

1. In 2.1, we have a graph of mean course grade by course prefix. I would like you to produce the same visual, but for a given course prefix, weight each course by its course size (including "Other"). Generate this visual (the one weighted by course size), only broken up into multiple rotated bar graphs. Each graph will be the same visual, but grouped by natural science, engineering, social science/humanities, fine arts, language, and other, respectively. Group computer science with engineering. Group math with natural science. You can make the judgment calls for groupings yourself. In addition to these graphs by "field group", which should be colored differently, you should have one that shows bars with the mean course grade by field group. These should be weighted by course size (including Other). There should also be a bar that aggregates all of the field groups. These bars should be colored by the colors from their respective field group graphs.

2. The line graph in 1.1 of the UT Austin population over time should be a stacked line graph.

3. The bar graph in 1.2 should be modified. The masters' and doctoral bars should be adjacent to their bachelor's counterpart, sort of like a triple bar graph with a legend. The law and special professional programs can still be "separate" as they are now.

4. 1.6 currently shows selectivity and yield. Can you generate a scatterplot of the selectivity of a program against its yield. You may want to apply a logarithm to one or both of the axes depending on what creates the best fit. Size the dots by the number of applicants to a program, but weight them equally.

5. After mentioning course size in 1.10, you should display a table of the top 10 largest non web-based courses in 2025-2026 academic year. 

There should be a 6th question on whether UT weeds students out. We will examine the CS, physics, and economics majors. We must be careful to follow the same cohorts and that the cohorts have completed their respective core sequences. For example, if a major takes class A followed by B followed by C, people who took C in Spring 2026 took B in Fall 2025 and A in Spring 2025, approximately. Yes there are people who failed classes, took them during the summer, skipped one, or found a way to take them concurrently, but these seem to be the minority.

1. The core sequence for CS is C S 312, C S 314, C S 429, and C S 439. Each is taken in subsequent semesters. You'll create a line graph showing each course on the horizontal axis. Each cohort, identified by when they took C S 439, is in a different color. Do this for the Spring 2026, Fall 2025, Spring 2025, Fall 2024, Spring 2024, and Fall 2023 cohorts. Let me know if the course classification changed. If there are multiple sections for a course number in a semester, add up their distributions to get the mean course size. Create a table with the exact numbers for what's visualized. The table should include the absolute and percentage change in enrollment for each cohort from C S 314 through C S 439. The reason we don't use C S 312 as the beginning period is that some people tested out of it. The table's columns, in addition to showing course enrollment should show average course grade. Finally, we should see the average percentage change in cohort size across all four cohorts. Repeat the line graph of enrollment, but for gpa. 

2. We're going to repeat step 1, but for the ECO prefix. The core sequence is 304K, 304L, 329, 420K/420S, 441K, and 320L. 420K is "Microeconomic Theory", while 420S is "Mathematical Microeconomic Theory with Advanced Applications". Students may choose one of the two. I want you to display 420K and 420S at the same horizontal position, so it's like the line bifurcates at that point and reconvenes afterwards (clarify this somewhere). As before, create the table and include gpa. There should be a line graph for gpa in addition to the enrollment one. 