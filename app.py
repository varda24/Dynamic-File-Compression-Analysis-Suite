import streamlit as st

st.set_page_config(
    page_title="Dynamic Compression Intelligence Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #0b1020 0%,
        #121b35 40%,
        #0d1328 100%
    );
}

[data-testid="stSidebar"]{
    background:#10182d;
}

.hero{
    background: linear-gradient(
        135deg,
        #00f5d4,
        #00bbf9
    );

    padding:40px;
    border-radius:25px;
    color:black;
    text-align:center;
    margin-bottom:20px;
}

.metric-card{
    background:rgba(255,255,255,0.06);
    backdrop-filter:blur(15px);

    border:1px solid rgba(255,255,255,0.15);

    border-radius:20px;
    padding:20px;

    text-align:center;
}

.metric-value{
    font-size:34px;
    font-weight:bold;
}

.metric-label{
    color:#bbbbbb;
}

.feature-card{
    background:rgba(255,255,255,0.04);
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.08);
    height:180px;
}

.footer{
    text-align:center;
    color:#888;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2910/2910791.png",
        width=100
    )

    st.title("Compression Suite")

    st.success("Version 2.0")

    st.markdown("---")

    st.markdown("""
### Modules

🏠 Dashboard

⚡ Compression Lab

📊 Analytics

🏆 Benchmark Arena

🌳 Visualization Studio

📑 Report Hub
""")

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero">

<h1>🚀 Dynamic Compression Intelligence Suite</h1>

<h4>
Advanced File Compression, Benchmarking,
Integrity Verification & Analytics Platform
</h4>

Compress • Analyze • Benchmark • Visualize

</div>
""", unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">52.49%</div>
        <div class="metric-label">
        Best Compression
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">100%</div>
        <div class="metric-label">
        Integrity Score
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">2</div>
        <div class="metric-label">
        Algorithms
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">PDF</div>
        <div class="metric-label">
        Reporting
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# OVERVIEW
# =========================

st.subheader("📌 Platform Overview")

st.info("""
Dynamic Compression Intelligence Suite is a
production-inspired compression platform built using
Data Structures & Algorithms.

The platform supports:

• Huffman Coding

• Run Length Encoding (RLE)

• Compression Benchmarking

• SHA256 Integrity Verification

• PDF / CSV Reporting

• Frequency Analysis

• Huffman Tree Visualization
""")

# =========================
# FEATURES
# =========================

st.subheader("✨ Core Modules")

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
<div class="feature-card">

<h3>⚡ Compression Lab</h3>

Upload files

Compress using:

• Huffman Coding

• RLE

Generate compressed outputs

</div>
""", unsafe_allow_html=True)

with c2:

    st.markdown("""
<div class="feature-card">

<h3>📊 Analytics</h3>

Real-time metrics

Compression ratio

Space saved

Performance statistics

</div>
""", unsafe_allow_html=True)

with c3:

    st.markdown("""
<div class="feature-card">

<h3>🏆 Benchmark Arena</h3>

Compare algorithms

Encoding speed

Decoding speed

Compression efficiency

</div>
""", unsafe_allow_html=True)

st.write("")

c4, c5, c6 = st.columns(3)

with c4:

    st.markdown("""
<div class="feature-card">

<h3>🌳 Visualization</h3>

Frequency Distribution

Huffman Tree

Compression Charts

</div>
""", unsafe_allow_html=True)

with c5:

    st.markdown("""
<div class="feature-card">

<h3>🔐 Integrity Center</h3>

SHA256 Verification

Lossless Recovery

Hash Matching

</div>
""", unsafe_allow_html=True)

with c6:

    st.markdown("""
<div class="feature-card">

<h3>📑 Report Hub</h3>

TXT Reports

CSV Reports

PDF Reports

</div>
""", unsafe_allow_html=True)

# =========================
# PROJECT STATS
# =========================

st.subheader("📈 Project Statistics")

a1, a2, a3 = st.columns(3)

with a1:
    st.metric(
        "Algorithms Implemented",
        "2"
    )

with a2:
    st.metric(
        "Compression Methods",
        "Lossless"
    )

with a3:
    st.metric(
        "Verification",
        "SHA-256"
    )

# =========================
# TIMELINE
# =========================

st.subheader("🧠 Compression Workflow")

st.markdown("""
```text
Input File
    ↓
Frequency Analysis
    ↓
Min Heap Construction
    ↓
Huffman Tree Generation
    ↓
Binary Encoding
    ↓
Compression
    ↓
Storage
    ↓
Decompression
    ↓
Integrity Verification
            """)