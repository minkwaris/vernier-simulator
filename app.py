import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Interactive Vernier Caliper Simulator (0.02 mm)", layout="centered")

st.markdown("## 🎯 ฝึกอ่านค่าเวอร์เนียร์คาลิเปอร์ (ความละเอียด 0.02 มม.)")
st.write("เลื่อนสไลด์ด้านล่างเพื่อปรับเปลี่ยนระยะห่าง แล้วฝึกอ่านค่าจากสเกลด้วยตัวเอง จากนั้นกดปุ่มตรวจคำตอบด้านล่าง")

# Initialize session state
if "val" not in st.session_state:
    st.session_state.val = 12.42

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# Slider for control
val = st.slider("ปรับระยะห่าง (มม.):", 0.0, 30.0, st.session_state.val, 0.02)
st.session_state.val = val

# Create Matplotlib Figure (designed to mimic MATLAB layout)
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.set_aspect("equal")
ax.set_xlim(-10, 85)
ax.set_ylim(-25, 20)
ax.axis("off")

# 1. Draw Fixed Main Beam & Main Jaw
ax.fill([-8, 87, 87, -8], [-6, -6, 16, 16], color="#E8E8EA", ec="#99999D", lw=1.5)
ax.fill([-8, 0, 0, -8], [-6, -6, -22, -22], color="#DCDCE0", ec="#99999D", lw=1.5)

# Main scale divisions (0 to 80 mm)
cTick = "#262626"
for m in range(0, 81):
    if m % 10 == 0:
        y2 = 8
        ax.text(m, y2 + 2.5, str(m), ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=cTick)
    elif m % 5 == 0:
        y2 = 5.5
    else:
        y2 = 3.5
    ax.plot([m, m], [0, y2], color=cTick, lw=0.9)

# 2. Vernier Movable Jaw & Body (Shifted by current value)
v_pos = st.session_state.val

# Vernier body polygon offset by v_pos
vx_coords = np.array([0, 0, 52, 52, 10, 0]) + v_pos
vy_coords = np.array([-22, 0, 0, -14, -14, -22])
ax.fill(vx_coords, vy_coords, color="#D2D3D8", ec="#80808A", lw=1.3)

# Vernier scale ticks (50 divisions = 49 mm)
vernier_pitch = 49 / 50
for v in range(51):
    vx = v_pos + (v * vernier_pitch)
    if v % 5 == 0:
        vy = -6
        ax.text(vx, vy - 2.5, f"{v / 5:.1f}", ha="center", va="top", fontsize=8.5, fontweight="bold", color=cTick)
    else:
        vy = -4
    ax.plot([vx, vx], [0, vy], color=cTick, lw=0.85)

ax.text(v_pos + 47, -11, '0.02 mm', fontsize=7.5, fontweight='bold', color='#4D4D4D', ha='center')

st.pyplot(fig)

# --- Teacher Controls & Answer Section ---
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("👁️ เปิด / ปิด เฉลยคำตอบ", use_container_width=True):
        st.session_state.show_answer = not st.session_state.show_answer

if st.session_state.show_answer:
    m_part = int(st.session_state.val)
    v_div = round((st.session_state.val % 1) / 0.02)
    v_part = v_div * 0.02
    st.success(f"### 💡 คำตอบที่ถูกต้อง: {m_part}.00 + {v_part:.2f} = **{st.session_state.val:.2f} มม.** (สเกลย่อยช่องที่: {v_div})")
else:
    st.info("### 🔒 สถานะ: ซ่อนคำตอบอยู่ (ให้เด็กๆ ลองอ่านค่าจากสเกลเองก่อน)")
