"""
Precision Vernier Caliper Interactive GUI (0.02 mm resolution)
Designed for teaching and reading exercises.

Python port of the original MATLAB function `vernier_interactive_sim`.
Requires: matplotlib  (pip install matplotlib)
Run:      python vernier_interactive_sim.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.transforms import Affine2D
from matplotlib.widgets import Slider, Button

FONT = ['Segoe UI', 'DejaVu Sans']


def vernier_interactive_sim():
    state = {
        'current_val': 12.42,      # Initial value
        'is_dragging': False,
        'drag_start_x': 0.0,
        'drag_start_val': 0.0,
        'show_answer': False,
        'updating': False,
    }

    # ---- 1. Create Main Figure & Axes ---------------------------------------
    f = plt.figure(num='Interactive Vernier Caliper Simulator (0.02 mm)',
                   figsize=(11.0, 4.8), dpi=100,
                   facecolor=(0.94, 0.94, 0.95))
    try:
        f.canvas.manager.set_window_title(
            'Interactive Vernier Caliper Simulator (0.02 mm)')
    except Exception:
        pass

    ax = f.add_axes([0.04, 0.28, 0.92, 0.65])
    ax.set_facecolor((0.94, 0.94, 0.95))
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-10, 85)
    ax.set_ylim(-25, 20)
    ax.set_axis_off()

    # ---- 2. Draw Fixed Main Beam -------------------------------------------
    # Main body
    ax.add_patch(Rectangle((-8, -6), 95, 22,
                           facecolor=(0.91, 0.91, 0.92),
                           edgecolor=(0.60, 0.60, 0.63), linewidth=1.5))

    # Main jaw (fixed)
    ax.add_patch(Polygon([[-8, -6], [0, -6], [0, -22], [-8, -22]],
                         closed=True,
                         facecolor=(0.86, 0.86, 0.88),
                         edgecolor=(0.60, 0.60, 0.63), linewidth=1.5))

    # Main scale divisions (0 to 80 mm)
    cTick = (0.15, 0.15, 0.15)
    for m in range(0, 81):
        if m % 10 == 0:
            y2 = 8
            ax.text(m, y2 + 2.5, str(m), ha='center',
                    fontfamily=FONT, fontsize=9.5,
                    fontweight='bold', color=cTick)
        elif m % 5 == 0:
            y2 = 5.5
        else:
            y2 = 3.5
        ax.plot([m, m], [0, y2], color=cTick, linewidth=0.9)

    # ---- 3. Slider Component Handles (Dynamic Group) ------------------------
    slider_group = []   # artists that translate with the vernier

    # Vernier movable jaw & body
    body = Polygon([[0, -22], [0, 0], [52, 0], [52, -14], [10, -14], [0, -22]],
                   closed=True,
                   facecolor=(0.82, 0.83, 0.86),
                   edgecolor=(0.50, 0.50, 0.55), linewidth=1.3)
    ax.add_patch(body)
    slider_group.append(body)

    # Vernier scale ticks (50 divisions = 49 mm -> 0.98 mm/div)
    vernier_pitch = 49 / 50
    for v in range(0, 51):
        vx = v * vernier_pitch
        if v % 5 == 0:
            vy = -6
            t = ax.text(vx, vy - 2.5, str(v // 5), ha='center',
                        fontfamily=FONT, fontsize=8.5,
                        fontweight='bold', color=cTick)
            slider_group.append(t)
        else:
            vy = -4
        ln, = ax.plot([vx, vx], [0, vy], color=cTick, linewidth=0.85)
        slider_group.append(ln)

    t_res = ax.text(47, -11, '0.02 mm', fontsize=7.5, fontweight='bold',
                    color=(0.3, 0.3, 0.3), ha='center', fontfamily=FONT)
    slider_group.append(t_res)

    # ---- 4. Control Panel & Teacher Controls --------------------------------
    # UI Slider label
    f.text(0.06, 0.16 + 0.025, 'Fine Adjust:', fontsize=10, fontweight='bold',
           ha='left', va='center', fontfamily=FONT,
           backgroundcolor=(0.94, 0.94, 0.95))

    ax_sld = f.add_axes([0.18, 0.17, 0.55, 0.05])
    sld = Slider(ax_sld, '', 0, 30, valinit=state['current_val'],
                 valstep=0.02, color=(0.25, 0.50, 0.85))
    sld.valtext.set_visible(False)

    # Toggle Answer Button
    ax_btn = f.add_axes([0.76, 0.16, 0.18, 0.07])
    btnToggle = Button(ax_btn, 'Show Answer',
                       color=(0.25, 0.50, 0.85),
                       hovercolor=(0.30, 0.56, 0.90))
    btnToggle.label.set_fontsize(10)
    btnToggle.label.set_fontweight('bold')
    btnToggle.label.set_color((1, 1, 1))
    btnToggle.label.set_fontfamily(FONT)

    # Readout Text / Hidden answer display
    txtDisplay = f.text(0.25 + 0.50 / 2, 0.03 + 0.09 / 2,
                        '??? mm (Answer Hidden)',
                        fontsize=13, fontweight='bold',
                        ha='center', va='center', fontfamily=FONT,
                        color=(0.4, 0.4, 0.4),
                        bbox=dict(facecolor=(1, 1, 1),
                                  edgecolor=(0.75, 0.75, 0.75)))

    # ---- Helper Functions & Callbacks --------------------------------------
    def updatePosition(val):
        val = round(val / 0.02) * 0.02   # Snap to physical resolution 0.02 mm
        state['current_val'] = max(0.0, min(30.0, val))
        cur = state['current_val']

        # Move vernier graphics
        tr = Affine2D().translate(cur, 0) + ax.transData
        for artist in slider_group:
            artist.set_transform(tr)

        state['updating'] = True
        sld.set_val(cur)
        state['updating'] = False

        # Update text reading
        if state['show_answer']:
            m_part = int(cur // 1)
            v_div = int(round((cur % 1) / 0.02))
            v_part = v_div * 0.02
            txtDisplay.set_text(
                'Reading: %d.00 + %.2f = %.2f mm (Division: %d)'
                % (m_part, v_part, cur, v_div))
            txtDisplay.set_color((0.1, 0.55, 0.2))
        else:
            txtDisplay.set_text('??? mm (Answer Hidden)')
            txtDisplay.set_color((0.4, 0.4, 0.4))

        f.canvas.draw_idle()

    def onSliderScroll(val):
        if state['updating']:
            return
        updatePosition(val)

    def onToggleAnswer(event):
        state['show_answer'] = not state['show_answer']
        if state['show_answer']:
            btnToggle.label.set_text('Hide Answer')
            btnToggle.color = (0.85, 0.35, 0.35)
            btnToggle.hovercolor = (0.90, 0.40, 0.40)
            ax_btn.set_facecolor((0.85, 0.35, 0.35))
        else:
            btnToggle.label.set_text('Show Answer')
            btnToggle.color = (0.25, 0.50, 0.85)
            btnToggle.hovercolor = (0.30, 0.56, 0.90)
            ax_btn.set_facecolor((0.25, 0.50, 0.85))
        updatePosition(state['current_val'])

    def onMouseDown(event):
        if event.inaxes is not ax or event.xdata is None:
            return
        mx, my = event.xdata, event.ydata
        cur = state['current_val']
        # Click on vernier body area to drag
        if cur <= mx <= (cur + 52) and -22 <= my <= 0:
            state['is_dragging'] = True
            state['drag_start_x'] = mx
            state['drag_start_val'] = cur

    def onMouseMove(event):
        if state['is_dragging']:
            if event.inaxes is not ax or event.xdata is None:
                return
            dx = event.xdata - state['drag_start_x']
            updatePosition(state['drag_start_val'] + dx)

    def onMouseUp(event):
        state['is_dragging'] = False

    sld.on_changed(onSliderScroll)
    btnToggle.on_clicked(onToggleAnswer)
    f.canvas.mpl_connect('button_press_event', onMouseDown)
    f.canvas.mpl_connect('motion_notify_event', onMouseMove)
    f.canvas.mpl_connect('button_release_event', onMouseUp)

    ax_btn.set_facecolor((0.25, 0.50, 0.85))
    updatePosition(state['current_val'])

    plt.show()
    return f


if __name__ == '__main__':
    vernier_interactive_sim()
