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

export function formatLabel(label: string) {
  return label
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export function getBadgeColor(metricValue: string) {
  const metricNumber = parseFloat(metricValue); // Use parseFloat to handle decimals like "7.5"

  if (metricNumber < 5) {
    return "bg-red-500 text-white";
  } else if (metricNumber >= 5 && metricNumber < 7) {
    return "bg-orange-500 text-white";
  } else {
    return "bg-green-500 text-white";
  }
}

function generateSessionId() {
  return crypto.randomUUID();
}

export function createOrRetrieveSessionId() {
  const storeKey = "cat-gen-session";
  const existingSession = localStorage.getItem(storeKey);
  if (existingSession) {
    return existingSession;
  }
  const newSessionId = generateSessionId();
  localStorage.setItem(storeKey, newSessionId);
  return newSessionId;
}
