import os
import json
import openai
from pydantic import BaseModel
from dotenv import load_dotenv


# "Strings are for Humans. Objects are for Engineers."

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==========================================
# ❌ THE OLD WAY (Don't do this)
# ==========================================
def get_user_bad():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Extract: John is 25."}]
    )
    data = response.choices[0].message.content
    
    # 💀 RISKY: What if the AI adds "Here is the JSON:"?
    try:
        user = json.loads(data)
        print(f"Old Way: {user['name']}")
    except json.JSONDecodeError:
        print("💥 CRASH: Invalid JSON returned.")

# ==========================================
# ✅ THE 3 SIGMA WAY (Pydantic)
# ==========================================
class User(BaseModel):
    name: str
    age: int
    is_engineer: bool

def get_user_good():
    # ✨ The Magic Line: client.beta.chat.completions.parse
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract user info."},
            {"role": "user", "content": "Neo is a 30 year old Matrix Engineer."}
        ],
        response_format=User, # 🛡️ Enforce Schema
    )

    user = completion.choices[0].message.parsed
    
    # It's not a dict. It's a typed Object.
    print(f"✅ Verified: {user.name} | Age: {user.age} | Engineer: {user.is_engineer}")

if __name__ == "__main__":
    # get_user_bad()
    get_user_good()
