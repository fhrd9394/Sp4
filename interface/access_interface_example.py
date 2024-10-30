import chatgui
"""
    example on how to use the chatgui
"""

# callback function, takes the user import as argument and returns a string
def create_response(msg):
    print(msg)
    if(msg == "A"):
        return "B"
    else:
        return "Thats not an A"

if __name__ == "__main__":
    # create the chat gui
    chatgui.opengui(callback=create_response)