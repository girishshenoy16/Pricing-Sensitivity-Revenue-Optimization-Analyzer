# 📊 Pricing Sensitivity & Revenue Optimization Analyzer

> An enterprise-style pricing intelligence system that models price elasticity, simulates demand response, identifies profit-maximizing price points, and delivers executive-ready insights through an interactive dashboard.

---

## 🧠 Problem Statement

Pricing is one of the most powerful business levers.

Yet many organizations struggle to answer:

* How sensitive is demand to price changes?
* Are we underpricing or overpricing?
* What price maximizes **profit**, not just revenue?
* How confident are we in our pricing decisions?
* Which product categories offer the highest optimization potential?

This project builds a **data-driven pricing analytics system** that:

* Estimates price elasticity using econometric modeling
* Simulates revenue and profit across dynamic price ranges
* Identifies statistically optimal price points
* Quantifies uncertainty via confidence intervals
* Ranks product categories by profit potential
* Provides executive-level insights via Streamlit dashboard

---

## 🏢 Real-World Relevance

This architecture mirrors pricing systems used in:

* Retail pricing analytics teams
* E-commerce revenue optimization
* SaaS subscription pricing strategy
* Portfolio margin management
* Revenue analytics departments

It simulates a structured pricing decision pipeline combining:

* Econometric modeling
* Profit optimization logic
* Confidence-aware simulation
* Strategic pricing insights
* Executive reporting

---

# 📊 Dataset Used

### 🔹 Retail Sales Dataset

* Source: Kaggle
* Contains multi-category retail transaction data
* Includes:

  * Product category
  * Price per unit
  * Quantity
  * Customer demographics

⚠ Dataset not included in repository due to licensing and size.

---

# 📥 Dataset Setup

1️⃣ Download dataset from Kaggle

2️⃣ Create folder:

```
data/raw/
```

3️⃣ Place dataset file inside:

```
data/raw/retail_sales_dataset.csv
```

---

# 🏗️ System Architecture

```
Raw Sales Data
   ↓
EDA
   ↓
Preprocessing (Cleaning + Feature Engineering)
   ↓
--------------------------------
Elasticity Modeling (Log-Log Regression)
--------------------------------
Demand Simulation Engine
   ↓
Profit Optimization Layer
   ↓
Confidence Interval Propagation
   ↓
Optimal Zone Identification
   ↓
Enterprise Dashboard
```

---

# 🛠️ Tech Stack

| Layer                | Tools                 |
| -------------------- | --------------------- |
| Data Processing      | Pandas, NumPy         |
| Econometric Modeling | Statsmodels           |
| Simulation Engine    | Custom Profit Logic   |
| Visualization        | Plotly                |
| Dashboard            | Streamlit             |
| Reporting            | ReportLab             |
| Model Persistence    | Joblib                |
| Logging              | Python Logging Module |

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/girishshenoy16/Pricing-Sensitivity-Revenue-Optimization-Analyzer.git
cd Pricing-Sensitivity-Revenue-Optimization-Analyzer
```

---

## 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# 🚀 Running the Project

## Step 1 — Train Elasticity Models

```bash
python -m src.main
```

This will:

* Preprocess data
* Engineer features
* Estimate price elasticity per category
* Apply economic constraints if needed
* Save trained models
* Generate elasticity summary metrics

---

## Step 2 — Launch Pricing Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard opens in browser.

---

# 📊 Dashboard Modules

### 📌 Optimization Overview

* Current profit
* Optimal profit
* Optimal price
* Profit delta vs baseline

---

### 📌 Profit Optimization Curve

* Profit curve across price range
* Subtle glow effect for premium visualization
* Confidence interval shading
* Optimal pricing zone highlight
* Current & scenario markers

---

### 📌 Multi-Scenario Comparison

* Compare:

  * Current price
  * Optimal price
  * Custom scenario price

---

### 📌 Category Profit Ranking

* Rank product categories by maximum profit potential
* Identify highest-margin optimization targets

---

### 📌 Executive Summary

* Elasticity classification
* Strategic pricing recommendation
* Risk-aware insight
* Downloadable PDF report

---

# 📈 Elasticity Interpretation Logic

| Elasticity (β) | Demand Type          | Pricing Insight                       |
| -------------- | -------------------- | ------------------------------------- |
| β < -1         | Highly Elastic       | Price increases reduce demand sharply |
| -1 ≤ β < 0     | Inelastic            | Price changes have moderate effect    |
| β ≥ 0          | Economically invalid | Constrained to maintain realism       |

---

# 📂 Project Structure

```
pricing-sensitivity-revenue-optimization-analyzer/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── outputs/
│
├── src/
│   ├── data_pipeline/
│   ├── model_training/
│   ├── services/
│   ├── config/
│   ├── utils/
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

# 📈 Key Results

* Demand elasticity estimated per category
* Profit-maximizing prices identified dynamically
* Confidence-aware optimization curve
* Strategic scenario comparison enabled
* Executive-ready PDF reporting
* SaaS-grade interactive dashboard

---

# 🎯 Resume Highlights

* Built econometric pricing optimization system using log-log regression
* Designed profit simulation engine with confidence interval propagation
* Implemented multi-scenario pricing comparison dashboard
* Created executive-ready reporting with PDF export
* Structured project with enterprise-style modular architecture
* Applied economic constraints for realistic elasticity behavior

---

# 🏆 Why This Project Stands Out

✔ Goes beyond regression into full profit optimization

✔ Incorporates statistical uncertainty into pricing decisions

✔ Includes confidence-aware simulation

✔ Provides executive-level strategic insights

✔ Modular, production-style architecture

✔ SaaS-grade interactive dashboard

✔ Demonstrates business-first analytical thinking