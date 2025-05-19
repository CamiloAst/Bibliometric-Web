import os
import pandas as pd

# Columnas esperadas
COL_TITLE = "Document Title"
COL_AUTHORS = "Authors"
COL_ABSTRACT = "Abstract"
COL_PDF = "PDF Link"
COL_TERMS = "IEEE Terms"
COL_DATE = "Online Date"


def export_bib(df, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for i, row in df.iterrows():
            key = f"ref{i+1}"
            title = str(row[COL_TITLE])
            authors = " and ".join(
                a.strip() for a in str(row[COL_AUTHORS]).split(";") if a.strip()
            )
            year = str(row[COL_DATE])[:4]
            abstract = str(row[COL_ABSTRACT]).replace("\n", " ")
            pdf = str(row[COL_PDF])
            terms = str(row[COL_TERMS])

            f.write(f"@article{{{key},\n")
            f.write(f"  title     = {{{title}}},\n")
            f.write(f"  author    = {{{authors}}},\n")
            f.write(f"  year      = {{{year}}},\n")
            f.write(f"  abstract  = {{{abstract}}},\n")
            f.write(f"  keywords  = {{{terms}}},\n")
            f.write(f"  url       = {{{pdf}}},\n")
            f.write("}\n\n")


def procesar_archivos_csv_para_bib(directorio_csv="media/archivos", salida="media/bib"):
    os.makedirs(salida, exist_ok=True)
    csv_files = [f for f in os.listdir(directorio_csv) if f.endswith(".csv")]

    if not csv_files:
        raise Exception("No se encontraron archivos .csv en la carpeta de entrada.")

    unique_titles = set()
    unique_entries = []
    duplicate_entries = []

    for nombre_archivo in csv_files:
        path_csv = os.path.join(directorio_csv, nombre_archivo)
        df = pd.read_csv(path_csv).fillna("")

        if not all(
            c in df.columns
            for c in [
                COL_TITLE,
                COL_AUTHORS,
                COL_ABSTRACT,
                COL_PDF,
                COL_TERMS,
                COL_DATE,
            ]
        ):
            print(f"❌ Archivo {nombre_archivo} omitido por columnas faltantes.")
            continue

        for _, row in df.iterrows():
            title = str(row[COL_TITLE]).strip().lower()
            if title in unique_titles:
                duplicate_entries.append(row)
            else:
                unique_titles.add(title)
                unique_entries.append(row)

    df_unique = pd.DataFrame(unique_entries)
    df_duplicates = pd.DataFrame(duplicate_entries)

    ruta_bib_unico = os.path.join(salida, "unified.bib")
    ruta_bib_duplicados = os.path.join(salida, "duplicates.bib")

    export_bib(df_unique, ruta_bib_unico)
    export_bib(df_duplicates, ruta_bib_duplicados)

    return {
        "unificados": len(df_unique),
        "duplicados": len(df_duplicates),
        "ruta_bib_unificado": ruta_bib_unico,
        "ruta_bib_duplicados": ruta_bib_duplicados,
    }
