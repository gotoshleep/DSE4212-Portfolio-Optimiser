# 📈 Portfolio Optimization Beyond Markowitz Using Data Science Methods

Traditional portfolio optimization relies on the Markowitz mean–variance framework, which constructs portfolios by balancing expected returns against risk, as measured by the covariance matrix of asset returns. However, this approach often performs poorly in practice due to out-of-sample estimation errors, instability in portfolio weights, and sensitivity to small changes in input parameters.

To address these limitations, this project investigates machine learning–based methods for **one-month-ahead portfolio optimization**, using **S&P 500 data** as the asset universe. Here, one month is defined as a **21-trading-day forecast horizon**. The **classical Markowitz model** is implemented as a benchmark, where expected returns and covariances are estimated from historical data.

---

## Methodology Overview

### Benchmark & Extensions
- **Baseline:** Markowitz optimization using historical mean returns  
- **Shrinkage-Enhanced Markowitz Models:** Apply Lasso, Ridge, and Elastic Net regularization to stabilize return estimates  
- **Risk-Only Portfolios:** Construct portfolios based solely on risk-based allocation methods  
- **Machine Learning Models:**  
  - Implement **XGBoost** and **regularized linear regressors** (Lasso, Ridge, Elastic Net) to forecast one-month-ahead returns  
  - Predicted returns are combined with the covariance matrix to generate optimized portfolio weights  

---

## Evaluation

- **Forecasting Accuracy:** Measured using **Root Mean Square Error (RMSE)** between predicted and realized returns  
- **Backtesting Setup:**  
  - Initial capital: **USD 1,000,000**  
  - Rebalanced monthly  
  - **Transaction cost:** 5 basis points (0.05%) per buy/sell  
- **Performance Metrics:**  
  - Cumulative returns  
  - Risk-adjusted performance  
  - Comparison against the classical Markowitz benchmark  

---

## Stress Testing

A **stress test** is conducted during the **COVID-19 period (20 February 2020 to 29 December 2020)**, a phase of extreme market volatility, to assess the **robustness and resilience** of each portfolio construction method under adverse market conditions.

---

## Objective

This project aims to identify which data-driven or machine learning strategies provide the **most robust and efficient portfolio construction** improvements over the **traditional mean–variance approach**.


## Setup Instructions

This section explains how to set up the environment to run the project on **macOS** and **Windows**.

### Prerequisites

- **Python 3.9+**
- **Git**
- **pip** (comes with Python)
- Recommended: **virtual environment** (`venv` or `conda`)

---

### macOS Setup

```bash
# 1. Clone the repository
git clone https://github.com/gotoshleep/DSE4212-Portfolio-Optimiser.git
cd DSE4212-Portfolio-Optimiser

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install required libraries
pip install -r requirements.txt

```

### macOS Setup
```bash
# 1. Clone the repository
git clone https://github.com/gotoshleep/DSE4212-Portfolio-Optimiser.git
cd DSE4212-Portfolio-Optimiser

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install required libraries
pip install -r requirements.txt

---
```
## How to Run the Project

This repository contains all scripts and notebooks required for **data preparation**, **feature engineering**, and **portfolio optimization modeling**.  
Follow the steps below to reproduce the workflow from raw data to model evaluation.

## Guide to running the files:
### Step 1: Data Cleaning and Preparation

**Notebook:**  
`Data prep and EDA/data_cleaning.ipynb`

**Description:**  
- Cleans and processes raw S&P 500 data from `raw_data/` and yfinance API.  
- Outputs two cleaned datasets:
  - `training_data.csv`
  - `covid_stress_test_data.csv`

**Output Location:**  
`Data prep and EDA/processed_data/`

⚠️ **Run this notebook first** — it generates the datasets required by all subsequent models.

---

### Step 2: Exploratory Data Analysis (EDA)

**Notebook:**  
`Data prep and EDA/EDA.ipynb`

**Description:**  
- Generates correlation heatmaps
- Helps validate data quality before modeling.

---

### Step 3: Model Training and Portfolio Optimization

All model notebooks are stored under the `Models/` folder.

| Notebook | Description |
|-----------|--------------|
| `benchmark_w_regularisation.ipynb` | Implements the **classical Markowitz model**, regularized extensions (Ridge, Lasso, Elastic Net) and risk based portfolios for return estimation. |
| `lasso_ridge_en.ipynb` | Implements **Lasso, Ridge, and Elastic Net regressions** for forecasting one-month-ahead returns. |
| `xgboost.ipynb` | Implements an **XGBoost-based model** for predicting future returns and constructing optimized portfolios. |

Each model notebook:
- Loads the processed datasets from `../Data prep and EDA/processed_data/`
- Trains and evaluate models on training and stress-test results
- Computes portfolio metrics such as cumulative return and Sharpe ratio based on backtesting

---

### Step 4: Evaluation and Comparison

After all models are run:
- Compare results across models (Markowitz vs Risk-based vs. ML-based approaches).
- Review backtesting plots and risk-adjusted metrics to identify the best-performing strategy.

---

### Recommended Execution Order

1. `Data prep and EDA/data_cleaning.ipynb`  
2. `Data prep and EDA/EDA.ipynb`  
3. `Models/benchmark_w_regularisation.ipynb`  
4. `Models/lasso_ridge_en.ipynb`  
5. `Models/xgboost.ipynb`

---


