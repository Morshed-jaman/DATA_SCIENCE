# Step 5: probability scenarios and business impact

## Required normal-model approximations

XA ~ Normal(mA, sA^2) and XB ~ Normal(mB, sB^2), using CSV sample means
and individual-duration sample SDs (ddof=1), NOT standard errors.
Displayed substitutions are rounded; computations retain full precision.

Both groups are right-skewed and non-normal. These are the assignment-required
normal-model approximations, not validated individual-duration distributions.
Large independent samples support inference for means but do not make individual
durations normal. The requested normal models remain untruncated, including their
theoretical support below zero; no data or model transformations are applied.

### (a) A UI_A session exceeds the UI_B sample mean

Mean = 99.6630740076 seconds; sample SD = 71.5636198220 seconds.
z_lower = (126.2584860638 - 99.6630740076) / 71.5636198220 = 0.3716331304.
Formula: `norm.sf((lower - mean) / sample_sd)`.
Substitution: norm.sf(0.3716331304) = 0.3550830093 = 35.508301%.
Under the normal approximation, about 35.51% of individual UI_A sessions satisfy this event.

The threshold is UI_B's full-precision sample mean, held fixed. This is NOT P(XA > XB).

### (b) A UI_A session lasts less than 80 seconds

Mean = 99.6630740076 seconds; sample SD = 71.5636198220 seconds.
z_upper = (80.0000000000 - 99.6630740076) / 71.5636198220 = -0.2747635468.
Formula: `norm.cdf((upper - mean) / sample_sd)`.
Substitution: norm.cdf(-0.2747635468) = 0.3917489530 = 39.174895%.
Under the normal approximation, about 39.17% of individual UI_A sessions satisfy this event.

### (c) A UI_B session lasts more than 150 seconds

Mean = 126.2584860638 seconds; sample SD = 83.6443611028 seconds.
z_lower = (150.0000000000 - 126.2584860638) / 83.6443611028 = 0.2838387863.
Formula: `norm.sf((lower - mean) / sample_sd)`.
Substitution: norm.sf(0.2838387863) = 0.3882669646 = 38.826696%.
Under the normal approximation, about 38.83% of individual UI_B sessions satisfy this event.

### (d) A UI_A session lasts strictly between 80 and 120 seconds

Mean = 99.6630740076 seconds; sample SD = 71.5636198220 seconds.
z_lower = (80.0000000000 - 99.6630740076) / 71.5636198220 = -0.2747635468.
z_upper = (120.0000000000 - 99.6630740076) / 71.5636198220 = 0.2841796718.
Formula: `norm.cdf(z_upper) - norm.cdf(z_lower)`.
Substitution: norm.cdf(0.2841796718) - norm.cdf(-0.2747635468) = 0.2201147005 = 22.011470%.
Under the normal approximation, about 22.01% of individual UI_A sessions satisfy this event.

## Supplementary empirical comparison

Observed proportions use the matching group denominator and strict inequalities.
They describe this sample directly and are not replacements for the required model answers.

| Question | Count / denominator | Observed proportion | Observed % | Normal-model % | Observed minus model (percentage points) |
|---|---:|---:|---:|---:|---:|
| a | 1405 / 5013 | 0.2802712946 | 28.027129 | 35.508301 | -7.481171 |
| b | 2448 / 5013 | 0.4883303411 | 48.833034 | 39.174895 | +9.658139 |
| c | 1542 / 4987 | 0.3092039302 | 30.920393 | 38.826696 | -7.906303 |
| d | 1057 / 5013 | 0.2108517854 | 21.085179 | 22.011470 | -0.926292 |

Differences reflect the normal approximation versus the observed, skewed distribution;
empirical rates are sample estimates, not exact population probabilities.

## Business impact

Absolute difference = mB - mA = 126.2584860638 - 99.6630740076 = 26.5954120562 seconds.
Percentage increase = 100 * (mB - mA) / mA = 100 * (126.2584860638 - 99.6630740076) / 99.6630740076 = 26.68532184%.
This is a relative percentage increase in mean duration, not percentage points.
The verified Step 4 Welch test gives two-sided p = 1.79827227e-64 and 95% CI [23.54318756, 29.64763655] seconds for UI_B minus UI_A.
The mean difference is statistically significant at alpha=0.05; the interval excludes zero.
Statistical significance does not establish business importance. If longer engagement is
the business objective, UI_B is a candidate for adoption, conditional on practical value,
implementation costs, and checks of relevant outcomes. Longer sessions alone do not prove
improved usability, satisfaction, revenue, or conversion; they could also reflect friction.
Independence remains the assignment-supplied assumption, not a consequence of unique IDs.

## Verification and scope

Z-score probabilities are verified against norm.cdf/norm.sf with loc and scale directly.
All probabilities are within [0,1]. Event counts are checked by direct iteration as well
as vectorized strict comparisons. The full notebook independently recomputes and checks
these results against the script CSVs. Earlier verified results and originals are preserved.
No final report is created in Step 5.
