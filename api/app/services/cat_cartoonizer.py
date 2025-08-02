from app.utils.get_image import get_cat_image, get_cartoonized_cat
from app.utils.file_utils import load_txt_instuctions, get_image_data_url
from app.utils.response_handlers import process_llm_json
from app.utils.decorators import retry_on_failure
from app.config.settings import app_settings
from app.services.websocket_manager import WebsocketManager
from openai import OpenAI
import base64
from app.utils.logger import logger
from typing import Dict
import json
import psutil

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
    
    async def initialize_generation_chat(self, ws_manager: WebsocketManager, session_id: str):
        if not self.original_image_url:
            self.original_image_url = get_cat_image(save_image=True)
            self.results["original_image_url"] = self.original_image_url
            self.results["runs"]=[]
            await ws_manager.notify(session_id=session_id, message={
            "type": "initial_notification",
            "original_image_url": self.original_image_url
        } )
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
        
    @retry_on_failure(max_retries=3, delay=1.0, backoff_exp=2.0)
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
    async def revise_prompt(self, evaluation_response:dict, iteration_num:int, session_id: str, ws_manager: WebsocketManager)->str:
                think_prompt={
                     "role":"user",
                     "content": f"""
            My feedback on the image generated from your description: 
            {evaluation_response["critique"]}
            
            Please think through:
            1. What specific issues were identified in the feedback?
            2. What aspects of the original prompt might have caused these issues?
            3. What changes should be made to address each concern?
            
            Please analyze the feedback step by step and concisely answer each question.
            Your response will be presented with 'AI had a thought: <your response>' so make sure you don't yap 
            DO NOT USE MARKDOWN
            EXAMPLES:
            "I need to emphasize sharper whiskers and brighter eyes. I added too much background detail that distracts from the cat."
"My cartoon style was too realistic. I should emphasize rounded features and simplify colors."  
"I missed the tabby stripes. I need to specify the orange and black pattern more clearly."
"I made the ears too small and eyes not expressive enough. I should add playful pose details."
"My color palette was too muted. I need vibrant cartoon colors and better contrast."
"I got the face proportions wrong - I should make eyes larger and nose smaller for a cute cartoon look."
            """}
                think_input=self.generation_chat_history+[think_prompt]
                ai_think=self.client.responses.create(
                                     model=self.models["generation_model"],
                    input=think_input,
                    temperature=0.3
                ).output_text
                logger.info(f"AI had a thought:{ai_think}")
                thought_notification={
        "iteration_num": iteration_num,
                "thought": ai_think,
                "type": "think_notification"

                }
                await ws_manager.notify(session_id, thought_notification)
                self.generation_chat_history.append(
                    {
                        "role":"user", 
                        "content":f"""My feedback on the image generated from your description: 
                        {evaluation_response["critique"]}
                        Please provide a revised image generation prompt based on this feedback to improve the cartoonized image of my cat."""
                    }
                )
                revised_prompt_response = self.client.responses.create(
                    model=self.models["generation_model"],
                    input=self.generation_chat_history,
                    temperature=0.3
                )
                revised_prompt_response = revised_prompt_response.output_text
                return revised_prompt_response

    async def run_generation_loop_live(self, ws_manager: WebsocketManager, session_id: str, iterations: int = 3 ):
        """
        Run the main loop for a specified number of iterations to generate cartoonized cat images.
        :param iterations: Number of iterations to run.
        """
        await self.initialize_generation_chat(ws_manager=ws_manager, session_id=session_id)
        generation_prompt = self.generate_prompt()
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
            
            result_data={
                "iteration_num": iteration_num,
                "prompt": generation_prompt,
                "cartoonized_image": get_image_data_url(output_image_path),
                "evaluation": evaluation_response
            }
            self.results["runs"].append(result_data)
            logger.info(f"Sending run_notification message to {session_id}")
            await ws_manager.notify(session_id, {**result_data, "type": "run_notification"})
            
            if score >= 9:
                logger.info(f"High quality result achieved with score {score}. Exiting loop early.")
                break
            else:
                logger.warning(f"Low overall impression ({score}). Revising prompt.")
            
            if "critique" not in evaluation_response:
                logger.error("Critique not found in evaluation response. Exiting loop.")
                break
                
            # Only continue with revision if we're not on the last iteration
            if iteration_num < iterations:
                logger.info(f"Evaluation response {iteration_num}: {evaluation_response}")
                revised_prompt_response=await self.revise_prompt(evaluation_response=evaluation_response, ws_manager=ws_manager, iteration_num=iteration_num, session_id=session_id)
                logger.info(f"Revised prompt:{revised_prompt_response}")
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

        return {
            "status": "success",
            "message": "Generation completed successfully",
            "total_iterations": len(self.results["runs"]), 
            "generation_data":self.results, 
        }