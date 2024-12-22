from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from contextlib import asynccontextmanager
import traceback
import os
from src.bot import CustomChatBot
from pydantic import BaseModel
import pandas as pd
import os as os
import csv

INDEX_DATA = bool(int(os.environ["INDEX_DATA"]))

# Set up logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager to ensure CustomChatBot is initialized and cleaned up correctly.
    """
    logger.info("Creating instance of custom chatbot.")
    logger.info(f"Index data to vector store: {INDEX_DATA}")
    app.state.chatbot = CustomChatBot(index_data=INDEX_DATA)
    try:
        yield
    finally:
        logger.info("Cleaning up chatbot instance.")
        del app.state.chatbot

# Create FastAPI app and configure CORS
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to restrict domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that handles communication with the client.
    """
    await websocket.accept()
    logger.info('Client connected.')

    try:
        while True:
            try:
                # Receive input from the WebSocket client
                input_data = await websocket.receive_text()
                logger.info(f"Received input: {input_data}")

                # Process the input using the chatbot's stream_answer method
                async for chunk in app.state.chatbot.astream(input_data):
                    chain_result = chunk
                    logger.info(f"Sending chunk: {chain_result}")
                    # Send the response chunk back to the client
                    await websocket.send_text(chain_result)

            except WebSocketDisconnect:
                # Graceful handling of WebSocket disconnection
                logger.info("Client disconnected.")
                break

            except Exception as e:
                # Handle unexpected errors during input processing
                logger.error(f"Error processing chatbot response: {str(e)}")
                logger.error(traceback.format_exc())
                await websocket.send_text(f"Error: {str(e)}")
                break

    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        logger.info('WebSocket connection closed.')

#NEU
class User(BaseModel):
    user_name: str
@app.get("/user")
def user(user: User):
    user_text = user.user_name

    path = os.path.join(os.getcwd(),"user.csv")
    
    if os.path.exists(path) == False:
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Punkte']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

    df = pd.read_csv(path, index_col = "Name")
    
    if user_text not in df.index:
        df.loc[user_text] = 0
        df.to_csv(path)

    Punkte = df.loc[user_text, "Punkte"]
    Punkte = str(Punkte)
    data = {"Punkte": Punkte}
    
    return(data)



if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, log_level="debug")
