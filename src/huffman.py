import heapq
import os
from collections import Counter
import pickle
import time


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:

    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        self.encoding_time = 0
        self.decoding_time = 0
        self.original_bits = 0
        self.encoded_bits = 0
        self.theoretical_ratio = 0
        self.root = None

    def build_frequency_table(self, text):
        return Counter(text)

    def build_heap(self, frequency):
        heap = []

        for char, freq in frequency.items():
            heapq.heappush(heap, Node(char, freq))

        return heap

    def build_huffman_tree(self, heap):

        while len(heap) > 1:

            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(None, left.freq + right.freq)

            merged.left = left
            merged.right = right

            heapq.heappush(heap, merged)

        return heap[0] if heap else None

    def generate_codes(self, root, current_code=""):

        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code if current_code else "0"
            self.reverse_codes[current_code if current_code else "0"] = root.char
            return

        self.generate_codes(root.left, current_code + "0")
        self.generate_codes(root.right, current_code + "1")

    def compress_text(self, text):

        encoded_text = ""

        for char in text:
            encoded_text += self.codes[char]

        return encoded_text

    def decompress_text(self, encoded_text):

        current_code = ""
        decoded_text = ""

        for bit in encoded_text:

            current_code += bit

            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""

        return decoded_text

    def compression_ratio(self, text, encoded_text):

        original_bits = len(text) * 8
        compressed_bits = len(encoded_text)

        if original_bits == 0:
            return 0

        ratio = (compressed_bits / original_bits) * 100

        return ratio

    def pad_encoded_text(self, encoded_text):
        """Pad encoded bits and prefix the padding length as one byte."""
        extra_padding = 8 - (len(encoded_text) % 8)
        if extra_padding == 8:
            extra_padding = 0

        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)

        return padded_info + encoded_text

    def get_byte_array(self, padded_encoded_text):
        """Convert a padded bit string into a bytearray."""
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("Invalid padding")

        byte_array = bytearray()

        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            byte_array.append(int(byte, 2))

        return byte_array

    def remove_padding(self, padded_text):
        """Remove the leading padding byte and trailing padding bits."""
        padded_info = padded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_text = padded_text[8:]

        if extra_padding:
            return padded_text[:-extra_padding]

        return padded_text

    def compress_file(self, input_path, output_path):

        with open(input_path, "r", encoding="utf-8") as file:
            text = file.read()

        start_time = time.perf_counter()

        self.codes = {}
        self.reverse_codes = {}
        frequency = self.build_frequency_table(text)
        heap = self.build_heap(frequency)
        self.root = self.build_huffman_tree(heap)
        self.generate_codes(self.root)
        encoded_text = self.compress_text(text)

        self.encoding_time = time.perf_counter() - start_time

        # Track theoretical compression (bit-level)
        self.original_bits = len(text) * 8
        self.encoded_bits = len(encoded_text)
        self.theoretical_ratio = (
            round((self.encoded_bits / self.original_bits) * 100, 2)
            if self.original_bits
            else 0
        )

        padded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_text)

        # Get original filename for metadata tracking
        import os
        original_filename = os.path.basename(input_path)

        metadata = {
            "format_version": 2,
            "algorithm": "huffman",
            "original_filename": original_filename,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": {
                "original_bits": self.original_bits,
                "encoded_bits": self.encoded_bits,
                "theoretical_ratio": self.theoretical_ratio,
            },
            "payload": {
                "data": bytes(byte_array),
                "codes": self.codes,
            },
        }

        # Save compressed data and metadata in a self-describing binary payload.
        with open(output_path, "wb") as file:
            pickle.dump(metadata, file)

        return self.encoding_time

    def decompress_file(self, input_path, output_path):

        start_time = time.perf_counter()

        with open(input_path, "rb") as file:
            data = pickle.load(file)
            if isinstance(data, dict):
                if data.get("algorithm") != "huffman":
                    raise ValueError(
                        f"File uses {data.get('algorithm')} compression, not Huffman"
                    )
                payload = data["payload"]
                byte_array = payload["data"]
                self.codes = payload["codes"]
                padding = payload.get("padding")
            else:
                # Backward compatibility with legacy tuple payloads.
                if len(data) == 4:
                    byte_array, self.codes, padding, _original_filename = data
                else:
                    byte_array, self.codes, padding = data

        # Build reverse codes
        self.reverse_codes = {v: k for k, v in self.codes.items()}

        # Convert bytes to bit string
        bit_string = ""
        for byte in byte_array:
            bit_string += format(byte, '08b')

        if padding is None:
            bit_string = self.remove_padding(bit_string)
        else:
            # Backward compatibility with older files that stored padding separately.
            bit_string = bit_string[:-padding] if padding else bit_string

        decoded_text = self.decompress_text(bit_string)

        self.decoding_time = time.perf_counter() - start_time

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(decoded_text)

        return self.decoding_time
