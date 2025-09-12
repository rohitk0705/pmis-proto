# matcher.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

def load_jobs_csv(path="jobs.csv") -> List[Dict]:
    df = pd.read_csv(path)
    jobs = df.to_dict(orient="records")  # list of dicts like JSON
    return jobs

def build_vectorizer(jobs: List[Dict]):
    corpus = [job["description"] for job in jobs]
    vect = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
    job_mat = vect.fit_transform(corpus)
    return vect, job_mat

def score_jobs_for_resume(resume_text: str, jobs: List[Dict], vect, job_mat,
                          candidate_location: str = "", candidate_income: int = None, top_k: int = 5):
    resume_vec = vect.transform([resume_text])
    sims = cosine_similarity(resume_vec, job_mat).flatten()

    results = []
    for i, job in enumerate(jobs):
        skill_sim = float(sims[i])
        location_score = 1.0 if candidate_location and candidate_location.lower() in str(job["location"]).lower() else 0.0
        accommodation_flag = 1 if str(job.get("provides_accommodation")).lower() == "true" else 0
        final_score = 0.7*skill_sim + 0.2*location_score + 0.1*accommodation_flag

        results.append({
            "job": job,
            "skill_sim": skill_sim,
            "location_score": location_score,
            "accommodation_flag": accommodation_flag,
            "final_score": final_score
        })

    results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    jobs = load_jobs_csv()
    vect, job_mat = build_vectorizer(jobs)
    sample_resume = "Python, pandas, data cleaning, SQL, visualization"
    out = score_jobs_for_resume(sample_resume, jobs, vect, job_mat, candidate_location="Bengaluru", top_k=5)
    for r in out:
        print(r["job"]["title"], r["final_score"], r["skill_sim"])
