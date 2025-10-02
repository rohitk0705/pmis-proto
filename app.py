# app.py
import streamlit as st
from matcher import load_jobs_csv
from resume_parser import parse_resume_text
from matcher import load_jobs_csv, build_vectorizer, score_jobs_for_resume
from fairness import fairness_rerank_for_candidate
import pandas as pd
from resume_parser import parse_resume_text, extract_text_from_pdf, extract_text_from_docx

st.set_page_config(page_title="PM Internship Match Demo", layout="wide")

st.title("AI Internship Matching — Demo Prototype")
st.markdown("Upload or paste a resume to see top internship matches (prototype).")

# Sidebar inputs
st.sidebar.header("Candidate Info (for demo)")
candidate_location = st.sidebar.text_input("Your current city/state (for location match)", value="")
candidate_income = st.sidebar.number_input("Annual family income (INR)", min_value=0, value=500000, step=50000)
top_k = st.sidebar.slider("Number of matches to show", min_value=3, max_value=10, value=5)

# Resume input
# app.py (replace the upload block)

st.subheader("Resume input")
upload = st.file_uploader("Upload resume (.pdf, .docx, .txt) OR paste text below", 
                          type=["pdf", "docx", "txt"])

resume_text = ""
if upload is not None:
    if upload.type == "application/pdf":
        resume_text = extract_text_from_pdf(upload)
    elif upload.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(upload)
    else:
        resume_text = upload.getvalue().decode("utf-8", errors="ignore")
else:
    resume_text = st.text_area("Or paste resume text here", height=200, value="")

if st.button("Find Matches"):

    if not resume_text.strip():
        st.error("Please paste or upload a resume text.")
    else:
        # parse resume
        profile = parse_resume_text(resume_text)
        profile["annual_income"] = int(candidate_income)
        profile["location"] = candidate_location

        st.markdown("**Parsed profile (demo)**")
        st.json({
            "name": profile.get("name"),
            "email": profile.get("email"),
            "skills": profile.get("skills"),
            "location": profile.get("location"),
            "annual_income": profile.get("annual_income")
        })

        # Load jobs & vectorizer
        jobs = load_jobs_csv("jobs.csv")
        vect, job_mat = build_vectorizer(jobs)

        # Build resume_text for vectorization: use raw_text + skills joined
        resume_for_vector = resume_text
        results = score_jobs_for_resume(resume_for_vector, jobs, vect, job_mat, candidate_location=candidate_location, candidate_income=profile["annual_income"], top_k=20)

        # fairness re-rank
        reranked = fairness_rerank_for_candidate(results, profile, required_accommodation_min=False, top_k=top_k)

        # prepare display table
        rows = []
        for r in reranked:
            j = r["job"]
            explanation = []
            explanation.append(f"Skill match: {r['skill_sim']:.2f}")
            if r["location_score"]>0:
                explanation.append("Location match")
            if r["accommodation_flag"]:
                explanation.append("Accommodation provided (boosted for low income)")
            rows.append({
                "Job ID": j["id"],
                "Company": j["company"],
                "Title": j["title"],
                "Location": j["location"],
                "Stipend": j["stipend"],
                "Score": round(r["final_score"], 3),
                "Explanation": "; ".join(explanation)
            })
        df = pd.DataFrame(rows)
        st.subheader("Top matches")
        st.table(df)

        st.info("This prototype uses TF-IDF + simple rules. For production, replace TF-IDF with sentence embeddings (SBERT) and add a two-tower scorer + audited fairness module.")
