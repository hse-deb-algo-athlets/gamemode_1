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
    


def pdf_upload(pdf_path:str):
    url = "http://backend:5001/pdf_upload"
    try:
        if pdf_path != None:
           #logger.info(f"pdf_path: {pdf_path}")
           with open (pdf_path,"rb") as pdf_file:
               #logger.info(f"geladen: {pdf_file}")
               files = {"file":pdf_file}
               response = requests.post(url,files=files)

    except Exception as ex:
        gr.Warning("Fehler" + str(ex))
        gr.Warning()    

def pdf_dropdown_choices():
    url = "http://backend:5001/pdf_dropdown_choices"
    try:
        answer = requests.get(url)
        #logger.info(answer)
        if answer == None:
            return ["Keine Pdf"]
        #logger.info(f"dadadaddasdasd {type(answer.json())}")
        return gr.Dropdown(label="Ausgewähltes Pdf",choices=answer.json(),interactive=True)
        
        
    except Exception as ex:
        gr.Warning("Fehler" + str(ex))
        gr.Warning()    

def pdf_from_dropdown(name):
    url = "http://backend:5001/pdf_from_dropdown"
    try:
        name_json = {"pdf_name": name}
        response = requests.post(url,json=name_json )
    except Exception as ex:
        gr.Warning("Fehler" + str(ex))
        gr.Warning()    

    


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
                        chatbot=gr.Chatbot(height=400,scale=8),
                        examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                        textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=3),
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
                    #pdfs einlesen
                    pdf_input = gr.File(label="Wähle eine PDF zum hochladen aus",file_types=[".pdf"])
                    pdf_input.change(fn=pdf_upload,inputs=pdf_input,outputs=None)
                    pdf_choice = gr.Dropdown(label="pdf auswahl")
                    button_fragen = gr.Button("Fragen generieren")
                    pdf_input.change(fn=pdf_dropdown_choices,outputs=pdf_choice)
                    text = gr.Textbox()
                    pdf_choice.select(fn=on_button_click,inputs=pdf_choice,outputs=text)
                    pdf_choice.select(fn=pdf_from_dropdown,inputs=pdf_choice)
            demo.launch(debug=True)
