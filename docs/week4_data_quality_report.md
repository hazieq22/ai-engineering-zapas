# Topic 4 — Data Quality & Bias Report

Sales Forecasting and Inventory Restocking Decision Support | 18 November 2026

## 1. Project and Data Overview

The project prepares historical retail sales for forecasts that can inform stock decisions. Two Topic 2 requirements guide this audit. FR2 needs dated sales at product and store level, valid monthly targets, and features available before each forecast. RAI1 needs a measure of prior sales history and an eligibility flag so the system can warn users when history is insufficient. This audit checks the flag, not the dashboard warning. The recorded target is units sold. [Topic 2 requirements](week2_requirements.md)

Audited asset. Pathway F, Topic 3 Part B, `data/processed/monthly_sales_features.csv`. Matching manifest: `data/week3_manifest.json`, pipeline `zapas-week3-v1.0`, source S01. A fresh SHA-256 check matched both the output and source entries in the manifest. [Manifest](../data/week3_manifest.json)

Sample. One item is a store–product–month row. I inspected 16 of 2,500 items using two contiguous eight-month windows: S001/P0001, January–August 2022, and S005/P0020, June 2023–January 2024. This deliberately includes early history and the incomplete final month. It is a diagnostic sample. The validation rules below cover all rows.

## 2. Five-Dimension Quality Scorecard

| Dimension | Observed finding and evidence | Impact and status |
|---|---|
| Completeness | S005/P0020 has 1 of 31 days in January 2024 and a blank monthly target. V1 found the same partial-month pattern in all 100 January rows. | Warning: retain partial sales separately and exclude them as complete targets. |
| Consistency | In the raw data, all 20 product IDs appear under more than one category and all 5 store IDs under more than one region. | Review: category and region cannot be treated as fixed attributes of these IDs. |
| Accuracy | S001/P0001 in April 2022 reconciles to 4,874 units across 30 daily records. V1 matched all monthly totals to the source. | Pass for source reconciliation. Accuracy against real transactions is N.V. because no independent records were available. |
| Timeliness | Latest observation: 1 January 2024. Latest complete month: December 2023. | Warning: supports historical experiments. Current stock and current sales coverage are N.V. |
| Uniqueness | Zero duplicate store–product–month keys and zero missing key fields across 2,500 prepared rows. | Pass: one row per forecast series per month. |

## 3. Validation Findings

V1 — Source reconciliation and target completeness (FR2). Regroup daily sales by store, product and calendar month. Require totals, observed days, days with sales values and last dates to agree with the export. A target must equal the source total when every day is present with a sales value and be blank otherwise. 2,500 tested, 2,500 passed, 0 failed. A future mismatch blocks the affected export until reconciled.

V2 — Past sales features and history flag (FR2, RAI1). Recompute the first three lags, three-month rolling mean and sales trend from prior complete months within each series. Require the history flag to reflect three available preceding months and training eligibility to additionally require a complete target month. 2,500 tested, 2,500 passed, 0 failed. A feature mismatch blocks model input. Insufficient history must produce a warning. Display of that warning is N.V. because this audit examined the prepared CSV.

## 4. Duplicate, Anomaly and Coverage Findings

No duplicate daily keys were found across 73,100 source rows. The 100 series have all 25 expected calendar rows. The incomplete final month and early history gaps in feature eligibility were retained with flags.

| Case | Observed coverage | Implication |
|---|---|---|
| Complete history, January 2022–December 2023 | 2,400 complete rows across 100 series. The first three months give 300 rows with valid sales but insufficient prior history. The remaining 2,100 are eligible. | Supports chronological forecast experiments and tests of the insufficient-history flag. |
| Partial month, January 2024 | 100 rows with one day each and no complete targets. All 100 have enough prior history to populate the history flag. | Supports checking forecast inputs and partial-month handling. Full January actuals are unavailable for scoring. |

## 5. Bias Assessment

Inferred measurement risk. The source records units sold. If an item ran out, unmet purchases would not appear in sales records. A model trained on these records could understate future sales when stock is available, which may lead to a low restocking suggestion. The size of this effect is N.V. because stockout events and unmet demand are not independently recorded. Describe outputs as sales forecasts, and compare errors for confirmed stockout and in-stock periods when such records become available.

## 6. Privacy, Rights and Governance

S01 came from the supplied local archive. Its SHA-256 identifies the exact audited bytes. The inventory attributes it to a Kaggle source, but the upstream release, collection basis, synthetic or operational status, and permission for use and redistribution are N.V. The inspected schema has store/product codes and operational fields. It has no direct customer identifiers. Consent or ownership cannot be inferred from the schema.

This report uses aggregate audit results and does not include a copy of the source dataset. The audit identified source permissions and existing repository exposure as unresolved governance issues. Access-controlled storage is the planned safeguard for data with unclear sharing rights. Changes to the source, scope, preparation logic or permissions will trigger another audit. [Data inventory](week3_data_inventory.md)

## 7. Mitigation and Impact on Requirements

1. Verify source permissions before further sharing. I will identify the exact source release, document the permitted uses, and review access to the existing repository data. These findings will determine which evidence can be used or shared for FR2 and RAI1.
2. Check data and warning behaviour before a live trial. I will obtain recent, authorised sales and dated stock records, repeat V1 and V2, and test how the system responds to insufficient history and missing or outdated stock figures. This addresses data freshness for FR2 and the warning required by RAI1. Unrecorded lost sales and changes in category or region labels remain risks.

## 8. Quality-Gate Decision

GO WITH CONDITIONS — historical coursework evaluation on the audited Pathway F output, subject to permission for that use. The two file hashes match the manifest and both rules passed for all 2,500 rows. The 2,100 eligible rows can support chronological experiments with the documented history rule. The latest observation and missing full January targets prevent current stock decisions or January accuracy claims. Re-review before expanding use, after obtaining permission and fresh records, or when the source version or feature logic changes. Forecast accuracy and operational suitability require separate evaluation.
