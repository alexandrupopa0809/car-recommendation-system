from django.core.cache import cache
import pandas as pd


def get_cached_dataframe():
    cached_embeddings = cache.get("cached_embeddings")

    if cached_embeddings is None:
        df = pd.read_pickle("/Users/alex9popa/Documents/Master/car-recommendation-system/data/merged_embeddings.pkl")
        cache.set("cached_embeddings", df, timeout=None)
    df = cache.get("cached_embeddings")
    return df
