import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ตั้งค่าหน้าเว็บให้จำลองหน้าต่าง Figure ของ MATLAB (Position: 1100x480)
st.set_page_config(
    page_title="Interactive Vernier Caliper Simulator (0.02 mm)",
    layout="centered"
)

# จำลอง MenuBar และ Title ของ MATLAB Figure
st.markdown(
    """
    <div style="background-color: #f0f0f1; padding: 6px 12px; border-top-left-radius: 6px; border-top-right-radius: 6px; border: 1px solid #d0d0d5; font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold; color: #333;">
        Interactive Vernier Caliper Simulator (0.02 mm)
    </div>
    """,
    unsafe_allow_html=True
)

# ค่าเริ่มต้น (Initial value) ตรงกับต้นฉบับ MATLAB
if "current_val" not in st.session_state:
    st.session_state.current_val = 12.42

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ฟังก์ชันปัดเศษตามความละเอียด 0.02 มม.
def update_val(v):
    v = round(v / 0.02) * 0.02
    st.session_state.current_val = max(0.0, min(30.0, v))

# --- 1. สร้าง Main Figure & Axes (จำลอง Axis ของ MATLAB) ---
fig, ax = plt.subplots(figsize=(11, 4.5))
fig.patch.set_facecolor('#f0f0f1')
ax.set_facecolor('#f0f0f1')
ax.set_aspect("equal")
ax.set_xlim(-10, 85)
ax.set_ylim(-25, 20)
ax.axis("off")

cTick = [0.15, 0.15, 0.15]

# --- 2. Draw Fixed Main Beam (ลำตัวหลักและปากวัดคงที่) ---
# Main body rectangle
main_body = plt.Rectangle((-8, -6), 95, 22, facecolor=[0.91, 0.91, 0.92], edgecolor=[0.60, 0.60, 0.63], linewidth=1.5)
ax.add_patch(main_body)

# Main jaw (fixed) patch
fixed_jaw = plt.Polygon([[-8, -6], [0, -6], [0, -22], [-8, -22]], facecolor=[0.86, 0.86, 0.88], edgecolor=[0.60, 0.60, 0.63], linewidth=1.5)
ax.add_patch(fixed_jaw)

# Main scale divisions (0 to 80 mm)
for m in range(0, 81):
    if m % 10 == 0:
        y2 = 8
        ax.text(m, y2 + 2.5, str(m), ha='center', va='bottom', fontname='DejaVu Sans', fontsize=9.5, fontweight='bold', color=cTick)
    elif m % 5 == 0:
        y2 = 5.5
    else:
        y2 = 3.5
    ax.plot([m, m], [0, y2], color=cTick, linewidth=0.9)

# --- 3. Slider Component Handles (Vernier Movable Scale & Jaw) ---
cur_val = st.session_state.current_val

# Vernier movable jaw & body (เลื่อนตามค่า cur_val)
vx_base = np.array([0, 0, 52, 52, 10, 0]) + cur_val
vy_base = np.array([-22, 0, 0, -14, -14, -22])
vernier_body = plt.Polygon(np.column_stack((vx_base, vy_base)), facecolor=[0.82, 0.83, 0.86], edgecolor=[0.50, 0.50, 0.55], linewidth=1.3)
ax.add_patch(vernier_body)

# Vernier scale ticks (50 divisions = 49 mm)
vernier_pitch = 49 / 50
for v in range(51):
    vx = cur_val + (v * vernier_pitch)
    if v % 5 == 0:
        vy = -6
        ax.text(vx, vy - 2.5, f"{v / 5:.1f}", ha='center', va='top', fontname='DejaVu Sans', fontsize=8.5, fontweight='bold', color=cTick)
    else:
        vy = -4
    ax.plot([vx, vx], [0, vy], color=cTick, linewidth=0.85)

ax.text(cur_val + 47, -11, '0.02 mm', fontsize=7.5, fontweight='bold', color=[0.3, 0.3, 0.3], ha='center')

st.pyplot(fig)

# --- 4. Control Panel & Teacher Controls (จำลอง uicontrol ของ MATLAB) ---
st.markdown("---")
col_lbl, col_sld, col_btn = st.columns([1.5, 5, 2.5])

with col_lbl:
    st.markdown("**Fine Adjust:**")

with col_sld:
    # uicontrol Slider 0 ถึง 30 มม.
    slider_val = st.slider(
        "Fine Adjust",
        min_value=0.0,
        max_value=30.0,
        value=cur_val,
        step=0.02,
        label_visibility="collapsed"
    )
    if slider_val != cur_val:
        update_val(slider_val)
        st.rerun()

with col_btn:
    # uicontrol Pushbutton (Toggle Answer)
    btn_label = "Hide Answer" if st.session_state.show_answer else "Show Answer"
    if st.button(btn_label, use_container_width=True):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()

# --- Readout Text / Hidden Answer Display (จำลอง annotation textbox) ---
m_part = int(st.session_state.current_val)
v_div = round((st.session_state.current_val % 1) / 0.02)
v_part = v_div * 0.02

if st.session_state.show_answer:
    box_text = f"Reading: {m_part}.00 + {v_part:.2f} = {st.session_state.current_val:.2f} mm (Division: {v_div})"
    st.success(f"**{box_text}**")
else:
    st.info("**??? mm (Answer Hidden)**")
