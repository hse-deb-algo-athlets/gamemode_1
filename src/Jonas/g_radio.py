import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

number = 9
demo = gr.ChatInterface(
    fn=greet,
    chatbot=gr.Chatbot(height=350),  # Adjusted height for better usability
    textbox=gr.Textbox(placeholder="Ask me questions about your script...", container=False, scale=8),
    #number = gr.Textbox(label="Punkte"),
    title="Chatbot_gamemode_1",
    description="",
    theme="soft",
    examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
    clear_btn="Clear"
)

demo.launch()

