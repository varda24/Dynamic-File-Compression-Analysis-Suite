import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.kpi-card{
    background:rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
}

.feature-card{
    background:rgba(255,255,255,0.04);
    border-radius:20px;
    padding:20px;
    border:1px solid rgba(255,255,255,0.08);
    height:220px;
}

.hero{
    background:linear-gradient(
        135deg,
        #00F5D4,
        #00BBF9
    );

    padding:40px;
    border-radius:25px;
    color:black;
    text-align:center;
    margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HERO
# =====================================

st.markdown("""
<div class="hero">

<h1>🚀 Dynamic Compression Intelligence Suite</h1>

<h4>
Advanced Compression • Analytics • Benchmarking
</h4>

</div>
""", unsafe_allow_html=True)

# =====================================
# KPI SECTION
# =====================================

st.subheader("📈 Platform Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Algorithms",
        "2"
    )

with c2:
    st.metric(
        "Verification",
        "SHA-256"
    )

with c3:
    st.metric(
        "Compression",
        "Lossless"
    )

with c4:
    st.metric(
        "Reports",
        "PDF/CSV/TXT"
    )

# =====================================
# HISTORY ANALYTICS
# =====================================

st.subheader("📊 Compression Analytics")

history_file = "logs/history.csv"

if os.path.exists(history_file):

    history = pd.read_csv(history_file)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Files Compressed",
            len(history)
        )

    with col2:

        avg_ratio = round(
            history["Ratio"].mean(),
            2
        )

        st.metric(
            "Average Ratio",
            f"{avg_ratio}%"
        )

    with col3:

        best_ratio = round(
            history["Ratio"].min(),
            2
        )

        st.metric(
            "Best Ratio",
            f"{best_ratio}%"
        )

else:

    st.warning(
        "No compression history found."
    )

# =====================================
# FEATURES
# =====================================

st.subheader("✨ Core Modules")

f1, f2, f3 = st.columns(3)

with f1:

    st.markdown("""
<div class="feature-card">

<h3>⚡ Compression Lab</h3>

Upload and compress files using:

• Huffman Coding

• Run Length Encoding

• Multi-file Compression

</div>
""", unsafe_allow_html=True)

with f2:

    st.markdown("""
<div class="feature-card">

<h3>📊 Analytics Center</h3>

Analyze:

• Compression Ratio

• Space Saved

• Performance Metrics

• Compression Trends

</div>
""", unsafe_allow_html=True)

with f3:

    st.markdown("""
<div class="feature-card">

<h3>🏆 Benchmark Arena</h3>

Compare:

• Huffman Coding

• RLE

• Encoding Speed

• Decoding Speed

</div>
""", unsafe_allow_html=True)

st.write("")

f4, f5, f6 = st.columns(3)

with f4:

    st.markdown("""
<div class="feature-card">

<h3>🌳 Visualization Studio</h3>

Generate:

• Frequency Graphs

• Huffman Trees

• Performance Charts

</div>
""", unsafe_allow_html=True)

with f5:

    st.markdown("""
<div class="feature-card">

<h3>🔐 Integrity Center</h3>

Verify:

• SHA256 Hashes

• Lossless Recovery

• Data Integrity

</div>
""", unsafe_allow_html=True)

with f6:

    st.markdown("""
<div class="feature-card">

<h3>📑 Report Hub</h3>

Export:

• TXT Reports

• CSV Reports

• PDF Reports

</div>
""", unsafe_allow_html=True)

# =====================================
# PROJECT WORKFLOW
# =====================================

st.subheader("🧠 Compression Workflow")

st.code("""
Input File
     ↓
Frequency Analysis
     ↓
Min Heap Construction
     ↓
Huffman Tree Generation
     ↓
Code Assignment
     ↓
Compression
     ↓
Storage
     ↓
Decompression
     ↓
Integrity Verification
""")

# =====================================
# RECENT HISTORY
# =====================================

st.subheader("📜 Recent Activity")

if os.path.exists(history_file):

    history = pd.read_csv(history_file)

    st.dataframe(
        history.tail(10),
        use_container_width=True
    )

else:

    st.info(
        "No history available yet."
    )

# =====================================
# FOOTER
# =====================================

st.divider()

st.caption(
    "Dynamic Compression Intelligence Suite | DSA Project"
)