# Dynamic File Compression Suite - Quick Start Guide

## 🚀 Quick Start (30 seconds)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Choose Your Action
```
========== Dynamic Compression Suite ==========
1. Compress File          → Choose files and algorithms
2. Decompress File        → Restore compressed files  
3. Compare Algorithms     → Benchmark Huffman vs RLE
4. Verify Integrity       → Verify file integrity
5. Generate Report        → Create analysis reports
6. Exit
===============================================
```

---

## 📂 File Structure

```
Dynamic-File-Compression-Utility/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── QUICKSTART.md              # This file
├── .gitignore                 # Git ignore rules
│
├── input_files/               # Your files to compress
├── compressed_files/          # Compressed output
├── decompressed_files/        # Decompressed files
├── reports/                   # Analysis reports
├── visualizations/            # Charts & graphs
├── logs/                      # Application logs
│
└── src/
    ├── huffman.py            # Huffman compression
    ├── rle.py                # Run-length encoding
    ├── file_handler.py       # File operations
    ├── analytics.py          # Statistics & analysis
    ├── integrity.py          # SHA256 verification
    ├── benchmark.py          # Algorithm comparison
    ├── visualizer.py         # Charts & visualization
    └── cli.py                # Interactive menu
```

---

## 🔧 System Requirements

- Python 3.7+
- pip (Python package manager)
- ~50MB disk space

---

## 📊 Algorithm Comparison

| Algorithm | Ratio | Speed | Best For |
|-----------|-------|-------|----------|
| **Huffman** | 40-50% | Medium | Text files |
| **RLE** | 60-80% | Fast | Repetitive data |

---

## 🎯 Common Tasks

### Compress a File
1. Run `python main.py`
2. Press `1` for Compress
3. Select file from list
4. Choose algorithm (1 for Huffman, 2 for RLE)
5. File saved to `compressed_files/`

### Compare Algorithms
1. Run `python main.py`
2. Press `3` for Compare
3. Select test file
4. View results and charts in `visualizations/`

### Verify Integrity
1. Compress then decompress a file
2. Run `python main.py`
3. Press `4` for Verify Integrity
4. Select decompressed file
5. System verifies SHA256 hashes match

### Generate Report
1. After compression, run `python main.py`
2. Press `5` for Generate Report
3. Select file
4. Report saved to `reports/`

---

## 💡 Tips & Tricks

### Test with Sample File
- Sample file included: `input_files/sample.txt`
- Use for testing before compressing important files

### Batch Processing
- Add multiple files to `input_files/` folder
- Process them one by one through menu

### View Visualizations
- After comparing algorithms, check `visualizations/`
- Charts show performance metrics

### Check Reports
- All reports saved in `reports/` folder
- View with any text editor

---

## 🐛 Troubleshooting

**No files appear in menu?**
- Add files to `input_files/` folder

**Decompression fails?**
- Ensure file was compressed with same algorithm
- Check file isn't corrupted

**Integrity check fails?**
- File may have been altered
- Try re-compressing and decompressing

**Charts not generating?**
- Ensure matplotlib installed: `pip install matplotlib`
- Check visualizations folder for write permissions

---

## 📚 Learn More

For detailed documentation:
- Read [README.md](README.md) for full feature list
- Check source code comments in `src/`

For DSA concepts:
- Study `src/huffman.py` for tree algorithms
- Learn about min-heaps in Huffman implementation
- See binary tree traversal in decompression

---

## 🔗 Dependencies

All automatically installed with:
```bash
pip install -r requirements.txt
```

- **matplotlib**: Charts and visualization
- **networkx**: Graph algorithms for trees
- **graphviz**: Advanced tree rendering

---

## ✅ Verification

Test installation:
```bash
python -c "from src.cli import CompressionCLI; print('✓ Ready to go!')"
```

---

**Enjoy compressing! 🎉**
