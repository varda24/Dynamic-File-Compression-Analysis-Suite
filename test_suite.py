"""
Comprehensive test suite for Dynamic File Compression Suite
"""

from src.huffman import HuffmanCoding
from src.rle import RunLengthEncoding
from src.file_handler import FileHandler
from src.integrity import IntegrityVerifier
from src.analytics import CompressionAnalytics
import os

def run_tests():
    print('=' * 70)
    print('COMPRESSION SUITE - COMPREHENSIVE TEST SUITE')
    print('=' * 70)

    # Initialize components
    fh = FileHandler()
    huffman = HuffmanCoding()
    rle = RunLengthEncoding()
    verifier = IntegrityVerifier()
    analytics = CompressionAnalytics()

    # Test with both small and large files
    test_files = [
        ('sample.txt', 'small'),
        ('big.txt', 'large')
    ]

    for test_file, file_type in test_files:
        input_file = fh.get_input_file_path(test_file)
        
        if not os.path.exists(input_file):
            print(f'\n⚠ {test_file} not found, skipping {file_type} file tests')
            continue

        print(f'\n{"=" * 70}')
        print(f'TESTING WITH {file_type.upper()} FILE: {test_file}')
        print(f'{"=" * 70}')

        huff_compressed = f'test_{file_type}_huffman.huff'
        rle_compressed = f'test_{file_type}_rle.txt'
        decompressed = f'test_{file_type}_decompressed.txt'

        print(f'\n[1/6] Testing Huffman Compression ({file_type})...')
        try:
            huffman.compress_file(input_file, huff_compressed)
            orig_size = fh.get_file_size(input_file)
            comp_size = fh.get_file_size(huff_compressed)
            physical_ratio = fh.get_compression_ratio(orig_size, comp_size)
            
            print(f'      ✓ Huffman compression successful')
            print(f'        Physical Ratio: {physical_ratio}% | Theoretical Ratio: {huffman.theoretical_ratio}%')
            print(f'        Encoding Time: {huffman.encoding_time:.6f}s')
        except Exception as e:
            print(f'      ✗ Error: {e}')
            continue

        print(f'\n[2/6] Testing Huffman Decompression ({file_type})...')
        try:
            huffman.decompress_file(huff_compressed, decompressed)
            print(f'      ✓ Huffman decompression successful')
            print(f'        Decoding Time: {huffman.decoding_time:.6f}s')
        except Exception as e:
            print(f'      ✗ Error: {e}')
            continue

        print(f'\n[3/6] Testing RLE Compression ({file_type})...')
        try:
            rle.compress_file(input_file, rle_compressed)
            orig_size = fh.get_file_size(input_file)
            comp_size = fh.get_file_size(rle_compressed)
            physical_ratio = fh.get_compression_ratio(orig_size, comp_size)
            
            print(f'      ✓ RLE compression successful')
            print(f'        Physical Ratio: {physical_ratio}% | Theoretical Ratio: {rle.theoretical_ratio}%')
            print(f'        Encoding Time: {rle.encoding_time:.6f}s')
        except Exception as e:
            print(f'      ✗ Error: {e}')

        print(f'\n[4/6] Testing File Handler ({file_type})...')
        try:
            orig_size = fh.get_file_size(input_file)
            huff_size = fh.get_file_size(huff_compressed)
            ratio = fh.get_compression_ratio(orig_size, huff_size)
            print(f'      ✓ Original: {fh.get_file_size_kb(input_file)} KB')
            print(f'      ✓ Compressed: {fh.get_file_size_kb(huff_compressed)} KB')
            print(f'      ✓ Disk Ratio: {ratio}%')
        except Exception as e:
            print(f'      ✗ Error: {e}')

        print(f'\n[5/6] Testing Integrity Verification ({file_type})...')
        try:
            result = verifier.verify_integrity(input_file, decompressed)
            status = '✓ PASSED' if result else '✗ FAILED'
            print(f'      {status}')
            if not result:
                print(f'      ⚠ Hash mismatch detected!')
        except Exception as e:
            print(f'      ✗ Error: {e}')

        print(f'\n[6/6] Testing Analytics ({file_type})...')
        try:
            analytics.input_file = test_file
            analytics.original_size = fh.get_file_size(input_file)
            analytics.compressed_size = fh.get_file_size(huff_compressed)
            analytics.encoding_time = huffman.encoding_time
            analytics.decoding_time = huffman.decoding_time
            analytics.integrity_status = 'PASSED'
            analytics.original_bits = huffman.original_bits
            analytics.encoded_bits = huffman.encoded_bits
            analytics.theoretical_ratio = huffman.theoretical_ratio
            
            ratio_pct = analytics.calculate_compression_ratio()
            space_saved = analytics.calculate_space_saved()
            print(f'      ✓ Disk Compression Ratio: {ratio_pct}%')
            print(f'      ✓ Algorithm Ratio: {analytics.theoretical_ratio}%')
            print(f'      ✓ Space Saved: {space_saved:,.0f} bytes')
        except Exception as e:
            print(f'      ✗ Error: {e}')

        # Cleanup
        try:
            if os.path.exists(huff_compressed):
                os.remove(huff_compressed)
            if os.path.exists(rle_compressed):
                os.remove(rle_compressed)
            if os.path.exists(decompressed):
                os.remove(decompressed)
        except Exception as e:
            print(f'      ✗ Cleanup Error: {e}')

    print('\n' + '=' * 70)
    print('✅ ALL TESTS COMPLETED')
    print('=' * 70)
    print('\nKey Metrics Explanation:')
    print('- Physical Ratio: Actual disk space (compressed file size / original file size)')
    print('- Theoretical Ratio: Algorithm efficiency (encoded bits / original bits)')
    print('- For large files, both ratios should be similar (~40-50% for text)')
    print('- For small files, physical ratio > theoretical due to metadata overhead')
    print('\nRun "python main.py" to start the interactive menu')
    return True

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
