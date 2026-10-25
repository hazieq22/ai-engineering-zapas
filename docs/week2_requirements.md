# **Zapas: Week 2 Requirements Specification**

## **Section 0: Project Framing & Application Scope Checkpoint**

### **Problem Evidence**

Retail businesses need accurate demand forecasting to manage inventory and avoid overstocking or stock shortages. Fildes et al. (2022) discussed challenges in retail forecasting, while Zhang et al. (2022) demonstrated how customer reviews can help identify customer needs and product improvement opportunities.

### **Existing Approaches**

1. **Makridakis et al. (2022):** Evaluated different forecasting methods through the M5 forecasting competition.  
2. **Zhang et al. (2022):** Used customer reviews to identify customer requirements and support product improvement.  
3. **Fan et al. (2017):** Combined historical sales data and customer review sentiment to improve sales forecasting.

### **Project / Engineering Gap**

Existing approaches may focus on demand forecasting, customer review analysis, or using sentiment to improve sales predictions. Zapas aims to integrate these functions into a single decision support system that considers both predicted product demand and customer complaints when recommending restocking and product improvement actions.

### **Objective 1**

To design an AI-based decision support system that integrates inventory demand forecasting and customer review analysis for retail businesses.

### 

### **Objective 2**

To develop the system using machine learning to predict product demand and natural language processing to identify customer sentiment and common product complaints, providing recommendations for restocking and product improvement.

### **Objective 3**

To evaluate the system's performance in terms of demand forecasting accuracy, sentiment classification performance, complaint identification accuracy, and the relevance of generated recommendations.

### **Intended Users**

Retail business owners, inventory managers, and product management teams.

### **Supported Tasks**

* Analyse historical product sales and inventory information.  
* Predict future product demand.  
* Classify customer reviews as positive, negative, or neutral.  
* Identify common product complaints.  
* Provide restocking and product improvement recommendations.  
* Display results through a management dashboard.

### **Information / Knowledge Domain**

Retail inventory management, clothing product sales, demand forecasting, and customer feedback analysis.

### **Operating Context**

Zapas is intended to operate as a web-based decision support application for retail businesses. Users can view product demand predictions, inventory information, customer feedback analysis, and recommendations through an interactive dashboard.

### **Important Constraints**

* The project will use publicly available sales and customer review datasets.  
* Synthetic customer reviews may be used when suitable real reviews are unavailable.  
* Inventory quantities may be simulated if actual stock records are unavailable.  
* The accuracy of predictions depends on the quality and availability of historical data.  
* The system must be manageable within one academic semester.

### **Explicit Out-of-Scope Tasks**

* Automatically purchasing or ordering products from suppliers.  
* Making final business decisions without human approval.  
* Managing supplier contracts or manufacturing processes.  
* Guaranteeing actual product quality based only on customer reviews.  
* Predicting demand for unrelated industries outside the selected retail scope.

### **Evaluation Focus**

The evaluation will determine whether Zapas can accurately forecast product demand, classify customer sentiment, identify common product complaints, and provide relevant restocking and product improvement recommendations to support retail inventory decisions.

## **Section 1: Functional Requirements**

| ID | Requirement — The System SHALL | Scope Boundary — SHALL NOT |
| ----- | ----- | ----- |
| FR1 | The system shall allow users to load and analyse product sales, inventory information, and customer review data. | The system shall not modify the original datasets or treat synthetic data as real customer records. |
| FR2 | The system shall predict future product demand based on historical sales data to support inventory planning. | The system shall not guarantee that predicted demand will match actual future sales. |
| FR3 | The system shall classify customer reviews into positive, negative, or neutral sentiment and identify common product complaints. | The system shall not assume that every negative review represents a verified product defect. |
| FR4 | The system shall provide restocking and product improvement recommendations based on predicted demand, available inventory, and customer review analysis. | The system shall not automatically purchase products, place restocking orders, or make final business decisions without human approval. |
| FR5 | The system shall display product sales trends, demand forecasts, inventory information, sentiment analysis results, and recommendations through an interactive dashboard. | The system shall not display unsupported predictions or missing information as verified results. |

## **Section 2: Non-Functional Requirements**

| ID | Quality Attribute | Requirement | Measurement Method | Metric | Threshold |
| ----- | ----- | ----- | ----- | ----- | ----- |
| NFR1 | Performance | The system shall provide demand predictions, sentiment analysis results, and recommendations within an acceptable response time. | Measure response time across repeated requests using a fixed test dataset with models already loaded. | 90th percentile response time (p90) | ≤ 5 seconds |
| NFR2 | Correctness | The system shall generate demand forecasts with lower prediction errors than a simple baseline forecasting method. | Compare predicted demand against actual sales using a chronological test dataset and a historical-average baseline. | Mean Absolute Error (MAE) improvement | ≥ 10% lower MAE than baseline |
| NFR3 | Correctness | The system shall classify customer reviews into positive, negative, and neutral sentiment with acceptable accuracy. | Evaluate the sentiment classification model using a separate labelled test dataset containing real customer reviews. | Macro F1-score | ≥ 0.75 |
| NFR4 | Reliability | The system shall process valid product data without unexpected failures and handle missing or invalid information appropriately. | Conduct 20 predefined test scenarios covering valid inputs, missing values, and invalid records. | Test scenario success rate | ≥ 95% |

## 

## **Section 3 — Responsible AI Requirements**

**Version: 1.0**

| ID | Responsible AI Risk | Requirement | Measurement Method | Metric | Threshold |
| ----- | ----- | ----- | ----- | ----- | ----- |
| RAI1 | Inaccurate Demand Forecasting | The system shall clearly indicate when demand predictions are based on insufficient historical sales data to prevent misleading restocking recommendations. | Test products with insufficient sales history and verify whether appropriate warnings are displayed. | Warning detection rate | 100% |
| RAI2 | Misinterpretation of Customer Reviews | The system shall ensure that identified product complaints are supported by the original customer reviews and avoid presenting unsupported issues as facts. | Manually evaluate extracted complaints against a labelled set of customer reviews. | Complaint extraction precision | ≥ 85% |
| RAI3 | Synthetic Data Bias | The system shall clearly distinguish synthetic customer reviews from real customer reviews to prevent misleading interpretations of customer feedback. | Inspect displayed review results and reports using test datasets containing both real and synthetic reviews. | Correct synthetic data identification rate | 100% |

### **Reflection**

**Which Responsible AI requirement will be the most difficult to measure or enforce technically? Why?**

RAI2 will be the most difficult to measure because customer reviews may contain sarcasm, unclear expressions, or both positive and negative opinions. The NLP model may incorrectly identify complaints or misinterpret the actual meaning of a review. Therefore, manual evaluation using labelled customer reviews will be necessary to determine whether the extracted product issues are accurate and supported by the original feedback.

