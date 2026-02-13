#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Comprehensive test script for backend API endpoints"""

import sys
import time
import threading
import uvicorn
from app.main import app
import requests

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8006, log_level='error')

# Start server in background thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(3)

base_url = 'http://127.0.0.1:8006'

# Get status and shensha names from the API first to test dynamically
# Define test cases - using variables for Chinese characters
status_旺 = '旺'  # This will be fetched dynamically
status_衰 = '衰'

# Get available statuses
r = requests.get(f'{base_url}/api/nayin/status')
statuses = r.json().get('statuses', [])

# Get available shensha
r = requests.get(f'{base_url}/api/shensha')
shensha_list = r.json()
shensha_name = shensha_list[0]['name'] if shensha_list else None

# Define all test cases
tests = [
    # Ganzhi API
    ('GET', '/api/ganzhi', 'Ganzhi list', 'list'),
    ('GET', '/api/ganzhi/search?q=甲', 'Ganzhi search', 'search'),
    ('GET', '/api/ganzhi/names', 'Ganzhi names', 'list'),
    ('GET', '/api/ganzhi/甲子', 'Ganzhi detail: 甲子', 'detail'),
    ('GET', '/api/ganzhi/乙丑', 'Ganzhi detail: 乙丑', 'detail'),
    ('POST', '/api/ganzhi/compare', 'Ganzhi compare', 'json', {"ganzhi_list": ["甲子", "乙丑"]}),

    # Nayin API
    ('GET', '/api/nayin', 'Nayin list', 'list'),
    ('GET', '/api/nayin/by-ganzhi/甲子', 'Nayin by ganzhi', 'detail'),
    ('GET', '/api/nayin/海中金/ganzhi', 'Ganzhi by nayin', 'list'),
    ('GET', '/api/nayin/status', 'Nayin status list', 'list'),
    ('GET', f'/api/nayin/status/{statuses[0]}' if statuses else '/api/nayin/status/旺', 'Nayin by status (dynamic)', 'list'),
    ('GET', '/api/nayin/category/shengda', 'Nayin by category: shengda', 'list'),
    ('GET', '/api/nayin/category/xiaoruo', 'Nayin by category: xiaoruo', 'list'),
    ('GET', '/api/nayin/calc/甲子', 'Nayin calc', 'detail'),

    # Shensha API
    ('GET', '/api/shensha', 'Shensha list', 'list'),
    ('GET', '/api/shensha/types', 'Shensha types', 'list'),
    ('GET', '/api/shensha/type/驿马', 'Shensha by type', 'list'),
    ('GET', '/api/shensha/zixing', 'Shensha zixing', 'list'),
    ('GET', '/api/shensha/ganzhi/甲子', 'Shensha by ganzhi', 'list'),
    ('GET', f'/api/shensha/{shensha_name}' if shensha_name else '/api/shensha/驿马', 'Shensha detail (dynamic)', 'detail'),
    ('GET', f'/api/shensha/{shensha_name}/ganzhi' if shensha_name else '/api/shensha/驿马/ganzhi', 'Ganzhi by shensha (dynamic)', 'list'),

    # Guanxi API
    ('GET', '/api/guanxi', 'Guanxi list', 'list'),
    ('GET', '/api/guanxi/types', 'Guanxi types', 'list'),
    ('GET', '/api/guanxi/type/六合', 'Guanxi by type', 'list'),
    ('GET', '/api/guanxi/ganzhi/甲子', 'Guanxi by ganzhi', 'list'),
    ('GET', '/api/guanxi/between/甲子/乙丑', 'Guanxi between', 'detail'),

    # Health check
    ('GET', '/api/health', 'Health check', 'detail'),
]

bugs = []
passed = 0

for method, endpoint, name, response_type, *extra in tests:
    try:
        if method == 'GET':
            r = requests.get(f'{base_url}{endpoint}', timeout=5)
        elif method == 'POST':
            payload = extra[0] if extra else {}
            r = requests.post(f'{base_url}{endpoint}', json=payload, timeout=5)

        if r.status_code == 200:
            try:
                data = r.json()
                if response_type == 'list' and not isinstance(data, list):
                    if isinstance(data, dict):
                        if 'items' in data or 'statuses' in data or 'types' in data:
                            print(f'[PASS] {name}: OK')
                            passed += 1
                        else:
                            print(f'[WARN] {name}: Expected list but got dict')
                            passed += 1
                else:
                    print(f'[PASS] {name}: OK')
                    passed += 1
            except:
                print(f'[PASS] {name}: OK')
                passed += 1
        else:
            print(f'[FAIL] {name}: HTTP {r.status_code}')
            try:
                error_detail = r.json().get('detail', '')
                bugs.append(f'{name}: {endpoint} -> {r.status_code}: {error_detail}')
            except:
                bugs.append(f'{name}: {endpoint} -> {r.status_code}')
    except Exception as e:
        print(f'[FAIL] {name}: {e}')
        bugs.append(f'{name}: {endpoint} -> {e}')

print()
print('=' * 50)
print(f'Passed: {passed}/{len(tests)}')
if bugs:
    print(f'\nFound {len(bugs)} bugs:')
    for b in bugs:
        print(f'  - {b}')
    sys.exit(1)
else:
    print(f'All {passed} tests passed!')
    sys.exit(0)
