"""Explore durations, assess normality, and verify two-sample mean inference."""
from pathlib import Path
import os
import warnings
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats


def create_normality_figures(groups, directory):
    """Save four full-range figures; identical histogram bins and axis limits."""
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.venv' / 'matplotlib_cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    directory.mkdir(parents=True, exist_ok=True)
    pooled = np.concatenate([np.asarray(v) for v in groups.values()])
    edges = np.linspace(pooled.min(), pooled.max(), 26)
    ymax = max(np.histogram(v, bins=edges)[0].max() for v in groups.values()) * 1.10
    paths = []
    for label, values in groups.items():
        color = {'UI_A': '#176B99', 'UI_B': '#B5571E'}[label]
        fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
        ax.hist(values, bins=edges, color=color, edgecolor='white', linewidth=0.8)
        ax.set(xlim=(0, edges[-1] * 1.02), ylim=(0, ymax),
               xlabel='Session duration (seconds)', ylabel='Frequency',
               title=f'{label} session durations | n = {len(values):,} | 25 shared bins')
        ax.grid(axis='y', alpha=0.2)
        ax.set_axisbelow(True)
        path = directory / f'{label}_histogram.png'
        fig.savefig(path, dpi=180)
        plt.close(fig)
        paths.append(path)

        fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
        scipy_stats.probplot(values, dist='norm', fit=True, plot=ax)
        ax.lines[0].set(color=color, markersize=3, alpha=0.6, label='Observed durations')
        ax.lines[1].set(color='#A32D38', linewidth=2, label='Fitted reference line')
        ax.set(xlabel='Theoretical normal quantiles', ylabel='Ordered session duration (seconds)',
               title=f'{label} normal Q-Q plot | n = {len(values):,}')
        ax.grid(alpha=0.2)
        ax.legend(loc='upper left')
        path = directory / f'{label}_qq_plot.png'
        fig.savefig(path, dpi=180)
        plt.close(fig)
        paths.append(path)
    return paths


def assess_normality(groups):
    rows = []
    for label, values in groups.items():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            result = scipy_stats.shapiro(values)  # All observations, no subsampling.
        messages = [f'{w.category.__name__}: {w.message}' for w in caught]
        for message in messages:
            print(f'{label} Shapiro-Wilk warning: {message}')
        rows.append({'ui_version': label, 'count': len(values),
                     'sample_skewness': scipy_stats.skew(values, bias=False),
                     'shapiro_W': result.statistic, 'shapiro_p_value': result.pvalue,
                     'warning': ' | '.join(messages)})
    return pd.DataFrame(rows).set_index('ui_version')

ROOT = Path(__file__).resolve().parents[1]
METRIC = 'session_duration_seconds'


def quality_checks(data):
    duration = pd.to_numeric(data[METRIC], errors='coerce')
    return pd.Series({
        'missing_cells': int(data.isna().sum().sum()),
        'duplicate_rows': int(data.duplicated().sum()),
        'duplicate_user_ids': int(data['user_id'].duplicated().sum()),
        'unexpected_ui_labels': int((~data['ui_version'].isin(['UI_A', 'UI_B'])).sum()),
        'non_numeric_or_nonfinite_durations': int((~np.isfinite(duration)).sum()),
        'nonpositive_durations': int((duration <= 0).sum()),
    }, name='count')


def verify_reference(stats):
    # Step 1 reference values are validation targets, never calculated outputs.
    for label, n, mean, sd in [('UI_A', 5013, 99.6631, 71.5636),
                               ('UI_B', 4987, 126.2585, 83.6444)]:
        assert stats.loc[label, 'count'] == n
        np.testing.assert_allclose(stats.loc[label, ['mean', 'std']],
                                   [mean, sd], rtol=0, atol=0.00005)


