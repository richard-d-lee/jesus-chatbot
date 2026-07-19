"""
Restore exported user-location data to the live site.

Usage:
    python scripts/restore_locations.py <export.json> [--url https://www.jesus.express]

Requires the ADMIN_API_KEY environment variable (or you'll be prompted).
Safe to run repeatedly: the server deduplicates on import.
"""
import argparse
import getpass
import json
import os
import sys

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('export_file', help='JSON file produced by GET /api/admin/locations')
    parser.add_argument('--url', default='https://www.jesus.express', help='Base URL of the deployment')
    args = parser.parse_args()

    api_key = os.environ.get('ADMIN_API_KEY') or getpass.getpass('Admin API key: ')

    with open(args.export_file, encoding='utf-8') as fh:
        data = json.load(fh)

    locations = data.get('locations', [])
    if not locations:
        sys.exit('No locations found in export file.')

    print(f"Importing {len(locations)} locations to {args.url} ...")
    response = requests.post(
        f'{args.url}/api/admin/locations/import',
        headers={'X-Admin-Key': api_key, 'Content-Type': 'application/json'},
        json={'locations': locations},
        timeout=120
    )
    print(response.status_code, response.text[:500])


if __name__ == '__main__':
    main()
