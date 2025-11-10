import requests
from flask import request

def get_client_ip():
    """
    Get the client's IP address from the request.
    Handles proxy headers like X-Forwarded-For.
    """
    if request.headers.get('X-Forwarded-For'):
        # Get the first IP in the chain (client IP)
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    
    return ip

def get_location_from_ip(ip_address):
    """
    Get location information from IP address using ip-api.com (free service).
    Returns a dictionary with location data.
    
    Note: This service is free but has rate limits (45 requests/minute).
    For production with high traffic, consider upgrading to a paid service.
    """
    if not ip_address or ip_address == '127.0.0.1' or ip_address.startswith('192.168.'):
        # Local/private IP addresses
        return {
            'country': 'Local',
            'region': 'Local',
            'city': 'Local',
            'latitude': None,
            'longitude': None
        }
    
    try:
        # Using ip-api.com free tier
        response = requests.get(
            f'http://ip-api.com/json/{ip_address}',
            timeout=3
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon')
                }
    except Exception as e:
        print(f"[WARNING] Geolocation lookup failed: {e}")
    
    # Return empty data if lookup fails
    return {
        'country': None,
        'region': None,
        'city': None,
        'latitude': None,
        'longitude': None
    }
