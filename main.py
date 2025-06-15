from get_image import get_cat_image, get_cartoonized_cat
from file_utils import load_txt_instuctions
from response_handlers import process_llm_json
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from logger import logger
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client= OpenAI(api_key=OPENAI_API_KEY)
original_image_url ="https://cdn2.thecatapi.com/images/92D9NZLs0.jpg" # Change to function later
generation_instruction_file_path="./generation_system_instructions.txt"
def run_loop(iterations:int=3):
    """
    Run the main loop for a specified number of iterations.
    :param iterations: Number of iterations to run.
    """
    generation_chat_history=[
        {
            "role":"developer", 
            "content":load_txt_instuctions(generation_instruction_file_path)
                },
    ]
    generation_chat_history.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": f"Here is a photo of my cat, please create a detailed description for a cute cartoon cat image based on this photo."
                },
                {
                    "type": "input_image",
                    "image_url": original_image_url
                }
            ]
        }
    )
    generation_prompt=client.responses.create(
        model="gpt-4o", 
        input=generation_chat_history,
        temperature=0.5
    ).output_text
    generation_chat_history.append(
            {
                "role":"assistant", 
                "content": generation_prompt
        }
        
    )
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
                "content": """You are an expert prompt engineer and are talented in evaluating AI-generated images. The user is trying to create a cartoonized image of their cat using the Stability AI API. 
                The aim for the image to be as close as possible to the original cat photo. 
                Your task is comprised of 2 parts:
                PART 1: Evaluate the image based on the following criteria:
                1. **Similarity to Original Photo**: How closely does the cartoonized image resemble the original cat photo in terms of features, colors, and overall appearance?
                2. **Cuteness Factor**: Does the cartoonized image capture the essence of cuteness? Are the features exaggerated in a way that enhances the cuteness?
                3. **Artistic Style**: Does the cartoonized image maintain a consistent and appealing cartoon style? Are the colors vibrant and the lines clean?
                4. **Overall Impression**: What is your overall impression of the cartoonized image? Does it evoke a positive emotional response?
                PART 2: 
                Provide critique and suggestions for the user to improve their prompt for generating a better cartoonized image of their cat.
                As an expert in AI imagine generation, include suggested prompt examples that could lead to better results. 
                Be explicit, do not simply refer to the photo as 'original' but mention the actual features of the cat in the photo.
                Be as helpful and detailed as possible in your evaluation and critique.
                Respond in the format of a JSON object with the following structure:
                {
                    "evaluation": {
                        "similarity_to_original": "Rating from 1 to 10",
                        "cuteness_factor": "Rating from 1 to 10",
                        "artistic_style": "Rating from 1 to 10",
                        "overall_impression": "Rating from 1 to 10"
                    },
                    "critique": "Your critique and suggestions for improving the prompt."
                }
                Respond with the JSON object only, do not include any additional text, or markdown formatting.
                """
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
                        "image_url": original_image_url
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
        evaluation_response = client.responses.create(
        model="gpt-4o",
        input=reflection_chat_history,
        temperature=0
    ).output_text
        evaluation_response = process_llm_json(evaluation_response)
        score = float(evaluation_response.get("evaluation", {}).get("overall_impression", 0))
        if score >= 9:
            logger.info(f"High quality result achieved with score {score}. Exiting loop early.")
            break
        else:
            logger.warning(f"Low overall impression ({score}). Revising prompt.")
        logger.info(f"Evaluation response {i+1}: {evaluation_response}")

        generation_chat_history.append(
            {
                "role":"user", 
                "content":f"""My feedback on the image generated from your description: 
                {evaluation_response["critique"]}
                Please provide a revised image generation prompt based on this feedback to improve the cartoonized image of my cat."""
            }
        )
        revised_prompt_response = client.responses.create(
            model="gpt-4o",
            input=generation_chat_history,
            temperature=0.5
        ).output_text
        logger.info(f"Revised prompt for cartoon image {i+1}: {revised_prompt_response}")
        generation_prompt = revised_prompt_response
        generation_chat_history.append(
            {
                "role":"assistant", 
                "content": revised_prompt_response
            }
        )
    logger.info("All iterations completed. Chat history:")
    logger.info(generation_chat_history)

if __name__ == "__main__":
    logger.info("Starting the cartoonized cat image generation process.")
    run_loop(iterations=3)
    logger.info("Process completed.")