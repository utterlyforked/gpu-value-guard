import streamlit as st
import pandas as pd
from scraper import get_baseline_price

# Configuration
st.set_page_config(page_title="Radeon Value Index", page_icon="🛡️", layout="wide")

# Fetch daily baseline
baseline = get_baseline_price()

# 1. UI Header
st.title("🛡️ GPU Stability & Value Index")
st.markdown(f"**Current 2025 Market Baseline:** RX 9060 XT (16GB) @ **£{baseline:.2f}**")
st.caption("Baseline price is updated every 24 hours from UK retail stock.")

# 2. GPU Data & Calculation Logic
gpus = [
    {"Name": "Radeon RX 9060 XT (16GB)", "RWA": 1.00, "Arch": 1.10, "Live": baseline},
    {"Name": "Radeon RX 7800 XT", "RWA": 1.15, "Arch": 1.00, "Live": 449.99},
    {"Name": "Radeon RX 6950 XT", "RWA": 1.35, "Arch": 0.80, "Live": 385.00},
]

results = []
for gpu in gpus:
    # Formula: (Baseline * RWA) * Arch_Mod
    mpp = (baseline * gpu["RWA"]) * gpu["Arch"]
    verdict = "✅ DEAL" if gpu["Live"] <= mpp else "❌ NO DEAL"
    
    results.append({
        "Card Name": gpu["Name"],
        "Calculated MPP": f"£{mpp:.2f}",
        "Market Price": f"£{gpu['Live']:.2f}",
        "Verdict": verdict
    })

# 3. Render Dashboard
df = pd.DataFrame(results)
st.table(df)

st.divider()

# 4. Stability Philosophy
st.header("⚡ Stability-First Philosophy")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### The Hardware Baseline
    * **Multi-Rail PSU:** Required to prevent shut-offs during RDNA transient spikes.
    * **1:1 PCIe Cables:** One separate cable per 8-pin connector. No pigtails.
    * **8+8 CPU Power:** Ensures stable rail delivery for 2025-era motherboards.
    """)

with col2:
    st.markdown("""
    #### The Value Logic
    * **Arch_Mod (1.10):** RDNA 4 gets a 10% premium for native **AV1** and **DP 2.1**.
    * **Arch_Mod (0.80):** RDNA 2 is docked 20% for lacking modern encoder support.
    * **RWA:** Weights value based on real-world resolution scaling (1440p/4K).
    """)
