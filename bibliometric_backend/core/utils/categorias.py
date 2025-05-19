import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
from wordcloud import WordCloud

# === CATEGORÍAS Y VARIABLES ===
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


def normalizar(text):
    return re.sub(r"[^\w\s]", "", str(text)).lower()


def contar_frecuencia(df, categorias):
    resultados = {}
    abstracts = df["Abstract"].dropna().astype(str).tolist()
    corpus = " ".join(abstracts)
    texto = normalizar(corpus)

    for cat, palabras in categorias.items():
        conteo = Counter()
        for palabra in palabras:
            claves = [normalizar(p) for p in palabra.split(" - ")]
            total = sum(texto.count(k) for k in claves)
            conteo[palabra] = total
        resultados[cat] = conteo
    return resultados


def generar_wordcloud(frecuencias, nombre, out_dir):
    wc = WordCloud(width=1200, height=600, background_color="white")
    wc.generate_from_frequencies(frecuencias)
    wc.to_file(os.path.join(out_dir, f"nube_{nombre}.png"))


def graficar_red_coocurrencia(df, out_dir):
    abstracts = df["Abstract"].dropna().astype(str).tolist()
    palabras_clave = [normalizar(p) for cat in CATEGORIAS.values() for p in cat]

    G = nx.Graph()
    for texto in abstracts:
        tokens = set(normalizar(texto).split())
        presentes = [p for p in palabras_clave if p in tokens]
        for i in range(len(presentes)):
            for j in range(i + 1, len(presentes)):
                G.add_edge(presentes[i], presentes[j])

    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(G, k=0.3)
    nx.draw_networkx(G, pos, node_size=30, font_size=8, with_labels=True)
    plt.title("Red de Co-ocurrencia de Palabras Clave")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "cooccurrence_network.png"))
    plt.close()


def procesar_categorias_y_nubes(ruta_csv, out_dir="media/categorias"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(ruta_csv)
    resultados = contar_frecuencia(df, CATEGORIAS)

    for cat, frecs in resultados.items():
        generar_wordcloud(frecs, cat.replace(" ", "_"), out_dir)

    total = Counter()
    for frec in resultados.values():
        total.update(frec)
    generar_wordcloud(total, "global", out_dir)

    graficar_red_coocurrencia(df, out_dir)

    return {
        "categorias": list(CATEGORIAS.keys()),
        "archivos_generados": os.listdir(out_dir),
    }
