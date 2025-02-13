

api_key = '*******'

from openai import OpenAI
client = OpenAI(api_key= api_key)

def sign_call(txt):
    msg = [
            {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "own context"}
        ]
                
    new_msg = {"role": "user", "content": txt}
    msg.append(new_msg)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= msg
    )
    
    reply = list(completion.choices[0].message)[0][1]

    return f"{reply}"
    
    

def user_call():
    while(True):
        
        msg = [
            {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "own context"}
        ]
        
        txt = input("Enter your qn : ")
        
        if txt == "leave" or txt == "exit":
            break
            
        new_msg = {"role": "user", "content": txt}
        msg.append(new_msg)
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= msg
        )

        print("Reply : ", list(completion.choices[0].message)[0][1])
        
        





