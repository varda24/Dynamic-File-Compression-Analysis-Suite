import os
import shutil
from pathlib import Path


class FileHandler:
    """Handle file operations for compression utility"""

    def __init__(self):
        self.input_dir = "input_files"
        self.compressed_dir = "compressed_files"
        self.decompressed_dir = "decompressed_files"
        self.reports_dir = "reports"
        self.visualizations_dir = "visualizations"
        self.logs_dir = "logs"

        self._create_directories()

    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        dirs = [
            self.input_dir,
            self.compressed_dir,
            self.decompressed_dir,
            self.reports_dir,
            self.visualizations_dir,
            self.logs_dir
        ]

        for dir_path in dirs:
            Path(dir_path).mkdir(exist_ok=True)

    def get_file_size(self, file_path):
        """Get file size in bytes"""
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0

    def get_file_size_kb(self, file_path):
        """Get file size in KB"""
        return round(self.get_file_size(file_path) / 1024, 2)

    def get_file_size_mb(self, file_path):
        """Get file size in MB"""
        return round(self.get_file_size(file_path) / (1024 * 1024), 2)

    def get_space_saved(self, original_size, compressed_size):
        """Calculate space saved"""
        return round(original_size - compressed_size, 2)

    def get_compression_ratio(self, original_size, compressed_size):
        """Calculate compression ratio as percentage"""
        if original_size == 0:
            return 0
        return round((compressed_size / original_size) * 100, 2)

    def list_input_files(self):
        """List all files in input directory"""
        if not os.path.exists(self.input_dir):
            return []
        return [f for f in os.listdir(self.input_dir) if os.path.isfile(os.path.join(self.input_dir, f))]

    def list_compressed_files(self):
        """List all files in compressed directory"""
        if not os.path.exists(self.compressed_dir):
            return []
        return [f for f in os.listdir(self.compressed_dir) if os.path.isfile(os.path.join(self.compressed_dir, f))]

    def get_input_file_path(self, filename):
        """Get full path for input file"""
        return os.path.join(self.input_dir, filename)

    def get_compressed_file_path(self, filename):
        """Get full path for compressed file"""
        return os.path.join(self.compressed_dir, filename + ".huff")

    def get_algorithm_compressed_file_path(self, filename, algorithm):
        """Get compressed path using an algorithm-specific filename."""
        base_name = os.path.splitext(filename)[0]
        algorithm_name = algorithm.lower()
        return os.path.join(self.compressed_dir, f"{base_name}_{algorithm_name}.huff")

    def find_compressed_versions(self, filename):
        """Find compressed files that belong to an input filename."""
        base_name = os.path.splitext(filename)[0]
        candidates = [
            self.get_algorithm_compressed_file_path(filename, "huffman"),
            self.get_algorithm_compressed_file_path(filename, "rle"),
            self.get_compressed_file_path(filename),
        ]
        return [path for path in candidates if os.path.exists(path)]

    def get_decompressed_file_path(self, filename):
        """Get full path for decompressed file"""
        return os.path.join(self.decompressed_dir, filename)

    def get_report_path(self, filename="report.txt"):
        """Get full path for report file"""
        return os.path.join(self.reports_dir, filename)

    def get_visualization_path(self, filename):
        """Get full path for visualization file"""
        return os.path.join(self.visualizations_dir, filename)

    def get_log_path(self, filename="compression.log"):
        """Get full path for log file"""
        return os.path.join(self.logs_dir, filename)

    def file_exists(self, file_path):
        """Check if file exists"""
        return os.path.exists(file_path)

    def delete_file(self, file_path):
        """Delete a file"""
        if os.path.exists(file_path):
            os.remove(file_path)

    def clear_directory(self, dir_path):
        """Clear all files in a directory"""
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
