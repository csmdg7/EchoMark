import json
import math

class ForensicLinkageScorer:
    """
    Evaluates correlation heuristics across multiple target vectors 
    to establish identity linkage probabilities for CID Karnataka briefs.
    """
    
    @staticmethod
    def evaluate_spatial_alignment(loc_a: str, loc_b: str) -> float:
        """Weight: 30 Points. Computes contextual geographic intersection."""
        if not loc_a or not loc_b or loc_a.upper() == "N/A" or loc_b.upper() == "N/A":
            return 0.0 # Insufficient footprint traces
            
        a_clean = loc_a.strip().lower()
        b_clean = loc_b.strip().lower()
        
        # Absolute match (e.g., "Bengaluru, India" == "begaluru, india")
        if a_clean == b_clean and a_clean != "":
            return 30.0
            
        # Cross-regional intersection sub-strings (e.g., "Bengaluru" inside "Bengaluru, Karnataka")
        if a_clean in b_clean or b_clean in a_clean:
            return 20.0
            
        return 0.0

    @staticmethod
    def evaluate_linguistic_similarity(bio_a: str, bio_b: str) -> float:
        """Weight: 40 Points. Analyzes lexical and marker density alignments."""
        if not bio_a or not bio_b:
            return 0.0
            
        # Tactical OSINT Tracking Signatures (Case Insensitive Token Sets)
        forensic_lexicon = ["nlp", "kannada", "threat", "actor", "bangalore", "bengaluru", "node", "cyber", "infosec"]
        
        words_a = set(bio_a.lower().split())
        words_b = set(bio_b.lower().split())
        
        # Count overlaps from the strategic tracking dictionary
        markers_a = [w for w in words_a if any(marker in w for marker in forensic_lexicon)]
        markers_b = [w for w in words_b if any(marker in w for marker in forensic_lexicon)]
        
        # Calculate behavioral match based on text intersections
        intersection = words_a.intersection(words_b)
        
        if len(intersection) > 0 or (len(markers_a) > 0 and len(markers_b) > 0):
            # Base alignment reward for sharing semantic space or thematic markers
            score = 25.0
            # Scale remaining points based on true vocabulary intersection density
            jaccard_similarity = len(intersection) / len(words_a.union(words_b))
            score += (jaccard_similarity * 15.0)
            return round(score, 2)
            
        return 0.0

    @staticmethod
    def evaluate_network_scale_ratio(metrics_a: dict, metrics_b: dict) -> float:
        """Weight: 30 Points. Gauges operational scale signatures (Follower / Following scales)."""
        f_a = max(metrics_a.get("inbound_subscribers", 0), 1)
        f_b = max(metrics_b.get("inbound_subscribers", 0), 1)
        
        # Use log transformations to safely compare structural footprints across scale gaps
        log_diff = abs(math.log10(f_a) - math.log10(f_b))
        
        if log_diff < 0.2: # High scale operational mirroring
            return 30.0
        elif log_diff < 0.7:
            return 20.0
        elif log_diff < 1.5:
            return 10.0
            
        return 5.0 # Baseline residual network score

    def compute_linkage_matrix(self, profile_a: dict, profile_b: dict) -> dict:
        """Aggregates correlation metrics into a unified forensic report structure."""
        
        geo_score = self.evaluate_spatial_alignment(
            profile_a.get("reported_geographic_anchor", ""),
            profile_b.get("reported_geographic_anchor", "")
        )
        
        ling_score = self.evaluate_linguistic_similarity(
            profile_a.get("biographical_manifest", ""),
            profile_b.get("biographical_manifest", "")
        )
        
        net_score = self.evaluate_network_scale_ratio(
            profile_a.get("metrics", {}),
            profile_b.get("metrics", {})
        )
        
        total_linkage = round(geo_score + ling_score + net_score, 2)
        
        # Categorize threat probability levels cleanly for presentation slides
        if total_linkage >= 75:
            confidence = "HIGH — DIRECT INFERENCE PROBABILITY"
        elif total_linkage >= 45:
            confidence = "MEDIUM — CORRELATED NODE ACTIVITY"
        else:
            confidence = "LOW — INDEPENDENT PROFILES"
            
        return {
            "overall_linkage_score": total_linkage,
            "confidence_classification": confidence,
            "vector_breakdown": {
                "geographic_coincidence_points": geo_score,
                "dialectal_linguistic_points": ling_score,
                "network_proximity_points": net_score
            }
        }