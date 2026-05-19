import { useState } from "react";

import { askFaq } from "../../shared/api/cv";

type ChatWidgetProps = {
  question: string;
  answer: string;
  onQuestionChange: (value: string) => void;
  onAnswerChange: (value: string) => void;
  onClose: () => void;
};

export function ChatWidget({
  question,
  answer,
  onQuestionChange,
  onAnswerChange,
  onClose,
}: ChatWidgetProps) {
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);
    const response = await askFaq(question);
    if (!response) {
      onAnswerChange("No se pudo responder la pregunta.");
      setLoading(false);
      return;
    }
    onAnswerChange(response.answer);
    setLoading(false);
  };

  return (
    <div className="fixed bottom-6 right-6 w-[320px] rounded-2xl bg-white shadow-soft border border-ink/10 p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold">Chat FAQs</p>
        <button onClick={onClose} className="text-xs text-ink/50">
          Cerrar
        </button>
      </div>
      <div className="mt-3 grid gap-2">
        <input
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="Escribe tu duda..."
          className="rounded-xl border border-ink/20 px-3 py-2 text-sm"
        />
        <button
          type="button"
          onClick={handleAsk}
          className="rounded-xl bg-ink text-white py-2 text-sm font-semibold"
        >
          {loading ? "Consultando..." : "Preguntar"}
        </button>
        {answer && <p className="text-sm text-ink/70">{answer}</p>}
      </div>
    </div>
  );
}
