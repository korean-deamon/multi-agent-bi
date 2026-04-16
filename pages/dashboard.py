import streamlit as st
import pandas as pd
from data_loader import load_sales_data, load_inventory_data, load_hr_data, load_finance_data


def show_dashboard():
    st.title("🚀 Executive Business Overview")
    st.markdown(
        "Comprehensive analysis across Sales, Inventory, Finance, and HR.")

    # Ma'lumotlarni yuklash
    sales_df = load_sales_data()
    inventory_df = load_inventory_data()
    hr_df = load_hr_data()
    finance_df = load_finance_data()

    # 2. ASOSIY KPI METRIKALARI (Eng yuqorida chiroyli bloklarda)
    st.subheader("Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        total_rev = sales_df['Revenue'].sum(
        ) if 'Revenue' in sales_df.columns else 0
        st.metric(label="Total Revenue",
                  value=f"${total_rev:,.0f}", delta="12% YoY")

    with kpi2:
        total_profit = finance_df['Profit'].sum(
        ) if 'Profit' in finance_df.columns else 0
        st.metric(label="Net Profit",
                  value=f"${total_profit:,.0f}", delta="5.4%")

    with kpi3:
        total_stock = inventory_df['Stock'].sum(
        ) if 'Stock' in inventory_df.columns else 0
        st.metric(label="Inventory Levels",
                  value=f"{total_stock:,} units", delta="-2% (Optimal)")

    with kpi4:
        avg_salary = hr_df['Salary'].mean() if 'Salary' in hr_df.columns else 0
        st.metric(label="Avg Employee Cost", value=f"${avg_salary:,.0f}")

    st.markdown("---")

    # 3. VIZUAL GRAFIKLAR (Ikki ustunda)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 Monthly Financial Trend")
        if 'Month' in finance_df.columns:
            # Revenue, Expenses va Profitni bitta grafikda ko'rsatamiz
            finance_chart = finance_df.set_index(
                'Month')[['Revenue', 'Expenses', 'Profit']]
            st.line_chart(finance_chart)
        else:
            st.info("Finance trend data not available.")

    with col_right:
        st.subheader("📊 Revenue by Product Category")
        if 'Product' in sales_df.columns and 'Revenue' in sales_df.columns:
            sales_by_prod = sales_df.groupby(
                'Product')['Revenue'].sum().sort_values(ascending=True)
            st.bar_chart(sales_by_prod, horizontal=True)

    st.markdown("---")

    # 4. PAZITSION TAHLIL (Pastki qatlam)
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.subheader("👥 Department Distribution")
        if 'Department' in hr_df.columns:
            dept_count = hr_df['Department'].value_counts()
            # Yoki pie chart o'rniga bar chart ishlatish mumkin
            st.write(dept_count)

    with col_b:
        st.subheader("⚠️ Low Stock Alerts")
        if 'Stock' in inventory_df.columns:
            # Stock 100 dan kam bo'lgan tovarlarni ogohlantirish sifatida ko'rsatish
            critical_stock = inventory_df[inventory_df['Stock'] < 100][[
                'Product', 'Stock']]
            if not critical_stock.empty:
                st.dataframe(critical_stock, hide_index=True,
                             use_container_width=True)
            else:
                st.success("All stock levels are healthy ✅")

    # 5. OXIRGI TRANZAKSIYALAR (Expander ichida yashirilgan)
    with st.expander("See Recent Transactions Detail"):
        st.table(sales_df.tail(5))
