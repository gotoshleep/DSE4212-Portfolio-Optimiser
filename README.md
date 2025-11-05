# 📈 Portfolio Optimization Beyond Markowitz Using Data Science Methods

Traditional portfolio optimization relies on the Markowitz mean–variance framework, which constructs portfolios by balancing expected returns against risk, as measured by the covariance matrix of asset returns. However, this approach often performs poorly in practice due to out-of-sample estimation errors, instability in portfolio weights, and sensitivity to small changes in input parameters.

To address these limitations, this project investigates machine learning–based methods for **one-month-ahead portfolio optimization**, using **S&P 500 data** as the asset universe. Here, one month is defined as a **21-trading-day forecast horizon**. The **classical Markowitz model** is implemented as a benchmark, where expected returns and covariances are estimated from historical data.

---

## 🧠 Methodology Overview

### Benchmark & Extensions
- **Baseline:** Markowitz optimization using historical mean returns  
- **Shrinkage-Enhanced Markowitz Models:** Apply Lasso, Ridge, and Elastic Net regularization to stabilize return estimates  
- **Risk-Only Portfolios:** Construct portfolios based solely on risk-based allocation methods  
- **Machine Learning Models:**  
  - Implement **XGBoost** and **regularized linear regressors** (Lasso, Ridge, Elastic Net) to forecast one-month-ahead returns  
  - Predicted returns are combined with the covariance matrix to generate optimized portfolio weights  

---

## 📊 Evaluation

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

## 🧪 Stress Testing

A **stress test** is conducted during the **COVID-19 period (20 February 2020 to 29 December 2020)**, a phase of extreme market volatility, to assess the **robustness and resilience** of each portfolio construction method under adverse market conditions.

---

## 🎯 Objective

This project aims to identify which data-driven or machine learning strategies provide the **most robust and efficient portfolio construction** improvements over the **traditional mean–variance approach**.


## ⚙️ Setup Instructions

This section explains how to set up the environment to run the project on **macOS** and **Windows**.

### 1️⃣ Prerequisites

- **Python 3.9+**
- **Git**
- **pip** (comes with Python)
- Recommended: **virtual environment** (`venv` or `conda`)

---

### 🧰 macOS Setup

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

### 🪟 macOS Setup
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
