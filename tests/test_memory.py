import pytest
import json
from pathlib import Path
from unittest.mock import patch
import sys

# Add the parent directory to sys.path so we can import memory_manager
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory import memory_manager

@pytest.fixture
def mock_memory_path(tmp_path):
    """Fixture to mock MEMORY_PATH so tests don't overwrite real user data."""
    test_memory_file = tmp_path / "long_term.json"
    with patch("memory.memory_manager.MEMORY_PATH", test_memory_file):
        yield test_memory_file

def test_load_memory_empty(mock_memory_path):
    # Ensure memory is empty when file doesn't exist
    memory = memory_manager.load_memory()
    assert "identity" in memory
    assert "preferences" in memory
    assert memory["preferences"] == {}

def test_remember_and_forget(mock_memory_path):
    # Remember a note
    res = memory_manager.remember("test_key", "test_value", "notes")
    assert "Remembered: notes/test_key = test_value" in res
    
    # Verify it was saved
    memory = memory_manager.load_memory()
    assert memory["notes"]["test_key"]["value"] == "test_value"
    
    # Forget the note
    res = memory_manager.forget("test_key", "notes")
    assert "Forgotten: notes/test_key" in res
    
    # Verify it was removed
    memory = memory_manager.load_memory()
    assert "test_key" not in memory["notes"]
