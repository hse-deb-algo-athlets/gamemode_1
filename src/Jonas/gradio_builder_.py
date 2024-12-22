import gradio as gr

#gr.themes.builder()


import gradio as gr

def my_function(img, text):
  # Hier kannst du deine Logik implementieren
  return "Danke für deine Eingabe!"

with gr.Blocks() as demo:
  with gr.Row():
    img_input = gr.Image(label="Lade ein Bild hoch")
    text_input = gr.Textbox(label="Gib hier deinen Text ein")
  output = gr.Textbox(label="Ausgabe")

  btn = gr.Button("Submit")
  btn.click(my_function, inputs=[img_input, text_input], outputs=output)

demo.launch()