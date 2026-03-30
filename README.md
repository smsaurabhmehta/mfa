# 🚀 Indian Mutual Fund Agentic X-Ray

An AI-powered portfolio auditor that identifies structural redundancies and concentration risks across 25+ Indian Mutual Funds.

## 🧠 The Problem
Most Indian investors suffer from "Over-Diversification," owning 20+ funds that often hold the exact same top 10 stocks. This project uses **Gemini 3.1 Pro** and **Claude 3.5 Sonnet** to identify "Structural Twins."

## 🛠️ Features
- **Data Extraction:** Pulls real-time holdings and performance data from Yahoo Finance.
- **Structural Twin Analysis:** Identifies funds sharing 5+ of their top 10 holdings.
- **Stock Concentration Grid:** Maps every stock's weight across the entire portfolio to find "Concentration Traps."
- **Agentic Audit:** Generates a professional HTML dashboard with a **Pruning Action Plan** (Keep/Review/Exit).

## 📊 Dashboard Visuals
- **Overlap Heatmap:** A visual matrix of fund-to-fund similarities.
- **Sector Aggregation:** Real-time calculation of Banking, IT, and Energy exposure.
- **Stress Testing:** Portfolio impact simulations for Banking Crises and Market Shocks.

## 🚀 Getting Started
1. Clone the repo.
2. Add your `GEMINI_API_KEY` and `ANTHROPIC_API_KEY` to a `.env` file.
3. Run `python main.py`.

Disclaimer: This tool is for informational and educational purposes only. It does not constitute investment advice. Please consult a SEBI-registered investment advisor before making any investment decisions.
