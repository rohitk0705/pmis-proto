"""Basic tests for the internship matching system."""

import unittest
from src.models import Candidate, Internship, SocialCategory, DistrictType, Sector
from src.matcher import InternshipMatcher
from src.sample_data import create_sample_candidates, create_sample_internships


class TestInternshipMatcher(unittest.TestCase):
    """Test cases for the InternshipMatcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.matcher = InternshipMatcher()
        self.candidates = create_sample_candidates()
        self.internships = create_sample_internships()
    
    def test_matcher_initialization(self):
        """Test that the matcher initializes correctly."""
        self.assertIsNotNone(self.matcher)
        self.assertFalse(self.matcher._fitted)
    
    def test_sample_data_loading(self):
        """Test that sample data loads correctly."""
        self.assertEqual(len(self.candidates), 5)
        self.assertEqual(len(self.internships), 5)
        
        # Check that all candidates have required fields
        for candidate in self.candidates:
            self.assertIsNotNone(candidate.id)
            self.assertIsNotNone(candidate.name)
            self.assertIsInstance(candidate.skills, list)
            self.assertIsInstance(candidate.cgpa, float)
    
    def test_matching_algorithm(self):
        """Test that the matching algorithm produces results."""
        matches = self.matcher.match_candidates(self.candidates, self.internships)
        
        # Should produce some matches
        self.assertGreater(len(matches), 0)
        
        # Check that matches have valid scores
        for match in matches:
            self.assertIsNotNone(match.candidate_id)
            self.assertIsNotNone(match.internship_id)
            self.assertGreaterEqual(match.total_score(), 0.0)
            self.assertLessEqual(match.total_score(), 1.0)
    
    def test_skill_matching(self):
        """Test skill matching functionality."""
        # Create test candidate and internship with overlapping skills
        candidate = Candidate(
            id="TEST_C",
            name="Test Candidate",
            skills=["Python", "Machine Learning"],
            qualifications=["BTech"],
            location="Mumbai",
            preferred_locations=["Mumbai"],
            sector_interests=[Sector.TECHNOLOGY],
            social_category=SocialCategory.GENERAL,
            district_type=DistrictType.URBAN,
            past_internships=[],
            cgpa=8.0,
            experience_months=6,
            languages=["English"]
        )
        
        internship = Internship(
            id="TEST_I",
            title="Test Internship",
            company="Test Company",
            sector=Sector.TECHNOLOGY,
            required_skills=["Python", "Data Analysis"],
            preferred_qualifications=["BTech"],
            location="Mumbai",
            remote_allowed=False,
            duration_months=6,
            stipend=25000,
            capacity=5,
            filled_positions=0,
            min_cgpa=7.0,
            min_experience_months=0,
            preferred_social_categories=[SocialCategory.GENERAL],
            rural_quota_percentage=10.0
        )
        
        skill_score = self.matcher._calculate_skill_match(candidate, internship)
        self.assertGreater(skill_score, 0.0)
    
    def test_affirmative_action_boost(self):
        """Test that affirmative action boost works correctly."""
        # Rural candidate should get boost
        rural_candidate = self.candidates[3]  # Ramesh Yadav - rural OBC
        self.assertEqual(rural_candidate.district_type, DistrictType.RURAL)
        
        internship = self.internships[2]  # Rural Development Intern
        boost = self.matcher._calculate_affirmative_action_boost(rural_candidate, internship)
        
        # Should get boost for rural district, social category, and no past internships
        self.assertGreater(boost, 0.3)  # At minimum should get rural boost
    
    def test_capacity_constraint(self):
        """Test capacity constraint checking."""
        # Test internship with available capacity
        available_internship = self.internships[0]  # Software Engineering - 5/10 filled
        self.assertTrue(self.matcher._check_capacity_constraint(available_internship))
        
        # Create internship at full capacity
        full_internship = Internship(
            id="FULL",
            title="Full Internship",
            company="Full Company",
            sector=Sector.TECHNOLOGY,
            required_skills=["Test"],
            preferred_qualifications=["Test"],
            location="Test",
            remote_allowed=False,
            duration_months=6,
            stipend=25000,
            capacity=5,
            filled_positions=5,  # Full capacity
            min_cgpa=7.0,
            min_experience_months=0,
            preferred_social_categories=[SocialCategory.GENERAL],
            rural_quota_percentage=10.0
        )
        
        self.assertFalse(self.matcher._check_capacity_constraint(full_internship))
    
    def test_top_matches_for_candidate(self):
        """Test getting top matches for a specific candidate."""
        matches = self.matcher.match_candidates(self.candidates, self.internships)
        
        candidate_id = self.candidates[0].id  # Priya Sharma
        top_matches = self.matcher.get_top_matches_for_candidate(candidate_id, matches, top_k=3)
        
        self.assertLessEqual(len(top_matches), 3)
        
        # Check that matches are sorted by score (descending)
        for i in range(len(top_matches) - 1):
            self.assertGreaterEqual(top_matches[i].total_score(), top_matches[i + 1].total_score())
    
    def test_top_candidates_for_internship(self):
        """Test getting top candidates for a specific internship."""
        matches = self.matcher.match_candidates(self.candidates, self.internships)
        
        internship_id = self.internships[0].id  # Software Engineering Intern
        top_candidates = self.matcher.get_top_candidates_for_internship(internship_id, matches, top_k=3)
        
        self.assertLessEqual(len(top_candidates), 3)
        
        # Check that candidates are sorted by score (descending)
        for i in range(len(top_candidates) - 1):
            self.assertGreaterEqual(top_candidates[i].total_score(), top_candidates[i + 1].total_score())
    
    def test_rural_quota_enforcement(self):
        """Test that rural quota is properly enforced."""
        matches = self.matcher.match_candidates(self.candidates, self.internships)
        
        # Find matches for Rural Development Intern (50% rural quota)
        rural_internship_id = "I103"
        rural_matches = [m for m in matches if m.internship_id == rural_internship_id]
        
        # Should have matches
        self.assertGreater(len(rural_matches), 0)
        
        # Check that rural candidates are prioritized
        candidates_dict = {c.id: c for c in self.candidates}
        rural_candidates = []
        non_rural_candidates = []
        
        for match in rural_matches:
            candidate = candidates_dict[match.candidate_id]
            if candidate.district_type in [DistrictType.RURAL, DistrictType.ASPIRATIONAL]:
                rural_candidates.append(match)
            else:
                non_rural_candidates.append(match)
        
        # Should have rural candidates in the matches
        self.assertGreater(len(rural_candidates), 0)


if __name__ == '__main__':
    unittest.main()