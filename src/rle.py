import time
import os
import pickle


class RunLengthEncoding:
    """Run Length Encoding compression algorithm"""

    def __init__(self):
        self.encoding_time = 0
        self.decoding_time = 0
        self.original_bits = 0
        self.encoded_bits = 0
        self.theoretical_ratio = 0

    def compress_text(self, text):
        """Compress text using RLE"""
        if not text:
            return ""

        start_time = time.perf_counter()
        compressed = []

        i = 0
        while i < len(text):
            char = text[i]
            count = 1

            while i + count < len(text) and text[i + count] == char:
                count += 1

            compressed.append(f"{char}{count}")
            i += count

        self.encoding_time = time.perf_counter() - start_time
        return "".join(compressed)

    def decompress_text(self, encoded_text):
        """Decompress RLE encoded text"""
        start_time = time.perf_counter()
        decompressed = []

        i = 0
        while i < len(encoded_text):
            char = encoded_text[i]
            count = ""
            i += 1

            while i < len(encoded_text) and encoded_text[i].isdigit():
                count += encoded_text[i]
                i += 1

            decompressed.append(char * int(count))

        self.decoding_time = time.perf_counter() - start_time
        return "".join(decompressed)

    def compression_ratio(self, original, compressed):
        """Calculate compression ratio"""
        if len(original) == 0:
            return 0
        return (len(compressed) / len(original)) * 100

    def compress_file(self, input_path, output_path):
        """Compress file using RLE"""
        with open(input_path, "r", encoding="utf-8") as file:
            text = file.read()

        compressed = self.compress_text(text)

        # Track theoretical compression
        self.original_bits = len(text) * 8
        self.encoded_bits = len(compressed) * 8
        self.theoretical_ratio = (
            round((self.encoded_bits / self.original_bits) * 100, 2)
            if self.original_bits
            else 0
        )

        # Store with original filename metadata
        original_filename = os.path.basename(input_path)
        metadata = {
            "format_version": 2,
            "algorithm": "rle",
            "original_filename": original_filename,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": {
                "original_bits": self.original_bits,
                "encoded_bits": self.encoded_bits,
                "theoretical_ratio": self.theoretical_ratio,
            },
            "payload": {
                "data": compressed,
            },
        }
        
        with open(output_path, "wb") as file:
            pickle.dump(metadata, file)

        return self.encoding_time

    def decompress_file(self, input_path, output_path):
        """Decompress RLE file"""
        with open(input_path, "rb") as file:
            data = pickle.load(file)
            if isinstance(data, dict):
                if data.get("algorithm") != "rle":
                    raise ValueError(
                        f"File uses {data.get('algorithm')} compression, not RLE"
                    )
                compressed = data["payload"]["data"]
            elif isinstance(data, tuple):
                # Backward compatibility with legacy tuple payloads.
                compressed, _original_filename = data
            else:
                compressed = data

        decompressed = self.decompress_text(compressed)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(decompressed)

        return self.decoding_time
