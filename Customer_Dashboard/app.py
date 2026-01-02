from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)
csv_path = r"E:\Python\Customer_Dashboard\khach_hang_500.csv"

@app.route('/')
def index():
    if not os.path.exists(csv_path):
        return "LỖI: Bạn chưa chạy file data.py để tạo dữ liệu!"

    df = pd.read_csv(csv_path)

    # 1. Biểu đồ Cột (Thu nhập)
    fig1 = px.bar(df.groupby('Nghe_Nghiep')['Tong_Thu_Nhap'].mean().reset_index(), 
                 x='Nghe_Nghiep', y='Tong_Thu_Nhap', title="Thu nhập TB năm (USD)",
                 color='Nghe_Nghiep', template="plotly_white")
    
    # 2. Biểu đồ Tròn (Nỗi lo)
    fig2 = px.pie(df, names='Noi_Lo_Chinh', title="Tỷ lệ các mối lo ngại", hole=0.4)

    # 3. Biểu đồ Đường (Xu hướng tháng)
    m_cols = [f'Thang_{i}' for i in range(1, 13)]
    df_m = df.groupby('Nghe_Nghiep')[m_cols].mean().reset_index().melt(id_vars='Nghe_Nghiep', var_name='Tháng', value_name='Lương')
    fig3 = px.line(df_m, x='Tháng', y='Lương', color='Nghe_Nghiep', title="Biến động 12 tháng")

    return render_template('index.html', plot1=fig1.to_html(), plot2=fig2.to_html(), plot3=fig3.to_html())

if __name__ == '__main__':
    app.run(debug=True)