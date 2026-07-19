import time
import logging
import threading
import requests
from flask import request

logger = logging.getLogger(__name__)

# Cache geolocation results per IP so repeat messages from the same visitor
# don't re-hit ip-api.com (free tier: 45 req/min) or add request latency.
_geo_cache = {}
_geo_cache_lock = threading.Lock()
GEO_CACHE_TTL = 24 * 3600  # seconds
GEO_CACHE_MAX = 5000

_EMPTY = {
    'country': None,
    'region': None,
    'city': None,
    'latitude': None,
    'longitude': None
}


def get_client_ip():
    """
    Get the client's IP address. ProxyFix (configured in main.py) has already
    resolved X-Forwarded-For from the trusted proxy, so remote_addr is the
    real client IP and can't be spoofed by request headers.
    """
    return request.remote_addr


def get_location_from_ip(ip_address):
    """
    Get location information from IP address using ip-api.com (free service).
    Results are cached for 24h per IP.
    """
    if not ip_address or ip_address == '127.0.0.1' or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        return {
            'country': 'Local',
            'region': 'Local',
            'city': 'Local',
            'latitude': None,
            'longitude': None
        }

    now = time.time()
    with _geo_cache_lock:
        cached = _geo_cache.get(ip_address)
        if cached and now - cached[0] < GEO_CACHE_TTL:
            return cached[1]

    result = dict(_EMPTY)
    try:
        response = requests.get(
            f'http://ip-api.com/json/{ip_address}',
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                result = {
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon')
                }
    except Exception as e:
        logger.warning("Geolocation lookup failed: %s", e)

    with _geo_cache_lock:
        if len(_geo_cache) >= GEO_CACHE_MAX:
            _geo_cache.clear()
        _geo_cache[ip_address] = (now, result)

    return result
