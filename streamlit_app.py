import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime
from scraper import get_daily_baseline

__version__ = "1.1.0"  # Multi-retailer support with source links

def get_git_version():
    """
    Retrieves version info from Git repository.
    Returns: (commit_hash, commit_date, branch) or fallback version string.
    """
    try:
        # Get short commit hash
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()

        # Get commit date
        commit_timestamp = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ct'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        commit_date = datetime.fromtimestamp(int(commit_timestamp)).strftime('%Y-%m-%d %H:%M')

        # Get current branch
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()

        return f"v{__version__} ({commit_hash} on {branch}, {commit_date})"
    except Exception:
        # Fallback if not in a git repo or git not available
        return f"v{__version__}"

st.set_page_config(page_title="Radeon Value Index", layout="centered")

# 1. Fetch Baseline
baseline_price, baseline_url, baseline_retailer = get_daily_baseline()

st.title("🛡️ Radeon Value Index (UK)")

# Display baseline with source link
if baseline_url:
    st.write(f"**Baseline:** RX 9060 XT (16GB) @ **£{baseline_price:.2f}** from [{baseline_retailer}]({baseline_url})")
else:
    st.write(f"**Baseline:** RX 9060 XT (16GB) @ **£{baseline_price:.2f}** ({baseline_retailer})")

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

# 5. Version Footer
st.divider()
st.caption(f"Radeon Value Index {get_git_version()}")
