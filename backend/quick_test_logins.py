import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

USERS = [
    {"role": "ADMIN", "email": "admin@transformiq.local", "name": "Sarah Connor"},
    {"role": "PROJECT_OWNER", "email": "owner@transformiq.local", "name": "Elena Rostova"},
    {"role": "BUSINESS_ANALYST", "email": "analyst@transformiq.local", "name": "Priya Sharma"},
    {"role": "SOLUTION_ARCHITECT", "email": "architect@transformiq.local", "name": "David Chen"},
    {"role": "MANAGER", "email": "manager@transformiq.local", "name": "Marcus Vance"},
    {"role": "MEMBER", "email": "member@transformiq.local", "name": "Liam Murphy"},
    {"role": "VIEWER", "email": "viewer@transformiq.local", "name": "Victoria Stone"},
]

PASSWORD = "TransformIQ@2026"

def make_req(endpoint, method="GET", data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}
    except Exception as ex:
        return 500, {"error": str(ex)}

print("Testing all logins:")
tokens = {}
for u in USERS:
    s, r = make_req("/auth/login", method="POST", data={"email": u["email"], "password": PASSWORD})
    if s == 200 and r.get("success"):
        tokens[u["role"]] = r["data"]["token"]["access_token"]
        print(f"  [OK] {u['role']:<20} -> {u['email']} | User: {r['data']['user']['full_name']}")
    else:
        print(f"  [ERR] {u['role']:<20} -> {u['email']} | Status: {s} | Resp: {r}")
    sys.stdout.flush()

if len(tokens) == len(USERS):
    print("\nALL 7 ACCOUNTS LOGGED IN SUCCESSFULLY!")
