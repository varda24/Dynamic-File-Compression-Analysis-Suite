import streamlit as st
import tempfile
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.benchmark import Benchmark

st.set_page_config(
    page_title="Benchmark Arena",
    page_icon="🏆",
    layout="wide"
)

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.winner-card{
    background:linear-gradient(
        135deg,
        #00F5D4,
        #00BBF9
    );

    padding:25px;
    border-radius:20px;
    text-align:center;
    color:black;
    font-weight:bold;
}

.battle-card{
    background:rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.title("🏆 Benchmark Arena")

st.caption(
    "Head-to-head algorithm comparison"
)

# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "Upload Text File",
    type=["txt"]
)

if uploaded_file:

    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Input Preview")

    st.text_area(
        "Preview",
        text[:1500],
        height=200
    )

    if st.button(
        "🚀 Run Benchmark",
        use_container_width=True
    ):

        with st.spinner(
            "Benchmarking algorithms..."
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".txt",
                mode="w",
                encoding="utf-8"
            ) as temp:

                temp.write(text)
                temp_path = temp.name

            benchmark = Benchmark()

            results = benchmark.compare_algorithms(
                temp_path
            )

        os.remove(temp_path)

        # =====================================
        # DATAFRAME
        # =====================================

        df = pd.DataFrame([
            {
                "Algorithm": algo,
                "Compression Ratio": data["ratio"],
                "Encoding Time": data["encoding_time"],
                "Decoding Time": data["decoding_time"]
            }
            for algo, data in results.items()
        ])

        st.success(
            "Benchmark Completed"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # =====================================
        # WINNER
        # =====================================

        winner = min(
            results.items(),
            key=lambda x: x[1]["ratio"]
        )

        st.markdown(f"""
        <div class="winner-card">

        <h1>🏆 Winner</h1>

        <h2>{winner[0]}</h2>

        Compression Ratio:
        {winner[1]['ratio']}%

        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # =====================================
        # COMPRESSION COMPARISON
        # =====================================

        st.subheader(
            "📊 Compression Ratio Battle"
        )

        fig = px.bar(
            df,
            x="Algorithm",
            y="Compression Ratio",
            color="Algorithm",
            text="Compression Ratio"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================
        # ENCODING TIME
        # =====================================

        st.subheader(
            "⚡ Encoding Performance"
        )

        fig = px.bar(
            df,
            x="Algorithm",
            y="Encoding Time",
            color="Algorithm"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================
        # DECODING TIME
        # =====================================

        st.subheader(
            "⏱ Decoding Performance"
        )

        fig = px.bar(
            df,
            x="Algorithm",
            y="Decoding Time",
            color="Algorithm"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================
        # RADAR CHART
        # =====================================

        st.subheader(
            "🛰 Algorithm Radar"
        )

        fig = go.Figure()

        for algo in results:

            fig.add_trace(
                go.Scatterpolar(
                    r=[
                        100-results[algo]["ratio"],
                        1/results[algo]["encoding_time"]
                        if results[algo]["encoding_time"] > 0
                        else 0,
                        1/results[algo]["decoding_time"]
                        if results[algo]["decoding_time"] > 0
                        else 0
                    ],
                    theta=[
                        "Compression",
                        "Encoding",
                        "Decoding"
                    ],
                    fill="toself",
                    name=algo
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True
                )
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================
        # PERFORMANCE SCORE
        # =====================================

        st.subheader(
            "🎯 Performance Score"
        )

        for algo, data in results.items():

            score = round(
                100 - data["ratio"],
                2
            )

            st.metric(
                algo,
                f"{score}/100"
            )

        # =====================================
        # RAW REPORT
        # =====================================

        with st.expander(
            "📄 Detailed Report"
        ):

            st.code(
                benchmark.get_comparison_report()
            )