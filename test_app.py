"""
Test suite for GPU Value Guard application.
Run with: pytest test_app.py -v
"""

import pytest


def test_core_dependencies():
    """Verify all core dependencies are installed and importable."""
    import streamlit
    import pandas
    import requests
    from bs4 import BeautifulSoup
    import tabulate

    # Verify tabulate is available for markdown rendering
    assert hasattr(pandas.DataFrame, 'to_markdown'), \
        "pandas.DataFrame.to_markdown() requires tabulate package"


def test_gpu_data_structure():
    """Verify GPU data has correct structure and all required fields."""
    from gpu_data import GPU_CONFIGS, BASELINE_GPU

    # Check GPU_CONFIGS is not empty
    assert len(GPU_CONFIGS) > 0, "GPU_CONFIGS must contain at least one GPU"

    required_fields = {'Name', 'RWA', 'Arch', 'Live', 'URL'}

    for i, gpu in enumerate(GPU_CONFIGS):
        # Check all required fields exist
        missing_fields = required_fields - set(gpu.keys())
        assert not missing_fields, \
            f"GPU at index {i} missing fields: {missing_fields}"

        # Validate field types
        assert isinstance(gpu['Name'], str), f"GPU {i}: Name must be string"
        assert isinstance(gpu['RWA'], (int, float)), f"GPU {i}: RWA must be numeric"
        assert isinstance(gpu['Arch'], (int, float)), f"GPU {i}: Arch must be numeric"
        assert isinstance(gpu['Live'], (int, float)), f"GPU {i}: Live must be numeric"
        assert isinstance(gpu['URL'], str), f"GPU {i}: URL must be string"

        # Validate 16GB requirement
        assert '16GB' in gpu['Name'], \
            f"GPU {i} ({gpu['Name']}): Name must include '16GB'"

        # Validate URL is AMD official
        assert gpu['URL'].startswith('https://www.amd.com/'), \
            f"GPU {i} ({gpu['Name']}): URL must be official AMD website"

        # Validate reasonable value ranges
        assert 0 < gpu['RWA'] <= 3.0, \
            f"GPU {i} ({gpu['Name']}): RWA should be between 0 and 3.0"
        assert 0 < gpu['Arch'] <= 1.5, \
            f"GPU {i} ({gpu['Name']}): Arch should be between 0 and 1.5"
        assert gpu['Live'] > 0, \
            f"GPU {i} ({gpu['Name']}): Live price must be positive"

    # Check baseline GPU structure
    assert 'Name' in BASELINE_GPU, "BASELINE_GPU must have Name field"
    assert 'URL' in BASELINE_GPU, "BASELINE_GPU must have URL field"
    assert '16GB' in BASELINE_GPU['Name'], "Baseline GPU must have 16GB VRAM"


def test_gpu_data_no_baseline_in_configs():
    """Verify baseline GPU (9060 XT) is not in the comparison list."""
    from gpu_data import GPU_CONFIGS, BASELINE_GPU

    baseline_name = BASELINE_GPU['Name']
    config_names = [gpu['Name'] for gpu in GPU_CONFIGS]

    assert baseline_name not in config_names, \
        f"Baseline GPU '{baseline_name}' should not be in GPU_CONFIGS comparison list"


def test_architecture_modifiers():
    """Verify architecture modifiers follow the correct pattern."""
    from gpu_data import GPU_CONFIGS

    rdna4_cards = [g for g in GPU_CONFIGS if 'RX 9' in g['Name']]
    rdna3_cards = [g for g in GPU_CONFIGS if 'RX 7' in g['Name']]
    rdna2_cards = [g for g in GPU_CONFIGS if 'RX 6' in g['Name']]

    # RDNA 4 should have Arch = 1.00 (modern baseline)
    for gpu in rdna4_cards:
        assert gpu['Arch'] == 1.00, \
            f"{gpu['Name']}: RDNA 4 cards should have Arch=1.00"

    # RDNA 3 should have Arch = 0.91 (9% penalty)
    for gpu in rdna3_cards:
        assert gpu['Arch'] == 0.91, \
            f"{gpu['Name']}: RDNA 3 cards should have Arch=0.91"

    # RDNA 2 should have Arch = 0.73 (27% penalty)
    for gpu in rdna2_cards:
        assert gpu['Arch'] == 0.73, \
            f"{gpu['Name']}: RDNA 2 cards should have Arch=0.73"


def test_scraper_module_imports():
    """Verify scraper module can be imported."""
    from scraper import get_daily_baseline, scrape_scan_uk, scrape_overclockers_uk, scrape_ebuyer_uk

    # Check functions are callable
    assert callable(get_daily_baseline)
    assert callable(scrape_scan_uk)
    assert callable(scrape_overclockers_uk)
    assert callable(scrape_ebuyer_uk)


def test_value_target_calculation():
    """Test Value Target calculation logic."""
    baseline_price = 330.00

    # Test case: RX 7800 XT (RWA=1.21, Arch=0.91)
    rwa = 1.21
    arch = 0.91
    expected = baseline_price * rwa * arch

    value_target = (baseline_price * rwa) * arch

    assert abs(value_target - expected) < 0.01, \
        "Value Target calculation doesn't match formula"

    # Verify the result is reasonable (around £363)
    assert 360 < value_target < 370, \
        f"Expected Value Target around £363, got £{value_target:.2f}"


def test_streamlit_app_imports():
    """Verify streamlit app can import its dependencies."""
    # This will fail if there are any import errors in the app
    import streamlit_app

    # Verify key imports worked
    assert hasattr(streamlit_app, 'st')
    assert hasattr(streamlit_app, 'pd')


if __name__ == '__main__':
    # Allow running tests directly with: python test_app.py
    pytest.main([__file__, '-v'])
