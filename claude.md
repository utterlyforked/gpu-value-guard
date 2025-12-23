# 🛡️ Radeon GPU Value Index - Project Context

A Streamlit-based web application and web scraper used to calculate the "Real-World Purchase Ceiling" (MPP) for AMD Radeon GPUs based on a dynamic 2025 market baseline.

## 🎯 Project Context
- **Baseline Strategy:** RX 9060 XT (16GB) @ ~£330 (Daily Scraped).
- **Core Logic:** MPP = (Baseline × Resolution_Weight) × Arch_Modifier.
- **Goal:** Identify market deals by penalizing legacy architectures (no AV1/DP 2.1) and weighting for resolution performance.

## 🔧 Tech Stack
- **Language:** Python 3.9+
- **Frontend/UI:** Streamlit (Dashboard)
- **Scraping:** BeautifulSoup4 (Scan.co.uk target)
- **Data Handling:** Pandas
- **Caching:** Streamlit `@st.cache_data` (24-hour TTL)

## 📁 Repository Structure
- `app.py`: Main entry point. Contains the Streamlit UI, MPP formula logic, and dataframe rendering.
- `scraper.py`: Dedicated module for web scraping. Uses headers to mimic a browser and returns a `(price, url)` tuple.
- `requirements.txt`: Python dependencies (streamlit, pandas, requests, beautifulsoup4).

## 🛠️ Common Commands
- **Run Development Server:** `streamlit run app.py`
- **Install Dependencies:** `pip install -r requirements.txt`
- **Scraper Verification:** `python -c "from scraper import get_baseline_data; print(get_baseline_data())"`

## 🚨 Critical Rules & Standards
- **Scraper Etiquette:** Never scrape on every request. Always wrap scraping logic in `@st.cache_data(ttl="24h")`.
- **Pricing Format:** All monetary values must be rendered as floats and formatted to two decimal places (e.g., £330.00).
- **Architecture Modifiers:**
    - RDNA 4 (9000 Series): 1.10
    - RDNA 3 (7000 Series): 1.00
    - RDNA 2 (6000 Series): 0.80 (Penalty for lack of modern encoder/ports).
- **UI Standard:** Use `st.dataframe` with `column_config` for clickable retail links to keep the interface clean.
