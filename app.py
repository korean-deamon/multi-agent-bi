import streamlit as st
import os
from dotenv import load_dotenv
from agents.orchestrator import run_query

# 1. Advanced Page Configuration
st.set_page_config(
    page_title="Executive BI Orchestrator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# 2. Custom CSS - Rasmni, radio aylanalarini va ortiqcha navigatsiyani yo'qotish
st.markdown("""
    <style>
        /* Tepadagi avtomatik 'pages' navigatsiyasini yashirish */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Radio button aylanalarini yashirish va matnni chiroyli qilish */
        div[data-testid="stSidebar"] div[role="radiogroup"] > label {
            background-color: #262730;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 5px;
            border: 1px solid #444;
            transition: 0.3s;
        }
        
        div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background-color: #3e404e;
            border-color: #007BFF;
        }

        /* Radio aylanachasini (circle) o'zini yashirish */
        div[data-testid="stSidebar"] div[role="radiogroup"] div[data-testid="stMarkdownContainer"] {
            margin-left: -20px;
        }
        
        div[data-testid="stSidebar"] div[role="radiogroup"] div[data-bv-is-checked="true"] {
            background-color: #007BFF !important;
            border-radius: 5px;
        }

        div[data-testid="stSidebar"] input[type="radio"] {
            display: none !important;
        }
        
        .main { background-color: #0E1117; }
        .stSidebar { background-color: #1E2329; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation (No Image, No Circles)
with st.sidebar:
    st.title("BI Control Panel")
    st.caption("Strategic Intelligence System")
    st.markdown("---")

    # Radio ishlatamiz, lekin CSS uni "aylanasiz" qilib ko'rsatadi
    page = st.radio(
        "Navigation",
        ["Dashboard", "Sales Analysis",
            "Inventory", "Finance", "HR Analytics"],
        label_visibility="collapsed"  # Sarlavhani yashirish
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 4. Dynamic Page Routing
page_map = {
    "Dashboard": "dashboard",
    "Sales Analysis": "sales",
    "Inventory": "inventory",
    "Finance": "finance",
    "HR Analytics": "hr"
}

current_page = page_map[page]

if current_page == "dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()
elif current_page == "sales":
    from pages.sales import show_sales
    show_sales()
elif current_page == "inventory":
    from pages.inventory import show_inventory
    show_inventory()
elif current_page == "finance":
    from pages.finance import show_finance
    show_finance()
elif current_page == "hr":
    from pages.hr import show_hr
    show_hr()

# 5. GLOBAL CHAT INTERFACE
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

st.subheader("💬 AI Business Orchestrator")
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_placeholder = st.container(height=350, border=True)

with chat_placeholder:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Ask a business question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Tahlil qilinmoqda..."):
                response = run_query(prompt)

                # Markdown table ni avto aniqlash va st.dataframe ga aylantirish
                if "|" in response and "—" in response:
                    st.markdown(response)
                else:
                    st.markdown(response)

                st.session_state.messages.append({"role": "assistant", "content": response})
