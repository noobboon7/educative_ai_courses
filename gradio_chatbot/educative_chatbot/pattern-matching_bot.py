import gradio as gr
import re
import random

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", height=300)
    msg = gr.Textbox()

    # Define patterns and responses
    patterns = {
        r"hello|hi": ["Hello there!", "Hi!", "Greetings!"],
        r"how are you": ["I'm doing well, thanks for asking!", "I'm okay."],
        r"what is your name": ["You can call me Chatty!", "I'm Chatty."],
        r"bye|goodbye": ["Goodbye!", "See you later!"],
        r"(.*)": ["I didn't quite understand that. Can you rephrase?"]
    }

    def respond(message, chat_history):
        for pattern, response in patterns.items():
            match = re.search(pattern, message.lower())
            if match:
                bot_message = random.choice(response)
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": bot_message})
                return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0")