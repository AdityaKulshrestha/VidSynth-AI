import os
from openai import OpenAI
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ['KRUTIM_API_KEY'],
            base_url=os.environ['BASE_LLM_URL'],
        )

    def chat_completion(
            self,
            messages_list: List[Dict],
            model_name: str,
            generation_config: Optional[Dict] = None):
        if generation_config is None:
            generation_config = {}
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages_list,
            **generation_config
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    client = LLMClient()
    messages = [
        {"role": "system", "content": "You are a maths expert who can solve any type of problem and return back its solution in latex"},
        {"role": "user", "content": "Solve the equation of x^2 + 4x + 2 = 8"}
    ]
    model_name = "DeepSeek-R1"
    response = client.chat_completion(messages, model_name)
    print(response)
