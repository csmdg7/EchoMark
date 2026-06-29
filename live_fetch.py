import os
import sys
import json
import requests

RAPIDAPI_HOST = "twitter-x.p.rapidapi.com"
API_KEYS = [
    "b687f2bd7bmsh3c4d05108f2ee57p151801jsn84b2e8763bc3", 
    "PASTE_YOUR_SECOND_FREE_ACCOUNT_KEY_HERE"
]

VAULT_DIR = "evidence_vault"
os.makedirs(VAULT_DIR, exist_ok=True)

def fetch_live_profile(username: str):
    clean_username = username.strip().lstrip("@").lower()
    clean_output_path = os.path.join(VAULT_DIR, f"{clean_username}_clean_report.json")
    
    # Cache layer protection
    if os.path.exists(clean_output_path):
        print(f"[+][CACHE] Local case record located for @{clean_username}. Loading from disk...")
        with open(clean_output_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"https://{RAPIDAPI_HOST}/user/details"
    querystring = {"username": clean_username}
    
    for entry_idx, active_key in enumerate(API_KEYS):
        if active_key.startswith("PASTE_"): continue
            
        print(f"[*][INGESTION] Querying active registry for @{clean_username} using Slot [{entry_idx}]...")
        headers = {"x-rapidapi-key": active_key, "x-rapidapi-host": RAPIDAPI_HOST}
        
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            if response.status_code == 200:
                raw_json = response.json()
                
                # Save raw payload for forensic integrity
                with open(os.path.join(VAULT_DIR, f"{clean_username}_raw.json"), "w", encoding="utf-8") as f:
                    json.dump(raw_json, f, indent=4, ensure_ascii=False)
                
                user_data = raw_json.get("data", {}).get("user", {}).get("result", {})
                legacy = user_data.get("legacy", {})
                
                clean_report = {
                    "subject_handle": clean_username,
                    "display_alias": legacy.get("name", "N/A"),
                    "biographical_manifest": legacy.get("description", "N/A"),
                    "reported_geographic_anchor": legacy.get("location", "Unknown Location"),
                    "metrics": {
                        "outbound_connections": legacy.get("friends_count", 0),
                        "inbound_subscribers": legacy.get("followers_count", 0),
                        "total_broadcasted_transmissions": legacy.get("statuses_count", 0)
                    }
                }
                
                with open(clean_output_path, "w", encoding="utf-8") as f:
                    json.dump(clean_report, f, indent=4, ensure_ascii=False)
                print(f"[+][INGESTION SUCCESS] Profile locked for @{clean_username}.")
                return clean_report
            elif response.status_code in [429, 403]:
                print(f"[!][RATE] Slot [{entry_idx}] exhausted. Rotating token...")
                continue
        except Exception as e:
            print(f"[!] Interruption on slot [{entry_idx}]: {e}")
            
    print("[!] CRITICAL: Out of live authorization options.")
    return None

if __name__ == "__main__":
    print("======================================================")
    print("       FORENSIC TARGET EXTRACTION INTERFACE           ")
    print("======================================================\n")
    
    # Check if a username was typed in the terminal command line
    if len(sys.argv) > 1:
        target_username = sys.argv[1]
    else:
        # Fallback interactive prompt if you just type 'python live_fetch.py'
        target_username = input("Enter target X handle to profile: ")
        
    if target_username.strip():
        report = fetch_live_profile(target_username)
        if report:
            print(f"\n[+] Processing complete. Target data structured successfully.")