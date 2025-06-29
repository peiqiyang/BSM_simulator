import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from datetime import datetime
from modules.bsm import BSM

# 页面设置
st.set_page_config(
    page_title="BSM 模拟器",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("🌱 BSM 土壤反射率模拟器")
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 8px;
            right: 12px;
            font-size: 1em;
            z-index: 100;
        }
    </style>
    <div class="footer">
        <b>Copyright © Peiqi Yang</b>, p.yang@njnu.edu.cn
    </div>
    """,
    unsafe_allow_html=True
)

# 工具函数：生成 TXT 文件
def generate_txt(wl, rdry, rwet, meta):
    buffer = io.StringIO()
    buffer.write("# 模拟参数: " + meta + "\n")
    buffer.write("Wavelength (nm)\tDry Reflectance\tWet Reflectance\n")
    for i in range(len(wl)):
        buffer.write(f"{wl[i]:.2f}\t{rdry[i]:.6f}\t{rwet[i]:.6f}\n")
    return buffer.getvalue().encode('utf-8')

# 初始化模拟状态
if 'results_list' not in st.session_state:
    st.session_state.results_list = []

# 显示选项
col1, col2 = st.sidebar.columns(2)
show_dry = col1.checkbox("显示干土", value=True)
show_wet = col2.checkbox("显示湿土", value=True)

# 模拟控制
col3, col4 = st.sidebar.columns(2)
retain_previous = col3.checkbox("保留前次结果", value=False)
simulate_button = col4.button("开始模拟")

# 输入参数区（带滑条 + 输入框）
st.sidebar.header("输入参数")

def hybrid_slider(name, minval, maxval, default, step):
    col_a, col_b = st.sidebar.columns([2, 1])
    val = col_a.slider(name, min_value=minval, max_value=maxval, value=default, step=step)
    col_b.number_input(" ", value=val, step=step, key=name)
    return val

B = hybrid_slider("土壤亮度 B", 0.0, 1.0, 0.5, 0.01)
lat = hybrid_slider("纬度 lat (°)", -30.0, 30.0, 10.0, 1.0)
lon = hybrid_slider("经度 lon (°)", 80.0, 120.0, 100.0, 1.0)
SMp = hybrid_slider("体积含水量 SMp (%)", 5.0, 55.0, 20.0, 1.0)

# 固定参数
SMC = 25
film = 0.015

# 点击开始模拟
if simulate_button:
    if not retain_previous:
        st.session_state.results_list = []

    try:
        wl = np.loadtxt("data/wavelengths.txt")
        nr = np.loadtxt("data/nr.txt")
        kw = np.loadtxt("data/kw.txt")
        GSV = np.loadtxt("data/GSV.txt")

        spec = {"GSV": GSV, "Kw": kw, "nw": nr}
        soilpar = {"B": B, "lat": lat, "lon": lon, "SMp": SMp}
        emp = {"SMC": SMC, "film": film}

        rdry, rwet = BSM(soilpar, spec, emp)

        st.session_state.results_list.append({
            "wl": wl,
            "rdry": rdry,
            "rwet": rwet,
            "label": f"B={B}, lat={lat}, lon={lon}, SMp={SMp}"
        })
    except Exception as e:
        st.error(f"模拟失败，错误信息: {e}")

# 绘图（标签英文）
fig, ax = plt.subplots(figsize=(12, 6))
has_plot = False

for result in st.session_state.results_list:
    if show_dry:
        ax.plot(result["wl"], result["rdry"], label=result["label"] + " - Dry Soil")
        has_plot = True
    if show_wet:
        ax.plot(result["wl"], result["rwet"], label=result["label"] + " - Wet Soil")
        has_plot = True

ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Reflectance")
ax.set_title("BSM Simulated Reflectance")
if has_plot:
    ax.legend(fontsize=8)
ax.grid(True)
st.pyplot(fig)

# 下载按钮
if st.session_state.results_list:
    latest = st.session_state.results_list[-1]
    txt_bytes = generate_txt(latest["wl"], latest["rdry"], latest["rwet"], latest["label"])
    filename = f"bsm_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    st.download_button(
        label="📥 下载当前模拟结果（.txt）",
        data=txt_bytes,
        file_name=filename,
        mime="text/plain"
    )
