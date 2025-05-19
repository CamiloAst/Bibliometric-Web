import React, { useEffect, useState } from "react";
import axios from "axios";
import ContenidoRequerimiento from "./ContenidoRequerimiento";
import {
  obtenerArchivos,
  ejecutarRequerimiento as ejecutarRequerimientoAPI,
} from "../services/api.js";
import SubirArchivo from "./SubirArchivo";

const requerimientos = [
  { nombre: "estadisticas", api: "estadisticas" },
  { nombre: "bibtex", api: "generar_bib" },
  { nombre: "categorias", api: "categorias" },
  { nombre: "agrupamiento", api: "agrupamiento" },
  { nombre: "coherencia", api: "coherencia" },
];

const ResultadosBibliometricos = () => {
  const [archivo, setArchivo] = useState("");
  const [archivosDisponibles, setArchivosDisponibles] = useState([]);
  const [requerimiento, setRequerimiento] = useState(null);
  const [respuesta, setRespuesta] = useState(null);

  useEffect(() => {
    obtenerArchivos().then((res) => {
      const nombreLimpio = res.data[0].archivo
        ? res.data[0].archivo.split("/").pop().replace(".csv", "")
        : res.data[0];
      setArchivosDisponibles(res.data);
      if (res.data.length > 0) setArchivo(nombreLimpio);
    });
  }, []);

  const ejecutarRequerimiento = (req) => {
    const nombreReq = req.api;
    setRequerimiento(req.nombre);
    setRespuesta(null);

    ejecutarRequerimientoAPI(nombreReq, archivo)
      .then((res) => setRespuesta(res.data))
      .catch((err) => setRespuesta({ error: err.message }));
    console.log("archivo (should be string):", archivo);
  };
  return (
    <div>
      <SubirArchivo
        onUploadSuccess={() => {
          obtenerArchivos().then((res) => {
            setArchivosDisponibles(res.data);
            if (!res.data.includes(archivo)) {
              setArchivo(res.data[0]); // si es nuevo
            }
          });
        }}
      />

      <div style={{ marginTop: "20px" }}>
        <label style={{ marginRight: "10px", fontWeight: "bold" }}>
          Seleccionar archivo:
        </label>
        <select
          value={archivo}
          onChange={(e) => setArchivo(e.target.value)}
          className="select-archivo"
        >
          {archivosDisponibles.map((item, idx) => {
            const nombre = item.archivo
              ? item.archivo.split("/").pop().replace(".csv", "")
              : item;
            return (
              <option key={idx} value={nombre}>
                {nombre}
              </option>
            );
          })}
        </select>
      </div>

      <div className="botones-container">
        {requerimientos.map((req) => (
          <button
            key={req.nombre}
            onClick={() => ejecutarRequerimiento(req)}
            className="boton-requerimiento"
            style={{
              backgroundColor:
                requerimiento === req.nombre ? "#5e2bb8" : "blueviolet",
            }}
          >
            {req.nombre.charAt(0).toUpperCase() + req.nombre.slice(1)}
          </button>
        ))}
      </div>

      {respuesta && (
        <div className="panel-resultado">
          <ContenidoRequerimiento
            archivo={archivo}
            requerimiento={requerimiento}
            datos={respuesta}
          />
        </div>
      )}
    </div>
  );
};

export default ResultadosBibliometricos;
