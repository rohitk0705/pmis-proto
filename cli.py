"""Command-line interface for the internship matching system."""

import click
from typing import List
from src.models import Candidate, Internship, Match
from src.matcher import InternshipMatcher
from src.sample_data import create_sample_candidates, create_sample_internships


def print_candidate_summary(candidate: Candidate):
    """Print a summary of candidate information."""
    print(f"\n📋 Candidate: {candidate.name} (ID: {candidate.id})")
    print(f"   🎓 Qualifications: {', '.join(candidate.qualifications)}")
    print(f"   💼 Skills: {', '.join(candidate.skills)}")
    print(f"   📍 Location: {candidate.location}")
    print(f"   🎯 Preferred Locations: {', '.join(candidate.preferred_locations)}")
    print(f"   🏢 Sector Interests: {', '.join([s.value for s in candidate.sector_interests])}")
    print(f"   📊 CGPA: {candidate.cgpa}")
    print(f"   🕒 Experience: {candidate.experience_months} months")
    print(f"   🏘️ District Type: {candidate.district_type.value}")
    print(f"   👥 Social Category: {candidate.social_category.value}")
    print(f"   📝 Past Internships: {len(candidate.past_internships)}")


def print_internship_summary(internship: Internship):
    """Print a summary of internship information."""
    available = internship.capacity - internship.filled_positions
    print(f"\n💼 Internship: {internship.title} (ID: {internship.id})")
    print(f"   🏢 Company: {internship.company}")
    print(f"   🏗️ Sector: {internship.sector.value}")
    print(f"   💼 Required Skills: {', '.join(internship.required_skills)}")
    print(f"   📍 Location: {internship.location} {'(Remote allowed)' if internship.remote_allowed else ''}")
    print(f"   💰 Stipend: ₹{internship.stipend:,}/month" if internship.stipend else "   💰 Stipend: Not specified")
    print(f"   👥 Capacity: {available}/{internship.capacity} positions available")
    print(f"   📊 Min CGPA: {internship.min_cgpa}")
    print(f"   🕒 Min Experience: {internship.min_experience_months} months")
    print(f"   🌾 Rural Quota: {internship.rural_quota_percentage}%")


def print_match_details(match: Match, candidate: Candidate, internship: Internship):
    """Print detailed match information."""
    print(f"\n🎯 Match Score: {match.total_score():.3f}")
    print(f"   💼 Skill Match: {match.skill_match_score:.3f}")
    print(f"   📍 Location Preference: {match.location_preference_score:.3f}")
    print(f"   🏢 Sector Interest: {match.sector_interest_score:.3f}")
    print(f"   ✅ Eligibility: {match.eligibility_score:.3f}")
    print(f"   🎊 Affirmative Action Boost: {match.affirmative_action_boost:.3f}")


@click.group()
def cli():
    """AI/ML Internship Matching System - Prototype"""
    pass


