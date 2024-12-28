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
    if points <= 10:
        return gr.Image(value="Bilder/Bild 10.jpg", visible=True), gr.Image(value="Bilder/Bild 20.jpg", visible=False), gr.Image(value="Bilder/Bild 30.jpg", visible=False)
    elif points <= 20:
        return gr.Image(value="Bilder/Bild 10.jpg", visible=True), gr.Image(value="Bilder/Bild 20.jpg", visible=True), gr.Image(value="Bilder/Bild 30.jpg", visible=False)
    elif points <= 30:
        return gr.Image(value="Bilder/Bild 10.jpg", visible=True), gr.Image(value="Bilder/Bild 20.jpg", visible=True), gr.Image(value="Bilder/Bild 30.jpg", visible=True)

def on_button_click(input_value):
    return input_value

# Update PDF function to ensure pdf is not None and correctly update the dropdown
def update_pdf(pdf, pdf_array):
    if pdf:  # Only proceed if a PDF is provided
        if pdf.name not in pdf_array:  # Check if the PDF file name is already in the array
            pdf_array.append(pdf.name)  # Append the PDF file name to the array
    return gr.Dropdown.update(choices=pdf_array), pdf_array  # Return updated dropdown choices

with gr.Blocks() as demo:
    gr.Markdown("# Chatbot_gamemode_1")
    
    with gr.Row():
        with gr.Column(scale=2):
            visibleity = gr.State("")
            with gr.Row():
                image1 = gr.Image()
            with gr.Row():
                image2 = gr.Image()
            with gr.Row():
                image3 = gr.Image()
            visibleity.change(fn=update_bild, inputs=visibleity, outputs=[image1, image2, image3])

        with gr.Column(scale=6):
            chatbot_1 = gr.ChatInterface(
                fn=greet, 
                chatbot=gr.Chatbot(height=400),
                textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=8),
                examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                clear_btn="Clear",
            )

        with gr.Column(scale=1, min_width=100):
            name_input = gr.Textbox(label="Username")
            button_login = gr.Button("Login")
            points_output = gr.Textbox(label="Points")
            button_refresh = gr.Button("Points/Picture load again")
            button_login.click(fn=update_username_points, inputs=name_input, outputs=points_output)
            button_login.click(fn=on_button_click, inputs=name_input, outputs=visibleity)
            button_refresh.click(fn=on_button_click, inputs=name_input, outputs=visibleity)

            pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            pdf_array = []  # Initialize pdf_array as an empty list
            dropdown_c = gr.Dropdown(choices=pdf_array, label="Uploaded Pdfs")
            pdf_input.change(fn=update_pdf, inputs=[pdf_input, pdf_array], outputs=[dropdown_c, pdf_array])  # Update both dropdown and pdf_array on file upload

    demo.launch()

