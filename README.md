# 🚀 Dynamic File Compression & Analysis Suite

A production-inspired file compression utility implementing Huffman Coding and Run Length Encoding (RLE) with benchmarking, integrity verification, reporting, visualization, multi-file compression, and performance analytics.

---

## 📌 Project Overview

Dynamic File Compression & Analysis Suite is a Data Structures and Algorithms (DSA) based project that compresses and decompresses text files using lossless compression algorithms.

The project demonstrates practical applications of:

* Huffman Coding
* Run Length Encoding (RLE)
* Min Heap
* Binary Trees
* Hash Maps
* Greedy Algorithms
* File Handling
* Data Integrity Verification

The system not only compresses files but also provides detailed analytics, benchmarking, visualization, and reporting.

---

# 🎯 Problem Statement

Large files consume storage space and increase transmission time.

This project aims to:

* Reduce file size using lossless compression
* Compare compression algorithms
* Analyze compression efficiency
* Verify decompressed file integrity
* Generate reports and visualizations

---

# ✨ Features

## Compression Features

✅ Huffman Compression

✅ Run Length Encoding (RLE)

✅ File Compression

✅ File Decompression

✅ Multi-file Compression

---

## Analysis Features

✅ Compression Ratio Calculation

✅ Algorithm Benchmarking

✅ Performance Measurement

✅ Project Statistics Dashboard

✅ Compression History Tracking

---

## Verification Features

✅ SHA-256 Integrity Verification

✅ Lossless Recovery Validation

---

## Reporting Features

✅ TXT Reports

✅ CSV Reports

✅ PDF Reports

---

## Visualization Features

✅ Character Frequency Distribution

✅ Huffman Tree Visualization

---

## User Interface

✅ Interactive Command Line Interface (CLI)

---

# 🏗️ System Architecture

Input File
↓
Read File Content
↓
Frequency Analysis
↓
Build Min Heap
↓
Construct Huffman Tree
↓
Generate Huffman Codes
↓
Compress File
↓
Store Compressed Data
↓
Decompress File
↓
Verify Integrity
↓
Generate Reports & Visualizations

---

# 📚 DSA Concepts Used

## 1. Min Heap (Priority Queue)

Used for selecting the two least frequent nodes while building the Huffman Tree.

Time Complexity:

O(log n)

---

## 2. Binary Tree

Used to construct the Huffman Tree.

Each leaf node stores a character and its frequency.

---

## 3. Hash Map (Dictionary)

Used for:

* Frequency Table
* Huffman Code Mapping
* Reverse Code Mapping

---

## 4. Greedy Algorithm

Huffman Coding is a Greedy Algorithm because it repeatedly chooses the lowest-frequency nodes to create an optimal tree.

---

## 5. Recursion

Used during Huffman code generation through tree traversal.

---

# ⚙️ Algorithms Implemented

## Huffman Coding

### Workflow

1. Count character frequencies
2. Build Min Heap
3. Construct Huffman Tree
4. Generate Binary Codes
5. Encode File
6. Compress Data
7. Decode Data
8. Recover Original File

### Advantages

* Lossless Compression
* Efficient for text data
* Optimal prefix coding

---

## Run Length Encoding (RLE)

### Example

Original:

AAAAABBBBCC

Encoded:

A5B4C2

### Advantages

* Simple implementation
* Excellent for repetitive data

### Limitations

* Poor performance on normal text

---

# 📂 Project Structure

Dynamic-File-Compression-Utility/

├── input_files/

├── compressed_files/

├── decompressed_files/

├── reports/

├── visualizations/

├── logs/

├── docs/

├── src/

├── main.py

├── requirements.txt

├── README.md

└── .gitignore

---

# 🖥️ Main Menu

1. Compress File

2. Decompress File

3. Compare Algorithms

4. Verify Integrity

5. Generate Report

6. Compress Multiple Files

7. View Compression History

8. Export PDF Report

9. Project Statistics

10. Exit

---

# 📊 Performance Results

## Huffman Compression

| Metric                 | Result   |
| ---------------------- | -------- |
| Original File Size     | 48.83 KB |
| Compressed File Size   | 25.63 KB |
| Disk Compression Ratio | 52.49%   |
| Theoretical Ratio      | 51.5%    |
| Integrity Verification | PASSED   |

---

## Benchmark Comparison

| Algorithm      | Ratio |
| -------------- | ----- |
| Huffman Coding | 51.5% |
| RLE            | 198%  |

Result:

Huffman Coding performs significantly better on normal text files.

---

# 🔐 Integrity Verification

The project verifies lossless recovery using SHA-256 hashing.

Example:

Original SHA256:
30f165fce2d3c65c0eec82f188acbe83b9f74122167d7432962921f9e6fe86c5

Recovered SHA256:
30f165fce2d3c65c0eec82f188acbe83b9f74122167d7432962921f9e6fe86c5

STATUS:
PASSED

---

# 📈 Reports Generated

The system automatically generates:

* TXT Report
* CSV Report
* PDF Report

Each report contains:

* File Information
* Compression Statistics
* Performance Metrics
* System Information
* Compression Ratio
* Integrity Status

---

# 📉 Visualizations

Generated automatically:

### Character Frequency Distribution

Displays character occurrence frequencies in the input file.

### Huffman Tree Diagram

Visual representation of the Huffman Coding Tree.

---

# 🛠️ Installation

## Clone Repository

git clone https://github.com/yourusername/Dynamic-File-Compression-Utility.git

cd Dynamic-File-Compression-Utility

---

## Install Dependencies

pip install -r requirements.txt

---

## Run Application

python main.py

---

# 📦 Requirements

matplotlib

networkx

graphviz

reportlab

psutil

---

# 🎓 Learning Outcomes

Through this project, I learned:

* Huffman Coding
* Run Length Encoding
* Priority Queues
* Min Heaps
* Binary Trees
* Hash Maps
* Greedy Algorithms
* File Compression Techniques
* Data Integrity Verification
* Data Visualization
* Performance Analysis
* Software Engineering Practices
* GitHub Project Management

---

# 💡 Future Enhancements

* LZW Compression
* Arithmetic Coding
* GUI Version using Tkinter
* Real Binary Bit Packing
* ZIP-like Archive Format
* Cloud Storage Integration
* Parallel Compression

---

# 🏆 Project Highlights

✔ Real-world DSA Application

✔ Compression & Decompression

✔ Benchmarking Framework

✔ SHA-256 Verification

✔ PDF/CSV Reporting

✔ Visualization Dashboard

✔ Multi-file Compression

✔ Interactive CLI

✔ Performance Analytics

---

# 👨‍💻 Author

Varda

B.Tech CSE (Artificial Intelligence & Machine Learning)

DSA Project – Dynamic File Compression & Analysis Suite

---

## ⭐ If you found this project useful, consider giving it a star.
