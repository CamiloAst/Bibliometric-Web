import React from "react";

const GraficaImagen = ({ titulo, src }) => (
  <div style={{ margin: "20px 0" }}>
    <h3>{titulo}</h3>
    <img src={src} alt={titulo} style={{ width: "100%", maxWidth: 800 }} />
  </div>
);

export default GraficaImagen;
