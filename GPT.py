import openai
import configparser

def gpt_interact(prompt):
    # Load API key from configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config['openai']['apikey']

    model="gpt-3.5-turbo"
    messages = [{
        "role": "system",
        "content": prompt
    }]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message['content']
