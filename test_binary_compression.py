"""
Test binary compression to verify it's real binary, not text
"""

from src.huffman import HuffmanCoding
from src.file_handler import FileHandler
from src.integrity import IntegrityVerifier
import os

def test_binary_compression():
    fh = FileHandler()
    huffman = HuffmanCoding()

    # Test with big.txt
    input_file = fh.get_input_file_path('big.txt')
    compressed_file = 'test_binary_check.huff'

    print('='*70)
    print('TESTING BINARY COMPRESSION')
    print('='*70)

    print('\nCompressing with big.txt (50 KB)...')
    huffman.compress_file(input_file, compressed_file)

    orig_size = fh.get_file_size(input_file)
    comp_size = fh.get_file_size(compressed_file)
    ratio = fh.get_compression_ratio(orig_size, comp_size)

    print(f'\n✓ Compression Complete:')
    print(f'  Original Size: {fh.get_file_size_kb(input_file)} KB')
    print(f'  Compressed Size: {fh.get_file_size_kb(compressed_file)} KB')
    print(f'  Compression Ratio: {ratio}%')

    # Check if file is binary
    print(f'\n✓ Binary Format Check:')
    with open(compressed_file, 'rb') as f:
        first_bytes = f.read(50)
        # Check for null bytes or high bytes (signs of binary data)
        has_null = b'\x00' in first_bytes
        high_bytes = sum(1 for b in first_bytes if b > 127)
        is_likely_binary = has_null or high_bytes > 5
        
        print(f'  Contains null bytes: {has_null}')
        print(f'  High bytes (>127): {high_bytes}')
        print(f'  Appears to be binary: {is_likely_binary}')
        print(f'  First 30 bytes (hex): {first_bytes[:30].hex()}')

    # Verify decompression works
    decompressed = 'test_binary_check.txt'
    print(f'\nDecompressing...')
    huffman.decompress_file(compressed_file, decompressed)
    print(f'✓ Decompression successful')

    # Verify integrity
    verifier = IntegrityVerifier()
    is_valid = verifier.verify_integrity(input_file, decompressed)
    print(f'✓ Hash verification: {"PASSED" if is_valid else "FAILED"}')
    
    if is_valid:
        print(f'  Original hash: {verifier.original_hash[:32]}...')
        print(f'  Recovered hash: {verifier.recovered_hash[:32]}...')

    # Cleanup
    os.remove(compressed_file)
    os.remove(decompressed)

    print('\n' + '='*70)
    print('✅ BINARY COMPRESSION TEST COMPLETE')
    print('='*70)

if __name__ == '__main__':
    test_binary_compression()
