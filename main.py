import os
import sys
import json
from live_fetch import fetch_live_profile
from confidence_scorer import ForensicLinkageScorer

def main():
    print("======================================================")
    print("    OSINT CROSS-PROFILE LINKAGE ANALYTICS WORKSTATION  ")
    print("======================================================\n")

    # Step 1: Capture command-line inputs or fall back to user prompts dynamically
    args = sys.argv[1:]
    
    if len(args) == 0:
        # Prompt for the primary suspect
        primary = input("Enter primary subject handle: ").strip()
        if not primary:
            print("[!] Error: A primary target handle is required.")
            return
        # Prompt for an optional secondary suspect
        secondary = input("Enter secondary verification handle (Leave blank for single profile scan): ").strip()
    elif len(args) == 1:
        primary = args[0]
        secondary = ""
    else:
        primary = args[0]
        secondary = args[1]

    # Clean the input handles
    target_a = primary.lstrip("@").lower()
    target_b = secondary.lstrip("@").lower() if secondary else ""

    # Step 2: Process Primary Target
    print(f"\n[*] Launching phase 1 investigation on: @{target_a}")
    profile_a = fetch_live_profile(target_a)
    
    if not profile_a:
        print(f"[!] Critical Failure: Unable to parse target profile [@{target_a}] payload. Pipeline stopped.")
        return

    # Step 3: Check if this is a Single Profile Scan or a Pairwise Linkage Scan
    if not target_b:
        print("\n" + "="*50)
        print(f"📊 ACTIONABLE INTELLIGENCE DOSSIER SUMMARY: @{target_a}")
        print("="*50)
        
        meta = profile_a["Case_Evidentiary_Metadata"]
        identity = profile_a["Target_Core_Identity"]
        metrics = profile_a["Platform_Volume_Metrics"]
        analysis = profile_a["Behavioral_Frequency_Analysis"]
        
        print(f"[+] Unique System ID : {meta['Permanent_Platform_ID_Number']}")
        print(f"[+] Account Age      : {meta['Account_Creation_Date']}")
        print(f"[+] Privacy Status   : {meta['Privacy_Enforcement_Level']}")
        print(f"[+] Location Anchor  : {identity['Stated_Geographic_Location']}")
        print(f"[+] Bio Manifest     : {identity['Profile_Bio_Text']}")
        print(f"[+] Following Count  : {metrics['Following_Count_Outbound']}")
        print(f"[+] Followers Count  : {metrics['Followers_Count_Inbound']}")
        print(f"[+] Hardware Devices : {json.dumps(analysis['Hardware_Device_Signatures'])}")
        print(f"\n[+] Comprehensive analytical file stored cleanly in: evidence_vault/.clean_report/{target_a}.json")
        print("======================================================")
        return

    # Step 4: Process Secondary Target (Only runs if a second handle was provided)
    print(f"\n[*] Launching phase 2 investigation on: @{target_b}")
    profile_b = fetch_live_profile(target_b)
    
    if not profile_b:
        print(f"[!] Critical Failure: Unable to parse target profile [@{target_b}] payload. Pipeline stopped.")
        return

    # Step 5: Run Correlation Matrix Scoring Engine
    print("\n" + "="*50)
    print("⚙️ EXECUTING CORRELATION MATRIX ALGORITHMIC SCORING")
    print("="*50)
    
    scorer = ForensicLinkageScorer()
    linkage_report = scorer.compute_linkage_matrix(profile_a, profile_b)
    
    # Format and save the combined comparison report to the vault root
    comparison_filename = f"{target_a}_{target_b}_linkage_matrix.json"
    comparison_path = os.path.join("evidence_vault", comparison_filename)
    
    with open(comparison_path, "w", encoding="utf-8") as f:
        json.dump(linkage_report, f, indent=4, ensure_ascii=False)
        
    print(json.dumps(linkage_report, indent=4))
    print("="*50)
    print(f"[+] Admissibility Linkage matrix report written to: {comparison_path}")

if __name__ == "__main__":
    main()