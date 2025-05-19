import React from "react";
import TablaCSV from "./TablaCSV";
import GraficaImagen from "./GraficaImagen";

const ContenidoRequerimiento = ({ archivo, requerimiento, datos }) => {
  const base = `http://localhost:8000/media/resultados/${archivo}/${requerimiento}`;

  switch (requerimiento) {
    case "estadisticas":
      return (
        <>
          <GraficaImagen titulo="Top Autores" src={`${base}/top_authors.png`} />
          <TablaCSV url={`${base}/top_authors.csv`} />
          <GraficaImagen
            titulo="Top Journals"
            src={`${base}/top_journals.png`}
          />
          <TablaCSV url={`${base}/top_journals.csv`} />
          <GraficaImagen
            titulo="Top Publishers"
            src={`${base}/top_publishers.png`}
          />
          <TablaCSV url={`${base}/top_publishers.csv`} />
          <GraficaImagen
            titulo="Tipo por Año"
            src={`${base}/type_by_year.png`}
          />
          <TablaCSV url={`${base}/type_by_year.csv`} />
        </>
      );

    case "bibtex":
      return (
        <>
          <a href={`${base}/unified.bib`} download>
            Descargar BibTeX Unificado
          </a>
          <br />
          <a href={`${base}/duplicates.bib`} download>
            Descargar BibTeX Duplicados
          </a>
        </>
      );

    case "categorias":
      const imagenes = datos.imagenes || [];
      return (
        <>
          {imagenes.map((nombre, idx) => (
            <div key={idx} className="item-seccion">
              <h4>
                {nombre
                  .replace("nube_", "")
                  .replace(".png", "")
                  .replace(/_/g, " ")}
              </h4>

              <img
                src={`http://localhost:8000/media/resultados/${archivo}/categorias/${nombre}`}
                alt={nombre}
                style={{ width: "100%", maxWidth: 800, marginBottom: "20px" }}
              />
            </div>
          ))}
        </>
      );

    case "agrupamiento":
      return (
        <>
          <GraficaImagen
            titulo="Dendrograma TF-IDF"
            src={`${base}/dendrograma_tfidf_coseno.png`}
          />
          <GraficaImagen
            titulo="Dendrograma Jaccard"
            src={`${base}/dendrograma_jaccard.png`}
          />
          <TablaCSV
            url={`${base}/clusters_tfidf.csv`}
            columnasVisibles={[
              "document title",
              "authors",
              "abstract",
              "cluster_tfidf",
              "cluster_jaccard",
            ]}
          />
        </>
      );

    case "coherencia":
      return (
        <>
          <GraficaImagen
            titulo="Heatmap - Ward"
            src={`${base}/coherencia_ward.png`}
          />
          <GraficaImagen
            titulo="Heatmap - Average"
            src={`${base}/coherencia_average.png`}
          />
        </>
      );

    default:
      return <p>Requerimiento no implementado.</p>;
  }
};

export default ContenidoRequerimiento;
