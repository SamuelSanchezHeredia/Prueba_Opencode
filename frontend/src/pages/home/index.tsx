"use client";

import { useState } from "react";
import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart } from "recharts";

import { Card } from "../../shared/ui/card";
import { ScoreRadar } from "../../widgets/score-radar";
import { UploadPanel } from "../../widgets/upload-panel";
import { SuggestionsPanel } from "../../widgets/suggestions-panel";
import { KeywordsPanel } from "../../widgets/keywords-panel";
import { IssuesPanel } from "../../widgets/issues-panel";
import { ReportPanel } from "../../widgets/report-panel";
import { ChatLauncher } from "../../widgets/chat-launcher";
import { ChatWidget } from "../../widgets/chat-widget";
import { analyzeCv, startSession } from "../../shared/api/cv";
import { AnalysisResult, InitialScores } from "../../shared/model/types";

const sectors = ["Tech", "Ventas", "Marketing"];

const initialScores: InitialScores = {
  overall_score: 0,
  ats_score: 0,
  keyword_score: 0,
  semantic_score: 0,
};

export default function HomePage() {
  const [sector, setSector] = useState(sectors[0]);
  const [file, setFile] = useState<File | null>(null);
  const [scores, setScores] = useState(initialScores);
  const [status, setStatus] = useState("Esperando CV...");
  const [corrections, setCorrections] = useState<AnalysisResult["corrections"]>([]);
  const [missingKeywords, setMissingKeywords] = useState<string[]>([]);
  const [foundKeywords, setFoundKeywords] = useState<string[]>([]);
  const [issues, setIssues] = useState<string[]>([]);
  const [chatOpen, setChatOpen] = useState(false);
  const [faqQuestion, setFaqQuestion] = useState("");
  const [faqAnswer, setFaqAnswer] = useState("");
  const [reportText, setReportText] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    setStatus("Procesando...");

    const session = await startSession(file, sector);
    if (!session) {
      setStatus("Error al subir el CV");
      return;
    }

    const analysis = await analyzeCv(session.session_id);
    if (!analysis) {
      setStatus("Error al analizar el CV");
      return;
    }

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
          (item) => `- ${item.original_text} -> ${item.suggested_text}`
        ),
        "",
        "Issues detectados:",
        ...(analysis.detected_issues || []).map((item) => `- ${item}`),
      ].join("\n")
    );
    setStatus("Analisis completado");
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
            <UploadPanel
              sectors={sectors}
              activeSector={sector}
              onSectorChange={setSector}
              onFileChange={setFile}
              onUpload={handleUpload}
              status={status}
            />
            <ScoreRadar scores={scores} />
          </div>

          <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-6">
            <SuggestionsPanel corrections={corrections} />

            <div className="grid gap-6">
              <KeywordsPanel found={foundKeywords} missing={missingKeywords} />
              <IssuesPanel issues={issues} />
              <ChatLauncher onOpen={() => setChatOpen(true)} />
              <ReportPanel reportText={reportText} />
            </div>
          </div>
        </section>
      </main>
      {chatOpen && (
        <ChatWidget
          question={faqQuestion}
          answer={faqAnswer}
          onQuestionChange={setFaqQuestion}
          onAnswerChange={setFaqAnswer}
          onClose={() => setChatOpen(false)}
        />
      )}
    </>
  );
}
