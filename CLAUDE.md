# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Streamlit web application that calculates the "Value Target" for AMD Radeon GPUs based on a dynamic market baseline. The baseline is the RX 9060 XT (16GB), scraped daily from UK retailers. The Value Target formula weights GPUs by gaming performance and applies value retention factors based on architecture generation, helping users identify fair prices for older hardware.

**CRITICAL: 16GB VRAM Only** - This tool exclusively tracks GPUs with 16GB VRAM. VRAM capacity matters for longevity and future-proofing. Never add cards with other VRAM capacities.

**Tech Stack:**
- Python 3.9+ (specifically 3.11 in devcontainer)
- Streamlit for UI
- BeautifulSoup4 for web scraping
- Pandas for data handling
- Requests for HTTP

## Commands

**Development:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (default port 8501)
streamlit run streamlit_app.py

# Run in devcontainer (auto-configured)
# Server runs with: streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
```

**Scraper Testing:**
```bash
# Test baseline scraper manually
python -c "from scraper import get_daily_baseline; print(get_daily_baseline())"

# Test individual retailer scrapers
python -c "from scraper import scrape_scan_uk; print(scrape_scan_uk())"
python -c "from scraper import scrape_overclockers_uk; print(scrape_overclockers_uk())"
python -c "from scraper import scrape_ebuyer_uk; print(scrape_ebuyer_uk())"
```

## Architecture

### Three-Module Design

**1. `streamlit_app.py` (Main UI)**
- Entry point for the application
- Fetches baseline price via `get_daily_baseline()` from scraper module
- Imports GPU configurations from `gpu_data.py`
- Calculates Value Target using formula: `(Baseline_Price × RWA) × Arch_Modifier`
- Renders results table as markdown (no index column) with clickable AMD product links
- **RX 9060 XT is NOT in the comparison table** - it's the baseline reference only

**2. `gpu_data.py` (GPU Configuration Data)**
- Central repository for all GPU configurations (`GPU_CONFIGS` list)
- Each GPU entry contains: Name, RWA, Arch, Live price, and official AMD URL
- Stores baseline GPU information (`BASELINE_GPU`)
- **All GPUs must have 16GB VRAM** - this is enforced by design
- Easy to version control and update independently from application logic

**3. `scraper.py` (Data Collection)**
- Contains individual scraper functions for each UK retailer:
  - `scrape_scan_uk()` - Scan.co.uk
  - `scrape_overclockers_uk()` - Overclockers UK
  - `scrape_ebuyer_uk()` - eBuyer UK
- `get_daily_baseline()` orchestrates all scrapers, returns lowest price found
- Returns tuple: `(price, url, retailer_name)`
- Falls back to £330.00 if all scrapers fail
- Decorated with `@st.cache_data(ttl="24h")` to prevent excessive scraping

### Scraping Strategy

All scrapers follow the same pattern:
1. Use realistic browser headers (Chrome on Windows)
2. Parse HTML with BeautifulSoup
3. Extract prices using regex: `r'[^\d.]'` to clean, `r'£?(\d+\.\d{2})'` to find
4. Return `(min_price, url)` tuple or `None` on failure
5. Silent failure - returns `None` on any exception

The `get_daily_baseline()` function tries all retailers and selects the minimum price.

### Value Target Calculation Logic

**Formula:** `Value_Target = (Baseline_Price × Performance_Weight) × Architecture_Value_Retention`

This represents "what you should pay for this GPU considering its performance and the value loss from older architecture."

**Architecture Value Retention (hardcoded in streamlit_app.py:24-40):**
- RDNA 4 (9000 Series): 1.00 - Modern baseline (AV1 encoding, DP 2.1, FSR 4)
- RDNA 3 (7000 Series): 0.91 - 9% value penalty for lacking modern encoders/ports
- RDNA 2 (6000 Series): 0.73 - 27% value penalty for two-generation-old architecture

**Performance Weight (RWA - Resolution Weighted Average):**
- Relative gaming performance compared to RX 9060 XT baseline
- 1.00 = equal performance, 1.80 = 80% faster, 0.68 = 32% slower
- Based on real-world gaming benchmarks across multiple resolutions
- Example: RX 9070 XT has RWA of 1.80 (80% faster than baseline)

**Economic Interpretation:**
- A 6950 XT is 33% faster (RWA 1.33) but two gens old (Arch 0.73)
- Value Target = £330 × 1.33 × 0.73 = £320.66
- Despite being faster, you shouldn't pay more than the modern baseline due to architectural disadvantages

## Critical Implementation Rules

**Scraping Etiquette:**
- NEVER scrape on every request - always use 24-hour cache
- All scraping must be wrapped in `@st.cache_data(ttl="24h")`
- Use realistic browser headers to avoid blocks
- Implement graceful fallback if scrapers fail

**Pricing Display:**
- All prices formatted to 2 decimal places: `£{price:.2f}`
- Display baseline source with clickable link when available
- Show warning caption when using fallback price

**Adding New GPUs:**
- **CRITICAL: Only add 16GB VRAM cards** - verify VRAM capacity before adding
- Add to `GPU_CONFIGS` list in gpu_data.py
- Required fields:
  - `Name`: Must include "(16GB)" suffix
  - `RWA`: Performance weight (benchmark vs 9060 XT)
  - `Arch`: Architecture value retention (1.00 RDNA4, 0.91 RDNA3, 0.73 RDNA2)
  - `Live`: Current market price estimate (placeholder until eBay scraping)
  - `URL`: Official AMD product page (canonical source)
- AMD URL pattern: `https://www.amd.com/en/products/graphics/desktops/radeon/[SERIES]/amd-radeon-rx-[MODEL].html`
- **DO NOT add RX 9060 XT to GPU_CONFIGS** - it's in BASELINE_GPU only
- Group by architecture generation with comments for clarity
- Use benchmark data to determine RWA (search "RX [MODEL] vs 9060 XT benchmark")

**Adding New Retailers:**
- Create scraper function in `scraper.py` following existing pattern
- Add to `retailers` list in `get_daily_baseline()` at scraper.py:122-126
- Function must return `(price, url)` tuple or `None`
- Use consistent headers and timeout (10s)

## Deployment

Configured for GitHub Codespaces via `.devcontainer/devcontainer.json`:
- Auto-installs dependencies on container creation
- Auto-starts Streamlit server on port 8501
- Opens preview automatically with `onAutoForward: "openPreview"`
