
import time
from functools import wraps
from app.utils.logger import logger

def retry_on_failure(max_retries:int=3, delay:float=1.0, backoff_exp:float=2.0):
    def decorator(func):
        @wraps(func)
        def retry_wrapper(*args, **kwargs):
            last_exception=None
            for attempt in range(max_retries + 1):
                try:
                    logger.info(f"{func.__name__} attempt {attempt + 1}/{max_retries + 1}")
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {str(e)}")
                    
                    if attempt < max_retries:
                        wait_time = delay * (backoff_exp ** attempt)
                        logger.info(f"Retrying {func.__name__} in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {func.__name__} attempts failed after {max_retries + 1} tries")
                        
            if func.__name__ == 'get_evaluation':
                logger.error(f"Returning fallback evaluation due to persistent failures: {last_exception}")
                return {
                    "evaluation": {
                        "similarity_to_original": 5,
                        "cuteness_factor": 5,
                        "artistic_style": 5,
                        "overall_impression": 5
                    },
                    "critique": f"Unable to evaluate due to technical issues: {str(last_exception)}. Using default scores."
                }
            else:
                # Re-raise the exception for other functions
                raise last_exception
                
        return retry_wrapper
    return decorator
