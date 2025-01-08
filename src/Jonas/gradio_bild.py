import gradio as gr


def greet(message, history):
    # Handle chatbot responses here.
    return "Hello, " + message

def update_username_points(name):  
    if name == "Felix":
         return 10
    elif name == "Jonas":
         return 20
    elif name == "Nico":
         return 30
    else:
         return 0    
    
def update_bild(name):
    points = update_username_points(name)
    if points >= 10 and points <= 19:
        return gr.Image(value="Bilder/Bild 10.jpg",visible= True),gr.Image(value="Bilder/Bild 20 Unlock.jpg",visible= True),gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True)
    elif points >= 20 and points <= 29:
        return gr.Image(value="Bilder/Bild 10.jpg",visible= True),gr.Image(value="Bilder/Bild 20.jpg",visible= True),gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True)
    elif points >= 30:
        return gr.Image(value="Bilder/Bild 10.jpg",visible= True),gr.Image(value="Bilder/Bild 20.jpg",visible= True),gr.Image(value="Bilder/Bild 30.jpg",visible= True)
    else:
        return gr.Image(value="Bilder/Bild 10 Unlock.jpg",visible= True),gr.Image(value="Bilder/Bild 20 Unlock.jpg",visible= True),gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True) 

def on_button_click(input_value):
    return input_value

def pdf_upload(pdf_path):
    if pdf_path == False:
        gr.Warning("keine Pdf ausgewählt")
    else:
        return pdf_path
markdown_text = """
<div style="text-align: center;">
    <h1>Chatbot gamemode_1</h1>
</div>
"""

with gr.Blocks() as demo:
            gr.Markdown(markdown_text)
            with gr.Row():
                with gr.Column(scale=2):
                    visibleity = gr.State("")
                    with gr.Row():
                        image1 = gr.Image(value="Bilder/Bild 10 Unlock.jpg",visible= True)
                    with gr.Row():
                        image2 = gr.Image(value="Bilder/Bild 20 Unlock.jpg",visible= True)
                    with gr.Row():
                        image3 = gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True)
                    visibleity.change(fn=update_bild, inputs=visibleity, outputs=[image1, image2, image3])
                with gr.Column(scale=6):
                    chatbot_1 = gr.ChatInterface(
                        fn=greet, 
                        chatbot=gr.Chatbot(height=500,scale=8),
                        examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                        textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=2),
                        clear_btn="Clear",
                    )
                with gr.Column(scale=1, min_width=100):
                    name_input = gr.Textbox(label="Username")
                    button_login = gr.Button("Login")
                    points_output = gr.Textbox(label="Points")
                    button_refresh = gr.Button("Points/Picture load again")
                    button_login.click(fn=update_username_points, inputs=name_input, outputs=points_output)
                    button_login.click(fn=on_button_click,inputs=name_input,outputs=visibleity)
                    button_refresh.click(fn=on_button_click,inputs=name_input,outputs=visibleity)
                    pdf_input = gr.File(label="Wähle eine PDF aus",file_types=[".pdf"])
                    pdf_input.change(fn=pdf_upload,inputs=pdf_input,outputs=None)
                    textbox_text = gr.Textbox()
                    pdf_choicesssss = [10,2]
                    pdf_choice = gr.Dropdown(label="pdf auswahl",choices=pdf_choicesssss,interactive=True)
                    pdf_choice.change(on_button_click,inputs=pdf_choice,outputs=textbox_text)

            demo.launch()