# Zapas — Monthly Sales Forecasting and Restocking Decision Support

## Current scope — Topic 3

The current project prepares monthly sales forecasting data separately for every Store ID and Product ID. All stores, categories, raw rows and original attributes are retained. Customer reviews, sentiment analysis and complaint analysis are outside the current scope. Restocking remains future human-reviewed decision support, not automatic ordering.

The Topic 3 submission implements data engineering (Pathway F), not model training. Later forecasting experiments are separate and are not included in this submission. The earlier proposal and Week 1/2 documents below may describe a superseded scope.

## Topic 3 — Data engineering pipeline

Zapas now prepares monthly sales by Store ID and Product ID across all stores/categories. All original rows and attributes remain available. Current scope is forecasting and restocking data preparation.

- [Executed pipeline notebook](notebooks/week3_pipeline.ipynb)
- [Data inventory](docs/week3_data_inventory.md)
- [Pipeline diagram](docs/week3_pipeline_diagram.png)
- [Decisions and stage contracts](docs/week3_pipeline_decisions.md)
- [Part B lineage](data/week3_manifest.json)
- [Part C pipeline](data/pipeline_v1/timeseries/)
- [Validation evidence](docs/test_report.json)

Local execution: 73,100 daily rows retained; 2,500 monthly records; 100 partial January 2024 records retained and excluded as full-month targets. Same-input reruns match. Historical features use only prior complete months within each series. This lab does not train or evaluate a forecasting model.

Submission files are stored in the linked repository paths above. See [commit history](https://github.com/hazieq22/ai-engineering-zapas/commits/main/) for publication history. Source licence and equivalence to the suffixed chat uploads remain unverified; see the provenance record.


---

## Earlier proposal — retained for history

# Zapas — AI-Based Inventory Demand Forecasting and Customer Review Analysis for Restocking Decision Support

Zapas is an AI-powered decision support system that helps retail businesses forecast product demand, analyse customer reviews, and make better restocking and product improvement decisions.

## Problem Statement

Retail businesses may face difficulties in making effective restocking decisions when relying only on historical sales and current inventory levels without considering customer feedback. Products with high sales may still receive negative reviews related to quality, which can lead to repeated customer dissatisfaction if the same products are restocked without improvement.

Zapas aims to integrate AI-based demand forecasting and customer review analysis to help businesses predict inventory needs, identify common product issues, and provide recommendations for better restocking and product improvement decisions.

## Evidence of the Problem

- **Retail Demand Forecasting:** Fildes et al. (2022) highlighted the challenges of retail demand forecasting, including variations in customer demand and product-level sales patterns.
- **Customer Review Analysis:** Zhang et al. (2022) demonstrated how online customer reviews can be analysed to identify customer needs and support product improvement strategies.

## Initial Related Work / Existing Approaches

1. **Makridakis et al. (2022) — Retail Sales Forecasting:** Investigated forecasting methods through the M5 competition. However, the study focused on forecasting accuracy rather than integrating customer complaints into product improvement and restocking decisions.
2. **Zhang et al. (2022) — Customer Review Analysis:** Proposed an approach for identifying customer requirements through sentiment analysis. However, the study did not integrate inventory demand forecasting.
3. **Fan et al. (2017) — Sales Forecasting Using Customer Reviews:** Combined historical sales data and online customer sentiment for sales forecasting. However, the study did not focus on integrated recommendations for inventory replenishment and product quality improvement.

## Engineering Gap / Limitation

Existing approaches often focus on inventory demand forecasting or customer review analysis separately. Although some studies integrate sales data and sentiment analysis, they do not necessarily provide combined recommendations for restocking and product quality improvement.

Zapas aims to address this gap by integrating demand forecasting, customer sentiment analysis, and complaint identification into a single decision support system.

## Project Objectives

- **O1:** To design an AI-based decision support system that integrates inventory demand forecasting and customer review analysis for retail businesses.
- **O2:** To develop the system using machine learning to predict product demand and natural language processing to identify customer sentiment and common product complaints, providing recommendations for restocking and product improvement.
- **O3:** To evaluate the system's performance in terms of demand forecasting accuracy, sentiment classification performance, complaint identification accuracy, and the relevance of generated recommendations.

## Target Users

- **Retail Business Owners:** Make informed inventory and product improvement decisions.
- **Inventory Managers:** Monitor stock levels and plan restocking based on predicted demand.
- **Product Management Teams:** Identify customer complaints and areas for product improvement.

## Data Sources

**Source 1: Fashion Retail Sales Dataset (GitHub)**

https://github.com/Ishita95-AIML/-Fashion-Retail-Sales-Dataset

A publicly available fashion retail dataset intended for historical sales analysis and demand forecasting.

**Source 2: Women's E-Commerce Clothing Reviews Dataset (Kaggle)**

https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews

A publicly available customer review dataset intended for developing and evaluating sentiment analysis.

**Synthetic Data**

Synthetic customer reviews may be used when suitable real customer reviews are unavailable. These reviews will be linked to products in the sales dataset to demonstrate how Zapas performs sentiment analysis, identifies common product complaints, and provides restocking and product improvement recommendations.

## Responsible AI Risks

- **Inaccurate Forecasting:** Incorrect predictions may lead to overstocking or understocking.
- **Sentiment Misclassification:** The NLP model may incorrectly interpret customer feedback and produce misleading recommendations.
- **Synthetic Data Bias:** Generated reviews may not accurately represent real customer opinions, affecting recommendation reliability.


## References

- Fan, Z.-P., Che, Y.-J., & Chen, Z.-Y. (2017). Product sales forecasting using online reviews and historical sales data: A method combining the Bass model and sentiment analysis. *Journal of Business Research, 74*, 90–100. https://doi.org/10.1016/j.jbusres.2017.01.010
- Fildes, R., Ma, S., & Kolassa, S. (2022). Retail forecasting: Research and practice. *International Journal of Forecasting, 38*(4), 1283–1318. https://doi.org/10.1016/j.ijforecast.2019.06.004
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting, 38*(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013
- Zhang, M., Sun, L., Wang, G. A., Li, Y., & He, S. (2022). Using neutral sentiment reviews to improve customer requirement identification and product design strategies. *International Journal of Production Economics, 254*, 108641. https://doi.org/10.1016/j.ijpe.2022.108641