@cli.command()
def demo():
    """Run a demonstration of the matching system."""
    print("🚀 AI/ML Internship Matching System - Demo")
    print("=" * 50)
    
    # Load sample data
    print("\n📊 Loading sample data...")
    candidates = create_sample_candidates()
    internships = create_sample_internships()
    
    print(f"✅ Loaded {len(candidates)} candidates and {len(internships)} internships")
    
    # Initialize matcher
    print("\n🧠 Initializing AI/ML matching algorithm...")
    matcher = InternshipMatcher()
    
    # Perform matching
    print("\n🔄 Calculating matches...")
    matches = matcher.match_candidates(candidates, internships)
    
    print(f"✅ Generated {len(matches)} potential matches")
    
    # Create lookup dictionaries
    candidates_dict = {c.id: c for c in candidates}
    internships_dict = {i.id: i for i in internships}
    
    # Show top matches overall
    print("\n🏆 TOP 10 MATCHES OVERALL")
    print("=" * 40)
    
    top_matches = sorted(matches, key=lambda m: m.total_score(), reverse=True)[:10]
    
    for i, match in enumerate(top_matches, 1):
        candidate = candidates_dict[match.candidate_id]
        internship = internships_dict[match.internship_id]
        
        print(f"\n{i}. {candidate.name} ↔ {internship.title}")
        print(f"   Company: {internship.company}")
        print(f"   Total Score: {match.total_score():.3f}")
        print(f"   Breakdown: Skills({match.skill_match_score:.2f}) + Location({match.location_preference_score:.2f}) + Sector({match.sector_interest_score:.2f}) + Eligibility({match.eligibility_score:.2f}) + AA Boost({match.affirmative_action_boost:.2f})")
    
    # Show matches for each candidate
    print("\n\n👤 MATCHES FOR EACH CANDIDATE")
    print("=" * 40)
    
    for candidate in candidates:
        candidate_matches = matcher.get_top_matches_for_candidate(candidate.id, matches, top_k=3)
        
        print_candidate_summary(candidate)
        
        if candidate_matches:
            print(f"\n   🎯 Top 3 Matches:")
            for j, match in enumerate(candidate_matches, 1):
                internship = internships_dict[match.internship_id]
                print(f"   {j}. {internship.title} at {internship.company} (Score: {match.total_score():.3f})")
        else:
            print("   ❌ No suitable matches found")
    
    # Show top candidates for each internship
    print("\n\n💼 TOP CANDIDATES FOR EACH INTERNSHIP")
    print("=" * 50)
    
    for internship in internships:
        internship_matches = matcher.get_top_candidates_for_internship(internship.id, matches, top_k=3)
        
        print_internship_summary(internship)
        
        if internship_matches:
            print(f"\n   🎯 Top 3 Candidates:")
            for j, match in enumerate(internship_matches, 1):
                candidate = candidates_dict[match.candidate_id]
                print(f"   {j}. {candidate.name} (Score: {match.total_score():.3f})")
                print(f"      CGPA: {candidate.cgpa}, Experience: {candidate.experience_months}mo, District: {candidate.district_type.value}")
        else:
            print("   ❌ No suitable candidates found")


@cli.command()
@click.option('--candidate-id', help='Show matches for specific candidate ID')
@click.option('--internship-id', help='Show candidates for specific internship ID')
def match(candidate_id, internship_id):
    """Show detailed matching results."""
    # Load sample data
    candidates = create_sample_candidates()
    internships = create_sample_internships()
    
    # Initialize matcher
    matcher = InternshipMatcher()
    matches = matcher.match_candidates(candidates, internships)
    
    # Create lookup dictionaries
    candidates_dict = {c.id: c for c in candidates}
    internships_dict = {i.id: i for i in internships}
    
    if candidate_id:
        candidate = candidates_dict.get(candidate_id)
        if not candidate:
            print(f"❌ Candidate {candidate_id} not found")
            return
        
        print_candidate_summary(candidate)
        candidate_matches = matcher.get_top_matches_for_candidate(candidate_id, matches)
        
        print(f"\n🎯 MATCHES FOR {candidate.name}")
        print("=" * 40)
        
        for i, match in enumerate(candidate_matches, 1):
            internship = internships_dict[match.internship_id]
            print(f"\n{i}. {internship.title} at {internship.company}")
            print_match_details(match, candidate, internship)
    
    elif internship_id:
        internship = internships_dict.get(internship_id)
        if not internship:
            print(f"❌ Internship {internship_id} not found")
            return
        
        print_internship_summary(internship)
        internship_matches = matcher.get_top_candidates_for_internship(internship_id, matches)
        
        print(f"\n🎯 CANDIDATES FOR {internship.title}")
        print("=" * 40)
        
        for i, match in enumerate(internship_matches, 1):
            candidate = candidates_dict[match.candidate_id]
            print(f"\n{i}. {candidate.name}")
            print_match_details(match, candidate, internship)
    
    else:
        print("Please specify either --candidate-id or --internship-id")


@cli.command()
def list_data():
    """List all available candidates and internships."""
    candidates = create_sample_candidates()
    internships = create_sample_internships()
    
    print("👤 AVAILABLE CANDIDATES")
    print("=" * 30)
    for candidate in candidates:
        print(f"{candidate.id}: {candidate.name} ({candidate.district_type.value}, {candidate.social_category.value})")
    
    print("\n💼 AVAILABLE INTERNSHIPS")
    print("=" * 30)
    for internship in internships:
        available = internship.capacity - internship.filled_positions
        print(f"{internship.id}: {internship.title} at {internship.company} ({available} positions)")


if __name__ == '__main__':
    cli()