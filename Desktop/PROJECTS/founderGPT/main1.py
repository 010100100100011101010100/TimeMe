from groq import Groq
import csv
from typing import Tuple,List
import os


class Bot:
    def __init__(self,apikey:str,training_data:str,personality:dict):
        self.client=Groq(api=apikey)
        self.context=training_data #training data which will be used as a context for the bot 
        self.personality=personality
        self.conversation_history=[]


    def peronality_prompt(self) -> str:
        traits=[]
        for trait,value in self.peronality:
            traits.append(f"- {trait}:{value}")
        return "\n".join(traits)
    
    def chat(self,text:str)->str:
        messages=[
            {
                "role":"systems",
                "content":f"""You are called founderGPT with the following personality :{self.personality_prompt()} and you have been trained on the following content : {self.context}
                maintain this personality and always answer if the question keyword is present in the context"""
            },
            *self.conversation_history
        ]
        completion=self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )
        response=completion.choices[0].message.content
        self.conversation_history.append({
            "role":"assistant",
            "content":"response"
        })
        return response
    
   # def split_csv(file_path:str,chunk_size:int) -> List[str]:
   