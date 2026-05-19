import { Card } from "../../shared/ui/card";
import { Correction } from "../../shared/model/types";

type SuggestionsPanelProps = {
  corrections: Correction[];
};

export function SuggestionsPanel({ corrections }: SuggestionsPanelProps) {
  return (
    <Card>
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
    </Card>
  );
}
