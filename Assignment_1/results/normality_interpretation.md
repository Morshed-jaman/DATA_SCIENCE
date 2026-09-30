# Step 3: normality assessment

All four exported figures were visually inspected before writing this interpretation.
Titles, group assignments, sample sizes, axes, and fitted reference lines are readable.

## Visual evidence

Both 25-bin histograms are unimodal and clearly right-skewed rather than symmetric
bell shapes. UI_A peaks in the shared bin around 28-55 seconds; UI_B peaks around
55-81 seconds. Both show long, sparse right tails. UI_B extends farther to the
right (maximum 666.51 seconds versus 525.95 for UI_A). Shared bin boundaries and
identical histogram axes permit direct comparison of frequencies.

Both normal Q-Q plots show pronounced upward curvature. Lower-tail points lie
above the fitted line and remain positive where the line extrapolates below zero;
many central points fall below the line, and upper-tail points rise markedly above
it. These systematic departures are inconsistent with normally distributed
individual durations. Negative fitted-line values are reference extrapolations,
not negative observed durations. The measured sample skewness is positive and
about 1.37 in both groups, consistent with the inspected plots.

## Shapiro-Wilk evidence and warning

H0: the group's individual durations follow a normal distribution.
H1: they do not follow a normal distribution. At alpha=0.05, both reported
p-values are far below the threshold, providing evidence against normality.
A large p-value would mean failure to reject H0, not proof of normality.
Large samples make normality tests sensitive even to small departures; here,
the visual departures and skewness also show substantial asymmetry.

UI_A uses all 5,013 observations and generates this captured SciPy warning:

> scipy.stats.shapiro: For N > 5000, computed p-value may not be accurate. Current N is 5013.

The exact UI_A p-value should therefore be treated cautiously, not as precisely
calibrated. SciPy documents that W remains accurate above 5,000 observations,
whereas the p-value may not. UI_B uses all 4,987 observations and does not trigger
that warning. No observations were subsampled and no warning was silently
suppressed: the warning is printed in both entry points and stored in the CSV.
The qualitative conclusion combines the test output with the visible curvature
and positive skewness rather than relying solely on UI_A's p-value magnitude.

Source: [SciPy Shapiro-Wilk documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html).

## Implications for later mean comparison

The distribution of individual durations differs from the sampling distribution
of a mean across repeated samples. Under independent sampling and finite population
variance, the central limit theorem supports an approximately normal sampling
distribution of the mean for sufficiently large samples even when individual
durations are non-normal. With roughly 5,000 observations per group, approximate
t-test inference for the difference in means may be reasonable under those
assumptions; raw-data normality is not established or required to become true.
Large sample size does not repair dependence, bias, or an unsuitable sampling design.

Independence is an assumption supplied by the assignment's scenario. Unique
session IDs do not establish independent users or observations, and the CSV alone
does not verify the collection design. Welch's test is a candidate for the next
stage because it accommodates unequal variances; it does not make the raw data
normal. No variance test or two-sample test has been performed at this stage.

All extreme values remain included. No durations were transformed and the
original files are unchanged. Probability scenarios and final-report creation
remain deferred.
