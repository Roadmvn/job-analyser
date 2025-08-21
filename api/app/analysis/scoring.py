from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_tfidf_cosine_scores(resume_text: str, job_texts: List[str]) -> List[float]:
    corpus = [resume_text] + job_texts
    vectorizer = TfidfVectorizer(stop_words=[
        "the","and","a","an","to","of","in","for","on","with",
        "le","la","les","de","des","du","et","un","une","au","aux",
    ])
    X = vectorizer.fit_transform(corpus)
    resume_vec = X[0]
    jobs_vec = X[1:]
    sims = cosine_similarity(resume_vec, jobs_vec).flatten()
    return sims.tolist()


