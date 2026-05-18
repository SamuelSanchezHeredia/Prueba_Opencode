import "./globals.css";

export const metadata = {
  title: "CV ATS Optimizer",
  description: "POC de correccion y scoring ATS",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
