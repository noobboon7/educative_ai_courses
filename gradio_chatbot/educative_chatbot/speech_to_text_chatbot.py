import gradio as gr
from groq import Groq

client = Groq()

def process_audio(audio):
    with open(audio, "rb") as audio_file:
      transcription = client.audio.transcriptions.create(
        file=(audio, audio_file.read()),
        model="whisper-large-v3",
        language="en",
        response_format="verbose_json",
      )      
      return transcription.text

with gr.Blocks() as demo:
    audio_input = gr.Audio(sources=["microphone"], type='filepath')
    text_output = gr.Textbox()
    audio_input.stop_recording(process_audio, inputs=audio_input, outputs=text_output)

demo.launch(server_name="0.0.0.0")
