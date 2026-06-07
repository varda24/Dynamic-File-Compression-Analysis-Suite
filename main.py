"""
Dynamic File Compression & Analysis Suite

Main entry point for the compression utility.
"""

from src.cli import CompressionCLI


def main():
    """Main function"""
    cli = CompressionCLI()
    cli.menu()


if __name__ == "__main__":
    main()
