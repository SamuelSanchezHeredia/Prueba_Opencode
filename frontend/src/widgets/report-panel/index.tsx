import { Card } from "../../shared/ui/card";

type ReportPanelProps = {
  reportText: string;
};

export function ReportPanel({ reportText }: ReportPanelProps) {
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
    <Card>
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
    </Card>
  );
}