def compare_means(ui_b, ui_a):
    """Assignment selection rule; B minus A; verify SciPy using summaries."""
    alpha = 0.05
    levene = scipy_stats.levene(ui_b, ui_a, center='median')
    pooled = bool(levene.pvalue >= alpha)
    variance = pd.DataFrame([{
        'test_name': 'Levene (median-centered / Brown-Forsythe)',
        'statistic': levene.statistic, 'p_value': levene.pvalue,
        'alpha': alpha, 'selected_test': 'Student pooled' if pooled else 'Welch',
        'reject_equal_variances': bool(levene.pvalue < alpha)}])
    n_b, n_a = len(ui_b), len(ui_a)
    mean_b, mean_a = ui_b.mean(), ui_a.mean()
    sd_b, sd_a = ui_b.std(ddof=1), ui_a.std(ddof=1)
    difference = mean_b - mean_a
    rows = []
    specifications = [(pooled, 'selected')]
    if pooled:
        specifications.append((False, 'sensitivity'))
    for equal_var, role in specifications:
        result = scipy_stats.ttest_ind(ui_b, ui_a, equal_var=equal_var,
                                      alternative='two-sided')
        ci = result.confidence_interval(confidence_level=0.95)
        # Independent summary-statistic formulas; never use SciPy's private SE.
        if equal_var:
            pooled_variance = ((n_b-1)*sd_b**2 + (n_a-1)*sd_a**2)/(n_b+n_a-2)
            se = np.sqrt(pooled_variance*(1/n_b + 1/n_a))
            df = n_b+n_a-2
        else:
            term_b, term_a = sd_b**2/n_b, sd_a**2/n_a
            se = np.sqrt(term_b+term_a)
            df = (term_b+term_a)**2/(term_b**2/(n_b-1)+term_a**2/(n_a-1))
        manual_t = difference/se
        manual_p = 2*scipy_stats.t.sf(abs(manual_t), df)
        margin = scipy_stats.t.ppf(0.975, df)*se
        manual_low, manual_high = difference-margin, difference+margin
        np.testing.assert_allclose([manual_t, df, manual_low, manual_high],
                                   [result.statistic, result.df, ci.low, ci.high],
                                   rtol=1e-12, atol=0)
        assert manual_p > 0 and result.pvalue > 0
        np.testing.assert_allclose(manual_p, result.pvalue, rtol=1e-10, atol=0)
        rows.append({
            'test_name': 'Student pooled' if equal_var else 'Welch', 'role': role,
            'difference_direction': 'UI_B minus UI_A', 'alternative': 'two-sided',
            'alpha': alpha, 'equal_var': equal_var,
            'n_B': n_b, 'mean_B': mean_b, 'sample_sd_B': sd_b,
            'n_A': n_a, 'mean_A': mean_a, 'sample_sd_A': sd_a,
            'mean_difference_seconds': difference, 'standard_error_seconds': se,
            't_statistic': result.statistic, 'degrees_of_freedom': result.df,
            'p_value': result.pvalue, 'ci_95_low_seconds': ci.low,
            'ci_95_high_seconds': ci.high,
            'decision': 'Reject H0' if result.pvalue < alpha else 'Fail to reject H0',
            'manual_t': manual_t, 'manual_df': df, 'manual_p_value': manual_p,
            'manual_ci_low': manual_low, 'manual_ci_high': manual_high,
            'manual_verified': True})
    return variance, pd.DataFrame(rows)


def probability_scenarios(ui_a, ui_b, tests):
    """Untruncated normal models for individuals, plus separate observed rates."""
    mA, sA = ui_a.mean(), ui_a.std(ddof=1)
    mB, sB = ui_b.mean(), ui_b.std(ddof=1)
    specifications = [
        ('a', 'UI_A', 'A UI_A session exceeds the UI_B sample mean', mB, np.inf),
        ('b', 'UI_A', 'A UI_A session lasts less than 80 seconds', -np.inf, 80.0),
        ('c', 'UI_B', 'A UI_B session lasts more than 150 seconds', 150.0, np.inf),
        ('d', 'UI_A', 'A UI_A session lasts strictly between 80 and 120 seconds', 80.0, 120.0),
    ]
    rows = []
    for question, group, event, lower, upper in specifications:
        values = ui_a if group == 'UI_A' else ui_b
        mean, sd = (mA, sA) if group == 'UI_A' else (mB, sB)
        zl, zu = (lower-mean)/sd, (upper-mean)/sd
        if np.isposinf(upper):
            probability = scipy_stats.norm.sf(zl)
            direct = scipy_stats.norm.sf(lower, loc=mean, scale=sd)
            formula = 'norm.sf((lower - mean) / sample_sd)'
        elif np.isneginf(lower):
            probability = scipy_stats.norm.cdf(zu)
            direct = scipy_stats.norm.cdf(upper, loc=mean, scale=sd)
            formula = 'norm.cdf((upper - mean) / sample_sd)'
        else:
            probability = scipy_stats.norm.cdf(zu)-scipy_stats.norm.cdf(zl)
            direct = (scipy_stats.norm.cdf(upper, loc=mean, scale=sd)
                      - scipy_stats.norm.cdf(lower, loc=mean, scale=sd))
            formula = 'norm.cdf(z_upper) - norm.cdf(z_lower)'
        count = int(((values > lower) & (values < upper)).sum())
        assert count == sum(lower < float(value) < upper for value in values)
        denominator = len(values)
        empirical = count/denominator
        assert 0 <= count <= denominator
        assert all(0 <= p <= 1 for p in [probability, direct, empirical])
        np.testing.assert_allclose(probability, direct, rtol=1e-13, atol=0)
        rows.append(dict(question=question, group=group, event=event,
                         model='Assignment normal-model approximation',
                         mean_seconds=mean, sample_sd_seconds=sd,
                         lower_bound_seconds=lower, upper_bound_seconds=upper,
                         z_lower=zl, z_upper=zu, formula=formula,
                         normal_probability=probability, normal_percentage=100*probability,
                         empirical_count=count, denominator=denominator,
                         empirical_proportion=empirical, empirical_percentage=100*empirical,
                         empirical_minus_normal_percentage_points=100*(empirical-probability)))
    selected = tests.loc[tests['role'].eq('selected')].iloc[0]
    difference = mB-mA
    np.testing.assert_allclose(difference, selected['mean_difference_seconds'], rtol=1e-13, atol=0)
    business = pd.DataFrame([dict(mean_A_seconds=mA, mean_B_seconds=mB,
        absolute_difference_seconds=difference, percentage_increase=100*difference/mA,
        difference_direction='UI_B minus UI_A', test_name=selected['test_name'],
        p_value=selected['p_value'], ci_95_low_seconds=selected['ci_95_low_seconds'],
        ci_95_high_seconds=selected['ci_95_high_seconds'],
        statistically_significant=bool(selected['p_value'] < 0.05))])
    return pd.DataFrame(rows), business


