from src.huffman import HuffmanCoding
from src.rle import RunLengthEncoding
import time
import tempfile
import os


class Benchmark:
    """Benchmark compression algorithms"""

    def __init__(self):
        self.results = {}

    def benchmark_huffman(self, input_file):
        """Benchmark Huffman compression"""
        huffman = HuffmanCoding()

        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()

        original_size = len(original_text)

        # Compress
        start = time.perf_counter()
        frequency = huffman.build_frequency_table(original_text)
        heap = huffman.build_heap(frequency)
        root = huffman.build_huffman_tree(heap)
        huffman.generate_codes(root)
        encoded_text = huffman.compress_text(original_text)
        encoding_time = time.perf_counter() - start

        # Add padding
        padding = 8 - (len(encoded_text) % 8)
        bit_string = encoded_text + "0" * padding

        # Convert to bytes
        byte_count = len(bit_string) // 8
        compressed_size = byte_count

        # Decompress
        start = time.perf_counter()
        huffman.decompress_text(bit_string[:-padding] if padding else bit_string)
        decoding_time = time.perf_counter() - start

        compression_ratio = (compressed_size / original_size) * 100

        self.results['Huffman'] = {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'ratio': round(compression_ratio, 2),
            'encoding_time': round(encoding_time, 6),
            'decoding_time': round(decoding_time, 6)
        }

        return self.results['Huffman']

    def benchmark_rle(self, input_file):
        """Benchmark RLE compression"""
        rle = RunLengthEncoding()

        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()

        original_size = len(original_text)

        # Compress
        start = time.perf_counter()
        compressed_text = rle.compress_text(original_text)
        encoding_time = time.perf_counter() - start

        compressed_size = len(compressed_text)

        # Decompress
        start = time.perf_counter()
        rle.decompress_text(compressed_text)
        decoding_time = time.perf_counter() - start

        compression_ratio = (compressed_size / original_size) * 100

        self.results['RLE'] = {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'ratio': round(compression_ratio, 2),
            'encoding_time': round(encoding_time, 6),
            'decoding_time': round(decoding_time, 6)
        }

        return self.results['RLE']

    def compare_algorithms(self, input_file):
        """Compare both algorithms"""
        huff_result = self.benchmark_huffman(input_file)
        rle_result = self.benchmark_rle(input_file)

        return {
            'Huffman': huff_result,
            'RLE': rle_result
        }

    def get_comparison_report(self):
        """Get comparison report"""
        report = "\n========== Algorithm Comparison ==========\n"
        report += f"{'Algorithm':<15} {'Ratio':<10} {'Enc Time':<12} {'Dec Time':<12}\n"
        report += "-" * 50 + "\n"

        for algorithm, data in self.results.items():
            report += f"{algorithm:<15} {data['ratio']:<10}% {data['encoding_time']:<12.6f}s {data['decoding_time']:<12.6f}s\n"

        report += "==========================================\n"
        return report

    def print_comparison(self):
        """Print comparison report"""
        print(self.get_comparison_report())

    def get_best_algorithm(self):
        """Get best algorithm based on compression ratio"""
        if not self.results:
            return None

        best = min(self.results.items(), key=lambda x: x[1]['ratio'])
        return best
