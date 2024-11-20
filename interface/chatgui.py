#imports
from tkinter import *

"""
    simple chatgui
    to use call opengui(callback)
    callback has to be a function that can process the user input (string)
    so callback will take a string message and return a string response
"""

# colors and fonts
BG_GRAY = "#756d6b"
BG_COLOR = "#264757"
TEXT_COLOR = "#d1e8f3"
CHAT_COLOR = "#354247"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# sending a message into the chat
def send(e, txt, callback):
    txt.config(state=NORMAL)

    send = "User: " + e.get()
    txt.insert(END, "\n" + send)

    user_input = e.get()

    e.delete(0, END)

    response = callback(user_input) # callback to process function and get response from there

    txt.insert(END, "\n" + "LLM: " + response)

    txt.config(state=DISABLED) # make textbox not interactive to user (so you cannot type in it)


# initializes the chat interface
def opengui(callback):
    root = Tk()
    root.title("Code Creator")

    headline_label = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="LLM Code", font=FONT_BOLD, pady=20, width=50, height=1).grid(row=0, column=0)
 
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)
 
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
 
    e = Entry(root, bg=CHAT_COLOR, fg=TEXT_COLOR, font=FONT, width=55)
    e.grid(row=2, column=0)
 
    # Return (enter) Key and Send button will send the message
    root.bind('<Return>', lambda event: send(e, txt, callback))
    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=lambda: send(e, txt, callback)).grid(row=2, column=1)
 
    root.mainloop()
