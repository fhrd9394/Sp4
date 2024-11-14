# imports
from interface import chatgui
from prompt import prompt_builder

"""
    connector for different modules
    opens the chat and takes the user input as the user_prompt
    calls prompt_builder to create an llm prompt and calls the llm to then return the llm response
"""

# variables

def call_llm(llm_prompt):
    # TODO: call llm and get response
    llm_response = ""
    return llm_response

def chat_callback(user_prompt):
    # get the prompt for the llm
    llm_prompt = prompt_builder.build_prompt(user_prompt)
    print("USER PROMPT: ")
    print(llm_prompt)
    # call the llm to get the response
    llm_response = call_llm(llm_prompt)

    return llm_response

def main():
    # init chat_interface and call chat_callback as return function
    chatgui.opengui(callback=chat_callback)

if __name__ == "__main__":
    main()