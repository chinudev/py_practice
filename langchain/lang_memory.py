import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory

llm_model = "gpt-3.5-turbo"

def use_memory():
    # pick a particular model, add some memory and make a conversation chain
    llm = ChatOpenAI(temperature=0.0, model=llm_model)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm, 
        memory = memory,
        verbose=True
    )

    conversation.predict(input="Hi, my name is inigo montoya ?")
    conversation.predict(input="What is 1+1?")
    conversation.predict(input="What is my name?")  # The model should remember the name from the first input   

    # Note that memory is keeping track of all the human and ai messages and sending them with each request.
    print(memory.buffer) 

def manual_memory():
    # We can add details manually... 
    memory = ConversationBufferMemory()
    memory.save_context({"input": "What is my favorite color?"}, {"output": "I don't know, what is your favorite color?"})
    memory.save_context({"input": "What is 1 + 1 ?"}, {"output": "One plus one is two ?"})
    print(memory.buffer)

    # repeat with limited memory
    print("Repeat with limited memory") 
    memory = ConversationBufferWindowMemory(k=1)
    memory.save_context({"input": "What is my favorite color?"}, {"output": "I don't know, what is your favorite color?"})
    memory.save_context({"input": "What is 1 + 1 ?"}, {"output": "One plus one is two ?"})
    print(memory.buffer)

# this function uses the older API for memory that no longer works
# .. I can still see the output in the memory buffer whcih shows the impact of limiting the memory.. 
def use_window_memory():
    llm = ChatOpenAI(temperature=0.0, model=llm_model)
    memory = ConversationBufferWindowMemory(k=1)
    conversation = ConversationChain(
        llm=llm, 
        memory = memory,
        verbose=True
    )

    conversation.predict(input="Hi, my name is inigo montoya ?")
    conversation.predict(input="What is 1+1?")
    conversation.predict(input="What is my name?")  
    print(memory.buffer)

#use_memory()
#manual_memory() 
use_window_memory()