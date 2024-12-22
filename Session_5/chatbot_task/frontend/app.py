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

            # Continuously receive and yield chunks until the connection is closed
            while True:
                try:
                    chunk = await websocket.recv()
                    logger.info(f"Received chunk: {chunk}")
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








# Launch Gradio Chat Interface
with gr.Blocks() as demo:
    gr.Markdown("# gamemode_1")

    with gr.Row():
        with gr.Column(scale=1, min_width=100):
            name = gr.Textbox(label="Name")
            button = gr.Button("Login")
            punkte = gr.Textbox(label="Punkte")

            button.click(fn=user, inputs=name, outputs=punkte)
    
        with gr.Column(scale=15):
            gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(height=400),  # Adjusted height for better usability
                textbox=gr.Textbox(placeholder="Ask me questions about your script...", container=False, scale=7),
                title="Chatbot",
                description="Ask me questions about your lecture.",
                theme="soft",
                examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                clear_btn="Clear",
            )
    demo.launch(debug=True)