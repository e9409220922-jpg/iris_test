import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px
import pandas as pd

# 網頁設定 (要在最前面)
st.set_page_config(page_title = "Iris Dashboard",
                   page_icon = "🌸",
                   layout = "wide",
                   initial_sidebar_state = "collapsed") # 強制收合

st.title("Iris 數據互動圖表 PROMAX")

#-----------------------------------------------------------

# 建立 SQLAlchemy 引擎
# 格式：mysql+mysqlconnector://帳號:密碼@主機/資料庫

# host = "localhost",
# user = "root",
# password = "Aa7895123",
# database = "iris"

# 修改連線字串並加入 ssl_ca 參數
# "mysql+mysqlconnector://avnadmin:密碼@Aiven主機:Port/iris"
engine = create_engine(
    "mysql+mysqlconnector://avnadmin:AVNS_5X7_DINH0sxIW2qigAq@mysql-uto-e9409220922-1cbb.a.aivencloud.com:26541/iris",
    connect_args={'ssl_ca': 'ca.pem'}
)


# 載入資料
sql = "SELECT * FROM iris_dataset;"
df = pd.read_sql_query(sql, engine)

print(df.head())

#-------------------------------------------------------

cols = df.columns.tolist() # 欄位清單
if "id" in cols:
    cols.remove("id")

# 控制面板
st.sidebar.header("控制面板")

# 選擇圖表類型
chart_type = st.sidebar.selectbox(
    "選擇圖表類型",
    ["2D 散佈圖", "3D 散佈圖", "箱型圖 (Box)", "直方圖 (Histogram)"]
)

st.sidebar.markdown("---")

# 選擇座標軸
st.sidebar.header("設定座標軸")
x_axis = st.sidebar.selectbox("選擇 X 軸欄位", cols, index = 0) # index 為預設選項
y_axis = st.sidebar.selectbox("選擇 Y 軸欄位", cols, index = 1)

# 3D 散佈圖要多一個 Z 軸
if chart_type == "3D 散佈圖":
    z_axis = st.sidebar.selectbox("選擇 Z 軸欄位", cols, index = 2)

# 選擇圖形分類
cols2 = ["variety"]
cs = st.sidebar.selectbox("選擇圖形分類", cols2, index = 0)

# 主畫面 ------------------------------------------------------------------------------

# 原始資料
with st.expander("原始資料"): # st.expander 預設隱藏
    st.dataframe(df)

st.subheader(f"圖表：{chart_type}")

# 生成圖表
if chart_type == "2D 散佈圖":
    fig = px.scatter(
        df, x = x_axis, y = y_axis, 
        color = cs, 
        symbol = cs,
        title = f"{x_axis} VS {y_axis}"
    )

elif chart_type == "3D 散佈圖":
    fig = px.scatter_3d(
        df, x = x_axis, y = y_axis, z = z_axis,
        color = cs,
        size = "petal_length",
        opacity = 0.8, # 透明度
        title = f"{x_axis} VS {y_axis} VS {z_axis}"
    )

elif chart_type == "箱型圖 (Box)":
    fig = px.box(
        df, x = "variety", y = y_axis,
        color = cs,
        notched = True, # 增加缺口效果
        title = f"{y_axis} 分佈"
    )

elif chart_type == "直方圖 (Histogram)":
    fig = px.histogram(
        df, x = x_axis, 
        color = cs,
        opacity = 0.8,
        title = f"{x_axis} 分佈"
    )

# 顯示圖表
st.plotly_chart(fig, use_container_width=True) # 自動適應螢幕寬度