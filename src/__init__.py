"""
Dynamic File Compression & Analysis Suite - Source Package
"""

__version__ = "1.0.0"
__author__ = "Compression Suite"
__description__ = "A production-inspired compression utility with multiple algorithms"

from src.huffman import HuffmanCoding
from src.rle import RunLengthEncoding
from src.file_handler import FileHandler
from src.analytics import CompressionAnalytics
from src.integrity import IntegrityVerifier
from src.benchmark import Benchmark
from src.visualizer import Visualizer
from src.cli import CompressionCLI

__all__ = [
    'HuffmanCoding',
    'RunLengthEncoding',
    'FileHandler',
    'CompressionAnalytics',
    'IntegrityVerifier',
    'Benchmark',
    'Visualizer',
    'CompressionCLI'
]
