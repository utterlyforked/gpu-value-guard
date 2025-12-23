import streamlit as st
import pandas as pd
from scraper import get_daily_baseline

__version__ = "1.2.0"  # Enhanced MPP formula with power and used market penalties

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

# 2. Data & MPP Formula
# RWA: Resolution Weighted Average | Arch: Architecture Modifier
# Used: Market availability penalty (0.85 for used-only cards)
# Power: TDP penalty relative to baseline (higher TDP = lower value)
gpu_configs = [
    {"Name": "RX 9060 XT (16GB)", "RWA": 1.00, "Arch": 1.10, "Used": 1.00, "TDP": 260, "Live": baseline_price},
    {"Name": "RX 7800 XT", "RWA": 1.15, "Arch": 1.00, "Used": 1.00, "TDP": 263, "Live": 449.00},
    {"Name": "RX 6950 XT", "RWA": 1.35, "Arch": 0.80, "Used": 0.85, "TDP": 335, "Live": 385.00},
]

# Baseline TDP for normalization
baseline_tdp = 260

# Process results
index_results = []
for gpu in gpu_configs:
    # Power penalty: higher TDP reduces value (£0.20 per 10W over baseline)
    power_penalty = 1.0 - ((gpu["TDP"] - baseline_tdp) / 10) * 0.02

    # Calculation: (Baseline * RWA) * Arch_Mod * Used_Penalty * Power_Penalty
    mpp = (baseline_price * gpu["RWA"]) * gpu["Arch"] * gpu["Used"] * power_penalty
    verdict = "🔥 DEAL" if gpu["Live"] <= mpp else "⚠️ NO DEAL"

    index_results.append({
        "Model": gpu["Name"],
        "Max Purchase Price (MPP)": f"£{mpp:.2f}",
        "Current Market": f"£{gpu['Live']:.2f}",
        "Verdict": verdict
    })

# 3. Render Table
st.table(pd.DataFrame(index_results))

# 4. Formula Documentation
with st.expander("How is the MPP calculated?"):
    st.write("""
    **Formula:** `(Baseline Price × Resolution Weight) × Architecture Mod × Used Penalty × Power Penalty`

    **Architecture Modifiers:**
    * **1.10 (9000 Series):** Premium for AV1 encode & DP 2.1
    * **1.00 (7000 Series):** Standard current-gen weight
    * **0.80 (6000 Series):** Penalty for lacking modern encoders/ports

    **Used Market Penalty:**
    * **0.85:** Applied to cards only available used (e.g., 6950 XT)
    * **1.00:** New retail cards (no penalty)

    **Power Penalty:**
    * **£0.20 deduction per 10W** over baseline TDP (260W)
    * Example: 6950 XT (335W) = 15% penalty for higher running costs
    """)

# 5. Version Footer
st.divider()
st.caption(f"Radeon Value Index v{__version__}")
