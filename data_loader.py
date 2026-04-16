import gspread
import pandas as pd
import streamlit as st

# Google Sheets API clientini keshda saqlash


@st.cache_resource
def get_gspread_client():
    """Authenticates using Streamlit secrets (recommended)"""
    creds = st.secrets["gcp_service_account"]
    return gspread.service_account_from_dict(creds)

# Ma'lumotlarni yuklash funksiyasi


@st.cache_data(ttl=600)
def load_sheet_data(worksheet_name):
    """Fetches data from a specific worksheet and returns a cleaned DataFrame"""
    try:
        client = get_gspread_client()
        # "BI_Data" nomli faylni ochish
        sheet = client.open("BI_Data").worksheet(worksheet_name)
        data = sheet.get_all_records()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        # Ustun nomlarini tozalash (bo'shliqlarni olish va inglizcha standartda saqlash)
        df.columns = [str(col).strip() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Error loading {worksheet_name}: {e}")
        return pd.DataFrame()

# Har bir modul uchun ma'lumot yuklovchilar


def load_sales_data():
    return load_sheet_data("sales_data")


def load_inventory_data():
    return load_sheet_data("inventory_data")


def load_finance_data():
    return load_sheet_data("finance_data")


def load_hr_data():
    return load_sheet_data("hr_data")



# import gspread
# import pandas as pd
# import streamlit as st

# # -------------------------------
# # Google Sheets Client (STREAMLIT SECRETS VERSION)
# # -------------------------------
# @st.cache_resource
# def get_gspread_client():
#     """Authenticates and returns Google Sheets client using Streamlit secrets"""
#     creds = st.secrets["gcp_service_account"]
#     return gspread.service_account_from_dict(creds)

# # -------------------------------
# # Load sheet data
# # -------------------------------
# @st.cache_data(ttl=600)
# def load_sheet_data(worksheet_name):
#     """Fetch data from Google Sheets worksheet and return DataFrame"""
#     try:
#         client = get_gspread_client()

#         sheet = client.open("BI_Data").worksheet(worksheet_name)
#         data = sheet.get_all_records()

#         if not data:
#             return pd.DataFrame()

#         df = pd.DataFrame(data)
#         df.columns = [str(col).strip() for col in df.columns]

#         return df

#     except Exception as e:
#         st.error(f"Error loading {worksheet_name}: {e}")
#         return pd.DataFrame()

# # -------------------------------
# # Domain loaders
# # -------------------------------
# def load_sales_data():
#     return load_sheet_data("sales_data")

# def load_inventory_data():
#     return load_sheet_data("inventory_data")

# def load_finance_data():
#     return load_sheet_data("finance_data")

# def load_hr_data():
#     return load_sheet_data("hr_data")