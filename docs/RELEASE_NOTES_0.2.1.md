# DietaryIndex-Py 0.2.1 final rereview candidate

Date: 2026-08-21

This candidate closes formula-review findings before the manuscript results are frozen.

## Formula corrections

- MIND now follows the exact category boundaries in Morris et al. (2015), Table 1:
  green leafy vegetables score 0 at exactly 2 servings/week; beans require more
  than 3 servings/week for 1 point; the nuts middle category starts at one
  serving/month (operationalized as 0.25/week); wine scores 1 only at exactly one
  glass/day and 0.5 from one glass/month to less than one/day; and the
  butter/margarine 0.5 category includes exactly 2 tablespoons/day.
- NRF9.3 now uses `nrf9.3_2009_metric_capped_lim` as the default. Every positive
  and limiting DV/MRV term is capped at 100%, so the total range is -300 to 900.
  The former behavior remains available only as the explicitly named
  `nrf9.3_2009_metric_uncapped_lim` sensitivity variant.
- The corrected CHINA-DII Table-4 constants and DBI-07 citation/bands remain in
  place and are included in the final rereview evidence.

## Evidence changes

- All 20 raw boundary-input CSV files are included, together with the Python
  and independent R outputs and case-level comparison JSON files.
- MIND boundary fixtures now exercise every component cutoff below, at, and
  above the threshold. NRF fixtures include exact 100% MRV and adjacent cases.
- Human-review acceptance now requires two distinct reviewer identities and no
  unresolved `minor_revision` or `major_revision` decisions; signatures alone
  cannot produce a PASS.

## Compatibility

The NRF default changes numerically from 0.2.0. Analyses that intentionally need
the former uncapped limiting-nutrient behavior must request the explicit
`nrf9.3_2009_metric_uncapped_lim` version and report that choice.
