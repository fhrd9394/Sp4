# imports
import sys
import os
from interface import chatgui
from prompt import prompt_builder

# Füge das Verzeichnis von app.py zum Python-Pfad hinzu
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Test_V1")
if app_path not in sys.path:
    sys.path.append(app_path)

from app import generate_code_from_prompt  # Importiere die Funktion aus app.py

"""
    Connector für verschiedene Module
    Öffnet die Chat-Schnittstelle, nimmt Benutzereingaben entgegen,
    erstellt den LLM-Prompt und gibt die Antwort zurück.

    Schritte:

    1.python app.py
    2.python connector.py
    3.prompt in interface senden
    4.Antwort warten
"""

def chat_callback(user_prompt):
    """
    Callback-Funktion für die Chat-Oberfläche.
    """
    try:
        # Generiere den Prompt mithilfe von prompt_builder
        llm_prompt = prompt_builder.build_prompt(user_prompt)
        print("USER PROMPT: ")
        print(llm_prompt)

        # Rufe die LLM-Generierungsfunktion auf
        llm_response = generate_code_from_prompt(llm_prompt)
        print("LLM RESPONSE:")
        print(llm_response)

        return llm_response
    except Exception as e:
        print(f"Error: {e}")
        return f"Fehler bei der Verarbeitung: {str(e)}"

def main():
    """
    Startet die Chat-GUI und setzt die Callback-Funktion.
    """
    chatgui.opengui(callback=chat_callback)

if __name__ == "__main__":
    main()



# # imports
# from interface import chatgui
# from prompt import prompt_builder

# """
#     connector for different modules
#     opens the chat and takes the user input as the user_prompt
#     calls prompt_builder to create an llm prompt and calls the llm to then return the llm response
# """

# # variables

# def call_llm(llm_prompt):
#     # TODO: call llm and get response
#     llm_response = ""
#     return llm_response

# def chat_callback(user_prompt):
#     # get the prompt for the llm
#     llm_prompt = prompt_builder.build_prompt(user_prompt)
#     print("USER PROMPT: ")
#     print(llm_prompt)
#     # call the llm to get the response
#     llm_response = call_llm(llm_prompt)

#     return llm_response

# def main():
#     # init chat_interface and call chat_callback as return function
#     chatgui.opengui(callback=chat_callback)

# if __name__ == "__main__":
#     main()