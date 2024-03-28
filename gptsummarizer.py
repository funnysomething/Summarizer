from openai import OpenAI
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['Credentials']['OPENAI_API_KEY']


async def generate_summary(messages):
    global api_key
    aiClient = OpenAI(api_key=api_key)
    messages1 = [
        {"role": "system", "content": f"Summarize the following discord messages."},
        {"role": "user", "content": "!summarize 1"}
    ]
    try:
        response = aiClient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")