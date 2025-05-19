import React, { useState } from "react";
import axios from "axios";

const SubirArchivo = ({ onUploadSuccess }) => {
  const [archivo, setArchivo] = useState(null);
  const [mensaje, setMensaje] = useState("");

  const handleChange = (e) => {
    setArchivo(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!archivo) {
      setMensaje("Selecciona un archivo .csv");
      return;
    }

    const formData = new FormData();
    formData.append("archivo", archivo);

    try {
      const res = await axios.post(
        "http://localhost:8000/api/subir/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setMensaje("Archivo subido correctamente ✅");
      onUploadSuccess(); // opcional para refrescar lista
    } catch (error) {
      setMensaje("Error al subir el archivo ❌");
      console.error(error);
    }
  };

  return (
    <div style={{ marginBottom: "30px" }}>
      <h3>Subir nuevo archivo CSV</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleChange} />
        <button type="submit" style={{ marginLeft: "10px" }}>
          Subir
        </button>
      </form>
      {mensaje && <p>{mensaje}</p>}
    </div>
  );
};

export default SubirArchivo;
