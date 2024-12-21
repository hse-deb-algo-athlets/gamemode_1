import gradio as gr

def greet(message, history):
    # Handle chatbot responses here.
    return "Hello, " + message

def number(name):
    if name == "Test10":
        return 10
    elif name == "Test20":
        return 20
    elif name == "Test30":
        return 30
    else:
        return 0



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
    secondary_hue="orange",
    neutral_hue="amber",
)


def update_theme(name): 
    points = number(name)
    if points <= 10:
        return theme_1
    elif points <= 20:
        return theme_2
    elif points <= 30:
        return theme_3
    else:
        return "default"

def them_app(name):
    theme = update_theme(name)
    with gr.Blocks(theme=theme) as demo:
            gr.Markdown("# Chatbot_gamemode_1")

            with gr.Row():
                with gr.Column(scale=1, min_width=100):
                    #name_input = gr.Textbox(label="Username")
                    #button = gr.Button("Login")
                    #points_output = gr.Textbox(label="Points",)
                    #button.click(fn=number, inputs=name_input, outputs=points_output)
                    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                    dropdown_c = gr.Dropdown()

            with gr.Column(scale=15):
                chat_bot = gr.ChatInterface(
                    fn=greet, 
                    chatbot=gr.Chatbot(height=400),
                    textbox=gr.Textbox(placeholder="Ask me questions...", container=False, scale=8),
                    description="",
                    theme=update_theme(name_input),  # <-- Theme update here
                    examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                    clear_btn="Clear",
                )
    return demo

with gr.Blocks() as demo:
    name_input = gr.Textbox(label="Username")
    button = gr.Button("Login")
    button.click(fn=them_app, inputs=name_input, outputs=demo)         
    demo.launch()