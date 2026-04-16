import streamlit as st
import pandas as pd
from data_loader import load_inventory_data


def show_inventory():
    st.title("📦 Inventory Control & Stock Management")
    st.markdown(
        "Monitor your stock levels, reorder points, and warehouse health.")

    df = load_inventory_data()

    if df.empty:
        st.error("Inventory ma'lumotlarini yuklab bo'lmadi.")
        return

    # 1. STOCK OVERVIEW METRICS
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        total_items = len(df)
        st.metric("Unique Products", total_items)
    with m2:
        total_stock = df['Stock'].sum()
        st.metric("Total Stock Units", f"{total_stock:,}")
    with m3:
        # Reorder Level dan past bo'lgan tovarlar soni
        critical_items = len(df[df['Stock'] <= df['Reorder Level']])
        st.metric("Critical Alerts", critical_items,
                  delta="- Action Required" if critical_items > 0 else "Healthy", delta_color="inverse")
    with m4:
        avg_stock = df['Stock'].mean()
        st.metric("Avg Stock per SKU", f"{avg_stock:.0f}")

    st.markdown("---")

    # 2. STOCK ANALYSIS VISUALS
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 Stock Levels vs Reorder Points")
        # Bar chart: Stock va Reorder levelni yonma-yon solishtirish
        chart_data = df.set_index('Product')[['Stock', 'Reorder Level']]
        st.bar_chart(chart_data)

    with col_right:
        st.subheader("🔔 Critical Low Stock")
        # Faqat reorder leveldan pastlarini chiqarish
        low_stock_df = df[df['Stock'] <=
                          df['Reorder Level']].sort_values(by='Stock')
        if not low_stock_df.empty:
            st.dataframe(
                low_stock_df[['Product', 'Stock', 'Reorder Level']],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.success("All products are above reorder levels! ✅")

    st.markdown("---")

    # 3. STOCK CATEGORIZATION & FULL LIST
    st.subheader("Warehouse Inventory Details")

    # Status ustunini qo'shish (Visual indicator)
    def highlight_stock(row):
        if row['Stock'] <= row['Reorder Level']:
            return '🔴 Reorder Now'
        elif row['Stock'] <= row['Reorder Level'] * 1.5:
            return '🟡 Warning'
        return '🟢 Sufficient'

    df['Status'] = df.apply(highlight_stock, axis=1)

    # Filter qismi
    status_filter = st.multiselect("Filter by Status", options=[
                                   '🔴 Reorder Now', '🟡 Warning', '🟢 Sufficient'], default=['🔴 Reorder Now', '🟡 Warning', '🟢 Sufficient'])

    filtered_df = df[df['Status'].isin(status_filter)]

    st.dataframe(
        filtered_df[['Product', 'Stock', 'Reorder Level', 'Status']],
        use_container_width=True,
        column_config={
            "Stock": st.column_config.ProgressColumn("Stock Level", help="Current stock amount", min_value=0, max_value=int(df['Stock'].max())),
            "Status": "Inventory Health"
        }
    )

    # 4. QUICK ACTIONS
    st.sidebar.markdown("---")
    st.sidebar.subheader("Warehouse Actions")
    if st.sidebar.button("Generate Purchase Order"):
        st.sidebar.info(f"Generated order for {critical_items} items.")
