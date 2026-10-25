# **Zapas — Week 2 Evaluation Criteria**

## **Part B — Evaluation Criteria**

| Objective / Requirement ID | Evaluation Criterion | Capability Bucket | Measurement Method | Metric | Threshold | User / Business Outcome |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| O3 / NFR2 | Demand Forecasting Accuracy | Domain-specific capability | Compare predicted product demand against actual sales using historical test data and a historical-average baseline. | Mean Absolute Error (MAE) improvement | ≥ 10% lower MAE than baseline | Helps inventory managers plan restocking more accurately and reduce stock shortages or excess inventory. |
| O3 / NFR3 | Sentiment Classification Performance | Domain-specific capability | Evaluate sentiment predictions using a separate labelled dataset containing real positive, negative, and neutral customer reviews. | Macro F1-score | ≥ 0.75 | Helps businesses understand customer satisfaction and identify negative feedback. |
| O2 / FR3 / RAI2 | Product Complaint Identification | Domain-specific capability | Compare identified complaints against manually labelled customer reviews to verify whether the extracted issues are supported by the text. | Complaint extraction precision | ≥ 85% | Helps businesses identify genuine product issues and avoid misleading improvement recommendations. |
| O2 / FR4 | Restocking Recommendation Relevance | Instruction-following capability | Evaluate recommendations using predefined scenarios with demand forecasts, inventory quantities, and customer sentiment results. Compare outputs against expected actions defined in a decision rubric. | Recommendation agreement rate | ≥ 85% | Helps managers make more informed restocking decisions while considering product quality concerns. |
| O2 / RAI3 | Synthetic Data Transparency | Instruction-following capability | Test datasets containing real and synthetic reviews and verify whether the system correctly identifies synthetic records. | Correct synthetic data identification rate | 100% | Prevents businesses from confusing generated reviews with genuine customer feedback. |
| O3 / RAI1 | Demand Forecast Reliability Warning | Instruction-following capability | Test products with insufficient historical sales data and verify whether the system displays the required warning. | Warning detection rate | 100% | Prevents managers from relying on demand predictions without sufficient historical evidence. |
| O3 / NFR1 | System Response Time | Cost and latency | Measure the response time of repeated dashboard requests using a fixed dataset and preloaded models. | 90th percentile latency (p90) | ≤ 5 seconds | Ensures inventory managers can access predictions and recommendations without excessive delays. |

## 

## **Evaluation Notes**

The proposed thresholds are initial targets and will be refined during system development if necessary.

Demand forecasting will be evaluated using historical sales data that is separated chronologically into training and testing periods to prevent data leakage.

Sentiment classification and complaint identification will be evaluated using labelled real customer reviews whenever possible. Synthetic reviews may be used for system demonstration and integration testing but will not be treated as evidence of actual customer satisfaction.

Restocking recommendation relevance will be evaluated using predefined test scenarios and expected actions. The system will provide recommendations only, while final inventory decisions remain the responsibility of business users.

## **Reflection**

**Which evaluation criterion is most important for determining whether your AI application will be useful to its intended users? Why?**

The most important evaluation criterion for Zapas is restocking recommendation relevance because the main purpose of the system is to help businesses make better inventory decisions. Although accurate demand forecasting and sentiment analysis are important, the system must also combine these results effectively to provide useful recommendations. For example, if a product has high predicted demand but receives many negative reviews about its quality, the system should recommend investigating the quality issues before restocking in large quantities. Therefore, evaluating recommendation relevance is important to determine whether Zapas can support practical business decisions.

