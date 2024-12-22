import gradio as gr


def user_punkte_laden(name):

    if name == "Felix":
         return 10
    elif name == "Jonas":
         return 20


def greet(message, history):
    # Handle chatbot responses here.
    return "Hello, " + message

def update_username(name):  # Pass theme_state as input
    points = user_punkte_laden(name)
    bild = 1
    return points,bild

with gr.Blocks() as demo:
            gr.Markdown("# Chatbot_gamemode_1")
            with gr.Row():
                with gr.Column(scale=2):
                    image = gr.Image(value="Bilder/Bild 10.jpg")
                    image = gr.Image(value="Bilder/Bild 20.jpg")
                    image = gr.Image(value="Bilder/Bild 30.jpg")
                with gr.Column(scale=6):
                    chatbot_1 = gr.ChatInterface(
                        fn=greet, 
                        chatbot=gr.Chatbot(height=400),
                        textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=8),
                        description="",
                        examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                        clear_btn="Clear",
                    )

                with gr.Column(scale=1, min_width=100):
                    name_input = gr.Textbox(label="Username")
                    button = gr.Button("Login")
                    points_output = gr.Textbox(label="Points")
                    button.click(fn=user_punkte_laden, inputs=name_input, outputs=points_output)  # Show points
                    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                    dropdown_c = gr.Dropdown()
            demo.launch()