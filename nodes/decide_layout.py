from models.slides import Presentation
from langchain_core.tools import tool
from models.LLMs import GPT_4o
import requests
from io import BytesIO
import json

llm = GPT_4o(temperature=0.7)

def decide_layout(outline: dict) -> dict:
    """Create a layout based on the given content."""
    prompt = f"""
    Hãy đưa ra một số ý tưởng về layout cho bài giảng này.
    
    Đây là mẫu định dạng của layout, bao gồm:
    - Vị trí của tiêu đề, nội dung, hình ảnh, etc. (ví dụ: tiêu đề ở bên trái, nội dung ở dưới, hình ảnh ở trên, etc.)
    - Kích thước của tiêu đề, nội dung, hình ảnh, etc. (ví dụ: tiêu đề lớn hơn nội dung, hình ảnh nhỏ hơn nội dung, etc.)
    - Màu sắc của tiêu đề, nội dung, hình ảnh, etc. (ví dụ: tiêu đề màu đỏ, nội dung màu xanh, hình ảnh màu tím, etc.)
    - Các phần tử có thể được sắp xếp theo chiều dọc hoặc chiều ngang, tuy nhiên cần đảm bảo tính đồng đều và cân đối.
    - Nếu có nhiều hơn 1 hình ảnh, hãy đưa ra các ý tưởng về cách sắp xếp chúng.
    - Nếu có nhiều hơn 1 nội dung, hãy đưa ra các ý tưởng về cách sắp xếp chúng.
    - Nếu nội dung chứa thông tin thời gian, hãy sắp xếp theo dạng timeline.

    Đây là outline của bài giảng:
    {outline}
    """

    structured_llm = llm.with_structured_output(Presentation)
    presentation = structured_llm.invoke(prompt)

    return presentation
