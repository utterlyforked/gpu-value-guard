import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def scrape_scan_uk():
    """
    Scrapes Scan.co.uk for the lowest 9060 XT 16GB price.
    Returns: (price, url) tuple or None if failed.
    """
    url = "https://www.scan.co.uk/shop/computer-hardware/gpu-amd-gaming/amd-radeon-rx-9060-xt-16gb-graphics-cards"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.content, "html.parser")

        # Extracts prices from 'price' class spans
        tags = soup.find_all("span", class_="price")
        prices = [float(re.sub(r'[^\d.]', '', t.text)) for t in tags if t.text]

        if prices:
            return (min(prices), url)
    except Exception:
        pass
    return None


def scrape_overclockers_uk():
    """
    Scrapes Overclockers UK for the lowest 9060 XT 16GB price.
    Returns: (price, url) tuple or None if failed.
    """
    url = "https://www.overclockers.co.uk/pc-components/graphics-cards/amd/radeon-rx-9060-xt"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.content, "html.parser")

        # Try common price selectors for Overclockers
        price_patterns = [
            soup.find_all("span", class_="price"),
            soup.find_all("p", class_="price"),
            soup.find_all(string=re.compile(r'£\d+\.\d{2}'))
        ]

        prices = []
        for pattern in price_patterns:
            for element in pattern:
                text = element if isinstance(element, str) else element.text
                matches = re.findall(r'£?(\d+\.\d{2})', text)
                prices.extend([float(m) for m in matches])

        if prices:
            return (min(prices), url)
    except Exception:
        pass
    return None


def scrape_ebuyer_uk():
    """
    Scrapes eBuyer UK for the lowest 9060 XT 16GB price.
    Returns: (price, url) tuple or None if failed.
    """
    url = "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD/subcat/AMD-Radeon-RX-9060-XT"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.content, "html.parser")

        # Try common price selectors
        price_tags = soup.find_all(["span", "p", "div"], class_=re.compile(r'price', re.I))
        prices = []

        for tag in price_tags:
            matches = re.findall(r'£?(\d+\.\d{2})', tag.text)
            prices.extend([float(m) for m in matches])

        if prices:
            return (min(prices), url)
    except Exception:
        pass
    return None


@st.cache_data(ttl="24h")
def get_daily_baseline():
    """
    Scrapes multiple UK retailers for the lowest 9060 XT 16GB price.
    Returns: (price, url, retailer_name) tuple.
    Default: (330.00, None, 'Fallback') if all scrapers fail.
    """
    retailers = [
        ("Scan.co.uk", scrape_scan_uk),
        ("Overclockers UK", scrape_overclockers_uk),
        ("eBuyer UK", scrape_ebuyer_uk),
    ]

    results = []

    for retailer_name, scraper_func in retailers:
        result = scraper_func()
        if result:
            price, url = result
            results.append((price, url, retailer_name))

    # Return the lowest price found across all retailers
    if results:
        return min(results, key=lambda x: x[0])

    # Fallback if all scrapers fail
    return (330.00, None, "Fallback")
