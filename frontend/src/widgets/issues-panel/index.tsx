import { Card } from "../../shared/ui/card";

type IssuesPanelProps = {
  issues: string[];
};

export function IssuesPanel({ issues }: IssuesPanelProps) {
  return (
    <Card>
      <h2 className="text-2xl font-display">Issues detectados</h2>
      <div className="mt-4 grid gap-2 text-sm text-ink/70">
        {issues.length === 0 ? (
          <p>Sin issues detectados.</p>
        ) : (
          issues.map((issue) => <p key={issue}>• {issue}</p>)
        )}
      </div>
    </Card>
  );
}
