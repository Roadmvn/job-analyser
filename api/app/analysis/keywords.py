from typing import List, Dict
import os
import re
import unicodedata
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
try:
    import nltk  # type: ignore
    from nltk.corpus import stopwords as nltk_stopwords  # type: ignore
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:  # download if missing
        nltk.download('stopwords', quiet=True)
    NLTK_EN = set(nltk_stopwords.words('english'))
    NLTK_FR = set(nltk_stopwords.words('french'))
except Exception:  # pragma: no cover
    NLTK_EN, NLTK_FR = set(), set()


EN_STOP = {
    "the","and","a","an","to","of","in","for","on","with","is","are","be","as","by","or","at","from","this","that","it","we","you"
}
FR_STOP = {
    "le","la","les","de","des","du","et","un","une","au","aux","en","dans","pour","sur","avec","est","sont","ou","par","ce","cet","cette","il","elle","nous","vous","ils","elles"
}

DEFAULT_STOPWORDS = sorted((EN_STOP | FR_STOP | NLTK_EN | NLTK_FR))


def strip_accents(text: str) -> str:
    try:
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        return text
    except Exception:
        return text


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = strip_accents(text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def maybe_lemmatize(texts: List[str]) -> List[str]:
    if os.getenv("LEMMATIZE_ENABLED", "false").lower() != "true":
        return texts
    try:
        import spacy
        model = os.getenv("SPACY_MODEL", "fr_core_news_sm")
        try:
            nlp = spacy.load(model, disable=["ner", "parser"])
        except Exception:
            # Fallback: English small if FR not available
            nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])  # may still fail
        out: List[str] = []
        for doc in nlp.pipe(texts, batch_size=32):
            lemmas = [t.lemma_.lower() for t in doc if t.lemma_]
            out.append(" ".join(lemmas))
        return out
    except Exception:
        return texts


def top_ngrams(texts: List[str], n_max: int = 3, topk: int = 30, min_df: int = 1) -> List[Dict]:
    texts = [clean_text(t) for t in texts if t]
    if not texts:
        return []
    texts = maybe_lemmatize(texts)
    cv = CountVectorizer(ngram_range=(1, n_max), min_df=min_df, stop_words=DEFAULT_STOPWORDS)
    X = cv.fit_transform(texts)
    freqs = X.sum(axis=0).A1
    vocab = cv.get_feature_names_out()
    pairs = sorted(zip(vocab, freqs), key=lambda x: x[1], reverse=True)[:topk]
    results = []
    for term, freq in pairs:
        ngram = len(term.split())
        results.append({"term": term, "ngram": ngram, "freq": int(freq), "tfidf": 0.0})
    return results


def tfidf_scores(texts: List[str], n_max: int = 3, topk: int = 30) -> List[Dict]:
    texts = [clean_text(t) for t in texts if t]
    if not texts:
        return []
    texts = maybe_lemmatize(texts)
    tv = TfidfVectorizer(ngram_range=(1, n_max), stop_words=DEFAULT_STOPWORDS)
    X = tv.fit_transform(texts)
    scores = X.sum(axis=0).A1
    vocab = tv.get_feature_names_out()
    pairs = sorted(zip(vocab, scores), key=lambda x: x[1], reverse=True)[:topk]
    results = []
    for term, score in pairs:
        ngram = len(term.split())
        results.append({"term": term, "ngram": ngram, "freq": 0, "tfidf": float(score)})
    return results


def merge_counts_tfidf(counts: List[Dict], tfidf: List[Dict], topk: int = 30) -> List[Dict]:
    by_term = {c["term"]: c for c in counts}
    for item in tfidf:
        if item["term"] in by_term:
            by_term[item["term"]]["tfidf"] = item["tfidf"]
        else:
            by_term[item["term"]] = item
    merged = list(by_term.values())
    merged.sort(key=lambda x: (x.get("tfidf", 0.0), x.get("freq", 0)), reverse=True)
    return merged[:topk]


