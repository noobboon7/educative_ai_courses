import gradio as gr
import random
import time
import re

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", height=300)
    msg = gr.Textbox()

    patterns = {
        r"hello|hi": ["Hello there!", "Hi!", "Greetings!"],
        r"how are you": ["I'm doing well, thanks for asking!", "I'm okay."],
        r"what is your name": ["You can call me Chatty!", "I'm Chatty."],
        r"bye|goodbye": ["Goodbye!", "See you later!"],
        r"(.*)": ["I didn't quite understand that. Can you rephrase?"]
    }

    def add_message(user_message, chat_history):
        return "", chat_history + [{"role": "user", "content": user_message}]

    def respond(chat_history):
        message = chat_history[-1]["content"]
        bot_message = ''
        for pattern, response in patterns.items():
            match = re.search(pattern, message.lower())
            if match:
                bot_message = random.choice(response)
                break
        chat_history.append({"role": "assistant", "content": ""})
        for character in bot_message:
            chat_history[-1]["content"] += character
            time.sleep(0.05)
            yield chat_history

    msg.submit(add_message, [msg, chatbot], [msg, chatbot]).then(
        respond, chatbot, chatbot
    )

demo.launch(server_name="0.0.0.0")