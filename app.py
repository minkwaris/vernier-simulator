"""
Precision Vernier Caliper Interactive GUI (0.02 mm resolution)
Designed for teaching and reading exercises.

Streamlit web version (ported from the original MATLAB vernier_interactive_sim).
Run locally:  streamlit run app.py
"""

import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import streamlit as st

FONT = ["Segoe UI", "DejaVu Sans"]
C_TICK = (0.15, 0.15, 0.15)
VERNIER_PITCH = 49 / 50  # 50 divisions = 49 mm -> 0.98 mm/div


# --------------------------------------------------------------------------
def draw_caliper(value: float):
    """Draw the caliper at the given reading (mm) and return the figure."""
    fig = plt.figure(figsize=(11.0, 4.2), dpi=110, facecolor=(0.94, 0.94, 0.95))
    ax = fig.add_axes([0.02, 0.05, 0.96, 0.90])
    ax.set_facecolor((0.94, 0.94, 0.95))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-10, 85)
    ax.set_ylim(-25, 20)
    ax.set_axis_off()

    # ---- Fixed main beam --------------------------------------------------
    ax.add_patch(Rectangle((-8, -6), 95, 22,
                           facecolor=(0.91, 0.91, 0.92),
                           edgecolor=(0.60, 0.60, 0.63), linewidth=1.5))

    # Main jaw (fixed)
    ax.add_patch(Polygon([[-8, -6], [0, -6], [0, -22], [-8, -22]], closed=True,
                         facecolor=(0.86, 0.86, 0.88),
                         edgecolor=(0.60, 0.60, 0.63), linewidth=1.5))

    # Main scale divisions (0 to 80 mm)
    for m in range(0, 81):
        if m % 10 == 0:
            y2 = 8
            ax.text(m, y2 + 2.5, str(m), ha="center", fontfamily=FONT,
                    fontsize=9.5, fontweight="bold", color=C_TICK)
        elif m % 5 == 0:
            y2 = 5.5
        else:
            y2 = 3.5
        ax.plot([m, m], [0, y2], color=C_TICK, linewidth=0.9)

    # ---- Movable vernier slider (translated by `value`) -------------------
    dx = value

    ax.add_patch(Polygon([[dx + 0, -22], [dx + 0, 0], [dx + 52, 0],
                          [dx + 52, -14], [dx + 10, -14], [dx + 0, -22]],
                         closed=True,
                         facecolor=(0.82, 0.83, 0.86),
                         edgecolor=(0.50, 0.50, 0.55), linewidth=1.3))

    for v in range(0, 51):
        vx = dx + v * VERNIER_PITCH
        if v % 5 == 0:
            vy = -6
            ax.text(vx, vy - 2.5, str(v // 5), ha="center", fontfamily=FONT,
                    fontsize=8.5, fontweight="bold", color=C_TICK)
        else:
            vy = -4
        ax.plot([vx, vx], [0, vy], color=C_TICK, linewidth=0.85)

    ax.text(dx + 47, -11, "0.02 mm", fontsize=7.5, fontweight="bold",
            color=(0.3, 0.3, 0.3), ha="center", fontfamily=FONT)

    return fig


# --------------------------------------------------------------------------
st.set_page_config(page_title="Interactive Vernier Caliper Simulator (0.02 mm)",
                   layout="wide")

st.title("Interactive Vernier Caliper Simulator (0.02 mm)")

if "value" not in st.session_state:
    st.session_state.value = 12.42          # Initial value

# Random question button (writes to session_state before the slider is made)
c1, c2 = st.columns([1, 5])
with c1:
    if st.button("🎲 Random"):
        st.session_state.value = round(random.uniform(0, 30) / 0.02) * 0.02

val = st.slider("Fine Adjust (mm)", min_value=0.0, max_value=30.0,
                step=0.02, key="value", format="%.2f")

st.pyplot(draw_caliper(val), use_container_width=True)

show_answer = st.toggle("Show Answer")

m_part = int(val // 1)
v_div = int(round((val % 1) / 0.02))
v_part = v_div * 0.02

if show_answer:
    st.success("Reading: %d.00 + %.2f = %.2f mm  (Division: %d)"
               % (m_part, v_part, val, v_div))
else:
    st.info("??? mm (Answer Hidden)")
