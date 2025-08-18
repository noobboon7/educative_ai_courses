import gradio as gr
from groq import Groq
import os
import google.generativeai as genai
import PIL.Image

# Gemini setup
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Groq setup
client = Groq()

with gr.Blocks() as demo:
	chat_context = [
		{
			"role": "system",
			"content": 'You are a friendly and helpful educational chatbot named "HTML Guide." Your purpose is to assist users in learning and understanding HyperText Markup Language (HTML). You excel at providing clear explanations, practical examples, and interactive exercises.',
		}
	]
	chatbot = gr.Chatbot(type="messages", height=320)
	msg = gr.MultimodalTextbox(file_types=['image'], placeholder="Enter message or upload an image...", show_label=False) 

	def add_message(user_message, chat_history):
		file = False
		text = False

		if user_message["text"] and user_message["text"].strip():
			text = True
			chat_context.append({"role": "user", "content": user_message["text"]})
			
		if user_message["files"]:
			file = True
			chat_context.append({'role': 'user', 'content': 'The user sent an image'}) 
			chat_history.append({"role": "user", "content": {"path": user_message["files"][0]}})  
  
		# Only text
		if text and not file:	
			chat_history.append({"role": "user", "content": user_message["text"]})
		# Only image
		elif file and not text:
			chat_history.append({"role": "user", "content": "What do you see in this image?"})
			chat_history.append({"role": "assistant", "content": "Processing image ..."})
		# Both text and image
		else:
			chat_history.append({"role": "user", "content": user_message["text"]})
			chat_history.append({"role": "assistant", "content": "Processing image ..."})

		return gr.MultimodalTextbox(value=None, interactive=False), chat_history

	def respond(chat_history):
		if chat_history[-1]["content"] == "Processing image ...": 		
			img = PIL.Image.open(chat_history[-3]["content"][0])
			response = model.generate_content([chat_history[-2]["content"], img], stream=True)
			chat_history[-1]["content"] = ""
			for chunk in response:
				chat_history[-1]["content"] += chunk.text
				yield chat_history
			chat_context.append({"role": "assistant", "content": chat_history[-1]["content"]})
		else:
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
		respond, chatbot, chatbot).then(
		lambda: gr.MultimodalTextbox(interactive=True), None, [msg])

demo.launch(server_name="0.0.0.0")