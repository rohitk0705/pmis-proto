"""AI/ML matching algorithm for internship matching system."""

import numpy as np
from typing import List, Dict, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from .models import Candidate, Internship, Match, SocialCategory, DistrictType, Sector


class InternshipMatcher:
    """AI/ML-based internship matching system."""
    
    def __init__(self):
        self.skill_vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.qualification_vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.scaler = StandardScaler()
        self._fitted = False
    
    def _calculate_skill_match(self, candidate: Candidate, internship: Internship) -> float:
        """Calculate skill match score using TF-IDF and cosine similarity."""
        candidate_skills_text = ' '.join(candidate.skills).lower()
        required_skills_text = ' '.join(internship.required_skills).lower()
        
        if not candidate_skills_text or not required_skills_text:
            return 0.0
        
        try:
            # Create TF-IDF vectors
            texts = [candidate_skills_text, required_skills_text]
            tfidf_matrix = self.skill_vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return max(0.0, similarity)
        except Exception:
            # Fallback to simple overlap calculation
            candidate_skills_set = set(skill.lower() for skill in candidate.skills)
            required_skills_set = set(skill.lower() for skill in internship.required_skills)
            
            if not required_skills_set:
                return 1.0
            
            overlap = len(candidate_skills_set.intersection(required_skills_set))
            return overlap / len(required_skills_set)
    
    def _calculate_qualification_match(self, candidate: Candidate, internship: Internship) -> float:
        """Calculate qualification match score."""
        candidate_quals_text = ' '.join(candidate.qualifications).lower()
        preferred_quals_text = ' '.join(internship.preferred_qualifications).lower()
        
        if not preferred_quals_text:
            return 1.0  # No specific qualifications required
        
        if not candidate_quals_text:
            return 0.0
        
        try:
            texts = [candidate_quals_text, preferred_quals_text]
            tfidf_matrix = self.qualification_vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return max(0.0, similarity)
        except Exception:
            # Fallback to simple overlap
            candidate_quals_set = set(qual.lower() for qual in candidate.qualifications)
            preferred_quals_set = set(qual.lower() for qual in internship.preferred_qualifications)
            
            overlap = len(candidate_quals_set.intersection(preferred_quals_set))
            return overlap / len(preferred_quals_set) if preferred_quals_set else 1.0
    
    def _calculate_location_preference_score(self, candidate: Candidate, internship: Internship) -> float:
        """Calculate location preference score."""
        # Perfect match for remote work
        if internship.remote_allowed:
            return 1.0
        
        # Check if internship location matches candidate's preferred locations
        preferred_locations_lower = [loc.lower() for loc in candidate.preferred_locations]
        internship_location_lower = internship.location.lower()
        
        if internship_location_lower in preferred_locations_lower:
            return 1.0
        
        # Check if candidate's current location matches internship location
        if candidate.location.lower() == internship_location_lower:
            return 0.8
        
        # Partial match for similar regions/states (simplified)
        for pref_loc in preferred_locations_lower:
            if pref_loc in internship_location_lower or internship_location_lower in pref_loc:
                return 0.6
        
        return 0.2  # Low score for location mismatch
    
    def _calculate_sector_interest_score(self, candidate: Candidate, internship: Internship) -> float:
        """Calculate sector interest score."""
        candidate_sectors = [sector.value for sector in candidate.sector_interests]
        return 1.0 if internship.sector.value in candidate_sectors else 0.3
    
    def _calculate_eligibility_score(self, candidate: Candidate, internship: Internship) -> float:
        """Calculate basic eligibility score."""
        eligibility_score = 1.0
        
        # CGPA requirement
        if candidate.cgpa < internship.min_cgpa:
            eligibility_score *= 0.2
        
        # Experience requirement
        if candidate.experience_months < internship.min_experience_months:
            eligibility_score *= 0.5
        
        return eligibility_score
    
    def _calculate_affirmative_action_boost(self, candidate: Candidate, internship: Internship) -> float:
        """Calculate affirmative action boost score."""
        boost = 0.0
        
        # Rural/aspirational district boost
        if candidate.district_type in [DistrictType.RURAL, DistrictType.ASPIRATIONAL]:
            boost += 0.3
        
        # Social category boost
        if candidate.social_category in internship.preferred_social_categories:
            boost += 0.2
        
        # Boost for candidates with fewer past internships (diversity in participation)
        if len(candidate.past_internships) == 0:
            boost += 0.2
        elif len(candidate.past_internships) <= 1:
            boost += 0.1
        
        return min(boost, 1.0)
    
    def _check_capacity_constraint(self, internship: Internship) -> bool:
        """Check if internship has available capacity."""
        return internship.filled_positions < internship.capacity
    
    def _apply_rural_quota(self, matches: List[Match], internships: Dict[str, Internship], 
                          candidates: Dict[str, Candidate]) -> List[Match]:
        """Apply rural quota constraints to matches."""
        # Group matches by internship
        internship_matches = {}
        for match in matches:
            if match.internship_id not in internship_matches:
                internship_matches[match.internship_id] = []
            internship_matches[match.internship_id].append(match)
        
        final_matches = []
        
        for internship_id, internship_match_list in internship_matches.items():
            internship = internships[internship_id]
            available_positions = internship.capacity - internship.filled_positions
            
            if available_positions <= 0:
                continue
            
            # Calculate rural quota positions
            rural_positions = int(available_positions * internship.rural_quota_percentage / 100)
            general_positions = available_positions - rural_positions
            
            # Sort matches by total score
            sorted_matches = sorted(internship_match_list, key=lambda m: m.total_score(), reverse=True)
            
            # Separate rural and non-rural candidates
            rural_matches = []
            non_rural_matches = []
            
            for match in sorted_matches:
                candidate = candidates[match.candidate_id]
                if candidate.district_type in [DistrictType.RURAL, DistrictType.ASPIRATIONAL]:
                    rural_matches.append(match)
                else:
                    non_rural_matches.append(match)
            
            # Select matches respecting quotas
            selected_matches = []
            
            # Fill rural quota first
            selected_matches.extend(rural_matches[:rural_positions])
            
            # Fill remaining positions from general pool
            remaining_positions = available_positions - len(selected_matches)
            if remaining_positions > 0:
                # Can use remaining rural candidates + non-rural candidates
                remaining_candidates = rural_matches[rural_positions:] + non_rural_matches
                remaining_candidates.sort(key=lambda m: m.total_score(), reverse=True)
                selected_matches.extend(remaining_candidates[:remaining_positions])
            
            final_matches.extend(selected_matches)
        
        return final_matches
    
    def match_candidates(self, candidates: List[Candidate], internships: List[Internship]) -> List[Match]:
        """
        Main method to match candidates with internships using AI/ML algorithms.
        
        Args:
            candidates: List of candidate profiles
            internships: List of internship opportunities
            
        Returns:
            List of matches sorted by relevance score
        """
        matches = []
        
        # Convert to dictionaries for efficient lookup
        candidates_dict = {c.id: c for c in candidates}
        internships_dict = {i.id: i for i in internships}
        
        # Filter internships with available capacity
        available_internships = [i for i in internships if self._check_capacity_constraint(i)]
        
        # Calculate matches for each candidate-internship pair
        for candidate in candidates:
            for internship in available_internships:
                # Calculate individual scores
                skill_score = self._calculate_skill_match(candidate, internship)
                qualification_score = self._calculate_qualification_match(candidate, internship)
                location_score = self._calculate_location_preference_score(candidate, internship)
                sector_score = self._calculate_sector_interest_score(candidate, internship)
                eligibility_score = self._calculate_eligibility_score(candidate, internship)
                affirmative_boost = self._calculate_affirmative_action_boost(candidate, internship)
                
                # Create match object
                match = Match(
                    candidate_id=candidate.id,
                    internship_id=internship.id,
                    match_score=0.0,  # Will be calculated by total_score()
                    skill_match_score=skill_score,
                    location_preference_score=location_score,
                    sector_interest_score=sector_score,
                    affirmative_action_boost=affirmative_boost,
                    eligibility_score=eligibility_score
                )
                
                # Only include matches with reasonable scores
                if match.total_score() > 0.3:  # Threshold for meaningful matches
                    matches.append(match)
        
        # Sort matches by total score
        matches.sort(key=lambda m: m.total_score(), reverse=True)
        
        # Apply affirmative action constraints (rural quota, etc.)
        final_matches = self._apply_rural_quota(matches, internships_dict, candidates_dict)
        
        return final_matches
    
    def get_top_matches_for_candidate(self, candidate_id: str, matches: List[Match], top_k: int = 5) -> List[Match]:
        """Get top K matches for a specific candidate."""
        candidate_matches = [m for m in matches if m.candidate_id == candidate_id]
        candidate_matches.sort(key=lambda m: m.total_score(), reverse=True)
        return candidate_matches[:top_k]
    
    def get_top_candidates_for_internship(self, internship_id: str, matches: List[Match], top_k: int = 10) -> List[Match]:
        """Get top K candidates for a specific internship."""
        internship_matches = [m for m in matches if m.internship_id == internship_id]
        internship_matches.sort(key=lambda m: m.total_score(), reverse=True)
        return internship_matches[:top_k]