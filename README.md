# 🚀 Dynamic File Compression & Analysis Suite

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![DSA](https://img.shields.io/badge/Data%20Structures%20%26%20Algorithms-Project-green)
![Compression](https://img.shields.io/badge/Compression-Huffman%20%7C%20RLE-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

> A production-inspired file compression utility implementing Huffman Coding and Run Length Encoding (RLE) with benchmarking, integrity verification, visualization, reporting, multi-file compression, and performance analytics.

---

## 📌 Project Overview

Dynamic File Compression & Analysis Suite is a Data Structures and Algorithms (DSA) based project that compresses and decompresses text files using lossless compression algorithms.

The project demonstrates practical applications of:

* Huffman Coding
* Run Length Encoding (RLE)
* Min Heap (Priority Queue)
* Binary Trees
* Hash Maps (Dictionaries)
* Greedy Algorithms
* File Handling
* SHA-256 Integrity Verification
* Data Visualization
* Performance Analysis

---

# 🎯 Problem Statement

Large files consume storage space and increase transmission time.

This project aims to:

* Reduce file size using lossless compression
* Compare multiple compression algorithms
* Analyze compression efficiency
* Verify decompressed file integrity
* Generate reports and visualizations
* Demonstrate real-world DSA applications

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

# 🏅 Key Achievements

* Achieved **52.49% compression** on large text datasets
* Implemented **lossless file recovery**
* Added **SHA-256 integrity verification**
* Generated **TXT, CSV, and PDF reports**
* Built **frequency distribution visualization**
* Built **Huffman tree visualization**
* Implemented **multi-file compression**
* Developed **algorithm benchmarking framework**
* Added **compression history tracking**
* Created **project analytics dashboard**

---

# 🏗️ System Architecture

```text
Input File
     │
     ▼
Read File Content
     │
     ▼
Frequency Analysis
     │
     ▼
Build Min Heap
     │
     ▼
Construct Huffman Tree
     │
     ▼
Generate Huffman Codes
     │
     ▼
Compress File
     │
     ▼
Store Compressed Data
     │
     ▼
Decompress File
     │
     ▼
Verify Integrity
     │
     ▼
Generate Reports & Visualizations
```

---

# 📚 DSA Concepts Used

## 1. Min Heap (Priority Queue)

Used for selecting the two least frequent nodes while building the Huffman Tree.

**Time Complexity:** O(log n)

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

Huffman Coding repeatedly chooses the lowest-frequency nodes to create an optimal tree.

---

## 5. Recursion

Used during Huffman Tree traversal and code generation.

---

# ⚙️ Algorithms Implemented

## Huffman Coding

### Workflow

1. Count Character Frequencies
2. Build Min Heap
3. Construct Huffman Tree
4. Generate Binary Codes
5. Encode File
6. Compress Data
7. Decode Data
8. Recover Original File

### Advantages

* Lossless Compression
* Efficient for Text Data
* Optimal Prefix Coding

---

## Run Length Encoding (RLE)

### Example

Original:

```text
AAAAABBBBCC
```

Encoded:

```text
A5B4C2
```

### Advantages

* Simple Implementation
* Excellent for Repetitive Data

### Limitations

* Poor Performance on Normal Text

---

# 📂 Project Structure

```text
Dynamic-File-Compression-Analysis-Suite/

├── input_files/
├── compressed_files/
├── decompressed_files/
├── reports/
├── visualizations/
├── logs/
├── docs/
├── src/
├── images/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🖥️ Main Menu

```text
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
```

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

## Algorithm Comparison

| Algorithm      | Ratio |
| -------------- | ----- |
| Huffman Coding | 51.5% |
| RLE            | 198%  |

### Conclusion

Huffman Coding performs significantly better on normal text datasets, while RLE performs best on highly repetitive data.

---

# 🔐 Integrity Verification

The project verifies lossless recovery using SHA-256 hashing.

Example:

```text
Original SHA256:
30f165fce2d3c65c0eec82f188acbe83b9f74122167d7432962921f9e6fe86c5

Recovered SHA256:
30f165fce2d3c65c0eec82f188acbe83b9f74122167d7432962921f9e6fe86c5

STATUS:
PASSED
```

---

# 📈 Reports Generated

The system automatically generates:

* TXT Reports
* CSV Reports
* PDF Reports

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

Displays frequency of characters in the input file.

### Huffman Tree Diagram

Visual representation of the Huffman Coding tree.

---

# 📸 Screenshots

## Main Menu

![Main Menu](images/screenshots/Main%20Menu.png)

## Compression Results

![Compression](images/screenshots/Compression%20of%20big.txt.png)

## Integrity Verification

![Integrity](images/screenshots/Integrity%20Verification.png)

## Algorithm Comparison

![Benchmark](images/screenshots/Algorithm%20Comparison.png)

## Compression History

![History](images/screenshots/Compression%20History.png)

## Project Statistics

![Statistics](images/screenshots//Project%20Statistics.png)

## Character Frequency Distribution

![Frequency](images/screenshots/Frequency%20Distribution%20Graph.png)

## Huffman Tree Visualization

![Tree](images/screenshots/Huffman%20Tree.png)

---

# 🛠️ Installation

## Clone Repository

```bash
git clone https://github.com/varda24/Dynamic-File-Compression-Analysis-Suite.git

cd Dynamic-File-Compression-Analysis-Suite
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python main.py
```

---

# 📦 Requirements

```text
matplotlib
networkx
graphviz
reportlab
psutil
```

---

# 💼 Skills Demonstrated

* Data Structures & Algorithms
* Huffman Coding
* Run Length Encoding
* Priority Queues
* Min Heaps
* Binary Trees
* Hash Maps
* Greedy Algorithms
* File Handling
* Data Visualization
* Performance Analysis
* Report Generation
* Software Engineering
* System Design Fundamentals

---

# 💡 Future Enhancements

* Binary Bit Packing
* LZW Compression
* Arithmetic Coding
* Archive Encryption
* Parallel Compression
* Web Dashboard
* Cloud Storage Integration

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

**Varda**

B.Tech CSE (Artificial Intelligence & Machine Learning)

Dynamic File Compression & Analysis Suite

---

## ⭐ If you found this project useful, consider giving it a star.
