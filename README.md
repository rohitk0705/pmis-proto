# PMIS Proto - AI/ML Internship Matching System

A smart, automated system that uses AI/ML algorithms to match candidates with internship opportunities based on skills, qualifications, location preferences, and sector interests. The system incorporates affirmative action considerations including representation from rural/aspirational districts, different social categories, past participation, and internship capacity management.

## Features

### Core Matching Algorithm
- **Skill Matching**: Uses TF-IDF vectorization and cosine similarity to match candidate skills with internship requirements
- **Location Preference**: Intelligent location matching with support for remote work and geographic preferences
- **Sector Interest Alignment**: Matches candidates' sector interests with internship sectors
- **Eligibility Scoring**: Validates CGPA, experience, and other qualification requirements

### Affirmative Action & Diversity
- **Social Category Considerations**: Support for General, OBC, SC, ST, and EWS categories
- **Rural/Aspirational District Representation**: Special consideration for candidates from rural and aspirational districts
- **Participation History**: Boosts candidates with fewer past internships to ensure diverse participation
- **Rural Quota Management**: Enforces rural quota percentages for each internship

### Capacity Management
- **Dynamic Capacity Tracking**: Tracks filled vs. available positions for each internship
- **Quota-based Allocation**: Ensures compliance with rural and social category quotas
- **Intelligent Ranking**: Balances merit with affirmative action requirements

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rohitk0705/pmis-proto.git
cd pmis-proto
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Run Complete Demo
```bash
python cli.py demo
```
This runs a comprehensive demonstration showing:
- Top matches overall
- Matches for each candidate 
- Top candidates for each internship
- Detailed scoring breakdown

#### List Available Data
```bash
python cli.py list-data
```
Shows all available candidates and internships with their IDs.

#### Get Detailed Matches for a Candidate
```bash
python cli.py match --candidate-id C001
```
Shows detailed match scores and breakdown for a specific candidate.

#### Get Top Candidates for an Internship
```bash
python cli.py match --internship-id I101
```
Shows top candidates for a specific internship with detailed scoring.

### Programmatic Usage

```python
from src.models import Candidate, Internship, SocialCategory, DistrictType, Sector
from src.matcher import InternshipMatcher
from src.sample_data import create_sample_candidates, create_sample_internships

# Load data
candidates = create_sample_candidates()
internships = create_sample_internships()

# Initialize matcher
matcher = InternshipMatcher()

# Get matches
matches = matcher.match_candidates(candidates, internships)

# Get top matches for a candidate
candidate_matches = matcher.get_top_matches_for_candidate("C001", matches, top_k=5)

# Get top candidates for an internship
internship_matches = matcher.get_top_candidates_for_internship("I101", matches, top_k=10)
```

## System Architecture

### Data Models
- **Candidate**: Represents an internship applicant with skills, qualifications, preferences, and demographics
- **Internship**: Represents an internship opportunity with requirements, location, and capacity details
- **Match**: Represents a candidate-internship pairing with detailed scoring

### Matching Algorithm
The AI/ML matching system uses a weighted scoring approach:

```
Total Score = (
    Skill Match × 0.3 +
    Location Preference × 0.2 +
    Sector Interest × 0.2 +
    Eligibility × 0.2 +
    Affirmative Action Boost × 0.1
)
```

### Affirmative Action Implementation
- **Rural/Aspirational District Boost**: +0.3 points
- **Preferred Social Category Boost**: +0.2 points  
- **First-time Participation Boost**: +0.2 points (no prior internships)
- **Second-time Participation Boost**: +0.1 points (1 prior internship)

### Rural Quota Enforcement
The system enforces rural quotas by:
1. Calculating rural quota positions per internship
2. Prioritizing rural/aspirational candidates for quota positions
3. Filling remaining positions from the general pool
4. Maintaining merit-based ranking within each category

## Sample Data

The system includes sample data with:
- **5 Diverse Candidates**: Representing different backgrounds, skills, and demographics
- **5 Varied Internships**: Across technology, finance, healthcare, government, and NGO sectors
- **Realistic Scenarios**: Including rural quotas, social category preferences, and capacity constraints

### Sample Candidates
- Priya Sharma (Urban, General) - Technology/Finance focus
- Arjun Kumar (Aspirational district, SC) - Technology/Government focus  
- Sneha Patel (Urban, OBC) - Finance/Technology focus
- Ramesh Yadav (Rural, OBC) - Agriculture/Government/NGO focus
- Kavya Reddy (Urban, General) - Healthcare/NGO focus

### Sample Internships
- Software Engineering (TechCorp India) - 20% rural quota
- Data Science (FinanceAI Solutions) - 15% rural quota
- Rural Development (Bharat Rural Foundation) - 50% rural quota
- Healthcare Analytics (MedTech Innovations) - 10% rural quota
- Government Policy (Ministry of Rural Development) - 30% rural quota

## Technical Details

### Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **scikit-learn**: Machine learning algorithms (TF-IDF, cosine similarity)
- **click**: Command-line interface framework
- **dataclasses-json**: JSON serialization for data models

### Key Algorithms
1. **TF-IDF Vectorization**: Converts skill and qualification text into numerical vectors
2. **Cosine Similarity**: Measures similarity between candidate and internship requirements
3. **Multi-criteria Scoring**: Combines multiple factors with weighted importance
4. **Constraint Satisfaction**: Ensures quota compliance while maximizing overall match quality

## Future Enhancements

- **Machine Learning Model Training**: Train on historical matching data for improved accuracy
- **Advanced NLP**: Use embedding models (Word2Vec, BERT) for better semantic matching
- **Geographic Intelligence**: Incorporate actual distance calculations and transportation preferences
- **Dynamic Weight Adjustment**: Allow customizable scoring weights per organization
- **Batch Processing**: Support for large-scale matching across thousands of candidates/internships
- **API Integration**: REST API for integration with external systems
- **Database Integration**: Persistent storage with SQL/NoSQL databases
- **Real-time Updates**: Live capacity updates and dynamic re-matching

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.