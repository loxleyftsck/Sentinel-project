"""
Test FastAPI Backend with Analysis Endpoint
"""
import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "dev-key-12345"  # From .env.example

def test_health_check():
    """Test health endpoint"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root_endpoint():
    """Test root endpoint"""
    print("=" * 60)
    print("TEST 2: Root Endpoint")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_analysis_without_auth():
    """Test analysis endpoint without authentication"""
    print("=" * 60)
    print("TEST 3: Analysis WITHOUT Auth (Should Fail)")
    print("=" * 60)

    payload = {
        "transaction": {
            "date": "2024-12-29T10:00:00",
            "company": "BBCA",
            "insider_name": "John Doe",
            "insider_role": "Director",
            "action": "SELL",
            "volume": 150000,
            "price": 9500
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=payload
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_analysis_with_auth():
    """Test analysis endpoint with authentication"""
    print("=" * 60)
    print("TEST 4: Analysis WITH Auth (Should Work)")
    print("=" * 60)

    payload = {
        "transaction": {
            "date": "2024-12-29T10:00:00",
            "company": "BBCA",
            "insider_name": "John Doe",
            "insider_role": "Director",
            "action": "SELL",
            "volume": 150000,
            "price": 9500
        }
    }

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=payload,
        headers=headers
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

    if response.status_code == 200:
        data = response.json()
        print("✅ ANALYSIS SUCCESS!")
        print(f"   Transaction ID: {data['transaction_id']}")
        print(f"   Alerts: {len(data['alerts'])}")
        print(f"   Risk Score: {data['risk_score']:.2f}")
        print(f"   Processing Time: {data['processing_time']:.2f}s")
        print()

def test_rate_limiting():
    """Test rate limiting (should block after 10 requests)"""
    print("=" * 60)
    print("TEST 5: Rate Limiting (10 req/min)")
    print("=" * 60)

    headers = {"X-API-Key": API_KEY}
    payload = {
        "transaction": {
            "date": "2024-12-29T10:00:00",
            "company": "BBCA",
            "insider_name": "Test",
            "insider_role": "Director",
            "action": "BUY",
            "volume": 1000,
            "price": 9500
        }
    }

    print("Sending 12 requests rapidly...")
    for i in range(1, 13):
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json=payload,
            headers=headers
        )
        print(f"Request {i}: Status {response.status_code}")

        if response.status_code == 429:
            print("✅ RATE LIMIT WORKING! Request blocked.")
            break
    print()

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 SENTINEL API - Comprehensive Test Suite")
    print("=" * 60)
    print()

    try:
        # Basic tests
        test_health_check()
        test_root_endpoint()

        # Security tests
        test_analysis_without_auth()
        test_analysis_with_auth()

        # Rate limiting test
        # test_rate_limiting()  # Commented to avoid hitting limit

        print("=" * 60)
        print("✅ ALL TESTS COMPLETE!")
        print("=" * 60)

    except requests.ConnectionError:
        print("❌ ERROR: Could not connect to API server")
        print("   Make sure server is running: python -m sentinel.api.main")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