def write_probability_interpretation(probabilities, business, path):
    """Build a reproducible Step 5 explanation from full-precision results."""
    lines = ['# Step 5: probability scenarios and business impact', '',
        '## Required normal-model approximations', '',
        'XA ~ Normal(mA, sA^2) and XB ~ Normal(mB, sB^2), using CSV sample means',
        'and individual-duration sample SDs (ddof=1), NOT standard errors.',
        'Displayed substitutions are rounded; computations retain full precision.', '',
        'Both groups are right-skewed and non-normal. These are the assignment-required',
        'normal-model approximations, not validated individual-duration distributions.',
        'Large independent samples support inference for means but do not make individual',
        'durations normal. The requested normal models remain untruncated, including their',
        'theoretical support below zero; no data or model transformations are applied.', '']
    for _, r in probabilities.iterrows():
        lines += [f"### ({r['question']}) {r['event']}", '',
                  f"Mean = {r.mean_seconds:.10f} seconds; sample SD = {r.sample_sd_seconds:.10f} seconds."]
        for side in ['lower', 'upper']:
            bound = r[f'{side}_bound_seconds']
            if np.isfinite(bound):
                lines.append(f"z_{side} = ({bound:.10f} - {r.mean_seconds:.10f}) / {r.sample_sd_seconds:.10f} = {r[f'z_{side}']:.10f}.")
        if np.isposinf(r.upper_bound_seconds):
            substitution = f'norm.sf({r.z_lower:.10f})'
        elif np.isneginf(r.lower_bound_seconds):
            substitution = f'norm.cdf({r.z_upper:.10f})'
        else:
            substitution = f'norm.cdf({r.z_upper:.10f}) - norm.cdf({r.z_lower:.10f})'
        lines += [f"Formula: `{r.formula}`.",
                  f"Substitution: {substitution} = {r.normal_probability:.10f} = {r.normal_percentage:.6f}%.",
                  f"Under the normal approximation, about {r.normal_percentage:.2f}% of individual {r.group} sessions satisfy this event.", '']
        if r.question == 'a':
            lines += ["The threshold is UI_B's full-precision sample mean, held fixed. This is NOT P(XA > XB).", '']
    lines += ['## Supplementary empirical comparison', '',
              'Observed proportions use the matching group denominator and strict inequalities.',
              'They describe this sample directly and are not replacements for the required model answers.', '',
              '| Question | Count / denominator | Observed proportion | Observed % | Normal-model % | Observed minus model (percentage points) |',
              '|---|---:|---:|---:|---:|---:|']
    for _, r in probabilities.iterrows():
        lines.append(f'| {r.question} | {r.empirical_count} / {r.denominator} | {r.empirical_proportion:.10f} | {r.empirical_percentage:.6f} | {r.normal_percentage:.6f} | {r.empirical_minus_normal_percentage_points:+.6f} |')
    r = business.iloc[0]
    lines += ['', 'Differences reflect the normal approximation versus the observed, skewed distribution;',
              'empirical rates are sample estimates, not exact population probabilities.', '',
              '## Business impact', '',
              f'Absolute difference = mB - mA = {r.mean_B_seconds:.10f} - {r.mean_A_seconds:.10f} = {r.absolute_difference_seconds:.10f} seconds.',
              f'Percentage increase = 100 * (mB - mA) / mA = 100 * ({r.mean_B_seconds:.10f} - {r.mean_A_seconds:.10f}) / {r.mean_A_seconds:.10f} = {r.percentage_increase:.8f}%.',
              'This is a relative percentage increase in mean duration, not percentage points.',
              f"The verified Step 4 {r.test_name} test gives two-sided p = {r.p_value:.8e} and 95% CI [{r.ci_95_low_seconds:.8f}, {r.ci_95_high_seconds:.8f}] seconds for UI_B minus UI_A.",
              'The mean difference is statistically significant at alpha=0.05; the interval excludes zero.',
              'Statistical significance does not establish business importance. If longer engagement is',
              'the business objective, UI_B is a candidate for adoption, conditional on practical value,',
              'implementation costs, and checks of relevant outcomes. Longer sessions alone do not prove',
              'improved usability, satisfaction, revenue, or conversion; they could also reflect friction.',
              'Independence remains the assignment-supplied assumption, not a consequence of unique IDs.', '',
              '## Verification and scope', '',
              'Z-score probabilities are verified against norm.cdf/norm.sf with loc and scale directly.',
              'All probabilities are within [0,1]. Event counts are checked by direct iteration as well',
              'as vectorized strict comparisons. The full notebook independently recomputes and checks',
              'these results against the script CSVs. Earlier verified results and originals are preserved.',
              'No final report is created in Step 5.']
    path.write_text('\n'.join(lines)+'\n', encoding='utf-8')


