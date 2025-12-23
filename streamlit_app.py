import streamlit as st
import pandas as pd
from scraper import get_daily_baseline

st.set_page_config(page_title="Radeon Value Index", layout="centered")

# 1. Fetch Baseline
baseline_price = get_daily_baseline()

st.title("🛡️ Radeon Value Index (UK)")
st.write(f"**Baseline:** RX 9060 XT (16GB) @ **£{baseline_price:.2f}**")

# 2. Data & MPP Formula
# RWA: Resolution Weighted Average | Arch: Architecture Modifier
gpu_configs = [
    {"Name": "RX 9060 XT (16GB)", "RWA": 1.00, "Arch": 1.10, "Live": baseline_price},
    {"Name": "RX 7800 XT", "RWA": 1.15, "Arch": 1.00, "Live": 449.00},
    {"Name": "RX 6950 XT", "RWA": 1.35, "Arch": 0.80, "Live": 385.00},
]

# Process results
index_results = []
for gpu in gpu_configs:
    # Calculation: (Baseline * RWA) * Arch_Mod
    mpp = (baseline_price * gpu["RWA"]) * gpu["Arch"]
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
    **Formula:** `(Baseline Price * Resolution Weight) * Architecture Modifier`
    
    * **Arch_Mod 1.10 (9000 Series):** High premium for AV1 & DP 2.1.
    * **Arch_Mod 1.00 (7000 Series):** Standard weight for previous gen.
    * **Arch_Mod 0.80 (6000 Series):** 20% penalty for lacking modern encoders/ports.
    """)
