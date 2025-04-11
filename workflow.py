from langgraph.graph import StateGraph, END
from nodes.create_presentation import create_presentation
from nodes.decide_layout import decide_layout
from nodes.create_slides import create_slides
from nodes.enhance_slides_position import enhance_slides_positions
from nodes.describe_images import describe_images
from states.PresentationState import PresentationState
from IPython.display import Image, display
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_presentation_node(state: PresentationState) -> PresentationState:
    topic = state["topic"]
    presentation = create_presentation(topic)
    state["presentation"] = presentation
    return state

def describe_images_node(state: PresentationState) -> PresentationState:
    # Get all image URLs from all slides
    all_image_urls = []
    for slide in state["presentation"]["slides"]:
        all_image_urls.extend(slide["slide_images"]) 
           
    # Process image descriptions in parallel
    images = describe_images(images=all_image_urls)
    state["images"] = images
    
    with open("./examples/images.json", "w") as f:
        json.dump(images, f)
    return state

def decide_layout_node(state: PresentationState) -> PresentationState:
    if not isinstance(state["presentation"], dict):
        raise ValueError("Expected Presentation object in state")
    
    final_presentation = decide_layout(outline=state["presentation"], image_descriptions=state["images"])
    # Convert Pydantic model to dictionary before serializing to JSON
    presentation_dict = final_presentation.dict()
    with open("./examples/presentation.json", "w") as f:
        json.dump(presentation_dict, f)
    state["presentation"] = presentation_dict
    return state

def create_slides_node(state: PresentationState) -> PresentationState:
    slides = create_slides(presentation=state["presentation"])
    # Access the attributes of the VisualizeSlides object
    state["slides"] = [slide.slide_content for slide in slides.presentation_content]
    state["css"] = slides.style
    return state

def enhance_slides_positions_node(state: PresentationState) -> PresentationState:
    # Pass the slides list and css string to the enhance_slides_positions function
    enhanced_slides = enhance_slides_positions(slides=state["slides"], css=state["css"])
    # Access the attributes of the VisualizeSlides object
    state["slides"] = [slide.slide_content for slide in enhanced_slides.presentation_content]
    state["css"] = enhanced_slides.style
    return state

builder = StateGraph(PresentationState)
    
builder.add_node("create_presentation", create_presentation_node)
builder.add_node("describe_images", describe_images_node)
builder.add_node("decide_layout", decide_layout_node)
builder.add_node("create_slides", create_slides_node)
builder.add_node("enhance_slides_positions", enhance_slides_positions_node)
# Set the entry point and endpoint.
builder.set_entry_point("create_presentation")
builder.add_edge("create_presentation", "describe_images")
builder.add_edge("describe_images", "decide_layout")
builder.add_edge("decide_layout", "create_slides")
builder.add_edge("create_slides", "enhance_slides_positions")
builder.add_edge("enhance_slides_positions", END)

# Compile the graph.
graph = builder.compile()
