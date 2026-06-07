import streamlit as st
import tempfile
import os
import time

from src.huffman import HuffmanCoding
from src.rle import RunLengthEncoding

st.set_page_config(
    page_title="Compression Lab",
    page_icon="⚡",
    layout="wide"
)

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.upload-box{
    padding:20px;
    border-radius:20px;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
}

.result-card{
    background:rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.title("⚡ Compression Lab")

st.caption(
    "Compress files using Huffman Coding or Run Length Encoding"
)

# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "Upload Text File",
    type=["txt"]
)

algorithm = st.selectbox(
    "Choose Algorithm",
    [
        "Huffman Coding",
        "Run Length Encoding"
    ]
)

# =====================================
# PREVIEW
# =====================================

if uploaded_file:

    content = uploaded_file.read().decode("utf-8")

    st.subheader("📄 File Preview")

    st.text_area(
        "Preview",
        content[:1500],
        height=250
    )

    original_size = len(content.encode("utf-8"))

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Characters",
            len(content)
        )

    with c2:
        st.metric(
            "Original Size",
            f"{original_size/1024:.2f} KB"
        )

    # =====================================
    # COMPRESS BUTTON
    # =====================================

    if st.button(
        "🚀 Start Compression",
        use_container_width=True
    ):

        with st.spinner("Compressing..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".txt",
                mode="w",
                encoding="utf-8"
            ) as temp_input:

                temp_input.write(content)

                input_path = temp_input.name

            output_path = input_path + ".compressed"

            start = time.perf_counter()

            # ---------------------------------

            if algorithm == "Huffman Coding":

                compressor = HuffmanCoding()

                output_path += ".huff"

                compressor.compress_file(
                    input_path,
                    output_path
                )

                encoding_time = compressor.encoding_time

                theoretical_ratio = (
                    compressor.theoretical_ratio
                )

            else:

                compressor = RunLengthEncoding()

                output_path += ".rle"

                compressor.compress_file(
                    input_path,
                    output_path
                )

                encoding_time = compressor.encoding_time

                theoretical_ratio = (
                    compressor.theoretical_ratio
                )

            total_time = (
                time.perf_counter() - start
            )

            compressed_size = (
                os.path.getsize(output_path)
            )

        st.success(
            "Compression Completed Successfully!"
        )

        # =====================================
        # RESULTS
        # =====================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Original Size",
                f"{original_size/1024:.2f} KB"
            )

        with c2:

            st.metric(
                "Compressed Size",
                f"{compressed_size/1024:.2f} KB"
            )

        with c3:

            ratio = (
                compressed_size /
                original_size
            ) * 100

            st.metric(
                "Disk Ratio",
                f"{ratio:.2f}%"
            )

        with c4:

            st.metric(
                "Encoding Time",
                f"{encoding_time:.5f}s"
            )

        st.divider()

        # =====================================
        # ANALYTICS
        # =====================================

        st.subheader("📊 Compression Analytics")

        a1, a2, a3 = st.columns(3)

        with a1:

            st.metric(
                "Original Bits",
                f"{len(content)*8:,}"
            )

        with a2:

            if hasattr(
                compressor,
                "encoded_bits"
            ):
                st.metric(
                    "Encoded Bits",
                    f"{compressor.encoded_bits:,}"
                )

        with a3:

            st.metric(
                "Theoretical Ratio",
                f"{theoretical_ratio}%"
            )

        st.divider()

        # =====================================
        # DOWNLOAD
        # =====================================

        st.subheader("⬇ Download")

        with open(
            output_path,
            "rb"
        ) as f:

            st.download_button(
                label="Download Compressed File",
                data=f,
                file_name=os.path.basename(
                    output_path
                ),
                use_container_width=True
            )

        # =====================================
        # SCORE
        # =====================================

        st.subheader("🏆 Compression Score")

        if theoretical_ratio < 60:

            st.success(
                "A+ Excellent Compression"
            )

        elif theoretical_ratio < 80:

            st.info(
                "A Good Compression"
            )

        else:

            st.warning(
                "C Compression Not Efficient"
            )

        # =====================================
        # CLEANUP
        # =====================================

        try:
            os.remove(input_path)
            os.remove(output_path)

        except:
            pass