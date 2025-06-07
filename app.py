import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

# Constants for layout
LANES = ['Experience layer', 'Process layer', 'System layer']
LANE_COLORS = ['#0B5ED7', '#00B1B0', '#8265F6']
LANE_Y = [0.8, 0.5, 0.2]

def draw_diagram(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('off')

    # Draw swimlanes
    for idx, (name, color, y) in enumerate(zip(LANES, LANE_COLORS, LANE_Y)):
        ax.add_patch(plt.Rectangle((0, y - 0.1), 1, 0.2, color=color, alpha=0.15))
        ax.text(-0.01, y, name, va='center', ha='right', fontsize=12, fontweight='bold')

    # Draw nodes and connectors
    node_pos = {}
    for i, row in df.iterrows():
        values = [row['Exp API'], row['Process API'], row['System API']]
        for j, val in enumerate(values):
            x = i * 0.15 + 0.1 * j
            y = LANE_Y[j]
            ax.add_patch(plt.Rectangle((x, y - 0.03), 0.12, 0.06, color='skyblue', ec='black', zorder=2))
            ax.text(x + 0.06, y, val, va='center', ha='center', fontsize=8, zorder=3)
            node_pos[val] = (x + 0.06, y)

        # Draw connectors
        for a, b in zip(values, values[1:]):
            if a in node_pos and b in node_pos:
                ax.annotate("",
                            xy=node_pos[b], xycoords='data',
                            xytext=node_pos[a], textcoords='data',
                            arrowprops=dict(arrowstyle='->', linestyle='dashed', color='gray'))

    return fig

# Streamlit UI
st.set_page_config(layout="wide")
st.title("Swimlane Diagram Generator")
st.markdown("Upload a CSV file to generate a 3-layer swimlane diagram (Experience → Process → System).")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {'Exp API', 'Process API', 'System API'}
    if not required_cols.issubset(df.columns):
        st.error("CSV must contain 'Exp API', 'Process API', and 'System API' columns.")
    else:
        fig = draw_diagram(df)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.pyplot(fig)

        st.download_button("Download PNG", buf.getvalue(), "swimlane_diagram.png", "image/png")
