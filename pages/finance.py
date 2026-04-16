import streamlit as st
import pandas as pd
from data_loader import load_finance_data


def show_finance():
    # 1. Page Header
    st.title("💸 Financial Performance & Profitability")
    st.markdown(
        "Monitor corporate fiscal health, revenue trends, and expense efficiency.")

    df = load_finance_data()

    if df.empty:
        st.error("Financial data could not be loaded. Please check the data source.")
        return

    # 2. FINANCIAL SUMMARY METRICS
    st.subheader("Executive Summary")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        total_rev = df['Revenue'].sum()
        st.metric("Total Revenue", f"${total_rev:,.0f}", delta="Annual Flow")
    with m2:
        total_exp = df['Expenses'].sum()
        st.metric("Total Expenses",
                  f"${total_exp:,.0f}", delta_color="inverse")
    with m3:
        total_profit = df['Profit'].sum()
        margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
        st.metric("Net Profit", f"${total_profit:,.0f}",
                  delta=f"{margin:.1f}% Margin")
    with m4:
        avg_monthly_profit = df['Profit'].mean()
        st.metric("Avg Monthly Profit", f"${avg_monthly_profit:,.0f}")

    st.markdown("---")

    # 3. TREND ANALYSIS (Revenue vs Expenses vs Profit)
    st.subheader("📈 Revenue, Expenses & Profit Trend")

    if 'Month' in df.columns:
        # Prepare data for line chart
        chart_data = df.set_index('Month')[['Revenue', 'Expenses', 'Profit']]
        st.line_chart(chart_data, height=400)
    else:
        st.warning("Month column missing. Trend analysis unavailable.")

    st.markdown("---")

    # 4. PROFITABILITY & EFFICIENCY ANALYSIS
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Profit Margin by Month (%)")
        # Calculate Margin % if not already in DF
        df['Margin %'] = (df['Profit'] / df['Revenue'] * 100).round(2)
        st.bar_chart(df.set_index('Month')['Margin %'])

    with col_right:
        st.subheader("💰 Expense Efficiency")
        avg_exp_ratio = (total_exp / total_rev * 100) if total_rev > 0 else 0
        st.info(f"Average Expense Ratio: **{avg_exp_ratio:.1f}%** of Revenue")
        st.write("""
            **Analysis:** This metric indicates the percentage of every dollar earned 
            that goes toward covering operating costs. A lower ratio suggests 
            better operational efficiency.
        """)

    st.markdown("---")

    # 5. DETAILED FINANCIAL LEDGER
    st.subheader("📑 Monthly Financial Records")

    # Styled dataframe with column configuration
    st.dataframe(
        df[['Month', 'Revenue', 'Expenses', 'Profit', 'Margin %']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn("Total Revenue", format="$ %d"),
            "Expenses": st.column_config.NumberColumn("Total Expenses", format="$ %d"),
            "Profit": st.column_config.NumberColumn("Net Profit", format="$ %d"),
            "Margin %": st.column_config.NumberColumn("Profit Margin", format="%.1f %%")
        }
    )

    # 6. SMART FINANCIAL INSIGHT
    highest_profit_month = df.loc[df['Profit'].idxmax(), 'Month']
    st.success(
        f"💡 **Key Insight:** The highest profitability was recorded in **{highest_profit_month}**.")
