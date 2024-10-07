import openai
from Token import OPENAITOKEN

openai.api_key = OPENAITOKEN

def AI_return(my_input):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=my_input+"，用繁體中文回答。",
        max_tokens=128,
        temperature=0.5,
    )

    completed_text = response["choices"][0]["text"]
    return completed_text

print(AI_return("hello"))