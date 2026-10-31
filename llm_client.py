from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-4o-mini") -> str:
    """Generate response using OpenAI with context"""
    system_prompt=f"""You are an AI assistant for NASA mission intelligence.
    context: {context}
    chat history: {conversation_history}
    """
    
    client = OpenAI(api_key=openai_key,base_url="https://openai.vocareum.com/v1")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=150,
    )
    assistant_response=response.choices[0].message.content if response.choices[0].message.content is not None else "NO RESPONSE"
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response
    # TODO: Define system prompt
    # TODO: Set context in messages
    # TODO: Add chat history
    # TODO: Creaet OpenAI Client
    # TODO: Send request to OpenAI
    # TODO: Return response


#########TESTING#########
#some_conversation_history = []
#print("What was Apollo 11?")
#response = generate_response("voc-58605238812667755290396ae080fde1b701.41181315", "What was Apollo 11?", "", some_conversation_history)
#print(response)
#print("Can you repeat that?")
#response=generate_response("voc-58605238812667755290396ae080fde1b701.41181315", "Can you repeat that?", "", some_conversation_history)
#print(response)
#print(some_conversation_history)