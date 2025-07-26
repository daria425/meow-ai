type EvaluationScores = {
  similarity_to_original: string;
  cuteness_factor: string;
  artistic_style: string;
  overall_impression: string;
};

type EvaluationData = {
  evaluation: EvaluationScores;
  critique: string;
};

export type RunData = {
  iteration_num: number;
  prompt: string;
  cartoonized_image: string;
  evaluation: EvaluationData;
};

type InitialNotificationMessage = {
  original_image_url: string;
  type: "initial_notification";
};
type RunNotificationMessage = {
  type: "run_notification";
  iteration_num: number;
  prompt: string;
  cartoonized_image: string;
  evaluation: EvaluationData;
};

export type WebSocketMessage =
  | InitialNotificationMessage
  | RunNotificationMessage;

export type GenerationRun = {
  original_image_url: string;
  runs: RunData[];
};

export type GenerationConfig = {
  iterations: number;
  //add stuff later
};

export type GenerationRunCompleteResponse = {
  status: string;
  message: string;
  total_iterations: number;
  generation_data: GenerationRun;
};
