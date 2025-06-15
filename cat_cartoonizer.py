from get_image import get_cat_image, get_cartoonized_cat
from file_utils import load_txt_instuctions
from response_handlers import process_llm_json
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from logger import logger
from typing import Dict
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
generation_instruction_file_path = "./generation_system_instructions.txt"
evaluation_system_instructions_file_path = "./evaluation_system_instructions.txt"
class CatCartoonizerAgent:
    def __init__(self, models:Dict[str, str]):
        """
        Initialize the CatCartoonizerAgent with the specified models.
        :param models: Dictionary containing model names and their corresponding IDs.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.models = models
        self.generation_chat_history = [
        ]
        self.reflection_chat_history = []
        self.original_image_url = None
    
    def initialize_generation_chat(self):
        if not self.original_image_url:
            self.original_image_url = get_cat_image(save_image=True)
            logger.info(f"Original cat image URL: {self.original_image_url}")
        self.generation_chat_history = [
            {
                "role": "developer",
                "content": load_txt_instuctions(generation_instruction_file_path)
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
        
    def run_generation_loop(self, iterations: int = 3):
        """
        Run the main loop for a specified number of iterations to generate cartoonized cat images.
        :param iterations: Number of iterations to run.
        """
        self.initialize_generation_chat()
        generation_prompt = self.generate_prompt()
        logger.info(f"Generated prompt for cartoon image: {generation_prompt}")
        for i in range(iterations):
            logger.info(f"Iteration {i + 1} of {iterations}")
            output_image_path = f"images/cartoonized_cat_{i + 1}.jpg"
            logger.info(f"Generated prompt for cartoon image: {generation_prompt}")
            get_cartoonized_cat(
                prompt=generation_prompt, 
                output_image_path=output_image_path
            )
            logger.info(f"Cartoonized cat image saved as '{output_image_path}'")
            with open(output_image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            reflection_chat_history=[
                {
                    "role":"developer", 
                    "content": load_txt_instuctions(evaluation_system_instructions_file_path)
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
        ).output_text
            evaluation_response = process_llm_json(evaluation_response)
            score = float(evaluation_response.get("evaluation", {}).get("overall_impression", 0))
            if score >= 9:
                logger.info(f"High quality result achieved with score {score}. Exiting loop early.")
                break
            else:
                logger.warning(f"Low overall impression ({score}). Revising prompt.")
            logger.info(f"Evaluation response {i+1}: {evaluation_response}")

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
            ).output_text
            logger.info(f"Revised prompt for cartoon image {i+1}: {revised_prompt_response}")
            generation_prompt = revised_prompt_response
            self.generation_chat_history.append(
                {
                    "role":"assistant", 
                    "content": revised_prompt_response
                }
            )
