import catCartoonizerServiceInstance from "../../services/catCartonizerService";
import meowAIPlaceholder from "../../assets/meow_ai_placeholder.svg";
import lottieLoader from "../../assets/lottie_loader.lottie";
import { DotLottieReact } from "@lottiefiles/dotlottie-react";
import { useQuery } from "@tanstack/react-query";
import type {
  GenerationRun,
  GenerationRunCompleteResponse,
  WebSocketMessage,
  GenerationConfig,
  RunData,
} from "@/types/catGeneration";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import OnboardingModal from "./OnboardingModal";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { useWebSocket } from "@/hooks/useWebsocket";
import { websocketUrl } from "@/lib/api";
import {
  simulateMockData,
  formatLabel,
  getBadgeColor,
  createOrRetrieveSessionId,
} from "@/lib/utils";
import mockGenerationRunData from "../../data/mockRun.json";
import {
  Images,
  WandSparkles,
  MessageCircleMore,
  RefreshCcw,
  SlidersHorizontal,
  Loader,
  Repeat,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useState, useEffect, useMemo } from "react";
function RunCard({ run }: { run: RunData }) {
  const evaluationMetrics = Object.entries(run.evaluation.evaluation);
  console.log(evaluationMetrics);
  return (
    <Card>
      <CardHeader className="flex items-center gap-4">
        <div className="font-semibold text-white h-8 w-8 rounded-full bg-gradient-to-r from-[#622a9b] to-[#c157c7] text-align-center flex items-center justify-center">
          {run.iteration_num}
        </div>
        <CardTitle className="text-sm">Iteration {run.iteration_num}</CardTitle>
      </CardHeader>
      <CardContent className="sm:grid sm:grid-cols-3 flex flex-col gap-4">
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
          <div className="space-y-2">
            {evaluationMetrics.map(([label, metric], idx) => (
              <div
                key={idx}
                className="flex justify-between items-center bg-gray-50 p-2 rounded"
              >
                <span className="text-xs font-medium text-gray-600">
                  {formatLabel(label)}:
                </span>
                <Badge className={getBadgeColor(metric)}>{metric}/10</Badge>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function StartGenerateButton({
  state,
  handleGenerate,
}: {
  state: "loading" | "error" | "success" | "idle";
  handleGenerate: () => void;
}) {
  if (state === "loading") {
    return (
      <Button
        className="bg-gradient-to-r from-[#622a9b] to-[#c157c7] text-white text-xs"
        disabled={true}
      >
        <Loader className="h-4 w-4" />
        Generating...
      </Button>
    );
  }
  return (
    <Button
      className="bg-gradient-to-r from-[#622a9b] to-[#c157c7] text-white text-xs"
      onClick={handleGenerate}
    >
      <Repeat className="h-4 w-4" />
      Generate
    </Button>
  );
}
function GenerationStatusCard({
  state,
  original_image_url,
  handleGenerate,
  generationConfig,
  handleUpdateGenerationConfig,
}: {
  state: "loading" | "error" | "success" | "idle";
  original_image_url: string | undefined;
  handleGenerate: () => void;
  generationConfig: GenerationConfig;
  handleUpdateGenerationConfig: (
    updateKey: string,
    updateValue: number | string,
    convertValueToNumber: boolean
  ) => void;
}) {
  return (
    <Card>
      <CardHeader className="flex items-center gap-4">
        <CardTitle className="text-sm">Cat Cartoonizer</CardTitle>
      </CardHeader>
      <CardContent className="sm:grid sm:grid-cols-3 flex flex-col gap-4">
        {/* Image Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Images className="h-4 w-4 text-violet-500" />
            <h4 className="font-semibold">Seed Image</h4>
          </div>

          <div className="h-64">
            {original_image_url ? (
              <img
                src={original_image_url}
                className="object-cover w-full h-full rounded-lg"
                alt="Original Cat"
              />
            ) : (
              <div className="h-full rounded-lg bg-zinc-500 flex justify-center items-center">
                <img
                  src={meowAIPlaceholder}
                  alt="Cat placeholder"
                  className="h-64"
                />
              </div> // placeholder
            )}
          </div>
          <StartGenerateButton state={state} handleGenerate={handleGenerate} />
        </div>

        {/* Status Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <RefreshCcw className="h-4 w-4 text-blue-500" />
            <h4 className="font-semibold">Generation Status</h4>
          </div>
          <div className="bg-blue-100 p-4 rounded-lg h-48 flex items-center justify-center">
            {state === "loading" && (
              <div className="flex flex-col justify-center items-center gap-2">
                <DotLottieReact src={lottieLoader} loop autoplay />
                <p className="text-pink-500">Generating...</p>
              </div>
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
        {/*Config Section*/}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <SlidersHorizontal className="h-4 w-4 text-emerald-500" />
            <h4 className="font-semibold">Parameters</h4>
          </div>
          <div className="bg-emerald-100 p-4 rounded-lg h-48">
            <label htmlFor="iteration-count" className="text-gray-500">
              Iterations
            </label>
            <Slider
              value={[generationConfig.iterations]}
              id="iteration-count"
              max={10}
              step={1}
              className="w-full"
              onValueChange={(value) =>
                handleUpdateGenerationConfig("iterations", value[0], true)
              }
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
export function CatGenerator() {
  const [startGeneration, setStartGeneration] = useState<boolean>(false);
  const [showOnboardingModal, setShowOnboardingModal] = useState<boolean>(true);
  const [generationConfig, setGenerationConfig] = useState<GenerationConfig>({
    iterations: 3,
  });
  const [generationRunData, setGenerationRunData] = useState<GenerationRun>({
    original_image_url: "",
    runs: [],
  });
  const [generationState, setGenerationState] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const sessionId = useMemo(() => createOrRetrieveSessionId(), []);
  const { status, message } = useWebSocket(`${websocketUrl}${sessionId}`);
  const addRunData = (messageData: WebSocketMessage) => {
    console.log(messageData);
    if (
      messageData.type === "initial_notification" &&
      messageData.original_image_url
    ) {
      setGenerationRunData((prevData) => ({
        ...prevData,
        original_image_url: messageData.original_image_url,
      }));
    } else if (
      messageData.type === "run_notification" &&
      messageData.iteration_num &&
      messageData.prompt
    ) {
      setGenerationRunData((prevData) => ({
        ...prevData,
        runs: [...prevData.runs, messageData as RunData],
      }));
    }
  };
  useEffect(() => {
    if (message) {
      addRunData(message);
    }
  }, [message]);
  console.log(status, message);
  const handleCloseOnboarding = () => {
    setShowOnboardingModal(false);
  };
  const { error, isLoading } = useQuery({
    queryKey: ["cartoonizedCat"],
    queryFn: async () => {
      console.log("Fetching cartoonized cat...");
      const response =
        await catCartoonizerServiceInstance.getLiveCartoonizedCatGeneration(
          generationConfig,
          sessionId
        );
      setStartGeneration(false); // Reset after fetching
      setGenerationState("success");
      return response as GenerationRunCompleteResponse;
    },
    enabled: startGeneration, // Only run query when startGeneration is true
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });
  useEffect(() => {
    if (isLoading) {
      setGenerationState("loading");
    } else if (error) {
      setGenerationState("error");
    }
  }, [isLoading, error]);
  const handleGenerate = () => {
    // Clear data first
    setGenerationState("idle");
    setGenerationRunData({
      original_image_url: "",
      runs: [],
    });

    if (import.meta.env.MODE === "development") {
      setGenerationState("loading");
      simulateMockData(mockGenerationRunData, setGenerationRunData, 2000);
    } else {
      setStartGeneration(true);
    }
  };
  const handleUpdateGenerationConfig = (
    updateKey: string,
    updateValue: number | string,
    convertValueToNumber: boolean = false
  ) => {
    const updatedConfig = {
      ...generationConfig,
      [updateKey]:
        typeof updateValue === "string" && convertValueToNumber
          ? parseInt(updateValue)
          : updateValue,
    };
    setGenerationConfig(updatedConfig);
  };
  return (
    <div className="text-xs space-y-4">
      {showOnboardingModal && (
        <OnboardingModal
          isOpen={showOnboardingModal}
          onClose={handleCloseOnboarding}
        />
      )}
      <GenerationStatusCard
        state={generationState}
        handleGenerate={handleGenerate}
        original_image_url={generationRunData.original_image_url}
        generationConfig={generationConfig}
        handleUpdateGenerationConfig={handleUpdateGenerationConfig}
      />
      {generationRunData.runs.map((run) => (
        <RunCard key={run.iteration_num} run={run} />
      ))}
    </div>
  );
}
