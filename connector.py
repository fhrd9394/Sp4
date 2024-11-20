# -*- coding: utf-8 -*-

# imports
import os

from interface import chatgui
from prompt import prompt_builder
# remove comment below if app.py can run on your PC
#from llama_3_1_8B_instruct import app as llm

"""
    connector for different modules
    opens the chat and takes the user input as the user_prompt
    calls prompt_builder to create an llm prompt and calls the llm to then return the llm response
"""

# variables
RESPONSE_DIR = "llm_outputs/"
file_index = 0

def call_llm(llm_prompt):
    #llm_response = llm.generate_code_from_prompt(llm_prompt)
    llm_response = "automatic response"
    return llm_response

# writes a string to a text file in RESPONSE_DIR and file_index (ascending)
def write_output_file(text):
    global file_index
    output_file_path = RESPONSE_DIR + str(file_index) + ".txt"

    while(os.path.isfile(output_file_path)): # if file exists because of earlier usage or similar, the index is increased so the old file isn't overwritten
        file_index += 1
        output_file_path = RESPONSE_DIR + str(file_index) + ".txt"
    file_index += 1 # write a new file every time

    with open(output_file_path, "w") as file:
        file.write(text)

    print("llm output saved to " + output_file_path)

def chat_callback(user_prompt):
    # save the output to an external file if the user writes #save# at the end
    save_output = False
    if user_prompt[-6:] == "#save#":
        save_output = True
        user_prompt = user_prompt[:len(user_prompt)-6] # remove #save# from the user_prompt, because the llm doesn't need that

    # get the prompt for the llm
    llm_prompt = prompt_builder.build_prompt(user_prompt)
    print("USER PROMPT: ")
    print(llm_prompt)
    print("\n")

    # call the llm to get the response
    llm_response = call_llm(llm_prompt)
    print("LLM RESPONSE: ")
    print(llm_response)
    print("\n")

    if save_output:
        write_output_file(llm_response)

    return llm_response

def main():
    # init chat_interface and call chat_callback as return function
    chatgui.opengui(callback=chat_callback)

if __name__ == "__main__":
    main()