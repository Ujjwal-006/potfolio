"""
Live Smoke Test Script:
Boots uvicorn server in a subprocess, executes httpx calls against all endpoints,
verifies status codes and SQLite database persistence, and checks server logs for errors.
"""
import json
import os
import subprocess
import sys
import time
import httpx

BASE_URL = "http://127.0.0.1:8000"
DB_FILE = "portfolio.db"

def run_smoke_tests():
    print("=" * 60)
    print("STARTING LIVE SMOKE TESTS")
    print("=" * 60)

    # 1. Start uvicorn server process
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--log-level", "info"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Wait for server to boot
    print("Waiting for server to boot on 127.0.0.1:8000...")
    ready = False
    for attempt in range(20):
        time.sleep(0.5)
        try:
            r = httpx.get(f"{BASE_URL}/health", timeout=2.0)
            if r.status_code == 200:
                ready = True
                print(f"Server is live! Health status: {r.json()}")
                break
        except Exception:
            pass

    if not ready:
        server_process.terminate()
        stdout, stderr = server_process.communicate()
        print("Server failed to start. Stdout:", stdout)
        print("Stderr:", stderr)
        sys.exit(1)

    failures = []

    # 2. Test HTML Page Routes
    html_routes = [
        "/",
        "/hero_page.html",
        "/about",
        "/about_me.html",
        "/projects",
        "/project.html",
        "/experience",
        "/contect_and_match_record.html",
        "/contact",
        "/transfer_desk.html",
        "/attributes",
        "/atribute.html",
    ]

    print("\n--- Testing HTML Page Delivery ---")
    for route in html_routes:
        url = f"{BASE_URL}{route}"
        try:
            res = httpx.get(url, timeout=5.0)
            if res.status_code == 200 and "text/html" in res.headers.get("content-type", ""):
                print(f"[PASS] {route} -> 200 OK (length: {len(res.text)} bytes)")
            else:
                msg = f"[FAIL] {route} -> expected 200 text/html, got {res.status_code}"
                print(msg)
                failures.append(msg)
        except Exception as e:
            msg = f"[ERROR] {route} -> {e}"
            print(msg)
            failures.append(msg)

    # 3. Test Valid Form Submission (POST -> 200)
    print("\n--- Testing Valid Form Submission ---")
    valid_payload = {
        "caller_name": "Ujjwal (Ujjwal's Scout Agent)",
        "caller_org": "Ujjwal Strategic Scouting",
        "caller_email": "ujjwalturkar2006@gmail.com",
        "engagement_type": "lead-architect",
        "contract_terms": "Engage as lead 3D WebGL graphics architect for live Premier League stadium kiosks.",
    }
    try:
        res = httpx.post(f"{BASE_URL}/api/transfer-inquiries", json=valid_payload, timeout=5.0)
        if res.status_code == 200:
            data = res.json()
            print(f"[PASS] POST /api/transfer-inquiries -> 200 OK (Created ID: {data.get('id')})")
        else:
            msg = f"[FAIL] Valid POST expected 200, got {res.status_code}: {res.text}"
            print(msg)
            failures.append(msg)
    except Exception as e:
        msg = f"[ERROR] Valid POST -> {e}"
        print(msg)
        failures.append(msg)

    # 4. Test Missing Required Field (POST -> 422)
    print("\n--- Testing Missing Required Field ---")
    invalid_missing_payload = {
        # caller_name omitted
        "caller_org": "Tactical Enterprise",
        "caller_email": "agent@tactical.dev",
        "engagement_type": "contract-webgl",
        "contract_terms": "Shader audit request",
    }
    try:
        res = httpx.post(f"{BASE_URL}/api/transfer-inquiries", json=invalid_missing_payload, timeout=5.0)
        if res.status_code == 422:
            print(f"[PASS] Missing Field POST -> 422 Unprocessable Entity as expected")
        else:
            msg = f"[FAIL] Missing field expected 422, got {res.status_code}: {res.text}"
            print(msg)
            failures.append(msg)
    except Exception as e:
        msg = f"[ERROR] Missing field POST -> {e}"
        print(msg)
        failures.append(msg)

    # 5. Test Invalid Email Format (POST -> 422)
    print("\n--- Testing Invalid Email Format ---")
    invalid_email_payload = {
        "caller_name": "Carlo Ancelotti",
        "caller_email": "carlo-not-an-email",
        "engagement_type": "advisory",
        "contract_terms": "European nights review",
    }
    try:
        res = httpx.post(f"{BASE_URL}/api/transfer-inquiries", json=invalid_email_payload, timeout=5.0)
        if res.status_code == 422:
            print(f"[PASS] Invalid Email POST -> 422 Unprocessable Entity as expected")
        else:
            msg = f"[FAIL] Invalid email expected 422, got {res.status_code}: {res.text}"
            print(msg)
            failures.append(msg)
    except Exception as e:
        msg = f"[ERROR] Invalid email POST -> {e}"
        print(msg)
        failures.append(msg)

    # 6. Test Dynamic Endpoints
    print("\n--- Testing Dynamic Endpoints ---")
    dynamic_endpoints = ["/api/projects", "/api/records", "/api/attributes", "/api/download-cv"]
    for ep in dynamic_endpoints:
        try:
            res = httpx.get(f"{BASE_URL}{ep}", timeout=5.0)
            if res.status_code == 200:
                print(f"[PASS] {ep} -> 200 OK")
            else:
                msg = f"[FAIL] {ep} expected 200, got {res.status_code}"
                print(msg)
                failures.append(msg)
        except Exception as e:
            msg = f"[ERROR] {ep} -> {e}"
            print(msg)
            failures.append(msg)

    # 7. Terminate server and inspect logs
    print("\nShutting down server process...")
    server_process.terminate()
    try:
        stdout, stderr = server_process.communicate(timeout=3.0)
    except subprocess.TimeoutExpired:
        server_process.kill()
        stdout, stderr = server_process.communicate()

    print("\n--- Server Process Stderr Log Summary ---")
    for line in stderr.splitlines():
        if "ERROR" in line or "Traceback" in line:
            msg = f"[LOG ERROR] {line}"
            print(msg)
            failures.append(msg)
        elif "INFO" in line:
            print(line)

    # 8. Check Database Persistence
    print("\n--- Verifying SQLite Persistence ---")
    import sqlite3
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, caller_name, caller_email, engagement_type FROM transfer_inquiries ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row and row[1] == "Ujjwal (Ujjwal's Scout Agent)":
        print(f"[PASS] SQLite verification: row id={row[0]}, name={row[1]}, email={row[2]}")
    else:
        msg = f"[FAIL] SQLite verification: expected saved row with name 'Ujjwal (Ujjwal's Scout Agent)', got {row}"
        print(msg)
        failures.append(msg)

    print("\n" + "=" * 60)
    if not failures:
        print("ALL LIVE SMOKE TESTS PASSED PERFECTLY! (0 FAILURES)")
        print("=" * 60)
        return 0
    else:
        print(f"SMOKE TESTS FAILED WITH {len(failures)} ISSUE(S):")
        for f in failures:
            print(" -", f)
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(run_smoke_tests())
