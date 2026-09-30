# Step 1 inspection â€” preliminary data audit, not the final assignment report

Source: D:\CSE_21201016_BRAC\DATA_SCIENCE\ASSIGN1_sarwar\A_B_Testing_Hypothesis_Testing_Assignment.docx
Source: D:\CSE_21201016_BRAC\DATA_SCIENCE\ASSIGN1_sarwar\ui_ab_testing_data.csv

Dataset: 10000 data rows x 9 columns; 10,001 records including header.
CSV column names (case-sensitive): user_id, ui_version, timestamp, session_duration_seconds, pages_visited, clicks, errors_encountered, conversion, bounce

## First 10 data rows

```csv
"user_id","ui_version","timestamp","session_duration_seconds","pages_visited","clicks","errors_encountered","conversion","bounce"
"1","UI_A","15-01-24 2:46","50.43","2","5","1","0","0"
"2","UI_B","20-01-24 23:28","8.71","9","6","0","0","0"
"3","UI_A","04-01-24 19:54","88.4","4","4","0","0","0"
"4","UI_A","20-01-24 22:06","91.6","3","4","0","1","0"
"5","UI_A","27-01-24 5:12","240.79","3","3","1","0","0"
"6","UI_B","20-01-24 20:59","138.44","3","3","0","0","1"
"7","UI_A","11-01-24 6:35","54.03","4","8","1","0","0"
"8","UI_A","10-01-24 1:37","17.28","3","7","0","0","0"
"9","UI_A","03-01-24 20:41","76.78","3","8","0","0","1"
"10","UI_B","29-01-24 22:09","141.43","4","4","1","0","0"
```

## Data quality

- Missing values in user_id: 0
- Missing values in ui_version: 0
- Missing values in timestamp: 0
- Missing values in session_duration_seconds: 0
- Missing values in pages_visited: 0
- Missing values in clicks: 0
- Missing values in errors_encountered: 0
- Missing values in conversion: 0
- Missing values in bounce: 0
- Duplicate full rows beyond first occurrence: 0
- Duplicate user IDs beyond first occurrence: 0
- Invalid, nonfinite, or nonpositive session durations: 0
- Unexpected UI labels: 0
- No records were removed, imputed, or transformed in the original CSV. Duplicate-free session IDs do not independently establish experimental independence.

## Initial descriptive statistics

Duration units: seconds. Sample SD = sqrt(sum((x - mean)^2)/(n - 1)); ddof=1. All rows retained.

| UI | Count | Mean | Sample SD | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| UI_A | 5013 | 99.66307401 | 71.56361982 | 1.61 | 525.95 |
| UI_B | 4987 | 126.25848606 | 83.64436110 | 2.25 | 666.51 |

## Assignment preview comparison

| Item | Assignment preview | CSV calculation | Finding |
|---|---|---|---|
| UI_A count | 5,013 | 5,013 | Matches |
| UI_B count | 4,987 | 4,987 | Matches |
| UI_A mean | 99.66 | 99.66307401 | Matches to 2 decimals |
| UI_B mean | 126.26 | 126.25848606 | Matches to 2 decimals |
| Mean difference B - A | +26.60 | +26.59541206 | Matches to 2 decimals |
| UI_A SD | 68.45 | 71.56361982 | CSV sample SD is 3.11361982 seconds higher |
| UI_B SD | 71.23 | 83.64436110 | CSV sample SD is 12.41436110 seconds higher |

The SD discrepancies exceed rounding differences. Their cause is not established by the source files. Use CSV-derived sample SDs for subsequent calculations. The preview provides no minimum or maximum for comparison.
The description capitalizes Timestamp, Clicks, Conversion, and Bounce; actual CSV headers are timestamp, clicks, conversion, and bounce. Use the actual lowercase headers in code.

## Python environment

Verified by actual imports: Python 3.13.1 at C:\Python313\python.exe; pip 24.3.1.
Core packages for the planned Python workflow are absent: pandas, numpy, scipy, matplotlib. Optional packages checked and absent: seaborn, statsmodels, python-docx (import docx), jupyter, nbformat.
No packages were installed. Step 1 uses PowerShell/.NET CSV and OOXML readers, so package absence is not a Step 1 blocker. Install the core packages into a project environment before later Python statistical analysis. Optional packages are not required if their functionality is covered by core packages or standard-library extraction.

## Preservation and scope

- A_B_Testing_Hypothesis_Testing_Assignment.docx SHA256: 6E65A1E21097616BD0A736F18660F4F334F84AA9A9988AF80F7675EF50BD127A (unchanged across inspection)
- ui_ab_testing_data.csv SHA256: 5FDD83F7ABF63F58E4DD3BEF9C5ED1BB4D28CBAEEA903BD07EDC395E11E4E96A (unchanged across inspection)
Complete source text and explicit table rows are saved in assignment_extracted.txt. No normality tests, hypothesis tests, probability calculations, plots, or final report were created. Step 1 blockers: none.
