#imports
import os

"""
    prompt builder
    defines what should be in the llm prompt before the user prompt and after and returns a complete prompt
"""

# variables
CURRENT_FILE = os.path.dirname(__file__)
PRE_DIR = os.path.join(CURRENT_FILE, 'pre_prompt.txt')
POST_DIR = os.path.join(CURRENT_FILE, 'post_prompt.txt')

# load the prompt that should be before the user prompt
def pre_user():
    file = open(PRE_DIR, 'r', encoding="utf-8")
    pre_prompt = file.read()
    file.close()
    return pre_prompt

# load the prompt that follows the user prompt
def post_user():
    file = open(POST_DIR, 'r', encoding="utf-8")
    post_prompt = file.read()
    file.close()
    return post_prompt

def build_prompt(user_prompt):
    pre = pre_user()

    post = post_user()
    # concat pre, user, post to create the complete prompt
    llm_prompt = pre + " " + user_prompt + " " + post
    return llm_prompt