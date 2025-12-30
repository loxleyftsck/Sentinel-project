"""
Security Tests for SENTINEL Foundation
Tests to verify security vulnerabilities are fixed
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from sentinel.data.loaders import TransactionDataLoader
from sentinel.models.rag import sanitize_query


class TestPathTraversalPrevention:
    """Test that path traversal attacks are blocked (FIX #8)"""

    def test_double_dot_blocked(self):
        """Test that .. pattern is blocked"""
        loader = TransactionDataLoader()

        with pytest.raises(ValueError, match="path traversal"):
            loader.load_specific_file("../../../etc/passwd")

    def test_absolute_path_blocked(self):
        """Test that absolute paths are blocked"""
        loader = TransactionDataLoader()

        with pytest.raises(ValueError, match="path traversal"):
            loader.load_specific_file("/etc/passwd")

    def test_windows_path_blocked(self):
        """Test that Windows absolute paths are blocked"""
        loader = TransactionDataLoader()

        with pytest.raises(ValueError, match="path traversal"):
            loader.load_specific_file("\\Windows\\System32\\config\\sam")

    def test_valid_filename_allowed(self):
        """Test that valid filenames are allowed"""
        loader = TransactionDataLoader()

        # This should not raise ValidationError (might raise FileNotFoundError)
        try:
            loader.load_specific_file("test_data.csv")
        except FileNotFoundError:
            pass  # Expected if file doesn't exist
        except ValueError as e:
            if "path traversal" in str(e):
                pytest.fail("Valid filename was incorrectly blocked")


class TestPromptInjectionPrevention:
    """Test that prompt injection attacks are blocked (FIX #9)"""

    def test_import_statement_blocked(self):
        """Test that import statements are blocked"""
        with pytest.raises(ValueError, match="forbidden pattern"):
            sanitize_query("import os; os.system('rm -rf /')")

    def test_exec_blocked(self):
        """Test that exec() is blocked"""
        with pytest.raises(ValueError, match="forbidden pattern"):
            sanitize_query("exec('malicious code')")

    def test_eval_blocked(self):
        """Test that eval() is blocked"""
        with pytest.raises(ValueError, match="forbidden pattern"):
            sanitize_query("eval('bad things')")

    def test_os_module_blocked(self):
        """Test that os. references are blocked"""
        with pytest.raises(ValueError, match="forbidden pattern"):
            sanitize_query("Tell me about os.system() usage")

    def test_subprocess_blocked(self):
        """Test that subprocess is blocked"""
        with pytest.raises(ValueError, match="forbidden pattern"):
            sanitize_query("Use subprocess to run commands")

    def test_normal_query_allowed(self):
        """Test that normal queries are allowed"""
        query = "Apa itu insider trading menurut POJK?"
        result = sanitize_query(query)
        assert result == query

    def test_long_query_truncated(self):
        """Test that very long queries are truncated"""
        long_query = "A" * 2000
        result = sanitize_query(long_query, max_length=1000)
        assert len(result) == 1000

    def test_null_bytes_removed(self):
        """Test that null bytes are removed"""
        query = "Test\x00query"
        result = sanitize_query(query)
        assert "\x00" not in result

    def test_non_string_rejected(self):
        """Test that non-string input is rejected"""
        with pytest.raises(ValueError, match="must be a string"):
            sanitize_query(12345)

    def test_case_insensitive_blocking(self):
        """Test that forbidden patterns are blocked case-insensitively"""
        with pytest.raises(ValueError, match="forbidden pattern"):
            sanitize_query("IMPORT OS")


class TestErrorHandling:
    """Test improved error handling (FIX #1)"""

    def test_missing_files_clear_message(self):
        """Test that missing files error message is helpful"""
        loader = TransactionDataLoader(data_dir="nonexistent/tmp/test")

        try:
            # This will fail because directory doesn't exist
            pass
        except FileNotFoundError:
            pass  # Expected

        # Create temp directory for actual test
        import tempfile
        import shutil

        temp_dir = tempfile.mkdtemp()
        try:
            loader = TransactionDataLoader(data_dir=temp_dir)

            with pytest.raises(FileNotFoundError) as exc_info:
                loader.load_latest_synthetic()

            error_msg = str(exc_info.value)
            # Check that error message is helpful
            assert "generate_synthetic.py" in error_msg
            assert "To generate data" in error_msg

        finally:
            shutil.rmtree(temp_dir)


# Performance/Security Tests
class TestSecurityBestPractices:
    """Test security best practices are followed"""

    def test_no_hardcoded_secrets_in_code(self):
        """Verify no hardcoded secrets in core modules"""
        import re

        files_to_check = [
            Path(__file__).parent.parent.parent / "src" / "sentinel" / "data" / "loaders.py",
            Path(__file__).parent.parent.parent / "src" / "sentinel" / "models" / "rag.py",
        ]

        secret_patterns = [
            r'password\s*=\s*["\'].*["\']',
            r'api_key\s*=\s*["\'].*["\']',
            r'secret\s*=\s*["\'].*["\']',
            r'token\s*=\s*["\'](?!YOUR_TOKEN_HERE).*["\']',  # Allow placeholder
        ]

        for file_path in files_to_check:
            if file_path.exists():
                content = file_path.read_text()
                for pattern in secret_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    assert not matches, f"Potential hardcoded secret found in {file_path}: {matches}"

    def test_input_validation_on_public_methods(self):
        """Verify public methods validate inputs"""
        loader = TransactionDataLoader()

        # Test that invalid inputs are caught
        with pytest.raises((ValueError, TypeError, FileNotFoundError)):
            loader.load_specific_file(None)  # None should be rejected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
