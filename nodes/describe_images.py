from models.images import Images
from langchain_core.tools import tool
from models.LLMs import GPT_4o
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = GPT_4o()

def describe_batch_images(image_urls: List[str]) -> Dict[str, Any]:
    """Describe a batch of images."""
    try:
        prompt = f"""
        You are an expert in describing images.
        You will be given a list of image URLs.
        You will need to describe each image in detail.
        These are the image URLs:
        {image_urls}
        
        Please provide a detailed description for each image, with resolution.
        The description should be clear and concise, describe the image in detail.
        Decide whether the image should be used as a background image or not, based on the content of the image, the image should have no text on it, and should cover the topic of the presentation.
        """
                
        structured_llm = llm.with_structured_output(Images, method="function_calling")
        response = structured_llm.invoke(prompt)

        
        return response.model_dump()
    except Exception as e:
        logger.error(f"Failed to describe images batch: {str(e)}")
        return None

def describe_images(images: List[str]) -> List[Dict[str, Any]]:
    """Describe the images in the presentation in parallel batches."""
    if not images:
        return []
    
    batch_size = 2
    image_descriptions = []
    
    # Create batches
    batches = [images[i:i+batch_size] for i in range(0, len(images), batch_size)]
    logger.info(f"Created {len(batches)} batches of up to {batch_size} images each")
    
    # Process batches in parallel
    with ThreadPoolExecutor(max_workers=min(len(batches), 5)) as executor:
        # Submit all batch tasks
        future_to_batch = {
            executor.submit(describe_batch_images, batch): batch 
            for batch in batches
        }
        
        # Process results as they complete
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                result = future.result()
                if result:
                    image_descriptions.append(result)
                    logger.info(f"Successfully processed batch with {len(batch)} images")
            except Exception as e:
                logger.error(f"Failed to process batch: {str(e)}")
    
    return image_descriptions
    
