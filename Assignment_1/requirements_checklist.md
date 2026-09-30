# Assignment requirements checklist

Source: `A_B_Testing_Hypothesis_Testing_Assignment.docx`, read completely, including both tables. Calculations must use `ui_ab_testing_data.csv`, not the preview.

## Step 1 — complete

- [x] Locate both original files in the current project.
- [x] Read the entire assignment, including the column-description and summary-preview tables.
- [x] Load and inspect the CSV; display the first 10 rows.
- [x] Confirm 10,000 data rows plus one header record (10,001 records including header).
- [x] Separate UI_A (5,013 rows) and UI_B (4,987 rows); extract session duration.
- [x] Document sample size, mean, sample standard deviation (ddof=1), minimum and maximum by UI.
- [x] Check columns, missing values, duplicate rows, duplicate session IDs, and group counts.
- [x] Check Python and assignment-related package availability.
- [x] Compare CSV statistics with the assignment preview and document discrepancies.
- [x] Preserve original files unchanged.

## User-requested Step 2 — environment and exploration complete

- [x] Create a project-local .venv with Python 3.13.1; leave global packages unchanged.
- [x] Install and verify pandas, numpy, scipy, matplotlib, nbformat, nbclient, and ipykernel; pin installed versions in requirements.txt.
- [x] Create AB_Testing_Assignment.ipynb and scripts/analyze_ab_testing.py with portable project paths.
- [x] Include objective, metric and units, two-sided hypotheses, and alpha=0.05 in the notebook.
- [x] Display first 10 rows, dimensions, column names, data types, group counts, and all requested data-quality checks.
- [x] Calculate count, mean, sample SD (ddof=1), minimum, quartiles, median, and maximum from the CSV without modifying observations.
- [x] Save full-precision statistics to results/descriptive_statistics.csv; round only for display.
- [x] Explain SD versus SE and document the assignment preview SD discrepancy.
- [x] Verify calculated counts, means, and SDs against Step 1 references.
- [x] Run the script and execute the notebook in a fresh project-environment kernel; save outputs and confirm all statistics agree.
- [x] Provide exact PowerShell execution commands in README.md and a notebook execution helper.
- [x] Verify both original files still match Step 1 SHA256 hashes.

The user's Step 2 is environment setup and exploration. The assignment's separately numbered normality step below was subsequently completed in user-requested Step 3. The first pip attempt failed with sandbox WinError 10013; the authorized network retry succeeded. Imports and pip dependency checks passed.

## Assignment Step 2 / User-requested Step 3 — complete

- [x] Validate normality before the independent samples t-test.
- [x] Create separate session-duration histograms for UI_A and UI_B, each with 20–30 bins.
- [x] Interpret bell shape, symmetry, and skewness in both histograms, considering sample sizes.
- [x] Create a normal Q-Q plot for each UI; interpret departures from the reference line.
- [x] State Shapiro-Wilk H0 (normal distribution) and H1 (non-normal distribution).
- [x] Run Shapiro-Wilk for each UI and report p-values with interpretation at alpha=0.05.
- [x] Discuss large-sample sensitivity and weigh visual diagnostics alongside test results.
- [x] Document the combined normality assessment and implications for subsequent analysis.

- [x] Use 25 shared histogram bins and comparable axes; show group sample sizes.
- [x] Use scipy.stats.probplot with fitted reference lines; inspect all four exported figures.
- [x] Compute sample skewness with bias=False and Shapiro-Wilk W/p on every observation.
- [x] Capture, display, save, and explain the UI_A N>5000 warning; display p-values in scientific notation.
- [x] Save results/normality_assessment.csv and interpretation; distinguish raw durations from the sampling distribution of means.
- [x] Explain Welch variance handling and the assignment-supplied independence assumption.
- [x] Run the script and complete notebook in a fresh project kernel; verify numerical agreement and saved outputs.
- [x] Confirm original files and prior descriptive CSV retain identical SHA256 hashes.

## Assignment Step 3 / User-requested Step 4 — complete

- [x] State H0: equal population mean session durations; H1: different population means.
- [x] Review normality and independence, distinguishing the assignment's collection assumptions from what the CSV can verify.
- [x] Optionally run Levene's test to assess equal variances (explicitly optional in the assignment).
- [x] Report group means and standard deviations.
- [x] Select and justify Student's t-test for equal variances or Welch's t-test for unequal variances.
- [x] Conduct a two-tailed independent samples t-test at alpha=0.05.
- [x] Report t-statistic, p-value, degrees of freedom, and a 95% confidence interval, clearly stating the difference direction.
- [x] Reject H0 if p<0.05; otherwise fail to reject H0. Explain the result in context.

- [x] Use median-centered Levene with UI_B first; explain robustness, non-significance, and preliminary-selection limitations.
- [x] Maintain UI_B minus UI_A throughout; use all observations, two-sided alpha=0.05.
- [x] Report the mean difference and its standard error alongside group sizes, means, and sample SDs.
- [x] Independently verify selected-test summary formulas, df, two-sided p-value, and 95% CI against SciPy.
- [x] Compare tiny p-values with relative tolerance and zero absolute tolerance; reject erroneous zero values.
- [x] Save variance_test.csv, t_test_results.csv, and hypothesis_test_interpretation.md.
- [x] Execute script and complete notebook in a fresh project kernel; verify script/notebook/manual agreement.
- [x] Preserve original files, earlier result files, and figures with unchanged SHA256 hashes.
- [x] Explain statistical versus business significance, raw non-normality, and assumed independence without computing percentage increase or probability scenarios.

