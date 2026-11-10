# Zapas Week 3 pipeline decisions

## B1 Selected pathway

Pathway F is selected because monthly forecasting requires timestamp parsing, chronology, per-series aggregation and history. CSV is the storage format; the task is time-series preparation. The other five pathways are not applicable.

## B2 and B3 Comparison and selected configuration

| Approach | Observed evidence | Benefit and limitation |
|---|---|---|
| Original daily source | 73,100 rows, 15 columns, 100 series | Preserves daily context; does not supply monthly targets or historical features |
| Parsed, sorted daily export plus monthly view | Daily count and attributes unchanged; 2,500 monthly records, 2,400 complete, 100 partial | Supports FR2 monthly forecasting and RAI1 completeness checks; monthly summaries hide within-month patterns, so daily data remain available |

Date parsing requires YYYY-MM-DD. Daily sorting uses Date, Store ID, Product ID. Invalid dates, absent identifiers and duplicate daily keys stop processing without modifying raw data. Missing non-key observations remain present. Missing sales make that monthly target unavailable. No category filter, store merging, sentiment processing or automatic row deletion occurs.

The monthly grain is Store ID + Product ID + month. Units Sold is summed; inventory_last_observed is the last day's recorded stock, with last_observed_date so partial periods cannot masquerade as month-end inventory. Category/region counts expose inconsistent mappings. All other attributes remain in the full daily export rather than being given misleading aggregations.

The target on month t is that month's complete sales. lag_1, lag_2, lag_3, lag_12, rolling_mean_3, rolling_mean_6 and sales_trend use complete sales strictly before t within the same series; month_number is known in advance. Calendar reindexing prevents gaps from turning row lags into incorrect month lags. No forward fill or zero imputation occurs. history_ready requires three immediately preceding complete months. Optional 6/12-month features may still be missing; a later model must choose a training-only missing-value policy or use the core lag_1/2/3 features.

Use only the manifest's model_feature_allowlist as numerical candidate predictors; Store ID/Product ID identify series. units_sold, target_units_sold, observed_days, complete_month, contemporaneous stock and source Demand Forecast are not predictors. Historical holdout labels use the final three eligible months for test and the preceding three for validation. This is rolling one-month-ahead evaluation: earlier test-month actuals become available for the next forecast origin. It is not a fixed-origin multi-step benchmark. January 2024 is retained as a partial observation with a null full-month target.

## B4 Metadata and C1 execution

Part B exports data/processed/ and data/week3_manifest.json. The identical transformation runs in Part C under data/pipeline_v1/timeseries/ with pipeline_manifest.json. Fingerprints cover input and outputs, output sizes, settings, source-output mappings and runtime versions. Repeatability compares two real executions, excluding execution timestamps. This proves same-runtime repeatability only.

Batch ETL is chosen: a static ZIP/CSV is ingested, transformed and validated, then loaded into prepared CSV storage. A streaming service is not justified by this input. Raw retention provides replay and audit. The notebook embeds the same implementation as src/week3_pipeline.py and needs no repository clone or credentials. It uses the lab's /content/week3_project workspace in Colab.

## C2 and C3 Stage contracts

| Stage | Contract and evidence | Failure response |
|---|---|---|
| Ingest | Exactly named CSV or one ZIP member; readable source and fingerprint | Stop for missing/ambiguous input |
| Inspect | Nonempty required schema; valid dates and series keys; missingness report | Stop on bad schema/date/duplicate keys; retain source for correction |
| Prepare | Full daily data plus separate monthly series; no cross-series lags | Raise on transform failure; rerun from unchanged raw |
| Validate | CSV readback matches values/schema/counts; sales conservation; no partial targets | Raise and treat run as failed; do not use exports from a failed run |
| Record lineage | Actual source and output hashes, sizes, mappings | Stop/report missing file or fingerprint mismatch |
| Repeat | Stable source/output fingerprints and mapping | Investigate input/configuration/runtime changes |

The diagram expands only sales/inventory preprocessing in docs/week2_architecture_v1.png. Its editable Draw.io source accompanies the PNG. Upstream Week 2 documents are historical context; this lab's explicit scope overrides their sentiment and clothing assumptions.

## C4 Publication and limitations

The existing public repository https://github.com/hazieq22/ai-engineering-zapas was inspected in the signed-in browser. Its data, docs, notebooks and src folders already exist, alongside earlier project material. The user chose manual upload; no remote files were changed. README_WEEK3_APPEND.md is a merge-ready addition for the existing README; do not overwrite prior weeks. The local package preserves the requested folder structure. C4a packaging is complete; C4b publishing and online verification remain the user's manual submission step.

Source licence/version and equivalence to the differently suffixed chat uploads remain unverified. Public redistribution requires confirming rights; the local complete archive is retained for the user. No model is trained and no restocking amount, accuracy, NFR response-time result or completion of the full NFR4 20-scenario benchmark is claimed.
