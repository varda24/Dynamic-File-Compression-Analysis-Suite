import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Analytics Center",
    page_icon="📊",
    layout="wide"
)

# =====================================
# HEADER
# =====================================

st.title("📊 Analytics Center")

st.caption(
    "Compression Intelligence Dashboard"
)

history_file = "logs/history.csv"

# =====================================
# LOAD HISTORY
# =====================================

if not os.path.exists(history_file):
    st.warning("No compression history available.")
    st.stop()

history = pd.read_csv(history_file)

# =====================================
# KPI CARDS
# =====================================

st.subheader("🚀 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Runs",
        len(history)
    )

with c2:
    st.metric(
        "Average Ratio",
        f"{history['Ratio'].mean():.2f}%"
    )

with c3:
    st.metric(
        "Best Compression",
        f"{history['Ratio'].min():.2f}%"
    )

with c4:
    st.metric(
        "Worst Compression",
        f"{history['Ratio'].max():.2f}%"
    )

st.divider()

# =====================================
# COMPRESSION HEALTH SCORE
# =====================================

st.subheader("🏆 Compression Health Score")

avg_ratio = history["Ratio"].mean()

score = max(0, 100 - avg_ratio)

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Efficiency Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#00F5D4"},
            "steps": [
                {"range": [0, 40], "color": "#ff4b4b"},
                {"range": [40, 70], "color": "#f9c74f"},
                {"range": [70, 100], "color": "#43aa8b"}
            ]
        }
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# RATIO TREND
# =====================================

st.subheader("📈 Compression Ratio Trend")

fig = px.line(
    history,
    x="Date",
    y="Ratio",
    markers=True,
    title="Compression Ratio Over Time"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# ALGORITHM USAGE
# =====================================

st.subheader("⚡ Algorithm Usage")

algo_counts = (
    history["Algorithm"]
    .value_counts()
    .reset_index()
)

algo_counts.columns = [
    "Algorithm",
    "Count"
]

fig = px.pie(
    algo_counts,
    names="Algorithm",
    values="Count",
    hole=0.6,
    title="Algorithm Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# ENCODING TIME
# =====================================

st.subheader("⏱ Encoding Performance")

fig = px.bar(
    history,
    x="File",
    y="EncodingTime",
    color="Algorithm",
    title="Encoding Time Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# TOP PERFORMING FILES
# =====================================

st.subheader("🥇 Best Compression Results")

best = history.sort_values(
    by="Ratio"
).head(10)

st.dataframe(
    best,
    use_container_width=True
)

# =====================================
# ANALYTICS SUMMARY
# =====================================

st.subheader("🧠 AI-Style Insights")

best_ratio = history["Ratio"].min()
avg_ratio = history["Ratio"].mean()

st.success(
    f"""
Best compression achieved:
{best_ratio:.2f}%

Average compression:
{avg_ratio:.2f}%

Compression engine is performing efficiently.
"""
)

# =====================================
# RAW DATA
# =====================================

with st.expander("📄 View Raw History"):

    st.dataframe(
        history,
        use_container_width=True
    )