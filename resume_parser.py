# resume_parser.py
import re
from typing import List

import pdfplumber
import docx

# Common skill keywords and their normalized form
SKILL_SYNONYMS = {
    "c++": ["c++", "cpp"],
    "c": ["c language", "c "],   # space avoids matching 'c++'
    "python": ["python", "py"],
    "javascript": ["javascript", "js"],
    "html": ["html", "hypertext markup language"],
    "css": ["css", "cascading style sheets"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "node", "nodejs"],
    "mongodb": ["mongodb", "mongo"],
    "machine learning": ["machine learning", "ml"],
    "nlp": ["nlp", "natural language processing"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "sql": ["sql", "structured query language"],
    "autocad": ["autocad", "auto cad"],
    "git": ["git", "github", "gitlab"],
    "django": ["django"],
    "flask": ["flask"],
    "rest api": ["rest api", "restful api", "api"],
    "java": ["java"],
    "matlab": ["matlab"],
    "excel": ["excel", "ms excel"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "arduino": ["arduino"],
    "iot": ["iot", "internet of things"],
    "aws": ["aws", "amazon web services"]
}


def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def simple_skill_extract(text: str) -> List[str]:
    """
    Improved skill extraction:
    - Handles symbols like 'c++'
    - Prefers longer matches over shorter ones
    """
    text_lower = text.lower()
    found = set()

def simple_skill_extract(text: str) -> List[str]:
    """
    Extract skills from resume using synonyms and exact-ish matching.
    """
    text_lower = text.lower()
    found = set()

    for normalized, variants in SKILL_SYNONYMS.items():
        for variant in variants:
            # exact-ish match (ignores case, matches whole word or phrase)
            pattern = r"(?<!\w)" + re.escape(variant) + r"(?!\w)"
            if re.search(pattern, text_lower):
                found.add(normalized)
                break  # stop after first variant matched

    return sorted(list(found))




def parse_resume_text(text: str) -> dict:
    skills = simple_skill_extract(text)
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'(\+?\d{2,4}[-\s]?)?\d{10}', text.replace('(', '').replace(')', ''))

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name = lines[0][:60] if lines else None

    return {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": skills,
        "raw_text": text
    }

# Quick test block (not executed when imported)
if __name__ == "__main__":
    sample_resume = """
    Rohit Sharma
    Email: rohit@example.com
    Skills: C++, Python, SQL, Data Structures
    """
    print(simple_skill_extract(sample_resume))

