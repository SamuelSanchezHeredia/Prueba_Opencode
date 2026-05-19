export type Scores = {
  overall_score: number;
  ats_score: number;
  keyword_score: number;
  semantic_score: number;
  missing_sections: string[];
  missing_keywords: string[];
  found_keywords: string[];
};

export type Correction = {
  original_text: string;
  suggested_text: string;
  explanation: string;
  category: string;
};

export type AnalysisResult = {
  session_id: string;
  scores: Scores;
  extracted_sections: Record<string, string>;
  raw_text: string;
  keywords_checked: { sector: string; total: number };
  corrections: Correction[];
  detected_issues: string[];
  semantic_contract: Record<string, unknown>;
};

export type SessionStartResponse = {
  session_id: string;
  filename: string;
  target_sector: string;
};

export type InitialScores = Pick<
  Scores,
  "overall_score" | "ats_score" | "keyword_score" | "semantic_score"
>;
