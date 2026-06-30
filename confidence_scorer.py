import json
import math

class ForensicLinkageScorer:
    """
    Evaluates correlation heuristics across profile identity, behavior matrices, 
    and network structures to compute an admissibility confidence rating.
    """
    
    @staticmethod
    def evaluate_spatial_alignment(loc_a: str, loc_b: str) -> float:
        """Weight: 30 Points. Computes contextual geographic intersection."""
        if not loc_a or not loc_b or loc_a.upper() == "N/A" or loc_b.upper() == "N/A":
            return 0.0
            
        a_clean = loc_a.strip().lower()
        b_clean = loc_b.strip().lower()
        
        if a_clean == b_clean and a_clean != "":
            return 30.0
        if a_clean in b_clean or b_clean in a_clean:
            return 20.0
        return 0.0

    @staticmethod
    def evaluate_linguistic_similarity(bio_a: str, bio_b: str) -> float:
        """Sub-Weight: 20 Points. Analyzes structural text overlaps in profile bios."""
        if not bio_a or not bio_b:
            return 0.0
            
        forensic_lexicon = ["nlp", "kannada", "threat", "actor", "bangalore", "bengaluru", "node", "cyber", "infosec"]
        words_a = set(bio_a.lower().split())
        words_b = set(bio_b.lower().split())
        
        intersection = words_a.intersection(words_b)
        markers_a = [w for w in words_a if any(m in w for m in forensic_lexicon)]
        markers_b = [w for w in words_b if any(m in w for m in forensic_lexicon)]
        
        if len(intersection) > 0 or (len(markers_a) > 0 and len(markers_b) > 0):
            score = 12.0  # Base point allocation for profile alignment
            union_len = len(words_a.union(words_b))
            jaccard = len(intersection) / union_len if union_len > 0 else 0
            score += (jaccard * 8.0)
            return round(score, 2)
        return 0.0

    @staticmethod
    def evaluate_matrix_overlaps(dict_a: dict, dict_b: dict, max_points: float) -> float:
        """Sub-Weight: 10 Pts each. Generic evaluator for tracking arrays (Hashtags/Mentions)."""
        if not dict_a or not dict_b:
            return 0.0
            
        keys_a = set(dict_a.keys())
        keys_b = set(dict_b.keys())
        
        shared_elements = keys_a.intersection(keys_b)
        if not shared_elements:
            return 0.0
            
        # Give a partial baseline reward for any intersection
        score = max_points * 0.5
        # Scale up remaining points according to intersection density vs total unique entries
        total_elements = len(keys_a.union(keys_b))
        overlap_ratio = len(shared_elements) / total_elements if total_elements > 0 else 0
        score += (overlap_ratio * (max_points * 0.5))
        return round(score, 2)

    @staticmethod
    def evaluate_network_scale_ratio(metrics_a: dict, metrics_b: dict) -> float:
        """Weight: 30 Points. Gauges operational scale signatures using logarithmic gaps."""
        f_a = max(metrics_a.get("inbound_subscribers", 0), 1)
        f_b = max(metrics_b.get("inbound_subscribers", 0), 1)
        
        log_diff = abs(math.log10(f_a) - math.log10(f_b))
        if log_diff < 0.2:
            return 30.0
        elif log_diff < 0.7:
            return 20.0
        elif log_diff < 1.5:
            return 10.0
        return 5.0

    def compute_linkage_matrix(self, profile_a: dict, profile_b: dict) -> dict:
        """Aggregates all algorithmic vectors using updated clear variables."""
        
        # 1. Geographic Anchor Scoring (30 Pts Max)
        geo_score = self.evaluate_spatial_alignment(
            profile_a.get("Target_Core_Identity", {}).get("Stated_Geographic_Location", ""),
            profile_b.get("Target_Core_Identity", {}).get("Stated_Geographic_Location", "")
        )
        
        # 2. Text Content Keyword Alignment (20 Pts Max)
        bio_score = self.evaluate_linguistic_similarity(
            profile_a.get("Target_Core_Identity", {}).get("Profile_Bio_Text", ""),
            profile_b.get("Target_Core_Identity", {}).get("Profile_Bio_Text", "")
        )
        
        # Extract frequency matrices block safely
        matrices_a = profile_a.get("Behavioral_Frequency_Analysis", {})
        matrices_b = profile_b.get("Behavioral_Frequency_Analysis", {})
        
        # 3. Behavioral Timeline Hashtag Analysis (10 Pts Max)
        hashtag_score = self.evaluate_matrix_overlaps(
            matrices_a.get("Most_Used_Hashtags_Clustering", {}),
            matrices_b.get("Most_Used_Hashtags_Clustering", {}),
            max_points=10.0
        )
        
        # 4. Social Graph Communication Node Overlaps (10 Pts Max)
        mention_score = self.evaluate_matrix_overlaps(
            matrices_a.get("Most_Interacted_With_Handles", {}),
            matrices_b.get("Most_Interacted_With_Handles", {}),
            max_points=10.0
        )
        
        total_behavioral_score = round(bio_score + hashtag_score + mention_score, 2)
        
        # 5. Network Scaling Footprint Profile (30 Pts Max)
        net_score = self.evaluate_network_scale_ratio(
            profile_a.get("Platform_Volume_Metrics", {}),
            profile_b.get("Platform_Volume_Metrics", {})
        )
        
        total_linkage = round(geo_score + total_behavioral_score + net_score, 2)
        
        if total_linkage >= 70:
            confidence = "HIGH — COURT-ADMISSIBLE INFERENCE INDICATOR"
        elif total_linkage >= 45:
            confidence = "MEDIUM — STRUCTURAL NODAL COUPLING"
        else:
            confidence = "LOW — INDEPENDENT PLATFORM PRESENCE"
            
        return {
            "Overall_Linkage_Score": total_linkage,
            "Confidence_Classification": confidence,
            "Vector_Analysis_Breakdown": {
                "Geographic_Coincidence_Points": geo_score,
                "Behavioral_Fingerprint_Metrics": {
                    "Profile_Text_Alignment": bio_score,
                    "Hashtag_Clustering_Alignment": hashtag_score,
                    "Interaction_Network_Alignment": mention_score,
                    "Aggregated_Behavioral_Score": total_behavioral_score
                },
                "Network_Proximity_Points": net_score
            }
        }