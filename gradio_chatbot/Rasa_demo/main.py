import gradio as gr
import requests
import json

chatbot_url= "http://0.0.0.0:3000/webhooks/rest/webhook"

def post_message(text):
  data = {
      "message": text,
      "sender": "user"
  }
  
  try:
      response = requests.post(chatbot_url, json=data)
      response.raise_for_status()

      try:
          response_data = json.loads(response.text)
          answer = response_data[0]["text"]
      except (json.JSONDecodeError, KeyError):
          answer = "Error processing response from chatbot"

  except requests.exceptions.RequestException as e:
      answer = "Error connecting to the chatbot. Perhaps Rasa is not ready yet."
  
  return answer

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", height=300)
    msg = gr.Textbox()

    def respond(message, chat_history):
        bot_message = post_message(message)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0")
