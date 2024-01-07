from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import re


model = SentenceTransformer("sentence-transformers/paraphrase-distilroberta-base-v1")


def preprocess_text(text: str):
    return re.sub(r"[^A-Za-z0-9]+", " ", text.strip())


def embedding_fn(sentences):
    return model.encode(sentences)


def get_bert_recommendations(df, query, top_n=10):
    query_embedd = embedding_fn(preprocess_text(query))
    results = (
        df.Embeddings.apply(
            lambda body: util.pytorch_cos_sim(query_embedd, body)
            .detach()
            .numpy()
            .flatten()
        )
        .astype(float)
        .nlargest(top_n)
    )
    vehicles_titles = {
        (df.loc[id]["Vehicle_Title"], df.loc[id]["Review"]): similarity
        for id, similarity in results.items()
    }
    return vehicles_titles
