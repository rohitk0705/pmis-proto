"""Data models for the internship matching system."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class SocialCategory(Enum):
    """Social categories for affirmative action."""
    GENERAL = "general"
    OBC = "obc"
    SC = "sc"
    ST = "st"
    EWS = "ews"


class DistrictType(Enum):
    """District classification for affirmative action."""
    RURAL = "rural"
    ASPIRATIONAL = "aspirational"
    URBAN = "urban"


class Sector(Enum):
    """Industry sectors."""
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    MANUFACTURING = "manufacturing"
    AGRICULTURE = "agriculture"
    GOVERNMENT = "government"
    NGO = "ngo"


@dataclass
class Candidate:
    """Represents a candidate for internship."""
    id: str
    name: str
    skills: List[str]
    qualifications: List[str]
    location: str
    preferred_locations: List[str]
    sector_interests: List[Sector]
    social_category: SocialCategory
    district_type: DistrictType
    past_internships: List[str]  # List of internship IDs
    cgpa: float
    experience_months: int
    languages: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for ML processing."""
        return {
            'id': self.id,
            'skills': self.skills,
            'qualifications': self.qualifications,
            'location': self.location,
            'preferred_locations': self.preferred_locations,
            'sector_interests': [s.value for s in self.sector_interests],
            'social_category': self.social_category.value,
            'district_type': self.district_type.value,
            'past_internships_count': len(self.past_internships),
            'cgpa': self.cgpa,
            'experience_months': self.experience_months,
            'languages': self.languages
        }


@dataclass
class Internship:
    """Represents an internship opportunity."""
    id: str
    title: str
    company: str
    sector: Sector
    required_skills: List[str]
    preferred_qualifications: List[str]
    location: str
    remote_allowed: bool
    duration_months: int
    stipend: Optional[float]
    capacity: int
    filled_positions: int
    min_cgpa: float
    min_experience_months: int
    preferred_social_categories: List[SocialCategory]  # For affirmative action
    rural_quota_percentage: float  # Percentage reserved for rural candidates
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for ML processing."""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'sector': self.sector.value,
            'required_skills': self.required_skills,
            'preferred_qualifications': self.preferred_qualifications,
            'location': self.location,
            'remote_allowed': self.remote_allowed,
            'duration_months': self.duration_months,
            'stipend': self.stipend or 0,
            'available_positions': self.capacity - self.filled_positions,
            'min_cgpa': self.min_cgpa,
            'min_experience_months': self.min_experience_months,
            'rural_quota_percentage': self.rural_quota_percentage
        }


@dataclass
class Match:
    """Represents a candidate-internship match with score."""
    candidate_id: str
    internship_id: str
    match_score: float
    skill_match_score: float
    location_preference_score: float
    sector_interest_score: float
    affirmative_action_boost: float
    eligibility_score: float
    
    def total_score(self) -> float:
        """Calculate total weighted score."""
        return (
            self.skill_match_score * 0.3 +
            self.location_preference_score * 0.2 +
            self.sector_interest_score * 0.2 +
            self.eligibility_score * 0.2 +
            self.affirmative_action_boost * 0.1
        )