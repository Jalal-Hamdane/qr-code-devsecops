import { useState } from "react";
import axios from "axios";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function Home() {
  const [url, setUrl] = useState("");
  const [qrCodeUrl, setQrCodeUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setQrCodeUrl("");

    try {
      const response = await axios.post(`${backendUrl}/api/generate`, { url });
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
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Entrez une URL"
          required
        />
        <button type="submit">Générer</button>
      </form>
      {loading && <p>Génération en cours...</p>}
      {qrCodeUrl && <img src={qrCodeUrl} alt="QR Code" />}
    </div>
  );
}
