import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import io

LANES = ['Experience layer', 'Process layer', 'System layer']
LANE_COLORS = ['#0B5ED7', '#00B1B0', '#8265F6']
LANE_Y = {'Experience': 0.8, 'Process': 0.5, 'System': 0.2}

def draw_swimlane(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('off')

    # Draw swimlane background bands
    for idx, (label, color) in enumerate(zip(LANES, LANE_COLORS)):
        y = list(LANE_Y.values())[idx]
        ax.add_patch(plt.Rectangle((0, y - 0.1), 1.2, 0.2, color=color, alpha=0.15))
        ax.text(-0.01, y, label, va='center', ha='right', fontsize=12, fontweight='bold')

    # Extract unique nodes and assign x-positions
    node_positions = {}
    connections = set()
    node_counters = defaultdict(int)

    x_gap = 0.2
    x_positions = defaultdict(float)

    def get_or_add_node(label, layer):
        if (label, layer) not in node_positions:
            x = x_positions[layer]
            y = LANE_Y[layer]
            node_positions[(label, layer)] = (x, y)
            x_positions[layer] += x_gap
        return node_positions[(label, layer)]

    # Parse and create nodes and edges
    for _, row in df.iterrows():
        exp = row['Exp API']
        prc = row['Process API']
        sys = row['System API']

        exp_pos = get_or_add_node(exp, 'Experience')
        prc_pos = get_or_add_node(prc, 'Process')
        sys_pos = get_or_add_node(sys, 'System')

        connections.update([
            ((exp, 'Experience'), (prc, 'Process')),
            ((prc, 'Process'), (sys, 'System'))
        ])

    # Draw nodes
    for (label, layer), (x, y) in node_positions.items():
        ax.add_patch(plt.Rectangle((x, y - 0.03), 0.15, 0.06, color='skyblue', ec='black', zorder=2))
        ax.text(x + 0.075, y, label, ha='center', va='center', fontsize=8, zorder=3)

    # Draw arrows
    for (src_label, src_layer), (dst_label, dst_layer) in connections:
        src_x, src_y = node_positions[(src_label, src_layer)]
        dst_x, dst_y = node_positions[(dst_label, dst_layer)]
        ax.annotate("",
                    xy=(dst_x + 0.075, dst_y),
                    xytext=(src_x + 0.075, src_y),
                    arrowprops=dict(arrowstyle='->', linestyle='dashed', color='gray'))

    return fig

# Streamlit interface
st.set_page_config(layout="wide")
st.title("Swimlane Diagram Generator (MuleSoft Style)")
st.markdown("Upload a CSV with columns: `Exp API`, `Process API`, `System API`")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {'Exp API', 'Process API', 'System API'}
    if not required_cols.issubset(df.columns):
        st.error("CSV must include columns: 'Exp API', 'Process API', 'System API'")
    else:
        fig = draw_swimlane(df)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.pyplot(fig)
        st.download_button("Download Diagram as PNG", buf.getvalue(), "swimlane_diagram.png", "image/png")
