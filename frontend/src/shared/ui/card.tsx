import { PropsWithChildren } from "react";

type CardProps = PropsWithChildren<{ className?: string }>;

export function Card({ className, children }: CardProps) {
  return (
    <div className={`glass rounded-3xl p-8 shadow-soft border border-white/60 ${className ?? ""}`}>
      {children}
    </div>
  );
}
