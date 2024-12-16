import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [url, setUrl] = useState("");
  const [qrCodeUrl, setQrCodeUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setQrCodeUrl(""); // Reset previous QR Code

    try {
      const response = await axios.post("http://localhost:8000/api/generate", {
        url,
      });
      setQrCodeUrl(response.data.qrCodeUrl);
    } catch (error) {
      console.error("Erreur lors de la génération du QR Code :", error);
      alert("Une erreur s'est produite. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Générateur de QR Code</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Entrez une URL"
          required
          style={{
            padding: "10px",
            fontSize: "16px",
            width: "300px",
            marginRight: "10px",
          }}
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            backgroundColor: "#0070f3",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Générer
        </button>
      </form>
      {loading && <p>Génération en cours...</p>}
      {qrCodeUrl && (
        <div>
          <h3>Votre QR Code :</h3>
          <img src={qrCodeUrl} alt="QR Code" style={{ marginTop: "20px" }} />
        </div>
      )}
    </div>
  );
}
