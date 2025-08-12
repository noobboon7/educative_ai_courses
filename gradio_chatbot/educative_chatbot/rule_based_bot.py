import gradio as gr

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", height=300)
    msg = gr.Textbox()

    def respond(message, chat_history):
        lower_case_message = message.lower()
        if "hello" in lower_case_message:
            bot_message = "Hello there!"
        elif "how are you" in lower_case_message:
            bot_message = "I'm doing well, thanks for asking!"
        elif "bye" in lower_case_message:
            bot_message = "Goodbye!"
        else:
            bot_message = "I didn't understand that."
        
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0")