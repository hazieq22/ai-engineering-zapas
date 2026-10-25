# **Zapas: V1 Architecture and Design Decisions**

## **Step C1: Start with the Simplest Architecture**

**1\. Main User Interaction**

Retail business owners and inventory managers interact with Zapas through a dashboard to view product sales, inventory levels, customer review analysis, and restocking recommendations.

**2\. AI Capability Needed**

The system requires machine learning to forecast future product demand and natural language processing (NLP) to classify customer sentiment and identify common product complaints. These results are combined to generate restocking and product improvement recommendations.

**3\. Simplest Architecture**

Retail Manager → Zapas Dashboard → AI Analysis (Demand Forecasting and Customer Review Analysis) → Restocking Recommendations and Results

**4\. Can Simple Architecture Satisfy the Requirements?**

The simple architecture can support basic demand forecasting, sentiment classification, and recommendation generation. However, it does not fully address data preprocessing, prediction reliability, synthetic review identification, and system evaluation.

**5\. Additional Components Needed**

Additional components are required for data preprocessing, integration of sales and review data, forecast reliability checks, synthetic data identification, input validation, and performance evaluation. These components will help Zapas satisfy its functional, non-functional, and Responsible AI requirements.

## 

## **Step C2: Identify Architecture Needs from Requirements**

| Requirement ID | What Does the Requirement Need? | Architecture Response |
| ----- | ----- | ----- |
| FR1 | Access to product sales, inventory information, and customer review data. | Data sources and preprocessing components to load, clean, and integrate product information. |
| FR2 / NFR2 | Accurate demand predictions based on historical product sales. | Demand forecasting component to predict future product demand. |
| FR3 / NFR3 / RAI2 | Sentiment classification and identification of common product complaints. | NLP component for customer review sentiment analysis and complaint identification. |
| FR4 | Recommendations based on predicted demand, inventory levels, and customer feedback. | Decision support component to generate restocking and product improvement recommendations. |
| FR5 / NFR1 | Clear presentation of results within an acceptable response time. | Interactive dashboard connected to the AI analysis and recommendation components. |
| RAI1 | Identification of insufficient historical data that may affect forecast reliability. | Forecast reliability check to detect insufficient sales history and display warnings. |
| RAI3 | Clear distinction between real and synthetic customer reviews. | Synthetic data identification control to label generated customer reviews. |
| NFR4 | Reliable processing of valid data and appropriate handling of invalid information. | Input validation and error handling within the data preprocessing component. |

## **Step C3: Draw Your V1 Conceptual Architecture**

**1\. User**

Retail business owners and inventory managers who interact with Zapas to monitor inventory, analyse customer feedback, and review restocking recommendations.

**2\. AI Application / Interface**

Zapas Dashboard provides an interactive interface displaying product sales trends, inventory information, demand forecasts, sentiment analysis results, common complaints, and recommendations.

**3\. AI Capability**

The system consists of two main AI capabilities:

* Demand Forecasting: Uses historical sales data to predict future product demand.  
* Customer Review Analysis: Uses NLP to classify customer sentiment and identify common product complaints.

The outputs are combined through a decision support component to generate restocking and product improvement recommendations.

**4\. Response / Output**

The system provides demand forecasts, inventory information, customer sentiment results, identified product complaints, and recommended restocking or product improvement actions.

**5\. Relevant Data / Knowledge Sources**

* Historical product sales dataset.  
* Inventory stock information.  
* Customer review dataset containing real or synthetic reviews.

**6\. Additional Controls or Components**

* Data Preprocessing: Cleans and integrates sales, inventory, and review data.  
* Forecast Reliability Check: Identifies insufficient sales history and displays warnings.  
* Synthetic Data Identification: Distinguishes generated reviews from real reviews.  
* Input Validation: Handles missing or invalid product information.  
* Evaluation and Monitoring: Measures forecasting accuracy, NLP performance, response time, and Responsible AI compliance.

**7\. Major Information Flows**

Product Sales, Inventory and Customer Reviews → Data Preprocessing → Demand Forecasting and Customer Review Analysis → Restocking Decision Support → Zapas Dashboard → Retail Manager

Responsible AI controls support data processing and recommendation generation, while evaluation and monitoring assess the system's performance.

