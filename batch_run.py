import os
import sys
import json
import itertools
from live_fetch import fetch_live_profile
from confidence_scorer import ForensicLinkageScorer

VAULT_DIR = "evidence_vault"
CLEAN_REPORT_DIR = os.path.join(VAULT_DIR, ".clean_report")

os.makedirs(CLEAN_REPORT_DIR, exist_ok=True)

def run_batch_investigation(target_handles: list):
    """
    Automates multi-account profile ingestion and computes an 
    all-pairs cross-linkage matrix across the target cluster.
    """
    print("======================================================")
    print("     OSINT BATCH PROCESSING & COORDINATION ENGINE     ")
    print("======================================================\n")
    
    # Filter out empty entries and normalize handles
    clean_targets = list(set([h.strip().lstrip("@").lower() for h in target_handles if h.strip()]))
    
    if len(clean_targets) < 2:
        print("[!] Aborted: Batch operations require a minimum of 2 valid target profiles.")
        return

    print(f"[*] Initializing batch cluster scan for targets: {', '.join(['@'+t for t in clean_targets])}")
    
    # Step 1: Sequential Ingestion Pool
    profile_pool = {}
    for handle in clean_targets:
        print(f"\n--- Processing Target Stream: @{handle} ---")
        profile_data = fetch_live_profile(handle)
        if profile_data:
            profile_pool[handle] = profile_data
        else:
            print(f"[!] Warning: Skipping @{handle} due to profile collection failure.")

    # Check if we have enough successfully parsed accounts to do a comparison
    if len(profile_pool) < 2:
        print("\n[!] Critical Failure: Insufficient account data captured to build matrix.")
        return

    print("\n" + "="*50)
    print("⚙️ GENERATING CROSS-LINKAGE ASSESSMENT MATRIX")
    print("="*50)

    scorer = ForensicLinkageScorer()
    batch_correlations = []
    
    # Step 2: Mathematical Combinatorics Loop (Pairwise Permutations)
    for target_a, target_b in itertools.combinations(profile_pool.keys(), 2):
        print(f"[*] Correlating: @{target_a} 🔄 @{target_b}")
        
        linkage_report = scorer.compute_linkage_matrix(profile_pool[target_a], profile_pool[target_b])
        
        # Synchronized keys matching Title_Case scoring outputs
        batch_correlations.append({
            "Pair": [target_a, target_b],
            "Linkage_Percentage_Score": linkage_report["Overall_Linkage_Score"],
            "Forensic_Classification": linkage_report["Confidence_Classification"],
            "Algorithmic_Breakdown": linkage_report["Vector_Analysis_Breakdown"]
        })

    # Step 3: Compile Consolidated Master Dossier
    master_batch_report = {
        "Batch_Metadata": {
            "Total_Monitored_Nodes": len(profile_pool),
            "Total_Computed_Edges": len(batch_correlations),
            "Cluster_Scope": list(profile_pool.keys())
        },
        "Computed_Linkage_Matrix": sorted(batch_correlations, key=lambda x: x["Linkage_Percentage_Score"], reverse=True)
    }

    # Step 4: Write Consolidation File to Disk Cache
    cluster_id = "_".join(sorted(list(profile_pool.keys())[:3])) 
    report_filename = f"batch_cluster_{cluster_id}.json"
    report_path = os.path.join(VAULT_DIR, report_filename)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(master_batch_report, f, indent=4, ensure_ascii=False)

    print("\n" + "📊" + " " + "BATCH MATRIX COMPUTATION PAYLOAD")
    print(json.dumps(master_batch_report, indent=4))
    print("="*60)
    print(f"[+] Master cluster briefing file successfully exported to: {report_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        raw_input = input("Enter target handles separated by spaces (e.g., nasa isro microsoft): ")
        targets = raw_input.split()
        
    run_batch_investigation(targets)