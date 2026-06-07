import streamlit as st
import tempfile
import os
from datetime import datetime

from src.analytics import CompressionAnalytics
from src.huffman import HuffmanCoding
from src.rle import RunLengthEncoding

st.set_page_config(
    page_title="Report Hub",
    page_icon="📑",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.hero{
    background:linear-gradient(
        135deg,
        #00F5D4,
        #00BBF9
    );
    padding:30px;
    border-radius:25px;
    color:black;
    text-align:center;
    margin-bottom:20px;
}

.card{
    background:rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    border:1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HERO
# =====================================

st.markdown("""
<div class="hero">

<h1>📑 Report Hub</h1>

<h4>
Generate Professional Compression Reports
</h4>

</div>
""", unsafe_allow_html=True)

# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "Upload Text File",
    type=["txt"]
)

algorithm = st.selectbox(
    "Compression Algorithm",
    [
        "Huffman Coding",
        "Run Length Encoding"
    ]
)

# =====================================
# PROCESS
# =====================================

if uploaded_file:

    text = uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )

    st.subheader("📄 File Preview")

    st.text_area(
        "Preview",
        text[:1000],
        height=200
    )

    if st.button(
        "📊 Generate Report",
        use_container_width=True
    ):

        with st.spinner(
            "Generating analytics..."
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".txt",
                mode="w",
                encoding="utf-8"
            ) as temp:

                temp.write(text)
                input_file = temp.name

            output_file = (
                input_file + ".compressed"
            )

            # =====================================
            # COMPRESS
            # =====================================

            if algorithm == "Huffman Coding":

                compressor = HuffmanCoding()

                output_file += ".huff"

                compressor.compress_file(
                    input_file,
                    output_file
                )

                algo_name = "Huffman"

            else:

                compressor = RunLengthEncoding()

                output_file += ".rle"

                compressor.compress_file(
                    input_file,
                    output_file
                )

                algo_name = "RLE"

            # =====================================
            # ANALYTICS
            # =====================================

            analytics = CompressionAnalytics()

            analytics.input_file = (
                uploaded_file.name
            )

            analytics.algorithm = (
                algo_name
            )

            analytics.original_size = (
                os.path.getsize(input_file)
            )

            analytics.compressed_size = (
                os.path.getsize(output_file)
            )

            analytics.encoding_time = (
                compressor.encoding_time
            )

            analytics.original_bits = (
                compressor.original_bits
            )

            analytics.encoded_bits = (
                compressor.encoded_bits
            )

            analytics.theoretical_ratio = (
                compressor.theoretical_ratio
            )

            analytics.integrity_status = (
                "GENERATED"
            )

            # =====================================
            # CREATE REPORTS
            # =====================================

            os.makedirs(
                "reports",
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            txt_report = (
                f"reports/report_{timestamp}.txt"
            )

            csv_report = (
                f"reports/report_{timestamp}.csv"
            )

            pdf_report = (
                f"reports/report_{timestamp}.pdf"
            )

            analytics.save_report(
                txt_report
            )

            analytics.save_csv_report(
                csv_report
            )

            try:

                analytics.save_pdf_report(
                    pdf_report
                )

                pdf_created = True

            except Exception:

                pdf_created = False

        st.success(
            "Reports Generated Successfully"
        )

        # =====================================
        # SUMMARY
        # =====================================

        summary = (
            analytics.get_summary()
        )

        st.subheader(
            "📈 Report Summary"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Original",
                summary["original_size"]
            )

        with c2:
            st.metric(
                "Compressed",
                summary["compressed_size"]
            )

        with c3:
            st.metric(
                "Ratio",
                summary["compression_ratio"]
            )

        with c4:
            st.metric(
                "Algorithm",
                algo_name
            )

        st.divider()

        # =====================================
        # REPORT PREVIEW
        # =====================================

        st.subheader(
            "📄 Report Preview"
        )

        st.code(
            analytics.get_analytics_report()
        )

        # =====================================
        # DOWNLOADS
        # =====================================

        st.subheader(
            "⬇ Download Reports"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            with open(
                txt_report,
                "rb"
            ) as f:

                st.download_button(
                    "TXT Report",
                    f,
                    file_name=os.path.basename(
                        txt_report
                    ),
                    use_container_width=True
                )

        with col2:

            with open(
                csv_report,
                "rb"
            ) as f:

                st.download_button(
                    "CSV Report",
                    f,
                    file_name=os.path.basename(
                        csv_report
                    ),
                    use_container_width=True
                )

        with col3:

            if pdf_created:

                with open(
                    pdf_report,
                    "rb"
                ) as f:

                    st.download_button(
                        "PDF Report",
                        f,
                        file_name=os.path.basename(
                            pdf_report
                        ),
                        use_container_width=True
                    )

            else:

                st.warning(
                    "ReportLab not installed"
                )

        # =====================================
        # CLEANUP
        # =====================================

        try:

            os.remove(input_file)
            os.remove(output_file)

        except:
            pass

else:

    st.info("""
Upload a file to generate:

✅ TXT Report

✅ CSV Report

✅ PDF Report

✅ Compression Analytics Summary

✅ Downloadable Documentation
""")