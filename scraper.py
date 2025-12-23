import requests
from bs4 import BeautifulSoup
import re
import streamlit as st

@st.cache_data(ttl="24h")
def get_baseline_price():
    """
    Scrapes the RX 9060 XT (16GB) price from Scan.co.uk.
    TTL is set to 24h to prevent redundant requests.
    """
    url = "https://www.scan.co.uk/shop/computer-hardware/gpu-amd-gaming/amd-radeon-rx-9060-xt-16gb-graphics-cards"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Target the price spans typically used by Scan
        price_tags = soup.find_all("span", class_="price")
        prices = [float(re.sub(r'[^\d.]', '', p.text)) for p in price_tags if p.text]
        
        # Return the lowest available price, or the 2025 baseline if none found
        return min(prices) if prices else 330.00
    except Exception:
        return 330.00 # Hardcoded 2025 Retail Baseline fallback
