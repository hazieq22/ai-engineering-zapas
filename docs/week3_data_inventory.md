# Zapas Week 3 data inventory

## A1 Requirements and current scope

The local Week 1 scope, all three Week 2 Markdown documents, and the Week 2 architecture image were inspected. The current user instruction supersedes their clothing/sentiment scope: all categories and stores are retained; forecasting is monthly per Store ID and Product ID. This implementation expands the sales/inventory input and preprocessing component of the Week 2 architecture. Review analysis is outside this lab's current scope.

| Requirement | Needed information | Implementation evidence |
|---|---|---|
| FR1 | Original sales and inventory | Immutable raw CSV and sorted daily export retaining every original attribute |
| FR2 | Monthly historical demand | Monthly units sold, calendar lags and strictly historical rolling means |
| FR4, restocking portion | Stock and forecast demand | Last observed inventory and its observation date retained; future recommendation logic requires supplier lead time, safety stock and human review |
| RAI1 | History sufficiency | history_ready, complete_month and eligible_for_training flags |
| NFR4 | Invalid-input handling | Fail on bad keys/schema/date; explicit missing-sales handling and validation evidence |
| NFR2 | Chronological evaluation | Month-based train/validation/test labels; no forecast accuracy claim in Topic 3 |

## A2 and A3 Source identity and actual inspection

| Source | Type/purpose | Version/owner | Access/rights | Evidence |
|---|---|---|---|---|
| S01 retail_store_inventory.csv | Daily sales and stock CSV | Local content hash in input_provenance.json; publisher attribution from prior inventory: anirudhchauhan | User's local ZIP; upstream licence/version unverified | 73,100 rows, 15 attributes, 2022-01-01 through 2024-01-01 |
| S01-A P0001 | Representative product subset, all stores | Same source | Same rights | First five original records printed in notebook |
| S01-B P0002 | Second representative product subset, all stores | Same source | Same rights | First five original records printed in notebook |

Referenced upstream source: https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset . The page was opened but exposed no readable licence metadata. Do not infer redistribution rights from public download access. The prior inventory describes the dataset as synthetic; this is an inherited attribution, not independently established from the CSV.

The referenced chat did not expose attachments. Actual local files inspected were `Topic 3_Lab.docx` and `archive (13).zip`; equivalence to `Topic 3_Lab(1).docx` and `archive (13)(2).zip` cannot be established. Their SHA-256 hashes and sizes are recorded. The archive contains one CSV, which matches the local extracted CSV byte-for-byte. These are actual user-local data, not replacement or generated retail records.

There are 5 stores, 20 products, 100 store/product series and 5 categories: Clothing, Electronics, Furniture, Groceries, Toys. There are no missing raw fields, invalid dates or duplicate store/product/day keys. Repeated dates across different series are expected and are never deduplicated by date alone.

## A4 Attribute inventory

| Attribute | Inferred raw dtype | Missing | Retention |
|---|---|---|---|
| Date | object | 0 | Daily export preserves this attribute |
| Store ID | object | 0 | Daily export preserves this attribute |
| Product ID | object | 0 | Daily export preserves this attribute |
| Category | object | 0 | Daily export preserves this attribute |
| Region | object | 0 | Daily export preserves this attribute |
| Inventory Level | int64 | 0 | Daily export preserves this attribute |
| Units Sold | int64 | 0 | Daily export preserves this attribute |
| Units Ordered | int64 | 0 | Daily export preserves this attribute |
| Demand Forecast | float64 | 0 | Daily export preserves this attribute |
| Price | float64 | 0 | Daily export preserves this attribute |
| Discount | int64 | 0 | Daily export preserves this attribute |
| Weather Condition | object | 0 | Daily export preserves this attribute |
| Holiday/Promotion | int64 | 0 | Daily export preserves this attribute |
| Competitor Pricing | float64 | 0 | Daily export preserves this attribute |
| Seasonality | object | 0 | Daily export preserves this attribute |

All raw bytes are retained under data/raw, including the original archive. All 15 attributes and 73,100 records also remain in prepared_timeseries.csv. Monthly aggregation is a separate analytical view, not a lossless replacement of the original. The source hash identifies an immutable input version.

## Observed limitations

All 20 products have varying category labels, and all 5 stores have varying region labels. No category or region is assigned as a stable dimension and no grouping uses these inconsistent attributes. Review identity semantics before real deployment.

January 2024 contains only January 1 for each series. Its observed sales remain present, but its full-month target is missing and it is ineligible for training. Missing calendar months are represented explicitly with missing sales, never invented zeros. A missing daily sales value also makes that month's training target unavailable.

Monthly sales are observed sales, not unconstrained demand; stockouts may censor demand. The source Demand Forecast has unknown production timing and is excluded from model inputs. Contemporaneous inventory, price, promotions and other future-unknown fields are preserved for audit but not included in the forecasting feature allowlist.

## Verified result

2,500 monthly records; 2,400 complete and 100 incomplete. 2,100 rows have at least three complete preceding months. Split counts: {'train': 1500, 'ineligible': 400, 'validation': 300, 'test': 300}. All raw sales reconcile to monthly observed sales: 9,975,582 units.

See data/processed/validation_report.json for computed evidence and notebook outputs for samples. Topic 4 must evaluate fitness for purpose; these checks do not establish production readiness or forecast quality.
