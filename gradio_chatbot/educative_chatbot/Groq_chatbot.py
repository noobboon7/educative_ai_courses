import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from a local .env file if present
load_dotenv()

with gr.Blocks() as demo:
	chat_context = []
	chatbot = gr.Chatbot(type="messages", height=300)
	msg = gr.Textbox()
	# Initialize Groq client with API key from environment (GROQ_API_KEY)
	client = Groq(api_key=os.getenv("GROQ_API_KEY"))
	
	def add_message(user_message, chat_history):
		chat_context.append({"role": "user", "content": user_message})
		return "", chat_history + [{"role": "user", "content": user_message}]

	def respond(chat_history):
		completion = client.chat.completions.create(
			model="llama-3.3-70b-versatile",
			messages=chat_context,
			temperature=1,
			max_tokens=1024,
			top_p=1,
			stream=True,
			stop=None,
		)
  
		chat_history.append({"role": "assistant", "content": ""})
		for chunk in completion:
			chat_history[-1]["content"] += chunk.choices[0].delta.content or ""
			yield chat_history
		chat_context.append({"role": "assistant", "content": chat_history[-1]["content"]})

	msg.submit(add_message, [msg, chatbot], [msg, chatbot]).then(
		respond, chatbot, chatbot
	)

demo.launch(server_name="0.0.0.0")