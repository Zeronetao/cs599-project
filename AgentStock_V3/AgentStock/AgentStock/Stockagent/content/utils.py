import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY", "")

def get_response(system_prompt, user_prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

def simple_log(text):
    print(f"[LOG] {text}")