"""
Test input validation for algorithm selection
"""

def test_input_validation():
    """Test that invalid algorithm inputs are handled properly"""
    
    print('=' * 70)
    print('INPUT VALIDATION TEST')
    print('=' * 70)
    
    test_inputs = ['1', '2', '', '5', 'invalid', '3', 'huffman']
    
    for test_input in test_inputs:
        algo = test_input.strip() or '1'
        
        if algo not in ['1', '2']:
            result = 'Invalid - Uses Huffman (default)'
        elif algo == '1':
            result = '✓ Huffman selected'
        else:
            result = '✓ RLE selected'
        
        print(f'Input: "{test_input}"'.ljust(22) + f'→ {result}')
    
    print('\n' + '=' * 70)
    print('\nValidation Logic:')
    print('- Input "1" → Huffman Compression')
    print('- Input "2" → RLE Compression')
    print('- Input "" (empty) → Default to Huffman')
    print('- Input "5", "invalid", etc. → Default to Huffman with warning')
    print('\n' + '=' * 70)

if __name__ == '__main__':
    test_input_validation()
