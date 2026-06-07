import csv
import os
import platform
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    canvas = None
    letter = None


class CompressionAnalytics:
    """Analyze and report compression statistics"""

    def __init__(self):
        self.original_size = 0
        self.compressed_size = 0
        self.encoding_time = 0
        self.decoding_time = 0
        self.algorithm = "Huffman"
        self.integrity_status = "UNKNOWN"
        self.input_file = ""
        self.compression_ratio = 0
        self.original_bits = 0
        self.encoded_bits = 0
        self.theoretical_ratio = 0
        self.timestamp = datetime.now()

    def calculate_compression_ratio(self):
        """Calculate compression ratio"""
        if self.original_size == 0:
            self.compression_ratio = 0
            return 0

        self.compression_ratio = round((self.compressed_size / self.original_size) * 100, 2)
        return self.compression_ratio

    def calculate_space_saved(self):
        """Calculate space saved"""
        return round(self.original_size - self.compressed_size, 2)

    def get_analytics_report(self):
        """Generate analytics report"""
        space_saved = self.calculate_space_saved()
        ratio = self.calculate_compression_ratio()
        system_info = self.get_system_info()
        
        # Build compression metrics section
        metrics = f"""
Original Bits: {self.original_bits}

Encoded Bits: {self.encoded_bits}

Theoretical Ratio: {self.theoretical_ratio}%""" if self.original_bits > 0 else ""

        report = f"""
============= Compression Report =============

Input File:
{self.input_file}

Original Size:
{self._format_size(self.original_size)}

Compressed Size:
{self._format_size(self.compressed_size)}

Space Saved:
{self._format_size(space_saved)}

Disk Compression Ratio:
{ratio}%
{metrics}

Encoding Time:
{self.encoding_time:.6f} sec

Decoding Time:
{self.decoding_time:.6f} sec

Algorithm:
{self.algorithm}

Integrity Check:
{self.integrity_status}

System Information:
OS: {system_info['os']}
CPU Cores: {system_info['cpu_cores']}
RAM: {system_info['ram']}

Timestamp:
{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

==============================================
"""
        return report

    def get_summary(self):
        """Get summary analytics"""
        space_saved = self.calculate_space_saved()
        ratio = self.calculate_compression_ratio()

        summary = {
            'input_file': self.input_file,
            'original_size': self._format_size(self.original_size),
            'compressed_size': self._format_size(self.compressed_size),
            'space_saved': self._format_size(space_saved),
            'compression_ratio': f"{ratio}%",
            'encoding_time': f"{self.encoding_time:.6f} sec",
            'decoding_time': f"{self.decoding_time:.6f} sec",
            'algorithm': self.algorithm,
            'integrity_status': self.integrity_status,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

        return summary

    def get_system_info(self):
        """Get basic system information for reports"""
        ram = "Unavailable"
        if psutil is not None:
            ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            ram = f"{ram_gb:.2f} GB"

        return {
            "os": f"{platform.system()} {platform.release()}",
            "cpu_cores": os.cpu_count() or "Unavailable",
            "ram": ram,
        }

    def to_csv_row(self):
        """Return analytics values as a CSV-friendly dictionary"""
        ratio = self.calculate_compression_ratio()
        return {
            "Date": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "File": self.input_file,
            "Algorithm": self.algorithm,
            "Original": self.original_size,
            "Compressed": self.compressed_size,
            "Ratio": ratio,
            "OriginalBits": self.original_bits,
            "EncodedBits": self.encoded_bits,
            "TheoreticalRatio": self.theoretical_ratio,
            "EncodingTime": f"{self.encoding_time:.6f}",
            "DecodingTime": f"{self.decoding_time:.6f}",
            "Integrity": self.integrity_status,
        }

    def _format_size(self, bytes_size):
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"

    def save_report(self, file_path):
        """Save analytics report to file"""
        with open(file_path, 'w') as f:
            f.write(self.get_analytics_report())

    def save_csv_report(self, file_path):
        """Save analytics report as CSV"""
        row = self.to_csv_row()
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writeheader()
            writer.writerow(row)

    def save_pdf_report(self, file_path):
        """Save analytics report as a PDF."""
        if canvas is None:
            raise RuntimeError("ReportLab is required for PDF export")

        pdf = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        y = height - 50

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Dynamic File Compression & Analysis Suite")
        y -= 28

        pdf.setFont("Helvetica", 10)
        for line in self.get_analytics_report().splitlines():
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50

            pdf.drawString(50, y, line[:100])
            y -= 14

        pdf.save()

    def append_history(self, file_path):
        """Append the current compression run to history CSV"""
        row = self.to_csv_row()
        fieldnames = [
            "Date",
            "File",
            "Algorithm",
            "Original",
            "Compressed",
            "Ratio",
            "EncodingTime",
        ]
        file_exists = os.path.exists(file_path)

        if file_exists:
            with open(file_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                existing_rows = list(reader)
                existing_fieldnames = reader.fieldnames or []

            if existing_fieldnames != fieldnames:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for existing_row in existing_rows:
                        writer.writerow({
                            key: existing_row.get(key, "")
                            for key in fieldnames
                        })

        with open(file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({key: row[key] for key in fieldnames})

    def print_report(self):
        """Print analytics report to console"""
        print(self.get_analytics_report())
