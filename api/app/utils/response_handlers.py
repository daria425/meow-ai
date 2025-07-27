import re
import json
from app.utils.error_handlers import categorize_error
from app.utils.logger import logger
def process_llm_json(response_content):
    """
    Process the response content from the LLM to extract JSON data.
    :param response_content: The content returned by the LLM.
    :return: Parsed JSON data or None if parsing fails.
    """
    content_to_process=response_content.strip()
    json_block_match = re.search(r'```(?:json)?([^`]*)```', content_to_process, re.DOTALL)
    if json_block_match:
            # Extract the JSON block
            content_to_process = json_block_match.group(1)
            content_to_process = content_to_process.strip()
        
    content_to_process = re.sub(r'^```json\s*', '', content_to_process)
    content_to_process = re.sub(r'\s*```$', '', content_to_process)
    try:
        content_to_process = content_to_process.strip()
        json_data = json.loads(content_to_process)
        return json_data
    except json.JSONDecodeError as e:
        logger.error(f"Unexpected response format from LLM. Expected JSON format but received:{response_content}")
        raise
        # error_category=categorize_error(error_message)
        # return {
        #     "error": True,
        #     "status": "error",
        #     "category": error_category,
        #     "message": error_message,
        #     "raw_content": response_content
        # }