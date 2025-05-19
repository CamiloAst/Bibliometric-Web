import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt


def cluster_abstracts(ruta_csv, out_dir="media/clusters", num_clusters=10):
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(ruta_csv)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["abstract"])
    abstracts = df["abstract"].tolist()

    # === TF-IDF + Coseno ===
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(abstracts)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix)
    linkage_tfidf = linkage(1 - cosine_sim_matrix, method="ward")
    clusters_tfidf = fcluster(linkage_tfidf, t=num_clusters, criterion="maxclust")
    df["cluster_tfidf"] = clusters_tfidf

    # === CountVectorizer + Jaccard ===
    vectorizer = CountVectorizer(stop_words="english", binary=True)
    binary_matrix = vectorizer.fit_transform(abstracts)
    jaccard_dist = pdist(binary_matrix.toarray(), metric="jaccard")
    linkage_jaccard = linkage(jaccard_dist, method="ward")
    clusters_jaccard = fcluster(linkage_jaccard, t=num_clusters, criterion="maxclust")
    df["cluster_jaccard"] = clusters_jaccard

    # === Exportar resultado general ===
    ruta_global = os.path.join(out_dir, "clusters_tfidf.csv")
    df.to_csv(ruta_global, index=False)

    # === Exportar CSVs por cluster
    for method in ["tfidf", "jaccard"]:
        col = f"cluster_{method}"
        for cluster_id in sorted(df[col].unique()):
            subset = df[df[col] == cluster_id]
            filename = os.path.join(out_dir, f"cluster_{method}_{cluster_id}.csv")
            subset.to_csv(filename, index=False)

    # === Dendrogramas
    plt.figure(figsize=(12, 6))
    dendrogram(
        linkage_tfidf,
        labels=clusters_tfidf,
        orientation="top",
        distance_sort="descending",
        no_labels=True,
    )
    plt.title("Dendrograma - TF-IDF + Coseno")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "dendrograma_tfidf_coseno.png"))
    plt.close()

    plt.figure(figsize=(12, 6))
    dendrogram(
        linkage_jaccard,
        labels=clusters_jaccard,
        orientation="top",
        distance_sort="descending",
        no_labels=True,
    )
    plt.title("Dendrograma - CountVectorizer + Jaccard")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "dendrograma_jaccard.png"))
    plt.close()

    return {
        "mensaje": "Agrupamiento completado",
        "ruta_resultado": ruta_global,
        "carpeta_clusters": out_dir,
        "dendrogramas": ["dendrograma_tfidf_coseno.png", "dendrograma_jaccard.png"],
    }
