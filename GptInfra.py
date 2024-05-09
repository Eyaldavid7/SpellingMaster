from openai import OpenAI
import os

def get_api_key(): 
    # Define the name of the API key
    name = "ChatGPTKey"
    # Retrieve the secret
    api_key = os.environ.get(name, 'Specified environment variable is not set.')

     

    return api_key
def Build_Prompet(Question):
    new_prompet = """Please correct the english gremmer for the follwoing sentence focus on time tenses, in you answe please include the currect sentence, the 
    parts with you repehased and the resaon for the reprhaseing the sentence, """ + Question
    return new_prompet

def SendToGpt(Question):
    client = OpenAI(
             # This is the default and can be omitted
             api_key=get_api_key(),
            )
     # Use the variable 'text' in the chat completion
    response = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content": Question,  # Using the variable instead of a hardcoded string
                }
            ],
            model="gpt-4",
        )
    name = response.choices[0].message.content
    print(name)
    return name