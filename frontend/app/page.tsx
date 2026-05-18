"use client";

import { useState } from "react";
import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart } from "recharts";

const sectors = ["Tech", "Ventas", "Marketing"];

const scoreColors: Record<string, string> = {
  low: "#d6452f",
  mid: "#f7c548",
  high: "#2f8f7f",
};

const initialScores = {
  overall_score: 0,
  ats_score: 0,
  keyword_score: 0,
  semantic_score: 0,
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function HomePage() {
  const [sector, setSector] = useState(sectors[0]);
  const [file, setFile] = useState<File | null>(null);
  const [scores, setScores] = useState(initialScores);
  const [status, setStatus] = useState("Esperando CV...");
  const [corrections, setCorrections] = useState<any[]>([]);
  const [missingKeywords, setMissingKeywords] = useState<string[]>([]);
  const [foundKeywords, setFoundKeywords] = useState<string[]>([]);
  const [faqQuestion, setFaqQuestion] = useState("");
  const [faqAnswer, setFaqAnswer] = useState("");
  const [chatOpen, setChatOpen] = useState(false);
  const [reportText, setReportText] = useState("");
  const [issues, setIssues] = useState<string[]>([]);

  const chartData = [
    { subject: "ATS", value: scores.ats_score },
    { subject: "Keywords", value: scores.keyword_score },
    { subject: "General", value: scores.overall_score },
  ];

  const scoreColor =
    scores.overall_score < 50
      ? scoreColors.low
      : scores.overall_score < 75
      ? scoreColors.mid
      : scoreColors.high;

  const handleUpload = async () => {
    if (!file) return;

    setStatus("Procesando...");
    const payload = new FormData();
    payload.append("file", file);
    payload.append("target_sector", sector);

    const startRes = await fetch(`${API_BASE}/session/start`, {
      method: "POST",
      body: payload,
    });

    if (!startRes.ok) {
      setStatus("Error al subir el CV");
      return;
    }

    const session = await startRes.json();
    const analyzePayload = new FormData();
    analyzePayload.append("session_id", session.session_id);
    const analyzeRes = await fetch(`${API_BASE}/session/analyze`, {
      method: "POST",
      body: analyzePayload,
    });

    if (!analyzeRes.ok) {
      setStatus("Error al analizar el CV");
      return;
    }

    const analysis = await analyzeRes.json();
    setScores(analysis.scores);
    setCorrections(analysis.corrections || []);
    setMissingKeywords(analysis.scores.missing_keywords || []);
    setFoundKeywords(analysis.scores.found_keywords || []);
    setIssues(analysis.detected_issues || []);
    setReportText(
      [
        `Score general: ${analysis.scores.overall_score}`,
        `ATS: ${analysis.scores.ats_score}`,
        `Keywords: ${analysis.scores.keyword_score}`,
        `Semantica: ${analysis.scores.semantic_score}`,
        "",
        "Sugerencias:",
        ...(analysis.corrections || []).map(
          (item: any) => `- ${item.original_text} -> ${item.suggested_text}`
        ),
        "",
        "Issues detectados:",
        ...(analysis.detected_issues || []).map((item: string) => `- ${item}`),
      ].join("\n")
    );
    setStatus("Analisis completado");
  };

  const handleFaq = async () => {
    if (!faqQuestion) return;
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: faqQuestion }),
    });

    if (!res.ok) {
      setFaqAnswer("No se pudo responder la pregunta.");
      return;
    }

    const data = await res.json();
    setFaqAnswer(data.answer);
  };

  const downloadReport = () => {
    if (!reportText) return;
    const blob = new Blob([reportText], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "reporte_cv.txt";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <>
      <main className="min-h-screen px-6 py-10">
        <section className="max-w-6xl mx-auto grid gap-8">
        <header className="flex flex-col gap-4">
          <p className="text-sm uppercase tracking-[0.2em] text-ember">POC CV ATS</p>
          <h1 className="text-4xl md:text-5xl font-display text-ink">
            Del papel al score ATS en minutos.
          </h1>
          <p className="max-w-2xl text-lg text-ink/70">
            Carga tu CV, elige sector y recibe un diagnostico de formato y palabras clave.
          </p>
        </header>

        <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-6">
          <div className="glass rounded-3xl p-8 shadow-soft border border-white/60">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-display">Zona de carga</h2>
              <span className="text-sm text-ink/60">{status}</span>
            </div>
            <div className="mt-6 grid gap-4">
              <label className="text-sm font-semibold uppercase tracking-[0.2em] text-ink/60">
                Sector profesional
              </label>
              <div className="flex gap-3 flex-wrap">
                {sectors.map((item) => (
                  <button
                    key={item}
                    type="button"
                    onClick={() => setSector(item)}
                    className={`rounded-full px-4 py-2 text-sm border transition ${
                      sector === item
                        ? "bg-ink text-white border-ink"
                        : "border-ink/20 text-ink hover:border-ink"
                    }`}
                  >
                    {item}
                  </button>
                ))}
              </div>

              <label className="mt-4 text-sm font-semibold uppercase tracking-[0.2em] text-ink/60">
                CV (PDF/DOCX)
              </label>
              <div className="border-2 border-dashed border-ink/20 rounded-2xl p-6 text-center bg-white/50">
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={(event) => setFile(event.target.files?.[0] ?? null)}
                  className="w-full text-sm"
                />
                <p className="mt-2 text-sm text-ink/60">
                  Arrastra tu archivo o haz click para seleccionar.
                </p>
              </div>
              <button
                type="button"
                onClick={handleUpload}
                className="mt-4 rounded-2xl bg-ember text-white py-3 text-base font-semibold shadow-soft hover:opacity-90"
              >
                Analizar CV
              </button>
            </div>
          </div>

          <div className="glass rounded-3xl p-8 shadow-soft border border-white/60">
            <h2 className="text-2xl font-display">Score general</h2>
            <div className="mt-6 flex flex-col items-center">
              <div className="relative">
                <RadarChart width={280} height={240} data={chartData}>
                  <PolarGrid stroke="#d9d2c3" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: "#4b4b4b" }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar dataKey="value" stroke={scoreColor} fill={scoreColor} fillOpacity={0.6} />
                </RadarChart>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-4xl font-display" style={{ color: scoreColor }}>
                      {scores.overall_score}
                    </p>
                    <p className="text-xs uppercase tracking-[0.2em] text-ink/60">Score</p>
                  </div>
                </div>
              </div>
              <div className="mt-6 grid gap-2 text-sm text-ink/70">
                <p>ATS: {scores.ats_score}</p>
                <p>Keywords: {scores.keyword_score}</p>
                <p>Semantica: {scores.semantic_score}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-6">
          <div className="glass rounded-3xl p-8 shadow-soft border border-white/60">
            <h2 className="text-2xl font-display">Mejoras sugeridas</h2>
            <div className="mt-6 grid gap-4">
              {corrections.length === 0 ? (
                <p className="text-sm text-ink/60">Sin sugerencias por ahora.</p>
              ) : (
                corrections.map((item, index) => (
                  <div key={index} className="grid md:grid-cols-2 gap-4 bg-white/70 rounded-2xl p-4">
                    <div>
                      <p className="text-xs uppercase tracking-[0.2em] text-ink/50">Original</p>
                      <p className="mt-2 text-sm text-ink/80">{item.original_text}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-[0.2em] text-ink/50">Sugerido</p>
                      <p className="mt-2 text-sm text-ink/80">{item.suggested_text}</p>
                      <p className="mt-2 text-xs text-ink/50">{item.explanation}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="grid gap-6">
            <div className="glass rounded-3xl p-8 shadow-soft border border-white/60">
              <h2 className="text-2xl font-display">Nube de keywords</h2>
              <div className="mt-6 flex flex-wrap gap-2">
                {foundKeywords.map((kw) => (
                  <span key={kw} className="rounded-full bg-sage/20 text-sage px-3 py-1 text-xs">
                    {kw}
                  </span>
                ))}
                {missingKeywords.map((kw) => (
                  <span key={kw} className="rounded-full bg-ink/10 text-ink/50 px-3 py-1 text-xs">
                    {kw}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass rounded-3xl p-8 shadow-soft border border-white/60">
              <h2 className="text-2xl font-display">Issues detectados</h2>
              <div className="mt-4 grid gap-2 text-sm text-ink/70">
                {issues.length === 0 ? (
                  <p>Sin issues detectados.</p>
                ) : (
                  issues.map((issue) => <p key={issue}>• {issue}</p>)
                )}
              </div>
            </div>

            <button
              type="button"
              onClick={() => setChatOpen(true)}
              className="rounded-2xl bg-ink text-white py-3 text-sm font-semibold shadow-soft"
            >
              Abrir chat de FAQs
            </button>

            <div className="glass rounded-3xl p-8 shadow-soft border border-white/60">
              <h2 className="text-2xl font-display">Reporte final</h2>
              <p className="mt-2 text-sm text-ink/60">
                Descarga un resumen en texto plano con scores y sugerencias.
              </p>
              <button
                type="button"
                onClick={downloadReport}
                className="mt-4 rounded-xl bg-ember text-white py-2 text-sm font-semibold"
              >
                Descargar reporte
              </button>
            </div>
          </div>
        </div>
        </section>
      </main>
      {chatOpen && (
        <div className="fixed bottom-6 right-6 w-[320px] rounded-2xl bg-white shadow-soft border border-ink/10 p-4">
          <div className="flex items-center justify-between">
            <p className="text-sm font-semibold">Chat FAQs</p>
            <button onClick={() => setChatOpen(false)} className="text-xs text-ink/50">
              Cerrar
            </button>
          </div>
          <div className="mt-3 grid gap-2">
            <input
              value={faqQuestion}
              onChange={(event) => setFaqQuestion(event.target.value)}
              placeholder="Escribe tu duda..."
              className="rounded-xl border border-ink/20 px-3 py-2 text-sm"
            />
            <button
              type="button"
              onClick={handleFaq}
              className="rounded-xl bg-ink text-white py-2 text-sm font-semibold"
            >
              Preguntar
            </button>
            {faqAnswer && <p className="text-sm text-ink/70">{faqAnswer}</p>}
          </div>
        </div>
      )}
    </>
  );
}
