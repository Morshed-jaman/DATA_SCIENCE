# Step 4: independent two-sample mean comparison

The target is population mean session duration in seconds. All differences are
UI_B minus UI_A. H0: mu_B - mu_A = 0; H1: mu_B - mu_A != 0.
The test is two-sided at alpha = 0.05. All original observations are retained,
without transformations or removal of extreme values.

## Variance assessment and selection

Median-centered Levene's test (Brown-Forsythe variant), called with UI_B first,
gives statistic 65.919294 and p = 5.25152025e-16. This is evidence against equal
population variances. Following the assignment's rule, select Welch's t-test
(`equal_var=False`). Had p been at least 0.05, the workflow would select Student's
pooled-variance test and additionally report Welch's as a sensitivity check.
A non-significant variance test would not prove equal variances.

Median centering makes the variance check more robust to departures from
normality, particularly skewness. It is not assumption-free. Selecting the mean
test through a preliminary variance test has limitations: the selection itself
is data-dependent, and nominal error rates of the resulting two-stage procedure
need not match those of either pre-specified test. This workflow follows the
assignment's rule rather than treating it as an universally optimal strategy.

Sources: [SciPy Levene documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.levene.html)
and [SciPy independent t-test documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html).

## Results (rounded for display only)

| Group | n | Mean (seconds) | Sample SD (ddof=1; seconds) |
|---|---:|---:|---:|
| UI_A | 5013 | 99.663074 | 71.563620 |
| UI_B | 4987 | 126.258486 | 83.644361 |

- Mean difference, UI_B minus UI_A: 26.595412 seconds.
- Standard error of the difference: 1.557093 seconds.
- Welch t-statistic: 17.080173.
- Welch-Satterthwaite degrees of freedom: 9748.829140.
- Two-sided p-value: 1.79827227e-64.
- 95% confidence interval for mu_B - mu_A: [23.543188, 29.647637] seconds.
- Decision at alpha = 0.05: reject H0.

UI_B has a higher estimated mean session duration by about 26.60 seconds. The
confidence interval is wholly positive and excludes zero. Under the stated
sampling assumptions, the data provide strong evidence of a difference in
population mean durations. The p-value measures tail extremeness under H0 and
the test model; it is not the probability that H0 is true.

Statistical significance does not establish business importance. Assessing
practical value requires a meaningful decision threshold, implementation costs,
and relevant outcomes. Longer sessions may reflect engagement or difficulty;
they do not by themselves prove better usability or user satisfaction. No
percentage increase or probability scenarios are calculated here.

## Assumptions and verification

Step 3 found non-normal, right-skewed individual durations. With roughly 5,000
observations per group, independent sampling and finite population variances
support approximate normal sampling distributions for the means and approximate
mean-difference inference. This does not make individual durations normal.
Welch accommodates unequal variances, not non-normality itself. Independence
remains an assumption supplied by the assignment scenario, not established by
unique IDs. Large samples do not correct dependence or biased sampling.

The script and notebook calculate summary-statistic SE, t, degrees of freedom,
two-sided p = 2*t.sf(abs(t), df), and confidence limits from full-precision data.
These are compared against SciPy's raw-data t-test and its confidence_interval
method. P-value checks use relative tolerance 1e-10 and absolute tolerance zero,
with explicit positivity checks, so an erroneous zero cannot pass. Other manual
comparisons use relative tolerance 1e-12 and absolute tolerance zero. The notebook
also checks agreement with the script's saved results. No final report has been
created; this is the Step 4 interpretation only.
