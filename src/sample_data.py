"""Sample data for testing the internship matching system."""

from .models import Candidate, Internship, SocialCategory, DistrictType, Sector


def create_sample_candidates():
    """Create sample candidate data."""
    return [
        Candidate(
            id="C001",
            name="Priya Sharma",
            skills=["Python", "Machine Learning", "Data Analysis", "SQL"],
            qualifications=["BTech Computer Science", "Machine Learning Certification"],
            location="Mumbai",
            preferred_locations=["Mumbai", "Pune", "Bangalore"],
            sector_interests=[Sector.TECHNOLOGY, Sector.FINANCE],
            social_category=SocialCategory.GENERAL,
            district_type=DistrictType.URBAN,
            past_internships=[],
            cgpa=8.5,
            experience_months=6,
            languages=["Hindi", "English", "Marathi"]
        ),
        Candidate(
            id="C002",
            name="Arjun Kumar",
            skills=["Java", "Spring Boot", "React", "Database Design"],
            qualifications=["BTech Information Technology"],
            location="Patna",
            preferred_locations=["Delhi", "Gurgaon", "Noida", "Patna"],
            sector_interests=[Sector.TECHNOLOGY, Sector.GOVERNMENT],
            social_category=SocialCategory.SC,
            district_type=DistrictType.ASPIRATIONAL,
            past_internships=[],
            cgpa=7.8,
            experience_months=3,
            languages=["Hindi", "English", "Bhojpuri"]
        ),
        Candidate(
            id="C003",
            name="Sneha Patel",
            skills=["Finance", "Excel", "Data Visualization", "Risk Analysis"],
            qualifications=["BCom Finance", "CFA Level 1"],
            location="Ahmedabad",
            preferred_locations=["Mumbai", "Ahmedabad", "Pune"],
            sector_interests=[Sector.FINANCE, Sector.TECHNOLOGY],
            social_category=SocialCategory.OBC,
            district_type=DistrictType.URBAN,
            past_internships=["I001"],
            cgpa=8.2,
            experience_months=4,
            languages=["Gujarati", "Hindi", "English"]
        ),
        Candidate(
            id="C004",
            name="Ramesh Yadav",
            skills=["Agriculture", "Research", "Data Collection", "Rural Development"],
            qualifications=["BSc Agriculture", "Rural Development Certificate"],
            location="Banda",
            preferred_locations=["Lucknow", "Kanpur", "Banda"],
            sector_interests=[Sector.AGRICULTURE, Sector.GOVERNMENT, Sector.NGO],
            social_category=SocialCategory.OBC,
            district_type=DistrictType.RURAL,
            past_internships=[],
            cgpa=7.5,
            experience_months=2,
            languages=["Hindi", "English"]
        ),
        Candidate(
            id="C005",
            name="Kavya Reddy",
            skills=["Healthcare", "Medical Research", "Patient Care", "Data Analysis"],
            qualifications=["MBBS", "Healthcare Management Certificate"],
            location="Hyderabad",
            preferred_locations=["Hyderabad", "Chennai", "Bangalore"],
            sector_interests=[Sector.HEALTHCARE, Sector.NGO],
            social_category=SocialCategory.GENERAL,
            district_type=DistrictType.URBAN,
            past_internships=["I002", "I003"],
            cgpa=9.1,
            experience_months=12,
            languages=["Telugu", "English", "Hindi"]
        )
    ]


def create_sample_internships():
    """Create sample internship data."""
    return [
        Internship(
            id="I101",
            title="Software Engineering Intern",
            company="TechCorp India",
            sector=Sector.TECHNOLOGY,
            required_skills=["Python", "Java", "React", "Database"],
            preferred_qualifications=["BTech Computer Science", "BTech IT"],
            location="Bangalore",
            remote_allowed=True,
            duration_months=6,
            stipend=25000,
            capacity=10,
            filled_positions=5,
            min_cgpa=7.0,
            min_experience_months=0,
            preferred_social_categories=[SocialCategory.SC, SocialCategory.ST],
            rural_quota_percentage=20.0
        ),
        Internship(
            id="I102",
            title="Data Science Intern",
            company="FinanceAI Solutions",
            sector=Sector.FINANCE,
            required_skills=["Python", "Machine Learning", "Data Analysis", "SQL"],
            preferred_qualifications=["BTech", "MTech", "Statistics"],
            location="Mumbai",
            remote_allowed=False,
            duration_months=4,
            stipend=30000,
            capacity=5,
            filled_positions=2,
            min_cgpa=8.0,
            min_experience_months=3,
            preferred_social_categories=[SocialCategory.GENERAL, SocialCategory.OBC],
            rural_quota_percentage=15.0
        ),
        Internship(
            id="I103",
            title="Rural Development Intern",
            company="Bharat Rural Foundation",
            sector=Sector.NGO,
            required_skills=["Rural Development", "Research", "Data Collection", "Agriculture"],
            preferred_qualifications=["BSc Agriculture", "Rural Development", "Social Work"],
            location="Lucknow",
            remote_allowed=False,
            duration_months=3,
            stipend=15000,
            capacity=8,
            filled_positions=1,
            min_cgpa=6.5,
            min_experience_months=0,
            preferred_social_categories=[SocialCategory.SC, SocialCategory.ST, SocialCategory.OBC],
            rural_quota_percentage=50.0
        ),
        Internship(
            id="I104",
            title="Healthcare Analytics Intern",
            company="MedTech Innovations",
            sector=Sector.HEALTHCARE,
            required_skills=["Healthcare", "Data Analysis", "Medical Research", "Statistics"],
            preferred_qualifications=["MBBS", "Healthcare Management", "Biostatistics"],
            location="Hyderabad",
            remote_allowed=True,
            duration_months=5,
            stipend=28000,
            capacity=6,
            filled_positions=2,
            min_cgpa=8.5,
            min_experience_months=6,
            preferred_social_categories=[SocialCategory.GENERAL],
            rural_quota_percentage=10.0
        ),
        Internship(
            id="I105",
            title="Government Policy Intern",
            company="Ministry of Rural Development",
            sector=Sector.GOVERNMENT,
            required_skills=["Policy Analysis", "Research", "Public Administration", "Data Analysis"],
            preferred_qualifications=["Public Administration", "Political Science", "Economics"],
            location="Delhi",
            remote_allowed=False,
            duration_months=6,
            stipend=20000,
            capacity=12,
            filled_positions=8,
            min_cgpa=7.5,
            min_experience_months=2,
            preferred_social_categories=[SocialCategory.SC, SocialCategory.ST, SocialCategory.OBC],
            rural_quota_percentage=30.0
        )
    ]