import streamlit as st
import pandas as pd
import plotly.express as px  # Agar plotly o'rnatilgan bo'lsa, yanada chiroyli chiqadi
from data_loader import load_sales_data


def show_sales():
    st.title("💰 Sales Performance Analytics")
    st.markdown(
        "Detailed breakdown of revenue, product performance, and sales volume.")

    df = load_sales_data()

    if df.empty:
        st.error("Sales ma'lumotlarini yuklab bo'lmadi.")
        return

    # Ma'lumotlarni tozalash va tayyorlash
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)

    # 1. TOP SALES METRICS
    m1, m2, m3 = st.columns(3)
    with m1:
        total_rev = df['Revenue'].sum()
        st.metric("Total Gross Revenue", f"${total_rev:,.0f}")
    with m2:
        avg_order = df['Revenue'].mean()
        st.metric("Average Order Value", f"${avg_order:,.2f}")
    with m3:
        total_qty = df['Quantity'].sum()
        st.metric("Total Units Sold", f"{total_qty:,} pcs")

    st.markdown("---")

    # 2. PRODUCT PERFORMANCE (Bar Chart & Table)
    col_chart, col_stat = st.columns([2, 1])

    with col_chart:
        st.subheader("Revenue by Product Category")
        product_sales = df.groupby(
            'Product')['Revenue'].sum().sort_values(ascending=False)
        st.bar_chart(product_sales)

    with col_stat:
        st.subheader("Top Selling Products")
        top_products = df.groupby('Product').agg({
            'Revenue': 'sum',
            'Quantity': 'sum'
        }).sort_values(by='Revenue', ascending=False)
        st.dataframe(top_products, use_container_width=True)

    st.markdown("---")

    # 3. DATE-BASED ANALYSIS
    st.subheader("Sales Velocity (Daily Trend)")
    if 'Date' in df.columns:
        # Sanani formatlash
        df['Date'] = pd.to_datetime(df['Date'])
        daily_sales = df.groupby('Date')['Revenue'].sum()
        st.line_chart(daily_sales)

    # 4. RAW DATA & SEARCH
    with st.expander("🔍 Search & Filter Raw Sales Data"):
        search = st.text_input("Filter by Product Name")
        if search:
            filtered_df = df[df['Product'].str.contains(search, case=False)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, width="stretch")

    # 5. DOWNLOAD SECTION
    st.sidebar.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Sales Report (CSV)",
        data=csv,
        file_name='sales_report.csv',
        mime='text/csv',
    )
