import os
import re
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from data_loader import load_sales_data, load_finance_data, load_inventory_data, load_hr_data
from dotenv import load_dotenv

load_dotenv()
def clean_response(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    # Agentning ortiqcha qismlarini tozalash
    text = re.sub(r"^(Thought|Action|Action Input|Observation|Final Answer:?)", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"dtype:.*|Name:.*", "", text)
    lines = [line.strip() for line in text.split("\n") if line.strip() and not line.startswith("```")]
    return "\n".join(lines).strip()

def detect_intent(query: str):
    q = query.lower()
    scores = {
        "sales": sum(1 for w in ["sale", "revenue", "product", "sold", "quantity"] if w in q),
        "finance": sum(1 for w in ["profit", "expense", "cost", "budget", "margin"] if w in q),
        "inventory": sum(1 for w in ["stock", "inventory", "reorder", "product"] if w in q),
        "": sum(1 for w in ["employee", "salary", "department", "staff", "hire"] if w in q),
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 1 else "all"   # threshold yuqoriroq qildik

def load_data_by_intent(intent: str):
    if intent == "sales":
        return load_sales_data(), "sales_data"
    elif intent == "finance":
        return load_finance_data(), "finance_data"
    elif intent == "inventory":
        return load_inventory_data(), "inventory_data"
    elif intent == "hr":
        return load_hr_data(), "hr_data"
    else:
        # Barcha data — agent ko'proq kontekst oladi
        dfs = {
            "sales": load_sales_data(),
            "finance": load_finance_data(),
            "inventory": load_inventory_data(),
            "hr": load_hr_data()
        }
        return list(dfs.values()), "all_data"

def run_query(user_query: str):
    try:
        intent = detect_intent(user_query)
        data, context = load_data_by_intent(intent)

        if (isinstance(data, list) and all(df.empty for df in data if isinstance(df, pd.DataFrame))) or \
           (not isinstance(data, list) and data.empty):
            return "Ma'lumotlar hozircha mavjud emas."

        # Groq LLM
        llm = ChatOpenAI(
            model="llama-3.3-70b-versatile",
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
            temperature=0.0,          # aniqroq javob uchun
            max_tokens=2048
        )

        from langchain_core.prompts import ChatPromptTemplate

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Siz professional Business Intelligence tahlilchisisiz.
Foydalanuvchi savoliga faqat berilgan ma'lumotlar asosida javob bering.
Har doim:
1. Avval markdown jadval chiqaring (agar savol sonlar bilan bog'liq bo'lsa)
2. Keyin qisqa tahlil va tavsif yozing (1-3 jumla).
Javobni o'zbek tilida bering.
Hech qachon ma'lumot o'ylab topmang."""),
            ("human", "Dataset nomi: {context}\n\nSavol: {question}")
        ])

        chain = prompt_template | llm

        # DataFrame ni string qilib uzatamiz
        if isinstance(data, list):
            data_str = "\n\n".join([f"--- {name} ---\n{df.to_string()}" for df, name in zip(data, ["sales", "finance", "inventory", "hr"])])
        else:
            data_str = data.to_string()

        response = chain.invoke({
            "context": context,
            "question": f"{user_query}\n\nQuyidagi ma'lumotlar:\n{data_str[:15000]}"  # token cheklash
        })

        return response.content

    except Exception as e:
        return f"Tahlilda xatolik: {str(e)[:200]}"