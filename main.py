from get_image import get_cat_image, get_cartoonized_cat
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
output_image_path = "images/cartoonized_cat.jpg"
revision_image_path = "images/revised_cartoonized_cat.jpg"
logger.info(f"Original cat image URL: {original_image_url}")
# First iteration: Get a random cat image from The Cat API
generation_chat_history=[
    {
        "role":"developer", 
        "content":f"""You are an expert prompt writer for the Stability AI API. The user will provide you with a photo of their cat.
        The user wants an adorable cartoon image as close to their cat photo as possible generated from Stability AI. 
        Your task is to create a detailed description of the image to generate a cute cartoon cat.
        image.
        Please provide a detailed description of the cat's appearance, colors, and any other relevant details that would help in generating a cute cartoon cat image. 
        Important details to include:
        - The cat's fur color and pattern (e.g., tabby, calico, solid)
        - The cat's eye color and shape
        - The cat's size and build (e.g., small, fluffy, slender)
        - Any distinctive features (e.g., unique markings, collar, toys)
        - The overall mood or expression of the cat (e.g., playful, sleepy, curious)
        - The setting or background (e.g., indoors, outdoors, with toys)
        - Emphasis on cuteness and cartoonish style
        - Use descriptive adjectives to enhance the prompt
        KEY GUIDELINES:
        Respond in the format of a prompt for the Stability AI API. Do not include any additional text or explanations, just the prompt itself.
        Do not say 'create an image' or 'generate an image', just provide the description directly."""
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
logger.info(f"Generated prompt for cartoon image: {generation_prompt}")
cartoon_image=get_cartoonized_cat(
    prompt=generation_prompt, 
    output_image_path=output_image_path
)
logger.info(f"Cartoonized cat image saved as 'images/cartoonized_cat.jpg'")
generation_chat_history.append(
    {
        "role":"assistant", 
        "content": generation_prompt
    }
    
)
with open(output_image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
# Evaluation
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
        PART 2: Provide critique and suggestions for the user to improve their prompt for generating a better cartoonized image of their cat.
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
logger.info(f"Evaluation response: {evaluation_response}")
generation_chat_history.append(
    {
        "role":"user", 
        "content":f"""My feedback on the image generated from your description: 
        {evaluation_response["critique"]}
        Please provide a revised description based on this feedback to improve the cartoonized image of my cat."""
    }
)
revised_prompt_response = client.responses.create(
    model="gpt-4o",
    input=generation_chat_history,
    temperature=0.5
).output_text
logger.info(f"Revised prompt for cartoon image: {revised_prompt_response}")

cartoon_image=get_cartoonized_cat(
    prompt=revised_prompt_response, 
    output_image_path=revision_image_path
)
logger.info(f"Revised cartoonized cat image saved as 'images/revised_cartoonized_cat.jpg'")

