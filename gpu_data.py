"""
GPU configuration data for Value Target calculations.
All GPUs listed here must have 16GB VRAM.

RWA: Resolution Weighted Average (performance relative to RX 9060 XT baseline)
Arch: Architecture Value Retention (value penalty for older architecture)
Live: Current market price estimate (placeholder until eBay scraping implemented)
URL: Official AMD product page
"""

GPU_CONFIGS = [
    # RDNA 4 (9000 Series) - Modern baseline architecture
    {
        "Name": "RX 9070 XT (16GB)",
        "RWA": 1.80,
        "Arch": 1.00,
        "Live": 599.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9070xt.html"
    },
    {
        "Name": "RX 9070 (16GB)",
        "RWA": 1.25,
        "Arch": 1.00,
        "Live": 499.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9070.html"
    },

    # RDNA 3 (7000 Series) - Previous gen, small penalty for lacking AV1/DP2.1
    {
        "Name": "RX 7900 GRE (16GB)",
        "RWA": 1.32,
        "Arch": 0.91,
        "Live": 519.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7900-gre.html"
    },
    {
        "Name": "RX 7800 XT (16GB)",
        "RWA": 1.21,
        "Arch": 0.91,
        "Live": 449.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7800-xt.html"
    },
    {
        "Name": "RX 7700 (16GB)",
        "RWA": 1.00,
        "Arch": 0.91,
        "Live": 329.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7700.html"
    },
    {
        "Name": "RX 7600 XT (16GB)",
        "RWA": 0.68,
        "Arch": 0.91,
        "Live": 279.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7600-xt.html"
    },

    # RDNA 2 (6000 Series) - Two gens old, larger penalty for older tech
    {
        "Name": "RX 6950 XT (16GB)",
        "RWA": 1.33,
        "Arch": 0.73,
        "Live": 385.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6950-xt.html"
    },
    {
        "Name": "RX 6900 XT (16GB)",
        "RWA": 1.27,
        "Arch": 0.73,
        "Live": 359.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6900-xt.html"
    },
    {
        "Name": "RX 6800 XT (16GB)",
        "RWA": 1.23,
        "Arch": 0.73,
        "Live": 329.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6800-xt.html"
    },
    {
        "Name": "RX 6800 (16GB)",
        "RWA": 1.08,
        "Arch": 0.73,
        "Live": 289.00,
        "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6800.html"
    },
]

# Baseline GPU information
BASELINE_GPU = {
    "Name": "RX 9060 XT (16GB)",
    "URL": "https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9060-xt.html"
}
