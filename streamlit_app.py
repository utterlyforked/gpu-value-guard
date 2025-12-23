import streamlit as st
import pandas as pd
from scraper import get_daily_baseline
from gpu_data import GPU_CONFIGS, BASELINE_GPU

st.set_page_config(page_title="Radeon Value Index", layout="centered")

# 1. Fetch Baseline
baseline_price, baseline_url, baseline_retailer = get_daily_baseline()

st.title("🛡️ Radeon Value Index (UK)")

# Display baseline with source link
if baseline_url:
    st.write(f"**Baseline:** [{BASELINE_GPU['Name']}]({BASELINE_GPU['URL']}) @ **£{baseline_price:.2f}** from [{baseline_retailer}]({baseline_url})")
else:
    st.write(f"**Baseline:** [{BASELINE_GPU['Name']}]({BASELINE_GPU['URL']}) @ **£{baseline_price:.2f}** (using default price)")
    st.caption("⚠️ Unable to fetch live pricing from retailers. Using fallback baseline.")

# 2. Calculate Value Targets
index_results = []
for gpu in GPU_CONFIGS:
    # Calculation: (Baseline * Performance Weight) * Architecture Value Retention
    value_target = (baseline_price * gpu["RWA"]) * gpu["Arch"]
    verdict = "🔥 DEAL" if gpu["Live"] <= value_target else "⚠️ NO DEAL"

    index_results.append({
        "Model": f"[{gpu['Name']}]({gpu['URL']})",
        "Value Target": f"£{value_target:.2f}",
        "Current Market": f"£{gpu['Live']:.2f}",
        "Verdict": verdict
    })

# 3. Render Table (without index column)
df = pd.DataFrame(index_results)
st.markdown(df.to_markdown(index=False))

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