def main():
    data = pd.read_csv(ROOT / 'ui_ab_testing_data.csv')
    print('First 10 rows:\n', data.head(10).to_string(index=False))
    print('\nDimensions:', data.shape)
    print('\nColumns:', data.columns.tolist())
    print('\nData types:\n', data.dtypes)
    print('\nMissing values by column:\n', data.isna().sum())
    checks = quality_checks(data)
    print('\nQuality checks:\n', checks)
    print('\nUI group counts:\n', data['ui_version'].value_counts(dropna=False))
    if checks.any():
        raise ValueError('Data quality issues found; review without deleting or transforming rows.')
    groups = {label: data.loc[data['ui_version'].eq(label), METRIC]
              for label in ['UI_A', 'UI_B']}
    stats = pd.DataFrame({label: {
        'count': len(values), 'mean': values.mean(), 'std': values.std(ddof=1),
        'min': values.min(), '25%': values.quantile(0.25),
        '50%': values.median(), '75%': values.quantile(0.75), 'max': values.max()
    } for label, values in groups.items()}).T
    stats.index.name = 'ui_version'
    stats['count'] = stats['count'].astype('int64')
    verify_reference(stats)
    output = ROOT / 'results' / 'descriptive_statistics.csv'
    output.parent.mkdir(exist_ok=True)
    stats.to_csv(output)  # No rounding of saved values.
    print('\nDescriptive statistics (seconds; sample SD, ddof=1):\n', stats.round(4))
    print('\nStep 1 references verified. Saved:', output.relative_to(ROOT))
    normality = assess_normality(groups)
    normality.to_csv(ROOT / 'results' / 'normality_assessment.csv')
    print('\nNormality statistics (all observations; skewness bias=False):')
    print(normality.drop(columns='warning').to_string(formatters={
        'sample_skewness': '{:.6f}'.format, 'shapiro_W': '{:.6f}'.format,
        'shapiro_p_value': '{:.6e}'.format}))
    for path in create_normality_figures(groups, ROOT / 'figures'):
        print('Saved:', path.relative_to(ROOT))
    variance, tests = compare_means(groups['UI_B'], groups['UI_A'])
    variance.to_csv(ROOT / 'results' / 'variance_test.csv', index=False)
    tests.to_csv(ROOT / 'results' / 't_test_results.csv', index=False)
    print('\nMedian-centered Levene test:\n', variance.to_string(index=False,
          formatters={'p_value': '{:.8e}'.format}))
    print('\nMean comparison, UI_B minus UI_A:\n', tests.to_string(index=False,
          formatters={'p_value': '{:.8e}'.format, 'manual_p_value': '{:.8e}'.format}))
    print('PASS: independent summary formulas agree with SciPy; p-value atol=0.')
    probabilities, business = probability_scenarios(groups['UI_A'], groups['UI_B'], tests)
    probabilities.to_csv(ROOT / 'results' / 'probability_scenarios.csv', index=False)
    business.to_csv(ROOT / 'results' / 'business_impact.csv', index=False)
    write_probability_interpretation(probabilities, business,
                                    ROOT / 'results' / 'probability_and_business_interpretation.md')
    print('\nProbability scenarios:\n', probabilities.to_string(index=False))
    print('\nBusiness impact:\n', business.to_string(index=False, formatters={'p_value': '{:.8e}'.format}))
    print('PASS: z-score/direct probabilities, bounds, and strict empirical counts verified.')


if __name__ == '__main__':
    main()
