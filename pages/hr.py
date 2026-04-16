import streamlit as st
import pandas as pd
from data_loader import load_hr_data


def show_hr():
    # 1. Page Header
    st.title("👥 Human Resources Analytics")
    st.markdown(
        "Analyze workforce distribution, department headcount, and payroll structures.")

    df = load_hr_data()

    if df.empty:
        st.error("HR data could not be loaded. Please check the data source.")
        return

    # 2. WORKFORCE KEY METRICS
    st.subheader("Workforce Overview")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        total_staff = len(df)
        st.metric("Total Employees", total_staff)
    with m2:
        num_depts = df['Department'].nunique(
        ) if 'Department' in df.columns else 0
        st.metric("Departments", num_depts)
    with m3:
        avg_salary = df['Salary'].mean() if 'Salary' in df.columns else 0
        st.metric("Avg Annual Salary", f"${avg_salary:,.0f}")
    with m4:
        total_payroll = df['Salary'].sum() if 'Salary' in df.columns else 0
        st.metric("Total Monthly Payroll", f"${total_payroll:,.0f}")

    st.markdown("---")

    # 3. DEPARTMENTAL ANALYSIS (Charts)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Headcount by Department")
        if 'Department' in df.columns:
            dept_dist = df['Department'].value_counts()
            st.bar_chart(dept_dist)
        else:
            st.info("Department column not found.")

    with col_right:
        st.subheader("💰 Salary Distribution by Department")
        if 'Department' in df.columns and 'Salary' in df.columns:
            # Grouping average salary by department
            salary_dept = df.groupby('Department')[
                'Salary'].mean().sort_values(ascending=False)
            st.bar_chart(salary_dept)

    st.markdown("---")

    # 4. EMPLOYEE TENURE & ROSTER
    st.subheader("📑 Employee Directory & Tenure")

    # Simple Tenure Calculation (Years since joining)
    if 'Joining date' in df.columns:
        df['Joining date'] = pd.to_datetime(df['Joining date'])
        current_year = pd.Timestamp.now().year
        df['Tenure (Years)'] = current_year - df['Joining date'].dt.year

    # Professional Data Table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Salary": st.column_config.NumberColumn("Annual Salary", format="$ %d"),
            "Joining date": st.column_config.DateColumn("Date Joined"),
            "Tenure (Years)": st.column_config.NumberColumn("Years in Company", format="%d Yrs")
        }
    )

    # 5. HR INSIGHTS (Sidebar or Bottom)
    st.sidebar.markdown("---")
    st.sidebar.subheader("HR Summary")
    if 'Department' in df.columns:
        largest_dept = df['Department'].value_counts().idxmax()
        st.sidebar.success(f"Largest Team: **{largest_dept}**")

    st.sidebar.info(f"Total Budgeted Payroll: **${total_payroll:,.2f}**")