## Probability scenarios / User-requested Step 5 — complete

- [x] Scenario 1: use the UI_A normal model and its sample statistics to calculate P(UI_A duration > UI_B mean).
- [x] Scenario 2: calculate P(UI_A duration < 80 seconds).
- [x] Scenario 2: calculate P(UI_B duration > 150 seconds).
- [x] Scenario 2: calculate P(80 < UI_A duration < 120 seconds).
- [x] Show z-scores and use the standard normal distribution/table or scipy.stats.norm.cdf for these scenarios.
- [x] Scenario 3: calculate the percentage increase in mean session duration from UI_A to UI_B.
- [x] Scenario 3: assess whether the increase is statistically significant at p<0.05 and explain business implications.

- [x] Use full-precision CSV means and individual-duration sample SDs, not standard errors.
- [x] Present each event in plain English with formulas, substituted values, z-scores, decimal/percentage answers, and interpretation.
- [x] Label untruncated normal-model approximations and explain non-normality and the distinction from mean inference.
- [x] Add separate empirical strict-inequality counts and matching group denominators, with the full-precision UI_B mean for question (a).
- [x] Compare empirical and normal-model percentages; distinguish sample proportions from model probabilities.
- [x] Report absolute and relative percentage increase, referencing Step 4 Welch significance and confidence interval.
- [x] Keep business recommendations conditional and avoid unsupported usability, satisfaction, revenue, or conversion claims.
- [x] Verify z-score calculations against direct loc/scale methods, probability bounds, counts, denominators, and script/notebook agreement.
- [x] Save probability_scenarios.csv, business_impact.csv, and probability_and_business_interpretation.md.
- [x] Run the full script and complete notebook in a fresh project kernel; preserve all original and prior result files and figures.

## Later deliverable and interpretation

- [x] Present the requested statistics, professional visualizations, normality interpretation, test results, confidence interval, probability answers, and business conclusion.
- [x] Retain the CSV as the authoritative source and disclose preview discrepancies.
- [x] Interpret session duration as engagement; avoid claiming the metric alone proves better user experience.

The DOCX does not specify a submission filename, report format, page count, deadline, or additional analyses of the other metrics. Report preparation was authorized and completed in user-requested Step 6. No normality tests, hypothesis tests, probability calculations, or final report were performed in Step 1.

## User-requested Step 6 - complete assignment report

- [x] Read original assignment including both tables, checklist, executed notebook, and saved outputs.
- [x] Create report/AB_Testing_Assignment_Report.docx and matching PDF with scripts/build_report.py.
- [x] Include numbered objective/hypotheses, exploration, normality, variance/Welch test, probability, business, and reproducibility/source sections.
- [x] Include all four figures with captions and the first ten rows/all nine columns in a landscape appendix.
- [x] Load calculated values from saved outputs; show formulas, substitutions, units, and scientific notation for tiny p-values.
- [x] Explain preview discrepancies, non-normality, independence, normal-model limitations, and conditional business implications.
- [x] Leave name, student ID, course, and section blank.
- [x] Export PDF directly from DOCX with project-local LibreOffice; render and visually inspect every page.
- [x] Fix initial orphaned caption, blank pages, long column label, and equation overflow; verify the final 10-page rendering.
- [x] Confirm key PDF values against saved CSVs and preserve originals, executed notebook, analysis script, and prior results.
- [x] Record report dependencies in requirements.txt and generation instructions in README.md.
- [x] Keep deliverables local; no submission, email, upload, or publication.

## User-requested Step 7 - final audit complete

- [x] Read the actual original assignment DOCX, including both tables, and map every requirement to the script, notebook, and final reports.
- [x] Run the analysis script and all 15 notebook code cells in a fresh project .venv kernel; save outputs and verify no cell errors.
- [x] Independently recalculate descriptive statistics, normality, median-centered Levene, Welch inference, four probabilities, strict empirical counts, and business increase from the original CSV.
- [x] Compare full-precision results using relative tolerance and zero absolute tolerance, including positive tiny p-values; verify displayed values with rounding only.
- [x] Check statistical interpretation and distinguish individual distributions, mean inference, model probabilities, empirical rates, and business importance.
- [x] Rebuild DOCX/PDF using the README command; confirm identical substantive text and four embedded figures.
- [x] Inspect all ten rendered pages and verify the appendix's ten rows and nine columns against the CSV.
- [x] Correct stale README SE wording and notebook introductory completion status.
- [x] Confirm original DOCX/CSV SHA-256 hashes remain unchanged; keep all artifacts local.
- [x] Record methods, coverage, evidence, renderer fallback, and manual fields in final_audit.md and audit/.

STEP 7: PASS. Name, student ID, course, and section remain blank. No unresolved assignment checks; nothing submitted, emailed, uploaded, or published.
