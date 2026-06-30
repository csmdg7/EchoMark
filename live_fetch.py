import os
import sys
import json
import requests
import re
from datetime import datetime

RAPIDAPI_HOST = "twitter-x.p.rapidapi.com"
API_KEYS = [
    "b687f2bd7bmsh3c4d05108f2ee57p151801jsn84b2e8763bc3",
    "PASTE_YOUR_SECOND_FREE_ACCOUNT_KEY_HERE"
]

# 🗂️ Clean Subdirectory Matrix Architecture
VAULT_DIR = "evidence_vault"
RAW_CACHE_DIR = os.path.join(VAULT_DIR, ".raw_cache")
CLEAN_REPORT_DIR = os.path.join(VAULT_DIR, ".clean_report")

os.makedirs(RAW_CACHE_DIR, exist_ok=True)
os.makedirs(CLEAN_REPORT_DIR, exist_ok=True)

def fetch_live_profile(username: str):
    clean_username = username.strip().lstrip("@").lower()
    
    # Updated Clean Pathing Configuration
    clean_output_path = os.path.join(CLEAN_REPORT_DIR, f"{clean_username}.json")
    raw_output_path = os.path.join(RAW_CACHE_DIR, f"{clean_username}.json")
    
    # 💾 Local Cache Verification Check
    if os.path.exists(clean_output_path):
        print(f"[+][CACHE] Criminal dossier successfully re-loaded from local vault for @{clean_username}.")
        with open(clean_output_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"https://{RAPIDAPI_HOST}/user/details"
    querystring = {"username": clean_username}
    
    for entry_idx, active_key in enumerate(API_KEYS):
        if active_key.startswith("PASTE_"): continue
            
        print(f"[*][INTEL] Scanning digital footprint markers for target: @{clean_username}...")
        headers = {"x-rapidapi-key": active_key, "x-rapidapi-host": RAPIDAPI_HOST}
        
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            
            if response.status_code == 404:
                print(f"[!] Target Not Found: The handle @{clean_username} does not exist on X.")
                return None
                
            if response.status_code == 200:
                raw_json = response.json()
                
                user_result = raw_json.get("data", {}).get("user", {}).get("result", {})
                if not user_result or user_result.get("__typename") == "UserUnavailable":
                    print(f"[!] Access Restriction: @{clean_username} is currently suspended, deactivated, or deleted.")
                    return None
                
                # 📥 Commits raw API JSON packet cleanly to the hidden cache subfolder
                with open(raw_output_path, "w", encoding="utf-8") as f:
                    json.dump(raw_json, f, indent=4, ensure_ascii=False)
                
                legacy = user_result.get("legacy", {})
                is_protected = legacy.get("protected", False)
                privacy_status = "PRIVATE (Timeline History Encrypted/Hidden)" if is_protected else "PUBLIC (Open Timeline Access)"
                
                investigative_location = legacy.get("location", "").strip() or "NOT SPECIFIED BY USER"
                investigative_bio = legacy.get("description", "").strip() or "BLANK PROFILE BIO"
                
                extracted_tweets = []
                all_hashtags = []
                all_mentions = []
                
                # 🛡️ Criminal Timeline Fingerprinting Arrays
                device_source_frequency = {}
                hourly_activity_profile = {str(hour).zfill(2) + ":00": 0 for hour in range(24)}
                
                timeline_tweets = raw_json.get("tweets", [])
                if isinstance(timeline_tweets, list) and not is_protected:
                    for tweet in timeline_tweets:
                        if isinstance(tweet, dict):
                            text = tweet.get("full_text") or tweet.get("text") or tweet.get("body")
                            if text:
                                # Regular expression sweeps
                                hashtags = re.findall(r"#(\w+)", text)
                                mentions = re.findall(r"@(\w+)", text)
                                all_hashtags.extend([h.lower() for h in hashtags])
                                all_mentions.extend([m.lower() for m in mentions])
                                
                                # 📱 1. Client Source Tracking (Device Signatures)
                                source_html = tweet.get("source", "Unknown Device")
                                device_match = re.search(r'>(.*?)</a>', source_html)
                                device_string = device_match.group(1) if device_match else source_html
                                device_source_frequency[device_string] = device_source_frequency.get(device_string, 0) + 1
                                
                                # ⏰ 2. Temporal Activity Processing (Sleep/Wake Cycle Anchor)
                                raw_time = tweet.get("created_at") # Format: "Wed May 24 15:43:22 +0000 2023"
                                try:
                                    # Parse string into python datetime object to isolate UTC broadcast hour
                                    parsed_time = datetime.strptime(raw_time, "%a %b %d %H:%M:%S %z %Y")
                                    hour_key = f"{str(parsed_time.hour).zfill(2)}:00"
                                    hourly_activity_profile[hour_key] += 1
                                except Exception:
                                    pass
                                
                                # 🛰️ 3. Precise GPS Coordinate Mapping Lookups
                                raw_geo = tweet.get("geo") or {}
                                raw_place = tweet.get("place") or {}
                                gps_coordinates = "NOT DETECTED (Mobile GPS Disabled)"
                                verified_city = "Not Tagged"
                                
                                if isinstance(raw_geo, dict) and raw_geo.get("coordinates"):
                                    coords = raw_geo.get("coordinates")
                                    gps_coordinates = f"LAT: {coords[0]}, LON: {coords[1]}"
                                if isinstance(raw_place, dict) and raw_place.get("full_name"):
                                    verified_city = raw_place.get("full_name")

                                extracted_tweets.append({
                                    "Tweet_ID": tweet.get("id_str", "N/A"),
                                    "Broadcast_Timestamp": raw_time,
                                    "Message_Content": text,
                                    "Device_Hardware_Source": device_string,
                                    "Geospatial_Footprint": {
                                        "Precise_GPS_Coordinates": gps_coordinates,
                                        "Verified_Location_Tag": verified_city
                                    }
                                })

                hashtag_frequency = {h: all_hashtags.count(h) for h in set(all_hashtags)}
                mention_frequency = {m: all_mentions.count(m) for m in set(all_mentions)}

                nested_handles = re.findall(r"@(\w+)", investigative_bio)
                cross_linked_pivots = {}
                for handle in nested_handles:
                    h_lower = handle.lower()
                    cross_linked_pivots[f"@{handle}"] = {
                        "Direct_Web_Link": f"https://x.com/{h_lower}",
                        "Investigator_Pivot_Command": f"python main.py [current_target] {h_lower}"
                    }

                # 👤 RETAINS CLEAN INVESTIGATOR-FIRST DICTIONARY VARIABLES
                investigative_report = {
                    "Case_Evidentiary_Metadata": {
                        "Permanent_Platform_ID_Number": user_result.get("rest_id", "N/A"),
                        "Account_Creation_Date": legacy.get("created_at", "N/A"),
                        "Privacy_Enforcement_Level": privacy_status,
                        "Premium_Verification_Status": "YES (Verified Badge)" if user_result.get("is_blue_verified", False) else "NO (Unverified)",
                        "Direct_Source_Verification_URL": f"https://x.com/{clean_username}"
                    },
                    "Target_Core_Identity": {
                        "Target_Username": clean_username,
                        "Target_Display_Name": legacy.get("name", "N/A"),
                        "Profile_Bio_Text": investigative_bio,
                        "Stated_Geographic_Location": investigative_location,
                        "Associated_External_Link": legacy.get("url") or "None Listed"
                    },
                    "Profile_Image_Assets": {
                        "Avatar_Image_Link": legacy.get("profile_image_url_https", ""),
                        "Header_Banner_Link": legacy.get("profile_banner_url") or "No custom header banner uploaded"
                    },
                    "Platform_Volume_Metrics": {
                        "Following_Count_Outbound": legacy.get("friends_count", 0),
                        "Followers_Count_Inbound": legacy.get("followers_count", 0),
                        "Total_Broadcast_Posts_Count": legacy.get("statuses_count", 0),
                        "Media_Uploads_Count": legacy.get("media_count", 0)
                    },
                    "Bio_Discovered_Network_Pivots": {
                        "Alternative_Handles_Found_In_Bio": nested_handles,
                        "Actionable_FollowUp_Links": cross_linked_pivots
                    },
                    "Behavioral_Frequency_Analysis": {
                        "Most_Used_Hashtags_Clustering": dict(sorted(hashtag_frequency.items(), key=lambda item: item[1], reverse=True)[:10]),
                        "Most_Interacted_With_Handles": dict(sorted(mention_frequency.items(), key=lambda item: item[1], reverse=True)[:10]),
                        "Hardware_Device_Signatures": dict(sorted(device_source_frequency.items(), key=lambda item: item[1], reverse=True)[:5]),
                        "Temporal_Hourly_Post_Profile_UTC": hourly_activity_profile
                    },
                    "Captured_Public_Timeline_Data": "No public posts available for private/protected accounts." if is_protected else extracted_tweets
                }
                
                # 💾 Write the final clean file cleanly to the dedicated clean folder
                with open(clean_output_path, "w", encoding="utf-8") as f:
                    json.dump(investigative_report, f, indent=4, ensure_ascii=False)
                print(f"[+][SUCCESS] Humanized data dossier exported to: {clean_output_path}")
                return investigative_report
                
            elif response.status_code in [429, 403]:
                print(f"[!][RATE] Key Slot [{entry_idx}] exhausted. Rotating parameters...")
                continue
        except Exception as e:
            print(f"[!] Access connection anomaly on key slot [{entry_idx}]: {e}")
            
    print("[!] CRITICAL: Investigative query terminated. All api lines exhausted.")
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_username = sys.argv[1]
    else:
        target_username = input("Enter target X handle to profile: ")
    if target_username.strip():
        fetch_live_profile(target_username)