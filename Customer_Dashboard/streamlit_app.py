import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Cấu hình trang (Phải là câu lệnh đầu tiên)
st.set_page_config(page_title="Customer Insight Dashboard", layout="wide")

st.title("📊 Chân Dung Khách Hàng Việt Kiều Mỹ 2026")

# Kiểm tra file CSV có tồn tại không
file_path = "khach_hang_500.csv"

if not os.path.exists(file_path):
    st.error(f"❌ Không tìm thấy file '{file_path}' trong thư mục hiện tại!")
    st.info("Hãy chạy lệnh 'python data.py' để tạo dữ liệu trước.")
else:
    # Đọc dữ liệu
    df = pd.read_csv(file_path)
    
    # Ép kiểu dữ liệu để tránh lỗi tính toán
    df['Tong_Thu_Nhap'] = pd.to_numeric(df['Tong_Thu_Nhap'], errors='coerce')

    # --- THANH BÊN (SIDEBAR) ---
    st.sidebar.header("Bộ lọc tìm kiếm")
    all_jobs = df["Nghe_Nghiep"].unique()
    job_filter = st.sidebar.multiselect("Chọn nghề nghiệp:", options=all_jobs, default=all_jobs)

    # Lọc dữ liệu theo lựa chọn
    filtered_df = df[df["Nghe_Nghiep"].isin(job_filter)]

    if filtered_df.empty:
        st.warning("⚠️ Vui lòng chọn ít nhất một nghề nghiệp để hiển thị dữ liệu.")
    else:
        # --- CHỈ SỐ NHANH (METRICS) ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tổng số khách hàng", f"{len(filtered_df)} người")
        with col2:
            avg_inc = filtered_df['Tong_Thu_Nhap'].mean()
            st.metric("Thu nhập TB năm", f"${int(avg_inc):,}")
        with col3:
            top_concern = filtered_df['Noi_Lo_Chinh'].mode()[0]
            st.metric("Nỗi lo phổ biến", top_concern)

        st.markdown("---")

        # --- BIỂU ĐỒ ---
        c1, c2 = st.columns(2)

        with c1:
            # Thu nhập theo nghề
            income_chart = filtered_df.groupby('Nghe_Nghiep')['Tong_Thu_Nhap'].mean().reset_index()
            fig_income = px.bar(income_chart, x='Nghe_Nghiep', y='Tong_Thu_Nhap',
                                title="Thu nhập TB theo nghề (USD)", 
                                color='Nghe_Nghiep', template="plotly_white")
            st.plotly_chart(fig_income, use_container_width=True)

        with c2:
            # Tỷ lệ nỗi lo
            fig_concern = px.pie(filtered_df, names='Noi_Lo_Chinh', title="Phân bổ nỗi lo chính",
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_concern, use_container_width=True)

        # Biểu đồ xu hướng tháng
        st.subheader("📈 Xu hướng thu nhập 12 tháng")
        month_cols = [f'Thang_{i}' for i in range(1, 13)]
        
        # Kiểm tra xem các cột tháng có tồn tại trong CSV không
        existing_months = [col for col in month_cols if col in filtered_df.columns]
        
        if existing_months:
            monthly_avg = filtered_df.groupby('Nghe_Nghiep')[existing_months].mean().reset_index()
            df_melt = monthly_avg.melt(id_vars='Nghe_Nghiep', var_name='Tháng', value_name='Thu nhập')
            fig_line = px.line(df_melt, x='Tháng', y='Thu nhập', color='Nghe_Nghiep', 
                               markers=True, title="Biến động thu nhập theo mùa vụ")
            st.plotly_chart(fig_line, use_container_width=True)

        # Xem bảng dữ liệu
        with st.expander("🔍 Xem danh sách dữ liệu chi tiết"):
            st.dataframe(filtered_df)
