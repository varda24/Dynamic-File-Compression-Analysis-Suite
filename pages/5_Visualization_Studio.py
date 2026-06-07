import streamlit as st
import tempfile
import os
from PIL import Image

from src.visualizer import Visualizer
from src.huffman import HuffmanCoding

st.set_page_config(
    page_title="Visualization Studio",
    page_icon="🌳",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.visual-card{
    background:rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    border:1px solid rgba(255,255,255,0.08);
}

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

</style>
""", unsafe_allow_html=True)

# =====================================
# HERO
# =====================================

st.markdown("""
<div class="hero">

<h1>🌳 Visualization Studio</h1>

<h4>
Explore Compression Intelligence Through Visual Analytics
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
        "🚀 Generate Visualizations",
        use_container_width=True
    ):

        with st.spinner(
            "Generating charts..."
        ):

            os.makedirs(
                "visualizations",
                exist_ok=True
            )

            visualizer = Visualizer()

            # =====================================
            # FREQUENCY GRAPH
            # =====================================

            frequency_path = (
                "visualizations/"
                "frequency_distribution.png"
            )

            visualizer.plot_frequency_distribution(
                text,
                frequency_path
            )

            # =====================================
            # HUFFMAN TREE
            # =====================================

            huffman = HuffmanCoding()

            frequency = (
                huffman.build_frequency_table(text)
            )

            heap = (
                huffman.build_heap(frequency)
            )

            root = (
                huffman.build_huffman_tree(heap)
            )

            tree_path = (
                "visualizations/"
                "huffman_tree.png"
            )

            visualizer.plot_huffman_tree(
                root,
                tree_path
            )

        st.success(
            "Visualizations Generated Successfully"
        )

        # =====================================
        # IMAGE DISPLAY
        # =====================================

        st.subheader(
            "📊 Generated Visualizations"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### Character Frequency Distribution"
            )

            st.image(
                frequency_path,
                use_container_width=True
            )

        with col2:

            st.markdown(
                "### Huffman Tree Structure"
            )

            st.image(
                tree_path,
                use_container_width=True
            )

        st.divider()

        # =====================================
        # DOWNLOADS
        # =====================================

        st.subheader(
            "⬇ Export Visualizations"
        )

        c1, c2 = st.columns(2)

        with c1:

            with open(
                frequency_path,
                "rb"
            ) as f:

                st.download_button(
                    "Download Frequency Graph",
                    f,
                    file_name=
                    "frequency_distribution.png",
                    use_container_width=True
                )

        with c2:

            with open(
                tree_path,
                "rb"
            ) as f:

                st.download_button(
                    "Download Huffman Tree",
                    f,
                    file_name=
                    "huffman_tree.png",
                    use_container_width=True
                )

        # =====================================
        # INSIGHTS
        # =====================================

        st.subheader(
            "🧠 Visualization Insights"
        )

        unique_chars = len(set(text))

        st.info(f"""
📌 Dataset Statistics

• Total Characters: {len(text):,}

• Unique Characters: {unique_chars}

• Visualization Type:
Character Frequency Distribution

• Compression Model:
Huffman Coding

• Tree Generated:
Successfully
""")

else:

    st.info("""
Upload a text file to generate:

✅ Character Frequency Distribution

✅ Huffman Tree Diagram

✅ Downloadable PNG Visualizations
""")