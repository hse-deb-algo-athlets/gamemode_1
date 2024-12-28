import gradio as gr
import pandas as pd
import os as os
import csv


def user_punkte_laden(name):

    path = os.path.join(os.getcwd(),"user.csv")
    
    if os.path.exists(path) != True:
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Punkte']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)


    df = pd.read_csv(path, index_col = "Name")
    
    if name not in df.index:
        df.loc[name] = 0
        df.to_csv(path)

    Punkte = df.loc[name]
    
    return Punkte


def greet(message, history):
    # Handle chatbot responses here.
    return "Hello, " + message




theme_1 = gr.themes.Soft(
    primary_hue="zinc",
).set(
    background_fill_primary_dark='*neutral_700',
    background_fill_secondary_dark='*neutral_500',
    block_background_fill='*secondary_50'
)

theme_2 = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="orange",
    neutral_hue="amber",
)

theme_3 = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="blue",
    neutral_hue="green",
)


def update_theme(username): 
    points = user_punkte_laden(username)
    if points <= 10:
        return theme_1
    elif points <= 20:
        return theme_2
    elif points <= 30:
        return theme_3
    else:
        return theme_1

def update_username(name, theme_state):  # Pass theme_state as input
    points = user_punkte_laden(name)
    theme = update_theme(name)
    return theme



def interface_theme(number):
    if number == 1:
        with gr.Blocks(theme_1) as demo:
            gr.Markdown("# Chatbot_gamemode_1")
            with gr.Row():
                with gr.Column(scale=15):
                    chatbot_1 = gr.ChatInterface(
                        fn=greet, 
                        chatbot=gr.Chatbot(height=400),
                        textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=8),
                        description="",
                        examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                        clear_btn="Clear",
                    )

                with gr.Column(scale=1, min_width=100):
                    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                    dropdown_c = gr.Dropdown()
                    
        return demo
    elif number == 2:
        with gr.Blocks(theme_2) as demo:
            gr.Markdown("# Chatbot_gamemode_1")
            with gr.Row():
                with gr.Column(scale=15):
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
                    theme_state = gr.State(theme_1)  # Create a state to store the theme
                    button.click(fn=update_username, inputs=[name_input, theme_state], outputs=theme_state)  # Update theme based on the username
                    button.click(fn=user_punkte_laden, inputs=name_input, outputs=points_output)  # Show points
                    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                    dropdown_c = gr.Dropdown()
                    
        return demo
    else:
        with gr.Blocks(theme_3) as demo:
            gr.Markdown("# Chatbot_gamemode_1")
            with gr.Row():
                with gr.Column(scale=15):
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
                    theme_state = gr.State(theme_1)  # Create a state to store the theme
                    button.click(fn=update_username, inputs=[name_input, theme_state], outputs=theme_state)  # Update theme based on the username
                    button.click(fn=user_punkte_laden, inputs=name_input, outputs=points_output)  # Show points
                    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                    dropdown_c = gr.Dropdown()
                    
        return demo
    

with gr.Blocks() as demo:
    name_input = gr.Textbox(label="Username")
    button = gr.Button("Login")
    points = user_punkte_laden(name_input)
    button.click(fn=interface_theme,inputs=points,outputs=None)
    demo.launch()