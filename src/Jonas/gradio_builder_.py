import gradio as gr

#gr.themes.builder()

import gradio as gr

def greet(message, history):
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
    primary_hue="blue",
    secondary_hue="green",
    neutral_hue="gray",
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
        return gr.themes.Default()  # Default theme if not matched

def create_ui(theme):
    with gr.Blocks(theme=theme) as demo:
        gr.Markdown("# Chatbot_gamemode_1")

        with gr.Row():
            with gr.Column(scale=1, min_width=100):
                name_input = gr.Textbox(label="Username")
                button = gr.Button("Login")
                points_output = gr.Textbox(label="Points")
                pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                dropdown_c = gr.Dropdown()

                # Define the click action for the button
                button.click(fn=update_theme, inputs=name_input, outputs=None)

        with gr.Column(scale=15):
            # Chatbot component
            chat_bot = gr.Chatbot(height=400)
            chat_input = gr.Textbox(placeholder="Ask me questions...", container=False, scale=8)

            gr.Markdown("### Chatbot Area")
            # The components are automatically rendered, so no need for .render()
            

    return demo

# Initial theme set to default
theme = theme_2

demo = create_ui(theme)
demo.launch()

