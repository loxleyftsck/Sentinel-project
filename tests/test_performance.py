"""
Performance baseline tests for SENTINEL API
Measures response times, throughput, and resource usage
"""

import time
import statistics
import requests
from concurrent.futures import ThreadPoolExecutor
import psutil
import os

# Configuration
API_URL = "http://localhost:8000/api/v1/analyze"
HEALTH_URL = "http://localhost:8000/health"
API_KEY = "dev_key_12345"

SAMPLE_TRANSACTION = {
    "transaction": {
        "date": "2024-12-30",
        "company": "BBCA",
        "insider_name": "Test User",
        "insider_role": "Director",
        "action": "buy",
        "volume": 10000,
        "price": 8500
    }
}


def measure_response_time(num_requests=10):
    """Measure average response time for single requests"""
    print("\n" + "=" * 60)
    print("TEST 1: Response Time (Sequential)")
    print("=" * 60)

    times = []
    success_count = 0

    for i in range(num_requests):
        try:
            start = time.time()
            response = requests.post(
                API_URL,
                json=SAMPLE_TRANSACTION,
                headers={"X-API-Key": API_KEY},
                timeout=30
            )
            end = time.time()

            if response.status_code == 200:
                success_count += 1
                times.append(end - start)
                print(f"Request {i+1}/{num_requests}: {(end-start):.2f}s ✓")
            else:
                print(f"Request {i+1}/{num_requests}: Failed ({response.status_code}) ✗")

        except Exception as e:
            print(f"Request {i+1}/{num_requests}: Error - {e} ✗")

    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        p95_time = sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else max_time

        print(f"\n📊 Results:")
        print(f"  Success Rate: {success_count}/{num_requests} ({success_count/num_requests*100:.1f}%)")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
        print(f"  P95: {p95_time:.2f}s")

        # Performance evaluation
        if avg_time < 2.0:
            print(f"  ✅ EXCELLENT (Target: <2s)")
        elif avg_time < 3.0:
            print(f"  ✅ GOOD (Target: <3s)")
        elif avg_time < 5.0:
            print(f"  ⚠️  ACCEPTABLE (Target: <5s)")
        else:
            print(f"  ❌ NEEDS OPTIMIZATION")

        return {
            "avg": avg_time,
            "min": min_time,
            "max": max_time,
            "p95": p95_time,
            "success_rate": success_count / num_requests
        }

    return None


def measure_concurrent_performance(num_workers=5, num_requests=20):
    """Measure performance under concurrent load"""
    print("\n" + "=" * 60)
    print(f"TEST 2: Concurrent Requests ({num_workers} workers)")
    print("=" * 60)

    def make_request():
        try:
            start = time.time()
            response = requests.post(
                API_URL,
                json=SAMPLE_TRANSACTION,
                headers={"X-API-Key": API_KEY},
                timeout=30
            )
            end = time.time()
            return {
                "success": response.status_code == 200,
                "time": end - start,
                "status": response.status_code
            }
        except Exception as e:
            return {"success": False, "time": 0, "error": str(e)}

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [f.result() for f in futures]

    total_time = time.time() - start_time

    success_count = sum(1 for r in results if r.get("success"))
    times = [r["time"] for r in results if r.get("success")]

    print(f"\n📊 Results:")
    print(f"  Total Time: {total_time:.2f}s")
    print(f"  Success Rate: {success_count}/{num_requests} ({success_count/num_requests*100:.1f}%)")
    print(f"  Throughput: {num_requests/total_time:.2f} req/s")

    if times:
        print(f"  Avg Response: {statistics.mean(times):.2f}s")
        print(f"  Max Response: {max(times):.2f}s")

    # Evaluation
    throughput = num_requests / total_time
    if throughput >= 10:
        print(f"  ✅ GOOD THROUGHPUT (≥10 req/s)")
    elif throughput >= 5:
        print(f"  ⚠️  ACCEPTABLE THROUGHPUT (≥5 req/s)")
    else:
        print(f"  ❌ LOW THROUGHPUT")

    return {
        "throughput": throughput,
        "success_rate": success_count / num_requests,
        "total_time": total_time
    }


