import hashlib


class IntegrityVerifier:
    """Verify file integrity using SHA256"""

    def __init__(self):
        self.original_hash = None
        self.recovered_hash = None
        self.status = None

    def calculate_hash(self, filename):
        """Calculate SHA256 hash of a file"""
        sha = hashlib.sha256()

        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(4096)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()

    def verify_integrity(self, original_file, recovered_file):
        """Verify integrity between original and recovered files"""
        self.original_hash = self.calculate_hash(original_file)
        self.recovered_hash = self.calculate_hash(recovered_file)

        if self.original_hash == self.recovered_hash:
            self.status = "PASSED"
            return True
        else:
            self.status = "FAILED"
            return False

    def get_report(self):
        """Get integrity verification report"""
        report = f"""
Original SHA256:
{self.original_hash}

Recovered SHA256:
{self.recovered_hash}

STATUS:
{self.status}
"""
        return report

    def get_short_report(self):
        """Get short integrity report"""
        return f"Original Hash: {self.original_hash}\nRecovered Hash: {self.recovered_hash}\nStatus: {self.status}"
