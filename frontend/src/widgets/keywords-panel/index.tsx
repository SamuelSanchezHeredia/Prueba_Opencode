import { Card } from "../../shared/ui/card";

type KeywordsPanelProps = {
  found: string[];
  missing: string[];
};

export function KeywordsPanel({ found, missing }: KeywordsPanelProps) {
  return (
    <Card>
      <h2 className="text-2xl font-display">Nube de keywords</h2>
      <div className="mt-6 flex flex-wrap gap-2">
        {found.map((kw) => (
          <span key={kw} className="rounded-full bg-sage/20 text-sage px-3 py-1 text-xs">
            {kw}
          </span>
        ))}
        {missing.map((kw) => (
          <span key={kw} className="rounded-full bg-ink/10 text-ink/50 px-3 py-1 text-xs">
            {kw}
          </span>
        ))}
      </div>
    </Card>
  );
}
