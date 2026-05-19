type ChatLauncherProps = {
  onOpen: () => void;
};

export function ChatLauncher({ onOpen }: ChatLauncherProps) {
  return (
    <button
      type="button"
      onClick={onOpen}
      className="rounded-2xl bg-ink text-white py-3 text-sm font-semibold shadow-soft"
    >
      Abrir chat de FAQs
    </button>
  );
}
