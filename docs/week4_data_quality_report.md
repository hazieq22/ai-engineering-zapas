# Topic 4 — Data Quality & Bias Report

Sales Forecasting and Inventory Restocking Decision Support | 18 November 2026

## 1. Project and Data Overview

The project uses historical retail sales to forecast monthly units sold and inform restocking decisions. The audit addresses two Topic 2 requirements. FR2 requires dated sales by store and product, complete monthly sales totals for evaluation, and inputs available at the time of forecasting. RAI1 requires the system to warn users when sales history is insufficient. The audit assessed the data flag that supports this warning. Its display in the dashboard was not verified. [Topic 2 requirements](week2_requirements.md)

The audited file was data/processed/monthly_sales_features.csv, produced in Topic 3 Part B under Pathway F. The corresponding manifest, data/week3_manifest.json, identifies source S01 and pipeline version zapas-week3-v1.0. The SHA-256 hashes of the prepared and source files matched their manifest entries. [Manifest](../data/week3_manifest.json)

Each row represents one product at one store in one calendar month. The audit examined 16 of 2,500 rows in two consecutive eight-month windows, January to August 2022 for S001/P0001 and June 2023 to January 2024 for S005/P0020. The windows were selected to include months with limited prior history and the incomplete final month. Both validation rules were applied to the full dataset.

## 2. Five-Dimension Quality Scorecard

| Dimension | Observed finding and evidence | Impact and status |
|---|---|
| Completeness | All 100 January 2024 rows contained sales for only one of 31 days and had no full-month target, including S005/P0020. | Warning. The recorded sales are retained, but the partial totals are excluded from full-month evaluation. |
| Consistency | Each of the 20 product IDs was associated with multiple categories. Each of the five store IDs was associated with multiple regions. | Review. Analysis by category or region requires a verified mapping. |
| Accuracy | The 30 daily records for S001/P0001 in April 2022 summed to the reported 4,874 units. All monthly totals matched the source under V1. | Pass for agreement with the source. Accuracy against actual transactions is N.V. because independent records were unavailable. |
| Timeliness | The latest observation was 1 January 2024. December 2023 was the last complete month. | Warning. The records support historical analysis. Current sales and stock levels are N.V. |
| Uniqueness | None of the 2,500 prepared rows had a duplicate key or a missing store, product or month value. | Pass. Each store and product combination has one row per month. |

## 3. Validation Findings

V1. Source reconciliation and target completeness (FR2). Daily sales were regrouped by store, product and calendar month. Monthly sales totals, day counts and the last observed dates were compared with the prepared file. A monthly target was expected only when every day had a recorded sales value. All 2,500 rows passed. A discrepancy in a future export would require reconciliation before use.

V2. Historical sales features and eligibility (FR2, RAI1). The first three monthly lags, three-month rolling mean and sales trend were recalculated from earlier complete months within each series. The history flag required three preceding complete months. Eligibility for model development and evaluation also required a complete target month. All 2,500 rows passed. A feature mismatch would prevent the affected data from being used as model input. The dashboard warning is N.V. because the audit covered the prepared file only.

## 4. Duplicate, Anomaly and Coverage Findings

The 73,100 daily source rows contained no duplicate store, product and date combinations. All 100 sales series contained the expected 25 monthly rows. The prepared data distinguish early months with insufficient prior history from the final month, which has enough prior history but an incomplete target.

| Case | Observed coverage | Implication |
|---|---|---|
| January 2022 to December 2023 | All 2,400 rows had complete monthly targets. The first 300 lacked three prior months of history. The remaining 2,100 met both eligibility conditions. | Provides data for chronological evaluation and examples of insufficient history. |
| January 2024 | All 100 rows met the history requirement and contained only one day of sales. | The prior history can support forecast inputs. A complete January sales total is unavailable for evaluating forecast accuracy. |

## 5. Bias Assessment

Stock availability is a potential source of measurement bias. Recorded sales count completed transactions. During a stockout, some customers who would have purchased a product may be unable to do so. A model trained on sales from those periods may underestimate future sales when the product is available, leading to a lower restocking quantity than required. The extent of this bias is N.V. because the audit had no independently verified records of stockouts or lost sales. The proposed control is to label predictions as forecasts of recorded sales and compare forecast errors across periods with verified differences in stock availability when suitable records are available.

## 6. Privacy, Rights and Governance

Source S01 was obtained from the supplied archive. Its SHA-256 hash identifies the exact version used in the audit. The data inventory records a Kaggle attribution. The upstream release, basis for collection, status as synthetic or operational data, and permissions for use and redistribution are N.V. The data fields examined contain store and product codes and operational values, with no direct customer identifiers. Ownership and any applicable consent arrangements remain unverified.

The report presents aggregate checks and limited examples. The proposed safeguard is restricted storage for data whose sharing rights remain unclear. The existing repository copies are included in the permissions review. Changes to the source, preparation steps, intended use or permissions will trigger revalidation. [Data inventory](week3_data_inventory.md)

## 7. Mitigation and Impact on Requirements

1. Dataset permissions. Further distribution depends on verifying the dataset release and its terms of use and reviewing access to existing repository copies. This establishes which data may be used for forecast evaluation under FR2 and for testing the sales history warning under RAI1.
2. Data freshness and warning tests. A live trial requires recent, authorised sales records and dated stock records. Repeating V1 and V2 checks whether the new sales data are suitable for forecasting under FR2. Tests with short sales histories check whether the RAI1 warning appears when required. Separate tests with missing or outdated stock records check whether the system withholds restocking suggestions when stock information is inadequate. Lost sales during stockouts and inconsistent category or region labels remain limitations.

## 8. Quality-Gate Decision

GO WITH CONDITIONS applies to historical coursework evaluation using the audited Pathway F output, subject to permission for that use. Both file hashes matched the manifest, both validation rules passed across all 2,500 rows, and 2,100 rows met the eligibility criteria for chronological evaluation. The incomplete January results cannot be used to assess full-month forecast accuracy, and current stock decisions require recent sales and dated stock records. The decision will be reviewed when source permissions are established, new records become available or the source version or feature logic changes. Forecast performance and suitability for operational use require separate evaluation.
