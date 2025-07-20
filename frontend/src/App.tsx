import { CatCartoonizer } from "./components/CatGenerator";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
function App() {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <CatCartoonizer />
    </QueryClientProvider>
  );
}

export default App;
