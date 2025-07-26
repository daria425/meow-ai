import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function simulateMockData<T>(
  mockData: T,
  setStateFunction: (data: T) => void,
  delay: number = 2000
): void {
  if (import.meta.env.MODE === "development") {
    setTimeout(() => {
      setStateFunction(mockData);
    }, delay);
  }
}
