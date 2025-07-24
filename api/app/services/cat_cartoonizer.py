from app.utils.get_image import get_cat_image, get_cartoonized_cat
from app.utils.file_utils import load_txt_instuctions, get_image_data_url
from app.utils.response_handlers import process_llm_json
from app.config.settings import app_settings
from app.services.websocket_manager import WebsocketManager
from openai import OpenAI
import base64
from app.utils.logger import logger
from typing import Dict
import json


class CatCartoonizerAgent:
    def __init__(self, models:Dict[str, str]):
        """
        Initialize the CatCartoonizerAgent with the specified models.
        :param models: Dictionary containing model names and their corresponding IDs.
        """
        self.client = OpenAI(api_key=app_settings.openai_api_key)
        self.models = models
        self.generation_chat_history = [
        ]
        self.reflection_chat_history = []
        self.original_image_url = None
        self.results={}
    
    def initialize_generation_chat(self):
        if not self.original_image_url:
            self.original_image_url = get_cat_image(save_image=True)
            self.results["original_image_url"] = self.original_image_url
            self.results["runs"]=[]
            logger.info(f"Original cat image URL: {self.original_image_url}")
        self.generation_chat_history = [
            {
                "role": "developer",
                "content": load_txt_instuctions(app_settings.file_paths['generation_instruction_file_path'])
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Here is a photo of my cat, please create a detailed description for a cute cartoon cat image based on this photo."
                    },
                    {
                        "type": "input_image",
                        "image_url": self.original_image_url
                    }
                ]
            }
        ]

    def generate_prompt(self):
            """
            Generate a prompt for cartoonizing the cat image.
            :return: The generated prompt.
            """
            generation_prompt = self.client.responses.create(
                model=self.models["generation_model"],
                input=self.generation_chat_history,
                temperature=0.5
            ).output_text
            self.generation_chat_history.append(
                {
                    "role": "assistant",
                    "content": generation_prompt
                }
            )
            return generation_prompt
        
    def get_evaluation(self,generation_prompt:str,  encoded_image:str):
        """
        Get evaluation for the generated cartoonized cat image.
        :param generation_prompt: The prompt used for generating the cartoonized image.
        :param output_image_path: Path to the generated cartoonized image.
        :return: Evaluation response from the LLM.
        """
        reflection_chat_history=[
            {
                "role":"developer", 
                "content": load_txt_instuctions(app_settings.file_paths['evaluation_system_instructions_file_path'])
            }, 
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"This is the original cat photo"
                    },
                    {
                        "type": "input_image",
                        "image_url": self.original_image_url
                    }, 
                    {
                        "type": "input_text",
                        "text": f"This is the cartoonized cat image generated based on the prompt: {generation_prompt}"
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                ]
            }
        ]
        evaluation_response = self.client.responses.create(
            model=self.models["evaluation_model"],
            input=reflection_chat_history,
            temperature=0.0
        )
        print(f"Evaluation response: {evaluation_response}")
        evaluation_response = evaluation_response.output_text
        return process_llm_json(evaluation_response)
    def run_generation_loop(self, iterations: int = 3):
        """
        Run the main loop for a specified number of iterations to generate cartoonized cat images.
        :param iterations: Number of iterations to run.
        """
        self.initialize_generation_chat()
        generation_prompt = self.generate_prompt()
        logger.info(f"Generated prompt for cartoon image: {generation_prompt}")
        for i in range(iterations):
            iteration_num=i+1
            logger.info(f"Iteration {iteration_num} of {iterations}")
            
            output_image_path = f"images/cartoonized_cat_{iteration_num}.jpg"
            logger.info(f"Generating cartoonized cat image with prompt attempt {iteration_num}: {generation_prompt}")
            get_cartoonized_cat(
                prompt=generation_prompt, 
                output_image_path=output_image_path
            )
            with open(output_image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            logger.info(f"Cartoonized cat image saved as '{output_image_path}'")
            evaluation_response = self.get_evaluation(generation_prompt, encoded_image)
            score = float(evaluation_response.get("evaluation", {}).get("overall_impression", 0))
            if score >= 9:
                logger.info(f"High quality result achieved with score {score}. Exiting loop early.")
                break
            else:
                logger.warning(f"Low overall impression ({score}). Revising prompt.")
            if "critique" not in evaluation_response:
                logger.error("Critique not found in evaluation response. Exiting loop.")
                break
            logger.info(f"Evaluation response {iteration_num}: {evaluation_response}")
            logger.info(f"Critique: {evaluation_response['critique']}")
            self.generation_chat_history.append(
                {
                    "role":"user", 
                    "content":f"""My feedback on the image generated from your description: 
                    {evaluation_response["critique"]}
                    Please provide a revised image generation prompt based on this feedback to improve the cartoonized image of my cat."""
                }
            )
            revised_prompt_response =self. client.responses.create(
                model=self.models["generation_model"],
                input=self.generation_chat_history,
                temperature=0.5
            )
            result_data={
                "iteration_num": iteration_num,
                "prompt": generation_prompt,
                "cartoonized_image": get_image_data_url(output_image_path),
                "evaluation": evaluation_response
            }
            self.results["runs"].append(result_data)
            revised_prompt_response = revised_prompt_response.output_text
            generation_prompt = revised_prompt_response
            self.generation_chat_history.append(
                {
                    "role":"assistant", 
                    "content": revised_prompt_response
                }
            )
        logger.info("Generation loop completed.")
        with open("results.json", "w") as results_file:
            json.dump(self.results, results_file, indent=4)
        return self.results
    
    async def run_generation_loop_live(self, ws_manager: WebsocketManager, session_id: str, iterations: int = 3, ):
        """
        Run the main loop for a specified number of iterations to generate cartoonized cat images.
        :param iterations: Number of iterations to run.
        """
        self.initialize_generation_chat()
        generation_prompt = self.generate_prompt()
        logger.info(f"Generated prompt for cartoon image: {generation_prompt}")
        for i in range(iterations):
            iteration_num=i+1
            logger.info(f"Iteration {iteration_num} of {iterations}")
            
            output_image_path = f"images/cartoonized_cat_{iteration_num}.jpg"
            logger.info(f"Generating cartoonized cat image with prompt attempt {iteration_num}: {generation_prompt}")
            get_cartoonized_cat(
                prompt=generation_prompt, 
                output_image_path=output_image_path
            )
            with open(output_image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            logger.info(f"Cartoonized cat image saved as '{output_image_path}'")
            evaluation_response = self.get_evaluation(generation_prompt, encoded_image)
            score = float(evaluation_response.get("evaluation", {}).get("overall_impression", 0))
            if score >= 9:
                logger.info(f"High quality result achieved with score {score}. Exiting loop early.")
                break
            else:
                logger.warning(f"Low overall impression ({score}). Revising prompt.")
            if "critique" not in evaluation_response:
                logger.error("Critique not found in evaluation response. Exiting loop.")
                break
            logger.info(f"Evaluation response {iteration_num}: {evaluation_response}")
            logger.info(f"Critique: {evaluation_response['critique']}")
            self.generation_chat_history.append(
                {
                    "role":"user", 
                    "content":f"""My feedback on the image generated from your description: 
                    {evaluation_response["critique"]}
                    Please provide a revised image generation prompt based on this feedback to improve the cartoonized image of my cat."""
                }
            )
            revised_prompt_response =self. client.responses.create(
                model=self.models["generation_model"],
                input=self.generation_chat_history,
                temperature=0.5
            )
            result_data={
                "iteration_num": iteration_num,
                "prompt": generation_prompt,
                "cartoonized_image": get_image_data_url(output_image_path),
                "evaluation": evaluation_response
            }
            self.results["runs"].append(result_data)
            revised_prompt_response = revised_prompt_response.output_text
            generation_prompt = revised_prompt_response
            await ws_manager.notify(session_id, result_data)
            self.generation_chat_history.append(
                {
                    "role":"assistant", 
                    "content": revised_prompt_response
                }
            )
        logger.info("Generation loop completed.")
        with open("results.json", "w") as results_file:
            json.dump(self.results, results_file, indent=4)
        return self.results
