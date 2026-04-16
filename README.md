# 🏢 Multi-Agent Business Intelligence System

A Streamlit-based AI Business Intelligence platform that integrates Google Sheets data with a multi-agent orchestration system for real-time analytics and insights.

---

## 🚀 Features

- 📊 Multi-page BI Dashboard (Sales, Finance, HR, Inventory)
- 📈 KPI tracking (Revenue, Profit, Employees, Stock)
- 🤖 AI Chat-based Business Analyst
- 🧠 Intent-based query routing
- ☁️ Google Sheets live data integration
- 📉 Interactive charts and analytics

---

## 🏗️ System Architecture

User Query  
→ Intent Detection  
→ Data Loader (Google Sheets)  
→ Domain Handler (HR / Sales / Finance / Inventory)  
→ LLM Fallback (LangChain Agent)  
→ Streamlit UI Response  

---

## 📂 Project Structure
multi_agent_bi/
│── app.py
│── data_loader.py
│── agents/
│ └── orchestrator.py
│── pages/
│ ├── dashboard.py
│ ├── sales.py
│ ├── finance.py
│ ├── hr.py
│ └── inventory.py
│── requirements.txt
│── .gitignore


---

## ⚙️ Setup Instructions

### 1. Clone Repository
git clone https://github.com/korean-deamon/multi-agent-bi.git
cd multi-agent-bi

### 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Environment Variables

Create a .env file in the project root:

OPENROUTER_API_KEY=your_api_key_here

### 5. Google Sheets Setup
Add credentials.json to the project root
Google Sheet name must be: BI_Data

Required worksheets:

sales_data
finance_data
inventory_data
hr_data

### 6. Run Application
    streamlit run app.py