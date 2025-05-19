import React, { useEffect, useState } from "react";
import Papa from "papaparse";

const TablaCSV = ({ url, columnasVisibles = null }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(url)
      .then((res) => res.text())
      .then((csv) => {
        const parsed = Papa.parse(csv, { header: true });
        setData(parsed.data);
      });
  }, [url]);

  if (!data.length) return <p>Cargando tabla...</p>;

  // Filtrar columnas si se proporciona una lista
  const columnas = columnasVisibles || Object.keys(data[0]);

  return (
    <div className="table-wrapper">
      <table className="csv-table">
        <thead>
          <tr>
            {columnas.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((fila, i) => (
            <tr key={i}>
              {columnas.map((col) => (
                <td key={col}>{fila[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaCSV;
