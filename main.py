from workflow import graph

if __name__ == "__main__":
    graph.invoke({"topic": "Artificial Intelligence"})
    
    initial_state = {"topic": "Artificial Intelligence", "presentation": None, "slides": None}
    final_state = graph.invoke(initial_state)
    
    if "slides" in final_state and final_state["slides"]:
        with open("./examples/slides.md", "w") as f:
            f.write("\n---\n".join(final_state["slides"]))
    else:
        print("Error: No slides were generated")
    
    if "css" in final_state and final_state["css"]:
        with open("./examples/theme.css", "w") as f:
            f.write(final_state["css"])
    else:
        print("Error: No css was generated")
