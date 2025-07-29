import type { ReactNode } from "react";
import meowAILogo from "../../assets/meow_ai_logo.svg";
export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <div className="bg-white flex items-center">
        <img className="h-[50px] w-[50px]" src={meowAILogo} alt="Logo"></img>
        <h1 className="text-lavender font-semibold text-lg">Meow AI</h1>
      </div>
      {children}
    </div>
  );
}
