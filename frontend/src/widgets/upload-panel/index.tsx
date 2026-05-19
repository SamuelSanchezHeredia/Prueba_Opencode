import { Card } from "../../shared/ui/card";

type UploadPanelProps = {
  sectors: string[];
  activeSector: string;
  status: string;
  onSectorChange: (value: string) => void;
  onFileChange: (file: File | null) => void;
  onUpload: () => void;
};

export function UploadPanel({
  sectors,
  activeSector,
  status,
  onSectorChange,
  onFileChange,
  onUpload,
}: UploadPanelProps) {
  return (
    <Card>
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
              onClick={() => onSectorChange(item)}
              className={`rounded-full px-4 py-2 text-sm border transition ${
                activeSector === item
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
            onChange={(event) => onFileChange(event.target.files?.[0] ?? null)}
            className="w-full text-sm"
          />
          <p className="mt-2 text-sm text-ink/60">
            Arrastra tu archivo o haz click para seleccionar.
          </p>
        </div>
        <button
          type="button"
          onClick={onUpload}
          className="mt-4 rounded-2xl bg-ember text-white py-3 text-base font-semibold shadow-soft hover:opacity-90"
        >
          Analizar CV
        </button>
      </div>
    </Card>
  );
}
