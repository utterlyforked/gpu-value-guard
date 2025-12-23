# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Streamlit web application that calculates the "Maximum Purchase Price" (MPP) for AMD Radeon GPUs based on a dynamic market baseline. The baseline is the RX 9060 XT (16GB), scraped daily from UK retailers. The MPP formula weights GPUs by resolution performance and penalizes legacy architectures lacking modern features (AV1 encoding, DisplayPort 2.1).

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

### Two-Module Design

**1. `streamlit_app.py` (Main UI)**
- Entry point for the application
- Fetches baseline price via `get_daily_baseline()` from scraper module
- Defines GPU configurations with Resolution Weighted Average (RWA) and Architecture modifiers
- Calculates MPP using formula: `(Baseline * RWA) * Arch_Modifier`
- Renders results table and displays verdict (DEAL vs NO DEAL)

**2. `scraper.py` (Data Collection)**
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

### MPP Calculation Logic

**Formula:** `MPP = (Baseline_Price * Resolution_Weight) * Architecture_Modifier`

**Architecture Modifiers (hardcoded in streamlit_app.py:24-26):**
- RDNA 4 (9000 Series): 1.10 - Premium for AV1 encoding and DP 2.1
- RDNA 3 (7000 Series): 1.00 - Standard baseline
- RDNA 2 (6000 Series): 0.80 - 20% penalty for lacking modern features

**Resolution Weighted Average (RWA):**
- Represents relative performance across resolutions
- Higher RWA = higher acceptable price ceiling
- Example: RX 7800 XT has RWA of 1.15 (15% faster than baseline)

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
- Add to `gpu_configs` list in streamlit_app.py:23-27
- Required fields: Name, RWA (resolution weight), Arch (architecture modifier), Live (current market price)
- MPP calculated automatically in loop at streamlit_app.py:32-33

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
