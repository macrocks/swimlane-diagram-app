import streamlit as st
import pandas as pd
from graphviz import Digraph

st.set_page_config(layout="wide")
st.title("Swimlane Diagram Generator from CSV")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    dot = Digraph('Swimlane', format='png')
    dot.attr(rankdir='LR', splines='polyline')

    layers = {
        "Experience Layer": "lightblue",
        "Process Layer": "lightgreen",
        "System Layer": "lightpink"
    }

    # Create subgraphs for layers
    for layer, color in layers.items():
        with dot.subgraph(name=f'cluster_{layer.replace(" ", "_")}') as c:
            c.attr(style='filled', color=color)
            c.attr(label=layer)

    for idx, row in df.iterrows():
        ext = row["External System"]
        exp = row["Exp API"]
        prc = row["Process API"]
        sys = row["System API"]
        dst = row["Downstream system"]

        dot.node(ext, shape="box", style="filled", fillcolor="lightblue")
        dot.node(exp, shape="box", style="filled", fillcolor="lightblue")
        dot.edge(ext, exp)

        dot.node(prc, shape="box", style="filled", fillcolor="lightgreen")
        dot.edge(exp, prc)

        dot.node(sys, shape="box", style="filled", fillcolor="lightpink")
        dot.edge(prc, sys)

        dot.node(dst, shape="box", style="filled", fillcolor="lightpink")
        dot.edge(sys, dst)

    st.graphviz_chart(dot)

    st.success("Diagram generated! Screenshot it or use the export version if running locally.")
