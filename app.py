import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Vernier Caliper Simulator (0.02 mm)", layout="centered")

st.title("🎯 โปรแกรมจำลองเวอร์เนียร์คาลิเปอร์ (ความละเอียด 0.02 มม.)")
st.write("เลื่อนสไลด์เพื่อเปลี่ยนค่า หรือฝึกอ่านค่าเวอร์เนียร์คาลิเปอร์จำลอง")

if "val" not in st.session_state:
    st.session_state.val = 12.42

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

val = st.slider("ปรับระยะห่าง (มม.):", 0.0, 30.0, st.session_state.val, 0.02)
st.session_state.val = val

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.set_aspect("equal")
ax.set_xlim(-5, 55)
ax.set_ylim(-18, 12)
ax.axis("off")

ax.axhline(0, color="black", linewidth=1.5)
ax.fill_between([-5, 50], 0, 5, color="#E6E6E8", ec="gray")
ax.fill_between([-5, 0], -18, 0, color="#D8D8DC", ec="gray")

for m in range(0, 51):
    h = 3 if m % 10 == 0 else (2 if m % 5 == 0 else 1)
    ax.plot([m, m], [0, h], color="black", lw=0.8)
    if m % 10 == 0:
        ax.text(m, 4.5, str(m), ha="center", va="bottom", fontsize=9, fontweight="bold")

v_pos = st.session_state.val
ax.fill_between([v_pos, v_pos + 40], -14, 0, color="#CFCFD6", ec="gray", alpha=0.9)

vernier_pitch = 49 / 50
for v in range(51):
    vx = v_pos + (v * vernier_pitch)
    vh = -4 if v % 5 == 0 else -2.5
    ax.plot([vx, vx], [0, vh], color="darkblue", lw=0.8)
    if v % 5 == 0:
        ax.text(vx, vh - 1.5, f"{v/5:.1f}", ha="center", va="top", fontsize=7, color="darkblue")

st.pyplot(fig)

if st.button("👁️ เปิด/ปิด เฉลยคำตอบ", use_container_width=True):
    st.session_state.show_answer = not st.session_state.show_answer

if st.session_state.show_answer:
    m_part = int(st.session_state.val)
    v_div = round((st.session_state.val % 1) / 0.02)
    v_part = v_div * 0.02
    st.success(f"### คำตอบที่ถูกต้อง: {m_part}.00 + {v_part:.2f} = **{st.session_state.val:.2f} มม.** (สเกลย่อยที่: {v_div})")
else:
    st.info("### สถานะ: ซ่อนคำตอบอยู่ (ให้เด็กๆ ลองอ่านค่าดูก่อนนะ)")
