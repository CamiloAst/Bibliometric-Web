import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import nltk

nltk.download("stopwords")
nltk.download("wordnet")

# === CATEGORÍAS ===
CATEGORIAS = {
    "Habilidades": [
        "Abstraction",
        "Algorithm",
        "Algorithmic thinking",
        "Coding",
        "Collaboration",
        "Cooperation",
        "Creativity",
        "Critical thinking",
        "Debug",
        "Decomposition",
        "Evaluation",
        "Generalization",
        "Logic",
        "Logical thinking",
        "Modularity",
        "Patterns recognition",
        "Problem solving",
        "Programming",
    ],
    "Conceptos Computacionales": [
        "Conditionals",
        "Control structures",
        "Directions",
        "Events",
        "Funtions",
        "Loops",
        "Modular structure",
        "Parallelism",
        "Sequences",
        "Software/hardware",
        "Variables",
    ],
    "Actitudes": [
        "Emotional",
        "Engagement",
        "Motivation",
        "Perceptions",
        "Persistence",
        "Self-efficacy",
        "Self-perceived",
    ],
    "Propiedades psicometricas": [
        "Classical Test Theory",
        "Confirmatory Factor Analysis",
        "Exploratory Factor Analysis",
        "Item Response Theory",
        "Reliability",
        "Structural Equation Model",
        "Validity",
    ],
    "Herramientas de evaluacion": [
        "Beginners Computational Thinking test",
        "Coding Attitudes Survey",
        "Collaborative Computing Observation Instrument",
        "Competent Computational Thinking test",
        "Computational thinking skills test",
        "Computational concepts",
        "Computational Thinking Assessment for Chinese Elementary Students",
        "Computational Thinking Challenge",
        "Computational Thinking Levels Scale",
        "Computational Thinking Scale",
        "Computational Thinking Skill Levels Scale",
        "Computational Thinking Test",
        "Computational Thinking Test for Elementary School Students",
        "Computational Thinking Test for Lower Primary",
        "Computational thinking-skill tasks on numbers and arithmetic",
        "Computerized Adaptive Programming Concepts Test",
        "CT Scale",
        "Elementary Student Coding Attitudes Survey",
        "General self-efficacy scale",
        "ICT competency test",
        "Instrument of computational identity",
        "KBIT fluid intelligence subtest",
        "Mastery of computational concepts Test and an Algorithmic Test",
        "Multidimensional 21st Century Skills Scale",
        "Self-efficacy scale",
        "STEM learning attitude scale",
        "The computational thinking scale",
    ],
    "Diseno de investigacion": [
        "No experimental",
        "Experimental",
        "Longitudinal research",
        "Mixed methods",
        "Post-test",
        "Pre-test",
        "Quasi-experiments",
    ],
    "Nivel de escolaridad": [
        "Upper elementary education",
        "Primary school",
        "Early childhood education",
        "Secondary school",
        "High school",
        "University",
    ],
    "Medio": [
        "Block programming",
        "Mobile application",
        "Pair programming",
        "Plugged activities",
        "Programming",
        "Robotics",
        "Spreadsheet",
        "STEM",
        "Unplugged activities",
    ],
    "Estrategia": [
        "Construct-by-self mind mapping",
        "Construct-on-scaffold mind mapping",
        "Design-based learning",
        "Evidence-centred design approach",
        "Gamification",
        "Reverse engineering pedagogy",
        "Technology-enhanced learning",
        "Collaborative learning",
        "Cooperative learning",
        "Flipped classroom",
        "Game-based learning",
        "Inquiry-based learning",
        "Personalized learning",
        "Problem-based learning",
        "Project-based learning",
        "Universal design for learning",
    ],
    "Herramienta": [
        "Alice",
        "Arduino",
        "Scratch",
        "ScratchJr",
        "Blockly Games",
        "Code.org",
        "Codecombat",
        "CSUnplugged",
        "Robot Turtles",
        "Hello Ruby",
        "Kodable",
        "LightbotJr",
        "KIBO robots",
        "BEE BOT",
        "CUBETTO",
        "Minecraft",
        "Agent Sheets",
        "Mimo",
        "Py",
        "SpaceChem",
    ],
}


stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)


def analizar_coherencia(
    ruta_csv, out_dir="media/coherencia", max_docs=100, k_clusters=5
):
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(ruta_csv)
    df.columns = df.columns.str.strip().str.lower()
    if "abstract" not in df.columns:
        raise ValueError("No se encontró la columna 'abstract'.")

    abstracts = df["abstract"].dropna().head(max_docs).tolist()
    titles = df["document title"].dropna().head(max_docs).tolist()
    abstracts_clean = [preprocess(a) for a in abstracts]

    # TF-IDF y distancia
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(abstracts_clean)
    distance_matrix = pairwise_distances(X, metric="euclidean")

    resultados = {}
    for metodo in ["ward", "average"]:
        linkage_matrix = linkage(distance_matrix, method=metodo)
        etiquetas = fcluster(linkage_matrix, k_clusters, criterion="maxclust")
        df_cluster = pd.DataFrame({"cluster": etiquetas, "abstract": abstracts_clean})

        # Coherencia: cuenta cuántas palabras de cada categoría hay por cluster
        coherencia = defaultdict(lambda: defaultdict(int))
        for _, row in df_cluster.iterrows():
            cluster = row["cluster"]
            for cat, palabras in CATEGORIAS.items():
                for palabra in palabras:
                    if palabra.lower() in row["abstract"]:
                        coherencia[cluster][cat] += 1

        df_coherencia = pd.DataFrame(coherencia).fillna(0).astype(int)
        heatmap_path = os.path.join(out_dir, f"coherencia_{metodo}.png")
        sns.heatmap(df_coherencia, annot=True, cmap="Blues")
        plt.title(f"Coherencia Categoría vs Cluster ({metodo})")
        plt.ylabel("Categoría")
        plt.xlabel("Cluster")
        plt.tight_layout()
        plt.savefig(heatmap_path)
        plt.close()

        resultados[metodo] = {
            "heatmap": heatmap_path,
            "coherencia": df_coherencia.to_dict(),
        }

    return resultados
