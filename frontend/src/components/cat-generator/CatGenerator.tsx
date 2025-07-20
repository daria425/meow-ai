import catCartoonizerServiceInstance from "../../services/catCartonizerService";
import { useQuery } from "@tanstack/react-query";
import type { GenerationRun, RunData } from "@/types/catGeneration";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Images,
  WandSparkles,
  MessageCircleMore,
  RefreshCcw,
} from "lucide-react";
import { useState } from "react";
function RunCard({ run }: { run: RunData }) {
  return (
    <Card>
      <CardHeader className="flex items-center gap-4">
        <div className="font-semibold text-white h-8 w-8 rounded-full bg-gradient-to-r from-[#622a9b] to-[#c157c7] text-align-center flex items-center justify-center">
          {run.iteration_num}
        </div>
        <CardTitle className="text-sm">Iteration {run.iteration_num}</CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-3 gap-4">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <WandSparkles className="h-4 w-4 text-violet-500" />
            <h4 className="font-semibold">Prompt</h4>
          </div>
          <div className="bg-violet-100 p-4 rounded-lg h-48 overflow-y-auto">
            <p className="leading-6">"{run.prompt}"</p>
          </div>
        </div>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Images className="h-4 w-4 text-zinc-500" />
            <h4 className="font-semibold">Generated Image</h4>
          </div>
          <div className="h-64">
            <img
              src={run.cartoonized_image}
              className="object-cover w-full h-full rounded-lg"
              alt={`Cartoonized Cat ${run.iteration_num}`}
            />
          </div>
        </div>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <MessageCircleMore className="h-4 w-4 text-emerald-500" />
            <h4 className="font-semibold">AI Critique</h4>
          </div>
          {/* <ul>
            <li>
              Similarity to Original:{" "}
              {run.evaluation.evaluation.similarity_to_original}
            </li>
            <li>
              Cuteness Factor: {run.evaluation.evaluation.cuteness_factor}
            </li>
            <li>Artistic Style: {run.evaluation.evaluation.artistic_style}</li>
            <li>
              Overall Impression: {run.evaluation.evaluation.overall_impression}
            </li>
          </ul> */}
          <div className="bg-emerald-100 p-4 rounded-lg h-48 overflow-y-auto">
            <p className="leading-6">"{run.evaluation.critique}"</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function GenerationStatusCard({
  state,
  original_image_url,
  handleGenerate,
}: {
  state: "loading" | "error" | "success" | "idle";
  original_image_url: string | undefined;
  handleGenerate: () => void;
}) {
  return (
    <Card>
      <CardHeader className="flex items-center gap-4">
        <CardTitle className="text-sm">Cat Cartoonizer</CardTitle>
        <button onClick={handleGenerate}>Generate</button>
      </CardHeader>
      <CardContent className="grid grid-cols-3 gap-4">
        {/* Image Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Images className="h-4 w-4 text-violet-500" />
            <h4 className="font-semibold">Seed Image</h4>
          </div>
          <div className="h-64">
            {state === "success" && original_image_url ? (
              <img
                src={original_image_url}
                className="object-cover w-full h-full rounded-lg"
                alt="Original Cat"
              />
            ) : (
              <div className="h-full rounded-lg bg-zinc-500"></div> // placeholder
            )}
          </div>
        </div>
        {/* Status Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <RefreshCcw className="h-4 w-4 text-blue-500" />
            <h4 className="font-semibold">Generation Status</h4>
          </div>
          <div className="bg-blue-100 p-4 rounded-lg h-48 flex items-center justify-center">
            {state === "loading" && (
              <p className="text-blue-600">Generating...</p>
            )}
            {state === "error" && (
              <p className="text-red-600">Error generating cat cartoon.</p>
            )}
            {state === "success" && (
              <p className="text-green-600">
                Cat cartoon generated successfully!
              </p>
            )}
            {state === "idle" && (
              <p className="text-gray-600">Click "Generate" to start.</p>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
export function CatGenerator() {
  const [startGeneration, setStartGeneration] = useState(false);
  const { data, isLoading, error } = useQuery({
    queryKey: ["cartoonizedCat"],
    queryFn: async () => {
      console.log("Fetching cartoonized cat...");
      const response = await catCartoonizerServiceInstance.getCartoonizedCat();
      setStartGeneration(false); // Reset after fetching
      return response as GenerationRun;
    },
    enabled: startGeneration, // Only run query when startGeneration is true
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });
  const handleGenerate = () => {
    setStartGeneration(true);
  };
  if (isLoading) {
    return (
      <GenerationStatusCard
        handleGenerate={handleGenerate}
        state="loading"
        original_image_url={undefined}
      />
    );
  }
  if (error) {
    return (
      <GenerationStatusCard
        handleGenerate={handleGenerate}
        state="error"
        original_image_url={undefined}
      />
    );
  }
  if (!data) {
    return (
      <GenerationStatusCard
        handleGenerate={handleGenerate}
        state="idle"
        original_image_url={undefined}
      />
    );
  }
  return (
    <div className="text-xs space-y-4">
      <GenerationStatusCard
        state={"success"}
        handleGenerate={handleGenerate}
        original_image_url={data.original_image_url}
      />
      {data.runs.map((run) => (
        <RunCard key={run.iteration_num} run={run} />
      ))}
    </div>
  );
}
