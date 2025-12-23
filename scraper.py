import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

@st.cache_data(ttl="24h")
def get_daily_baseline():
    """
    Scrapes Scan.co.uk for the lowest 9060 XT 16GB price.
    Target: 2025 Retail Baseline. Default: £330.
    """
    url = "https://www.scan.co.uk/shop/computer-hardware/gpu-amd-gaming/amd-radeon-rx-9060-xt-16gb-graphics-cards"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Extracts prices from 'price' class spans
        tags = soup.find_all("span", class_="price")
        prices = [float(re.sub(r'[^\d.]', '', t.text)) for t in tags if t.text]
        
        return min(prices) if prices else 330.00
    except Exception:
        return 330.00 # Fallback default
