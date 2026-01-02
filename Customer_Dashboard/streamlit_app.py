import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang
st.set_page_config(page_title="Customer Insight Dashboard", layout="wide")

# Tiêu đề chính
st.title("📊 Chân Dung Khách Hàng Việt Kiều Mỹ 2026")
st.markdown("---")

# Đọc dữ liệu
@st.cache_data
def load_data():
    return pd.read_csv("khach_hang_500.csv")

df = load_data()

# --- THANH BÊN (SIDEBAR) ĐỂ LỌC DỮ LIỆU ---
st.sidebar.header("Bộ lọc tìm kiếm")
job_filter = st.sidebar.multiselect("Chọn nghề nghiệp:", 
                                    options=df["Nghe_Nghiep"].unique(), 
                                    default=df["Nghe_Nghiep"].unique())

filtered_df = df[df["Nghe_Nghiep"].isin(job_filter)]

# --- CHỈ SỐ NHANH (METRICS) ---
col1, col2, col3 = st.columns(3)
col1.metric("Tổng số khách hàng", len(filtered_df))
col2.metric("Thu nhập TB năm", f"${int(filtered_df['Tong_Thu_Nhap'].mean()):,}")
col3.metric("Nỗi lo phổ biến nhất", filtered_df['Noi_Lo_Chinh'].mode()[0])

st.markdown("---")

# --- BIỂU ĐỒ ---
c1, c2 = st.columns(2)

with c1:
    fig_income = px.bar(filtered_df.groupby('Nghe_Nghiep')['Tong_Thu_Nhap'].mean().reset_index(),
                        x='Nghe_Nghiep', y='Tong_Thu_Nhap', 
                        title="Thu nhập TB theo nghề", color='Nghe_Nghiep')
    st.plotly_chart(fig_income, use_container_width=True)

with c2:
    fig_concern = px.pie(filtered_df, names='Noi_Lo_Chinh', title="Phân bổ nỗi lo")
    st.plotly_chart(fig_concern, use_container_width=True)

# Biểu đồ xu hướng tháng
st.subheader("📈 Xu hướng thu nhập 12 tháng")
month_cols = [f'Thang_{i}' for i in range(1, 13)]
monthly_avg = filtered_df.groupby('Nghe_Nghiep')[month_cols].mean().reset_index()
df_melt = monthly_avg.melt(id_vars='Nghe_Nghiep', var_name='Tháng', value_name='Thu nhập')
fig_line = px.line(df_melt, x='Tháng', y='Thu nhập', color='Nghe_Nghiep', markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# Hiển thị bảng dữ liệu nếu muốn
if st.checkbox("Xem dữ liệu chi tiết"):
    st.write(filtered_df)
