import streamlit as st
import pandas as pd
from scraper import get_daily_baseline

st.set_page_config(page_title="Radeon Value Index", layout="centered")

# 1. Fetch Baseline
baseline_price, baseline_url, baseline_retailer = get_daily_baseline()

st.title("🛡️ Radeon Value Index (UK)")

# Display baseline with source link
if baseline_url:
    st.write(f"**Baseline:** RX 9060 XT (16GB) @ **£{baseline_price:.2f}** from [{baseline_retailer}]({baseline_url})")
else:
    st.write(f"**Baseline:** RX 9060 XT (16GB) @ **£{baseline_price:.2f}** (using default price)")
    st.caption("⚠️ Unable to fetch live pricing from retailers. Using fallback baseline.")

st.caption("**16GB VRAM cards only** - VRAM capacity matters for longevity and future-proofing")

# 2. Data & Value Target Formula
# RWA: Resolution Weighted Average (performance relative to baseline)
# Arch: Architecture Modifier (value retention factor for older tech)
gpu_configs = [
    # RDNA 4 (9000 Series) - Modern baseline architecture
    {"Name": "RX 9070 XT (16GB)", "RWA": 1.80, "Arch": 1.00, "Live": 599.00},
    {"Name": "RX 9070 (16GB)", "RWA": 1.25, "Arch": 1.00, "Live": 499.00},

    # RDNA 3 (7000 Series) - Previous gen, small penalty for lacking AV1/DP2.1
    {"Name": "RX 7900 GRE (16GB)", "RWA": 1.32, "Arch": 0.91, "Live": 519.00},
    {"Name": "RX 7800 XT (16GB)", "RWA": 1.21, "Arch": 0.91, "Live": 449.00},
    {"Name": "RX 7700 (16GB)", "RWA": 1.00, "Arch": 0.91, "Live": 329.00},
    {"Name": "RX 7600 XT (16GB)", "RWA": 0.68, "Arch": 0.91, "Live": 279.00},

    # RDNA 2 (6000 Series) - Two gens old, larger penalty for older tech
    {"Name": "RX 6950 XT (16GB)", "RWA": 1.33, "Arch": 0.73, "Live": 385.00},
    {"Name": "RX 6900 XT (16GB)", "RWA": 1.27, "Arch": 0.73, "Live": 359.00},
    {"Name": "RX 6800 XT (16GB)", "RWA": 1.23, "Arch": 0.73, "Live": 329.00},
    {"Name": "RX 6800 (16GB)", "RWA": 1.08, "Arch": 0.73, "Live": 289.00},
]

# Process results
index_results = []
for gpu in gpu_configs:
    # Calculation: (Baseline * Performance Weight) * Architecture Value Retention
    value_target = (baseline_price * gpu["RWA"]) * gpu["Arch"]
    verdict = "🔥 DEAL" if gpu["Live"] <= value_target else "⚠️ NO DEAL"

    index_results.append({
        "Model": gpu["Name"],
        "Value Target": f"£{value_target:.2f}",
        "Current Market": f"£{gpu['Live']:.2f}",
        "Verdict": verdict
    })

# 3. Render Table
st.table(pd.DataFrame(index_results))

# 4. Formula Documentation
with st.expander("How is the Value Target calculated?"):
    st.write("""
    **Formula:** `(Baseline Price × Performance Weight) × Architecture Value Retention`

    The Value Target represents what you should pay for a GPU considering both its performance
    and the value loss from buying older architecture.

    **Performance Weight (RWA):**
    - Relative gaming performance vs RX 9060 XT baseline
    - Example: 1.80 = 80% faster, 0.68 = 32% slower

    **Architecture Value Retention:**
    - **1.00 (RDNA 4 - 9000 Series):** Modern features (AV1, DP 2.1, FSR 4)
    - **0.91 (RDNA 3 - 7000 Series):** -9% for lacking modern encoders/ports
    - **0.73 (RDNA 2 - 6000 Series):** -27% for two-generation-old architecture

    **Verdict Logic:**
    - 🔥 **DEAL**: Market price ≤ Value Target (fair price or better)
    - ⚠️ **NO DEAL**: Market price > Value Target (overpaying for old tech)
    """)