def measure_health_check_performance():
    """Measure health check endpoint performance"""
    print("\n" + "=" * 60)
    print("TEST 3: Health Check Performance")
    print("=" * 60)

    times = []
    for i in range(20):
        start = time.time()
        response = requests.get(HEALTH_URL, timeout=5)
        end = time.time()
        times.append(end - start)

    avg_time = statistics.mean(times)
    print(f"\n📊 Results:")
    print(f"  Average: {avg_time*1000:.0f}ms")

    if avg_time < 0.1:
        print(f"  ✅ EXCELLENT (<100ms)")
    elif avg_time < 0.5:
        print(f"  ✅ GOOD (<500ms)")
    else:
        print(f"  ⚠️  SLOW")

    return avg_time


def measure_memory_usage():
    """Measure memory usage during testing"""
    print("\n" + "=" * 60)
    print("TEST 4: Resource Usage")
    print("=" * 60)

    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()

    print(f"\n📊 Current Process:")
    print(f"  Memory (RSS): {mem_info.rss / 1024 / 1024:.1f} MB")
    print(f"  Memory (VMS): {mem_info.vms / 1024 / 1024:.1f} MB")

    # Try to get system memory
    try:
        system_mem = psutil.virtual_memory()
        print(f"\n📊 System Memory:")
        print(f"  Total: {system_mem.total / 1024 / 1024 / 1024:.1f} GB")
        print(f"  Available: {system_mem.available / 1024 / 1024 / 1024:.1f} GB")
        print(f"  Used: {system_mem.percent:.1f}%")
    except:
        pass

    return mem_info.rss / 1024 / 1024  # MB


def run_all_tests():
    """Run complete performance test suite"""
    print("\n" + "=" * 80)
    print("SENTINEL API - PERFORMANCE BASELINE TEST")
    print("=" * 80)
    print(f"Target API: {API_URL}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    results = {}

    # Test 1: Response Time
    results["response_time"] = measure_response_time(10)

    # Test 2: Concurrent Performance
    results["concurrent"] = measure_concurrent_performance(5, 20)

    # Test 3: Health Check
    results["health_check"] = measure_health_check_performance()

    # Test 4: Memory
    results["memory_mb"] = measure_memory_usage()

    # Summary
    print("\n" + "=" * 80)
    print("PERFORMANCE BASELINE SUMMARY")
    print("=" * 80)

    if results.get("response_time"):
        rt = results["response_time"]
        print(f"\n✅ Response Time:")
        print(f"   Average: {rt['avg']:.2f}s")
        print(f"   P95: {rt['p95']:.2f}s")
        print(f"   Success: {rt['success_rate']*100:.1f}%")

    if results.get("concurrent"):
        ct = results["concurrent"]
        print(f"\n✅ Throughput:")
        print(f"   {ct['throughput']:.2f} requests/second")
        print(f"   Success: {ct['success_rate']*100:.1f}%")

    print(f"\n✅ Health Check:")
    print(f"   {results['health_check']*1000:.0f}ms average")

    print(f"\n✅ Memory Usage:")
    print(f"   {results['memory_mb']:.1f} MB")

    # Overall Assessment
    print("\n" + "=" * 80)
    print("ASSESSMENT")
    print("=" * 80)

    passing_tests = 0
    total_tests = 0

    # Check response time
    total_tests += 1
    if results.get("response_time") and results["response_time"]["avg"] < 3.0:
        print("✅ Response Time: PASS (< 3s)")
        passing_tests += 1
    else:
        print("❌ Response Time: NEEDS OPTIMIZATION")

    # Check throughput
    total_tests += 1
    if results.get("concurrent") and results["concurrent"]["throughput"] >= 5:
        print("✅ Throughput: PASS (≥ 5 req/s)")
        passing_tests += 1
    else:
        print("❌ Throughput: NEEDS OPTIMIZATION")

    # Check success rate
    total_tests += 1
    if results.get("response_time") and results["response_time"]["success_rate"] > 0.95:
        print("✅ Reliability: PASS (> 95%)")
        passing_tests += 1
    else:
        print("❌ Reliability: NEEDS OPTIMIZATION")

    print(f"\nOverall: {passing_tests}/{total_tests} tests passed")

    if passing_tests == total_tests:
        print("🎉 ALL PERFORMANCE TARGETS MET!")
    elif passing_tests >= total_tests * 0.66:
        print("⚠️  ACCEPTABLE FOR MVP")
    else:
        print("❌ OPTIMIZATION REQUIRED")

    print("=" * 80)

    return results


if __name__ == "__main__":
    try:
        results = run_all_tests()

        # Save results to file
        import json
        with open("performance_baseline.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\n💾 Results saved to: performance_baseline.json")

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
