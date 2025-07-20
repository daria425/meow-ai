import { CatGenerator } from "./components/cat-generator/CatGenerator";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
function App() {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-r from-[#ddbeed] via-[#e0bdab] via-[#a8e3c1] via-[#dadaa9] to-[#a99beb]">
        <div className="max-w-6xl mx-auto px-8">
          <CatGenerator />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
