import streamlit as st
import pandas as pd
from graphviz import Digraph

st.set_page_config(layout="wide")
st.title("API-Led Swimlane Diagram Generator")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    dot = Digraph("Swimlane", format="png")
    dot.attr(rankdir='LR', splines='polyline', nodesep='1.0', ranksep='1.0')

    # Layer ranks
    experience_nodes = set()
    process_nodes = set()
    system_nodes = set()

    # Add nodes and edges
    for _, row in df.iterrows():
        ext_sys = row["External System"]
        exp_api = row["Exp API"]
        prc_api = row["Process API"]
        sys_api = row["System API"]
        dst_sys = row["Downstream system"]

        # Layer node assignment
        experience_nodes.update([ext_sys, exp_api])
        process_nodes.add(prc_api)
        system_nodes.update([sys_api, dst_sys])

        # Draw connections
        dot.edge(ext_sys, exp_api, label="calls")
        dot.edge(exp_api, prc_api, label="invokes")
        dot.edge(prc_api, sys_api, label="delegates")
        dot.edge(sys_api, dst_sys, label="connects")

    # Grouping by layer using invisible edges and same rank
    with dot.subgraph() as s:
        s.attr(rank='same')
        for node in experience_nodes:
            s.node(node, shape="box", style="filled", fillcolor="#C6E5FF")

    with dot.subgraph() as s:
        s.attr(rank='same')
        for node in process_nodes:
            s.node(node, shape="box", style="filled", fillcolor="#C7F3D4")

    with dot.subgraph() as s:
        s.attr(rank='same')
        for node in system_nodes:
            s.node(node, shape="box", style="filled", fillcolor="#FAD7A0")

    # Render the diagram
    st.graphviz_chart(dot)
    st.markdown("✅ Swimlane diagram generated. Screenshot it or run locally to export as PNG.")
