from typing import TypedDict, Optional, Dict, List, Any

class PresentationState(TypedDict):
    topic: str
    presentation: Optional[Dict]
    slides: Optional[List[str]]
    css: Optional[str]
    images: List[str]