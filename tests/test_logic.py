from core.logic import expected_hashes_by_difficulty

def test_expected_hashes_by_difficulty():
    assert expected_hashes_by_difficulty(0) == 1
    assert expected_hashes_by_difficulty(1) == 16
    assert expected_hashes_by_difficulty(2) == 256
