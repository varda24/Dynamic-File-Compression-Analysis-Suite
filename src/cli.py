import os
import pickle
import csv
import json
import tempfile
import time
from src.huffman import HuffmanCoding
from src.rle import RunLengthEncoding
from src.file_handler import FileHandler
from src.analytics import CompressionAnalytics
from src.integrity import IntegrityVerifier
from src.benchmark import Benchmark
from src.visualizer import Visualizer


class CompressionCLI:
    """Interactive CLI for compression utility"""

    def __init__(self):
        self.file_handler = FileHandler()
        self.huffman = HuffmanCoding()
        self.rle = RunLengthEncoding()

    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _read_compressed_metadata(self, compressed_path):
        """Read metadata from compressed file without decompressing it."""
        with open(compressed_path, "rb") as file:
            data = pickle.load(file)

        if isinstance(data, dict):
            return {
                "algorithm": data.get("algorithm"),
                "original_filename": data.get("original_filename"),
                "format_version": data.get("format_version"),
                "stats": data.get("stats", {}),
            }

        if isinstance(data, tuple):
            if len(data) in (3, 4) and isinstance(data[1], dict):
                return {
                    "algorithm": "huffman",
                    "original_filename": data[3] if len(data) == 4 else None,
                    "format_version": "legacy",
                    "stats": {},
                }
            return {
                "algorithm": "rle",
                "original_filename": data[1] if len(data) > 1 else None,
                "format_version": "legacy",
                "stats": {},
            }

        return {
            "algorithm": "rle",
            "original_filename": None,
            "format_version": "legacy",
            "stats": {},
        }

    def _normalize_original_name(self, decompressed_file):
        """Map algorithm-suffixed decompressed filenames back to originals."""
        name, extension = os.path.splitext(decompressed_file)
        name = name.replace("_huffman", "")
        name = name.replace("_rle", "")
        return name + extension

    def _extract_archive_if_needed(self, decompressed_path):
        """Extract a decompressed multi-file archive JSON payload."""
        try:
            with open(decompressed_path, "r", encoding="utf-8") as file:
                archive_data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return False

        if archive_data.get("type") != "multi_file_archive":
            return False

        archive_name = os.path.splitext(os.path.basename(decompressed_path))[0]
        output_dir = os.path.join(self.file_handler.decompressed_dir, archive_name)
        os.makedirs(output_dir, exist_ok=True)

        for archived_file in archive_data.get("files", []):
            filename = os.path.basename(archived_file["name"])
            output_path = os.path.join(output_dir, filename)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(archived_file["content"])

        print(f"Archive extracted to: {output_dir}")
        return True

    def _generate_compression_artifacts(self, filename, input_path, compressed_path,
                                       algorithm, encoding_time, physical_ratio,
                                       original_bits, encoded_bits, theoretical_ratio,
                                       huffman_root=None, original_size=None):
        """Generate compression reports and visualizations automatically"""
        try:
            # Generate compression report
            analytics = CompressionAnalytics()
            analytics.input_file = filename
            analytics.algorithm = algorithm
            analytics.original_size = (
                original_size
                if original_size is not None
                else self.file_handler.get_file_size(input_path)
            )
            analytics.compressed_size = self.file_handler.get_file_size(compressed_path)
            analytics.encoding_time = encoding_time
            analytics.original_bits = original_bits
            analytics.encoded_bits = encoded_bits
            analytics.theoretical_ratio = theoretical_ratio
            
            base_name = os.path.splitext(filename)[0]
            report_filename = f"report_{int(time.time())}_{base_name}.txt"
            report_path = self.file_handler.get_report_path(report_filename)
            analytics.save_report(report_path)
            print(f"   ✓ Report saved: {report_filename}")

            csv_filename = report_filename.replace(".txt", ".csv")
            csv_path = self.file_handler.get_report_path(csv_filename)
            analytics.save_csv_report(csv_path)
            analytics.save_report(self.file_handler.get_report_path("report.txt"))
            analytics.save_csv_report(self.file_handler.get_report_path("report.csv"))
            try:
                pdf_filename = report_filename.replace(".txt", ".pdf")
                pdf_path = self.file_handler.get_report_path(pdf_filename)
                analytics.save_pdf_report(pdf_path)
                analytics.save_pdf_report(self.file_handler.get_report_path("report.pdf"))
                print(f"   ✓ PDF report saved: {pdf_filename}")
            except RuntimeError as error:
                print(f"   ⚠ PDF report skipped: {error}")
            analytics.append_history(self.file_handler.get_log_path("history.csv"))
            print(f"   ✓ CSV report saved: {csv_filename}")
            print("   ✓ History updated: logs/history.csv")
            
            # Generate frequency distribution visualization
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            visualizer = Visualizer()
            viz_filename = f"frequency_{int(time.time())}_{base_name}.png"
            viz_path = self.file_handler.get_visualization_path(viz_filename)
            visualizer.plot_frequency_distribution(text, viz_path)
            print(f"   ✓ Visualization saved: {viz_filename}")

            if huffman_root is not None:
                tree_path = self.file_handler.get_visualization_path("huffman_tree.png")
                visualizer.plot_huffman_tree(huffman_root, tree_path)
                print("   ✓ Huffman tree saved: huffman_tree.png")
            
        except Exception as e:
            print(f"   ⚠ Could not generate artifacts: {str(e)}")

    def compress_file(self):
        """Interactive file compression"""
        print("\n========== Compress File ==========")

        files = self.file_handler.list_input_files()
        if not files:
            print("No files found in input_files/ directory")
            return

        print("\nAvailable files:")
        for idx, file in enumerate(files, 1):
            size = self.file_handler.get_file_size_kb(
                self.file_handler.get_input_file_path(file)
            )
            print(f"{idx}. {file} ({size} KB)")

        try:
            choice = int(input("\nSelect file number: "))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
                algo = input("Choose algorithm (1=Huffman, 2=RLE) [Default=1]: ").strip() or "1"
                
                # Validate algorithm input
                if algo not in ["1", "2"]:
                    print("Invalid choice. Using Huffman (default).")
                    algo = "1"

                input_path = self.file_handler.get_input_file_path(filename)
                algorithm_key = "rle" if algo == "2" else "huffman"
                compressed_path = self.file_handler.get_algorithm_compressed_file_path(
                    filename,
                    algorithm_key
                )

                print("\nCompressing...")

                original_size = self.file_handler.get_file_size(input_path)
                
                # Show warning for small files
                if original_size < 1024:
                    print("\n⚠ Warning: Small files may show poor compression because")
                    print("  metadata overhead can exceed compression savings.")

                if algo == "2":
                    self.rle.compress_file(input_path, compressed_path)
                    algorithm_name = "RLE"
                    encoding_time = self.rle.encoding_time
                    theoretical_ratio = self.rle.theoretical_ratio
                    original_bits = self.rle.original_bits
                    encoded_bits = self.rle.encoded_bits
                    huffman_root = None
                else:
                    self.huffman.compress_file(input_path, compressed_path)
                    algorithm_name = "Huffman"
                    encoding_time = self.huffman.encoding_time
                    theoretical_ratio = self.huffman.theoretical_ratio
                    original_bits = self.huffman.original_bits
                    encoded_bits = self.huffman.encoded_bits
                    huffman_root = self.huffman.root

                compressed_size = self.file_handler.get_file_size(compressed_path)
                physical_ratio = self.file_handler.get_compression_ratio(original_size, compressed_size)

                print(f"\n✓ Compression successful!")
                print(f"\n📊 Physical Compression (Disk):")
                print(f"   Original Size: {self.file_handler.get_file_size_kb(input_path)} KB")
                print(f"   Compressed Size: {self.file_handler.get_file_size_kb(compressed_path)} KB")
                print(f"   Disk Ratio: {physical_ratio}%")
                
                print(f"\n🔬 Algorithm Compression (Bit-Level):")
                print(f"   Original Bits: {original_bits:,}")
                print(f"   Encoded Bits: {encoded_bits:,}")
                print(f"   Theoretical Ratio: {theoretical_ratio}%")
                
                print(f"\n⏱ Performance:")
                print(f"   Encoding Time: {encoding_time:.6f} sec")
                print(f"   Saved to: {compressed_path}")
                
                # Generate report and visualization automatically
                print(f"\n📋 Generating reports and visualizations...")
                self._generate_compression_artifacts(
                    filename, input_path, compressed_path,
                    algorithm_name,
                    encoding_time, physical_ratio, 
                    original_bits, encoded_bits, theoretical_ratio,
                    huffman_root
                )
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

    def decompress_file(self):
        """Interactive file decompression"""
        print("\n========== Decompress File ==========")

        files = self.file_handler.list_compressed_files()
        if not files:
            print("No compressed files found in compressed_files/ directory")
            return

        print("\nAvailable compressed files:")
        for idx, file in enumerate(files, 1):
            size = self.file_handler.get_file_size_kb(
                os.path.join(self.file_handler.compressed_dir, file)
            )
            print(f"{idx}. {file} ({size} KB)")

        try:
            choice = int(input("\nSelect file number: "))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
                compressed_path = os.path.join(self.file_handler.compressed_dir, filename)
                metadata = self._read_compressed_metadata(compressed_path)
                algorithm = metadata["algorithm"]
                output_name = metadata.get("original_filename") or filename.replace('.huff', '')
                decompressed_path = self.file_handler.get_decompressed_file_path(output_name)

                print(f"\nDetected algorithm: {algorithm.title()}")
                print("Decompressing...")

                if algorithm == "rle":
                    self.rle.decompress_file(compressed_path, decompressed_path)
                    decoding_time = self.rle.decoding_time
                elif algorithm == "huffman":
                    self.huffman.decompress_file(compressed_path, decompressed_path)
                    decoding_time = self.huffman.decoding_time
                else:
                    print("Unknown compression algorithm in file metadata")
                    return

                print(f"\n✓ Decompression successful!")
                print(f"Decoding Time: {decoding_time:.6f} sec")
                print(f"Saved to: {decompressed_path}")
                self._extract_archive_if_needed(decompressed_path)
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

    def benchmark(self):
        """Compare compression algorithms"""
        print("\n========== Algorithm Comparison ==========")

        files = self.file_handler.list_input_files()
        if not files:
            print("No files found in input_files/ directory")
            return

        print("\nAvailable files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")

        try:
            choice = int(input("\nSelect file number: "))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
                input_path = self.file_handler.get_input_file_path(filename)
                file_size = self.file_handler.get_file_size(input_path)

                if file_size < 1024:
                    print("File too small for meaningful benchmark")
                    return

                print("\nBenchmarking...")
                benchmark = Benchmark()
                results = benchmark.compare_algorithms(input_path)

                benchmark.print_comparison()

                # Generate visualizations
                visualizer = Visualizer()
                visualizer.plot_compression_comparison(
                    results,
                    self.file_handler.get_visualization_path("comparison.png")
                )
                visualizer.plot_execution_time_comparison(
                    results,
                    self.file_handler.get_visualization_path("timing_comparison.png")
                )

                print("\nVisualizations saved to visualizations/ directory")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

    def verify_integrity(self):
        """Verify file integrity"""
        print("\n========== Verify Integrity ==========")

        decompressed_dir = self.file_handler.decompressed_dir
        decompressed_files = [f for f in os.listdir(decompressed_dir) 
                             if os.path.isfile(os.path.join(decompressed_dir, f))]

        if not decompressed_files:
            print("No decompressed files found")
            return

        print("\nAvailable decompressed files:")
        for idx, file in enumerate(decompressed_files, 1):
            size_kb = round(os.path.getsize(os.path.join(decompressed_dir, file)) / 1024, 2)
            print(f"{idx}. {file} ({size_kb} KB)")

        try:
            choice = int(input("\nSelect file number: "))
            if 1 <= choice <= len(decompressed_files):
                decompressed_file = decompressed_files[choice - 1]
                original_name = self._normalize_original_name(decompressed_file)
                
                # Algorithm-suffixed files like big_huffman.txt map back to big.txt.
                original_path = self.file_handler.get_input_file_path(original_name)
                decompressed_path = os.path.join(decompressed_dir, decompressed_file)

                if not os.path.exists(original_path):
                    print(f"\n✗ Original file not found: {original_path}")
                    print(f"  Expected location: input_files/{original_name}")
                    return

                print(f"\nVerifying integrity...")
                verifier = IntegrityVerifier()
                result = verifier.verify_integrity(original_path, decompressed_path)

                print("\n" + verifier.get_report())
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

    def generate_report(self):
        """Generate compression report"""
        print("\n========== Generate Report ==========")

        files = self.file_handler.list_input_files()
        if not files:
            print("No files found")
            return

        print("\nAvailable files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")

        try:
            choice = int(input("\nSelect file number: "))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
                input_path = self.file_handler.get_input_file_path(filename)
                compressed_versions = self.file_handler.find_compressed_versions(filename)

                if not compressed_versions:
                    print("File not compressed yet")
                    return

                if len(compressed_versions) == 1:
                    compressed_path = compressed_versions[0]
                else:
                    print("\nAvailable compressed versions:")
                    for idx, path in enumerate(compressed_versions, 1):
                        metadata = self._read_compressed_metadata(path)
                        algorithm = (metadata.get("algorithm") or "unknown").title()
                        print(f"{idx}. {os.path.basename(path)} ({algorithm})")

                    version_choice = int(input("\nSelect compressed version: "))
                    if not 1 <= version_choice <= len(compressed_versions):
                        print("Invalid selection")
                        return
                    compressed_path = compressed_versions[version_choice - 1]

                analytics = CompressionAnalytics()
                analytics.input_file = filename
                analytics.original_size = self.file_handler.get_file_size(input_path)
                analytics.compressed_size = self.file_handler.get_file_size(compressed_path)
                metadata = self._read_compressed_metadata(compressed_path)
                analytics.algorithm = (metadata.get("algorithm") or "huffman").title()
                stats = metadata.get("stats", {})
                analytics.original_bits = stats.get("original_bits", 0)
                analytics.encoded_bits = stats.get("encoded_bits", 0)
                analytics.theoretical_ratio = stats.get("theoretical_ratio", 0)

                # Try to get timing info
                huffman = HuffmanCoding()
                with tempfile.NamedTemporaryFile(
                    suffix=".huff",
                    dir=self.file_handler.compressed_dir,
                    delete=False
                ) as temp_file:
                    temp_path = temp_file.name
                try:
                    huffman.compress_file(input_path, temp_path)
                    analytics.encoding_time = huffman.encoding_time
                    if not analytics.original_bits:
                        analytics.original_bits = huffman.original_bits
                        analytics.encoded_bits = huffman.encoded_bits
                        analytics.theoretical_ratio = huffman.theoretical_ratio
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                analytics.decoding_time = huffman.decoding_time

                analytics.print_report()

                # Save report
                base_name = os.path.splitext(filename)[0]
                report_path = self.file_handler.get_report_path(f"report_{base_name}.txt")
                analytics.save_report(report_path)
                csv_path = self.file_handler.get_report_path(f"report_{base_name}.csv")
                analytics.save_csv_report(csv_path)
                pdf_path = self.file_handler.get_report_path(f"report_{base_name}.pdf")
                try:
                    analytics.save_pdf_report(pdf_path)
                    analytics.save_pdf_report(self.file_handler.get_report_path("report.pdf"))
                except RuntimeError as error:
                    print(f"PDF report skipped: {error}")
                analytics.save_report(self.file_handler.get_report_path("report.txt"))
                analytics.save_csv_report(self.file_handler.get_report_path("report.csv"))
                print(f"\nReport saved to: {report_path}")
                print(f"CSV report saved to: {csv_path}")
                if os.path.exists(pdf_path):
                    print(f"PDF report saved to: {pdf_path}")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

    def view_compression_history(self):
        """Display persisted compression history"""
        print("\n========== Compression History ==========")

        history_path = self.file_handler.get_log_path("history.csv")
        if not os.path.exists(history_path):
            print("No compression history found")
            return

        with open(history_path, "r", newline="") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            print("No compression history found")
            return

        print(f"{'Date':<20} {'File':<20} {'Algorithm':<12} {'Ratio':<10} {'Time':<12}")
        print("-" * 78)

        for row in rows[-15:]:
            date = row.get("Date", "")
            filename = row.get("File", "")
            algorithm = row.get("Algorithm", "")
            ratio = row.get("Ratio", "")
            encoding_time = row.get("EncodingTime", "")
            if encoding_time:
                encoding_time = f"{float(encoding_time):.6f}s"

            print(
                f"{date:<20} "
                f"{filename:<20} "
                f"{algorithm:<12} "
                f"{ratio:<10} "
                f"{encoding_time:<12}"
            )

    def view_project_statistics(self):
        """Display aggregate project metrics from compression history."""
        print("\n========== Project Statistics ==========")

        history_path = self.file_handler.get_log_path("history.csv")
        if not os.path.exists(history_path):
            print("No compression history found")
            return

        with open(history_path, "r", newline="") as file:
            rows = list(csv.DictReader(file))

        valid_rows = []
        for row in rows:
            try:
                valid_rows.append({
                    "file": row.get("File", ""),
                    "algorithm": row.get("Algorithm", "Unknown"),
                    "original": float(row.get("Original") or 0),
                    "ratio": float(row.get("Ratio") or 0),
                })
            except ValueError:
                continue

        if not valid_rows:
            print("No valid compression statistics found")
            return

        algorithm_counts = {}
        for row in valid_rows:
            algorithm_counts[row["algorithm"]] = algorithm_counts.get(row["algorithm"], 0) + 1

        total_files = len(valid_rows)
        total_processed = sum(row["original"] for row in valid_rows)
        average_ratio = sum(row["ratio"] for row in valid_rows) / total_files
        best_row = min(valid_rows, key=lambda row: row["ratio"])
        most_used_algorithm = max(
            algorithm_counts.items(),
            key=lambda item: item[1]
        )[0]

        formatter = CompressionAnalytics()
        print(f"Total Files Compressed: {total_files}")
        print(f"Total Data Processed: {formatter._format_size(total_processed)}")
        print(f"Average Compression Ratio: {average_ratio:.2f}%")
        print(f"Best Compression Ratio: {best_row['ratio']:.2f}% ({best_row['file']})")
        print(f"Most Used Algorithm: {most_used_algorithm}")

    def compress_multiple_files(self):
        """Compress multiple input files into one Huffman archive."""
        print("\n========== Multi-file Compression ==========")

        files = self.file_handler.list_input_files()
        if not files:
            print("No files found in input_files/ directory")
            return

        print("\nAvailable files:")
        for idx, file in enumerate(files, 1):
            size = self.file_handler.get_file_size_kb(
                self.file_handler.get_input_file_path(file)
            )
            print(f"{idx}. {file} ({size} KB)")

        raw_selection = input("\nSelect file numbers separated by commas or type 'all': ").strip()
        if raw_selection.lower() == "all":
            selected_files = files
        else:
            try:
                selected_indexes = [
                    int(value.strip())
                    for value in raw_selection.split(",")
                    if value.strip()
                ]
            except ValueError:
                print("Invalid selection")
                return

            if not selected_indexes or any(index < 1 or index > len(files) for index in selected_indexes):
                print("Invalid selection")
                return

            selected_files = [files[index - 1] for index in selected_indexes]

        archive_name = input("Archive name [Default=archive]: ").strip()
        if not archive_name:
            archive_name = "archive"
        if archive_name.isdigit():
            print("Archive name cannot be only numbers. Using default: archive")
            archive_name = "archive"

        archive_base = os.path.splitext(archive_name)[0]
        archive_output = os.path.join(
            self.file_handler.compressed_dir,
            f"{archive_base}_huffman.huff"
        )

        archive_data = {
            "type": "multi_file_archive",
            "files": [],
        }

        original_size = 0
        for filename in selected_files:
            input_path = self.file_handler.get_input_file_path(filename)
            original_size += self.file_handler.get_file_size(input_path)
            with open(input_path, "r", encoding="utf-8") as file:
                archive_data["files"].append({
                    "name": filename,
                    "content": file.read(),
                })

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".archive",
                dir=self.file_handler.compressed_dir,
                encoding="utf-8",
                delete=False
            ) as temp_file:
                temp_path = temp_file.name
                json.dump(archive_data, temp_file)

            self.huffman.compress_file(temp_path, archive_output)
            with open(archive_output, "rb") as file:
                archive_metadata = pickle.load(file)
            archive_metadata["original_filename"] = f"{archive_base}.archive.json"
            with open(archive_output, "wb") as file:
                pickle.dump(archive_metadata, file)

            compressed_size = self.file_handler.get_file_size(archive_output)
            physical_ratio = self.file_handler.get_compression_ratio(
                original_size,
                compressed_size
            )

            print("\n✓ Multi-file compression successful!")
            print(f"   Files archived: {len(selected_files)}")
            print(f"   Original Size: {round(original_size / 1024, 2)} KB")
            print(f"   Compressed Size: {self.file_handler.get_file_size_kb(archive_output)} KB")
            print(f"   Disk Ratio: {physical_ratio}%")
            print(f"   Saved to: {archive_output}")

            self._generate_compression_artifacts(
                f"{archive_base}_archive",
                temp_path,
                archive_output,
                "Huffman Archive",
                self.huffman.encoding_time,
                physical_ratio,
                self.huffman.original_bits,
                self.huffman.encoded_bits,
                self.huffman.theoretical_ratio,
                self.huffman.root,
                original_size
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    def menu(self):
        """Main menu"""
        while True:
            print("\n========== Dynamic Compression Suite ==========")
            print("1. Compress File")
            print("2. Decompress File")
            print("3. Compare Algorithms")
            print("4. Verify Integrity")
            print("5. Generate Report")
            print("6. Compress Multiple Files")
            print("7. View Compression History")
            print("8. Export PDF Report")
            print("9. Project Statistics")
            print("10. Exit")
            print("===============================================")

            choice = input("Choose Option: ")

            if choice == "1":
                self.compress_file()
            elif choice == "2":
                self.decompress_file()
            elif choice == "3":
                self.benchmark()
            elif choice == "4":
                self.verify_integrity()
            elif choice == "5":
                self.generate_report()
            elif choice == "6":
                self.compress_multiple_files()
            elif choice == "7":
                self.view_compression_history()
            elif choice == "8":
                self.generate_report()
            elif choice == "9":
                self.view_project_statistics()
            elif choice == "10":
                print("Thank you for using Dynamic Compression Suite!")
                break
            else:
                print("Invalid option. Please try again.")

            input("\nPress Enter to continue...")
