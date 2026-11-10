# Topic 3 lab completion checklist

Project: Zapas. Selected pathway: F, time-series. Source: the user's local retail_store_inventory.csv, retained in full. This checklist follows the inspected Topic 3_Lab.docx. Equivalence to the suffixed chat attachment cannot be confirmed; see input_provenance.json.

| Lab step | Status | Deliverable or evidence |
|---|---|---|
| A1 Requirements to data needs | Complete | week3_data_inventory.md maps FR1, FR2, the restocking portion of FR4, RAI1 and NFR4; Week 1/2 documents and architecture inspected |
| A2 Workspace and source access | Implemented and locally executed | Notebook workspace/upload/source-verification cells; Colab uses /content/week3_project |
| A3 Inspect source and two subsets | Complete | Executed notebook prints schema, missingness, dates and P0001/P0002 samples |
| A4 Source inventory | Complete | week3_data_inventory.md and input_provenance.json |
| B1 Pathway selection | Complete | Pathway F justified by monthly forecasting and chronological preparation |
| B2 Preparation | Complete | Explicit source selection, parsed dates, stable chronology, full daily export and separate monthly store/product view |
| B3 Compare and validate | Complete | Original-versus-prepared comparison, readback checks, preserved data, reconciled totals and feature validation |
| B4 Source/output lineage | Complete | data/week3_manifest.json with SHA-256 hashes, sizes, settings and source/output relationships |
| C1 Executable V1 pipeline | Complete | src/week3_pipeline.py and self-contained notebook; data/pipeline_v1/timeseries/ outputs and manifest |
| C1 Repeatability | Complete | Two actual reruns; repeatability_report.json and test_report.json; notebook exports match script exports |
| C2 Executed workflow diagram | Complete | week3_pipeline_diagram.png and editable .drawio; actual stages and two failure responses |
| C3 Decisions and contracts | Complete | week3_pipeline_decisions.md covers comparison, configuration, requirements, ETL, batch rationale, limitations and stage contracts |
| C4a Save/package artefacts | Complete | Full local package, exact lab folder paths and executed notebook |
| C4b Commit and verify online | Repository submission | Files committed into existing repository folders; publication is verifiable through GitHub commit history and the linked notebook, manifests and documentation |

## Verified outcomes

- 73,100 daily records and all 15 original attributes retained.
- Five stores, 20 products and all 100 store/product series retained across all five categories.
- 2,500 monthly records: 2,400 complete months and 100 partial January 2024 records.
- 2,100 rows eligible under the three-month history rule; chronological split is 1,500 train, 300 validation and 300 test rows.
- Partial periods remain visible with no full-month target. No invented zero-sales months or cross-store aggregation.
- Eleven verification groups passed, including independent aggregation checks, leakage, series isolation, bad-input handling, hashes, reruns and complete notebook execution.

## Scope and evidence boundaries

This is the Topic 3 data engineering lab. It does not train a forecasting model, evaluate model accuracy, perform sentiment analysis or place restocking orders. Other preparation pathways are alternatives and are not required. Comprehensive Topic 4 data-quality and Responsible AI assessment remains later work.

The notebook was executed with a real local Jupyter kernel, not in hosted Google Colab. The exact local input files and dependency versions are recorded. Dataset licence/version and equivalence to differently suffixed chat uploads remain unverified. The submission reuses the existing repository folders. The root README identifies the current scope and links all Topic 3 deliverables; earlier Week 1/2 files are preserved.
