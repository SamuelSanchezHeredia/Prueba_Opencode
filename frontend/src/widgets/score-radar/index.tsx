import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart } from "recharts";

import { Card } from "../../shared/ui/card";
import { InitialScores } from "../../shared/model/types";

const scoreColors: Record<string, string> = {
  low: "#d6452f",
  mid: "#f7c548",
  high: "#2f8f7f",
};

type ScoreRadarProps = {
  scores: InitialScores;
};

export function ScoreRadar({ scores }: ScoreRadarProps) {
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

  return (
    <Card>
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
    </Card>
  );
}
