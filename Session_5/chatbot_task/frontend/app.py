import gradio as gr
import websockets
import logging
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket chat function (asynchronous generator)
async def websocket_chat(message: str):
    uri = "ws://backend:5001/ws"  # Ensure this URI is correct and accessible
    try:
        async with websockets.connect(uri) as websocket:
            logger.info(f"Sending message to WebSocket: {message}")
            await websocket.send(message)
            bool = True
            # Continuously receive and yield chunks until the connection is closed
            while bool:
                try:
                    chunk = await websocket.recv()
                    logger.info(f"Received chunk: {chunk}")
                    if chunk == "":
                        bool = False
                        break
                    yield chunk  # Yield each chunk as a separate message
                except websockets.exceptions.ConnectionClosed:
                    logger.info("WebSocket connection closed by the server.")
                    break
                except Exception as e:
                    logger.error(f"Error receiving chunk: {str(e)}")
                    yield f"Error: {str(e)}"
                    break
    except Exception as e:
        logger.error(f"Error during WebSocket communication: {str(e)}")
        yield f"Error: {str(e)}"

# Chat function to update the chatbot message history
async def chat(message: str, history=[]):
    if not message.strip():
        yield "Please enter a valid question."
        return

    try:        
        # Stream chunks from WebSocket and append them incrementally
        bot_message = ""
        async for chunk in websocket_chat(message):
            bot_message += str(chunk)  # Accumulate chunks
            yield bot_message  # Yield updated history incrementally for display

    except Exception as e:
        message = f"Error: {e}"
        yield message


#NEU
def user(Name: str):
    uri = "http://backend:5001/user"
    try:
        name_json = {"user_name": Name}
        antwort = requests.get(uri, json= name_json )
        a = antwort.json()["Punkte"]
        return a
    
    except Exception as ex:
        gr.Warning("Fehler" + str(ex))

def update_bild(Name: str):
    uri = "http://backend:5001/Bilder"
    Bild = "Keins"
    try:
        name_json = {"user_name": Name}
        antwort = requests.get(uri, json= name_json )
        Bild = antwort.json()["AAA"]
    except Exception as ex:
        gr.Warning("Fehler" + str(ex))
        gr.Warning()

    if Bild == "Bild_1":
        return gr.Image(value="Bilder/Bild 10.jpg",visible= True),gr.Image(value="Bilder/Bild 20 Unlock.jpg",visible= True),gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True)
    elif Bild == "Bild_2":
        return gr.Image(value="Bilder/Bild 10.jpg",visible= True),gr.Image(value="Bilder/Bild 20.jpg",visible= True),gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True)
    elif Bild == "Bild_3":
        return gr.Image(value="Bilder/Bild 10.jpg",visible= True),gr.Image(value="Bilder/Bild 20.jpg",visible= True),gr.Image(value="Bilder/Bild 30.jpg",visible= True)
    else:
        return gr.Image(value="Bilder/Bild 10 Unlock.jpg",visible= True),gr.Image(value="Bilder/Bild 20 Unlock.jpg",visible= True),gr.Image(value="Bilder/Bild 30 Unlock.jpg",visible= True)
    

def on_button_click(input_value):
    return input_value

# Launch Gradio Chat Interface

with gr.Blocks() as demo:
            gr.Markdown("# Chatbot_gamemode_1")
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
                        fn=chat, 
                        chatbot=gr.Chatbot(height=400),
                        textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=8),
                        examples=["Stelle eine frage", "Antwort:"],
                        clear_btn="Clear",
                    )

                with gr.Column(scale=1, min_width=100):
                    name_input = gr.Textbox(label="Username")
                    button_login = gr.Button("Login")
                    points_output = gr.Textbox(label="Points")
                    button_refresh = gr.Button("Points/Picture load again")
                    button_login.click(fn=user, inputs=name_input, outputs=points_output)
                    button_login.click(fn=on_button_click,inputs=name_input,outputs=visibleity)
                    button_refresh.click(fn=on_button_click,inputs=name_input,outputs=visibleity)
                    #button_login.click(fn=update_username_points, inputs=name_input, outputs=points_output)
                    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                    pdf_array = []
                    dropdown_c = gr.Dropdown(choices=pdf_array, label="Uploaded Pdfs")
                    button_Frage = gr.Button("Stelle Frage")
                    button_Frage_message = gr.Textbox(visible=False, value="Stelle eine frage")
                    button_Frage.click(fn=chat,inputs=button_Frage_message)
                    #pdf_input.change(fn=update_pdf,inputs=[pdf_input,dropdown_c],outputs=dropdown_c)
            demo.launch(debug=True)