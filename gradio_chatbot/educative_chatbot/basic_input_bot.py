import gradio as gr

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", height=300)
    msg = gr.Textbox()

    def respond(message, chat_history):
        bot_message = "You said:" + message
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0")
