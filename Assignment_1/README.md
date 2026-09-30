# A/B testing assignment: data exploration

This stage compares descriptive session-duration statistics and assesses
normality for UI_A and UI_B, then performs a verified independent two-sample
mean comparison. The original CSV is authoritative and remains unchanged.
Step 5 adds assignment-required normal-model probabilities, separate empirical
comparisons, and percentage change in mean duration. Step 6 creates the complete
report using the builder described below.

## PowerShell commands

Run from the project folder. Activation is unnecessary; every command explicitly
uses the project environment, leaving global Python packages unchanged.

```powershell
Set-Location 'D:\CSE_21201016_BRAC\DATA_SCIENCE\ASSIGN1_sarwar'

# Only if the project environment does not exist (Python must be 3.13.1):
python --version
if (-not (Test-Path '.\.venv\Scripts\python.exe')) { python -m venv .venv }

# Install the recorded environment:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Run the exploration script first to generate the reference CSV:
.\.venv\Scripts\python.exe scripts\analyze_ab_testing.py

# Execute every notebook cell in a fresh project kernel and save outputs:
.\.venv\Scripts\python.exe scripts\execute_notebook.py
```

Open `AB_Testing_Assignment.ipynb` in a notebook-capable editor to read the saved
outputs. For interactive execution, select `.venv\Scripts\python.exe` as the
kernel and use the project folder as the working directory. A Jupyter web server
is not required by the execution helper.

## Files and calculation conventions

- `scripts/analyze_ab_testing.py`: loads the CSV, prints exploration and quality
  checks, computes statistics, verifies Step 1 references, and saves the results.
  It also calculates full-sample Shapiro-Wilk and bias-corrected sample skewness,
  prints and saves captured warnings, and creates four normality figures.
- `AB_Testing_Assignment.ipynb`: explains the objective and hypotheses, explores
  the data, independently calculates statistics, compares with the script CSV,
  and saves the verified statistics to the same output path.
- `scripts/execute_notebook.py`: launches a fresh kernel explicitly using the
  project interpreter, runs all cells in order, and saves their outputs.
- `results/descriptive_statistics.csv`: full-precision computed statistics;
  `std` is sample SD (ddof=1), `50%` is the median; durations are seconds.
- `requirements.txt`: pinned installed versions, including dependencies.
- `results/normality_assessment.csv`: full-precision sample counts, skewness
  (`bias=False`), Shapiro-Wilk W and p-values, and captured warning text.
- `figures/UI_A_histogram.png`, `figures/UI_B_histogram.png`: 25 shared bins
  covering the full pooled range, with identical duration and frequency limits.
- `figures/UI_A_qq_plot.png`, `figures/UI_B_qq_plot.png`: normal probability
  plots made with `scipy.stats.probplot`, including fitted reference lines.
- `results/normality_interpretation.md`: interpretation written after inspecting
  all four plots, including the Shapiro-Wilk warning and next-step assumptions.
- `results/variance_test.csv`: median-centered Levene statistic, p-value, and
  selected test under the assignment's rule.
- `results/t_test_results.csv`: labeled selected test (and Welch sensitivity if
  Student is selected), group summaries, UI_B-minus-UI_A difference, SE, t, df,
  two-sided p-value, 95% CI, decision, and manual-verification values.
- `results/hypothesis_test_interpretation.md`: Step 4 interpretation, assumptions,
  selection limitations, and statistical versus business significance.
- `results/step4_verification.json`: execution, agreement, and preservation audit.
- `results/probability_scenarios.csv`: four full-precision normal-model answers,
  z-scores, formulas, model parameters, strict empirical counts/denominators,
  observed proportions, and model-versus-observed percentage comparisons.
- `results/business_impact.csv`: absolute and relative percentage change in mean
  duration, plus the verified Step 4 test and confidence interval.
- `results/probability_and_business_interpretation.md`: plain-English events,
  formulas with substitutions, interpretations, model limitations, supplementary
  empirical comparisons, and conditional business implications.
- `results/step5_verification.json`: fresh-kernel execution and preservation audit.

The existing PowerShell commands execute all completed stages. Run the script
before the notebook: the notebook independently recomputes normality statistics
and verifies agreement against the script CSV before saving them. Small p-values
are displayed in scientific notation. All observations are used; no subsampling
is performed. Matplotlib's cache is stored inside `.venv`.

Step 4 uses `levene(ui_b, ui_a, center="median")`: p < 0.05 selects Welch;
otherwise Student pooled is selected with Welch as a sensitivity check.
`ttest_ind` always receives UI_B first and UI_A second, with a two-sided
alternative. Both entry points verify the selected test against explicit summary
formulas. Tiny p-value comparisons use relative tolerance 1e-10 and absolute
tolerance zero, with positivity assertions. The notebook also compares its
independent results with the script CSVs. Run the same PowerShell commands above
to execute the complete analysis through Step 5. Historical Step 3 and Step 4 notes remain
preserved; their references to deferred tests describe that earlier checkpoint.

Step 5 uses individual-duration sample SDs (ddof=1), not standard errors. The
assignment's normal models are untruncated despite the observed non-normality.
Each z-score calculation is checked against direct `norm.cdf`/`norm.sf` with
`loc` and `scale`. Observed rates use strict inequalities and the matching group
denominator; question (a) compares UI_A durations with the full-precision UI_B
sample mean, not a randomly drawn UI_B duration. The notebook independently
recomputes probabilities and counts and compares them with the script CSVs.
Business percentage change uses UI_A's mean as the baseline, and is not a
percentage-point change. Only displayed values are rounded.

## Generate the assignment report (Step 6)

The report builder reads the original assignment, executed notebook, original
CSV, saved result CSVs, and existing figures. It preserves the analysis files.
Install the updated `requirements.txt` into `.venv` as shown above. Additional
report dependencies are `python-docx`, `lxml`, and `PyMuPDF`.

```powershell
Set-Location 'D:\CSE_21201016_BRAC\DATA_SCIENCE\ASSIGN1_sarwar'
.\.venv\Scripts\python.exe scripts\build_report.py
```

Outputs:

- `report/AB_Testing_Assignment_Report.docx`
- `report/AB_Testing_Assignment_Report.pdf` (exported directly from the DOCX)

The builder uses the project-local LibreOffice renderer at
`.tools\LibreOffice\program\soffice.exe`. On another computer, install LibreOffice
and specify its executable explicitly, or set the `SOFFICE` environment variable:

```powershell
.\.venv\Scripts\python.exe scripts\build_report.py --soffice 'C:\Program Files\LibreOffice\program\soffice.exe'
```

`--docx-only` creates the DOCX without PDF export. A missing renderer causes the
normal build to report an error, not a successful PDF conversion. Page images
and rendering metadata are written to `report/qa/` for visual inspection after
each build. Review every rendered page after changing report content. Personal
name, student ID, course, and section remain blank for completion by the student.
No files are submitted or published by these commands.

Paths in code are relative to the project or script location. The notebook must
be run from the project folder. Quantiles use pandas' default linear interpolation.
Only displayed values are rounded. No outliers are deleted and no duration
values are transformed. SD describes variation among individual sessions;
standard error describes uncertainty of an estimated mean (SD / sqrt(n) for
independent observations). The mean comparison calculates the standard error of
the difference between means using the Welch formula.

The assignment preview gives SDs of 68.45 and 71.23 seconds; these differ from
the CSV-derived sample SDs. Use the actual CSV for all later analysis.
