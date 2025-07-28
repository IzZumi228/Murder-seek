from openai import OpenAI
from dotenv import load_dotenv
import os
import random
from settings import *

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

#roles are based on indexes - characters[0] is murdere, for the rest look in system prompt
characters = ["Sylvia", "Marlowe", "Elsie", "Jasper"]
random.shuffle(characters)




SYSTEM_PROMPT = f"""
You are an AI Dialogue Generator for a simple murder mystery game. The premise of the game is a murder on a distant farm, and a detective (player) was sent to investigate. The elder of the farm was killed. There are 4 characters on the farm. When the detective interacts with a character, he can only ask 2 questions:

Personal Statement — “What were you doing on the day of the murder?” 

Observation — “Did you see anything unusual that day?”

Your task is to generate an answer for both questions for each character.

Characters Overview:

Sylvia Pine — A quiet carpenter

Marlowe Reed — A mysterious traveler who sells rare seeds and artifacts

Elsie Bloom — A kind-hearted botanist passionate about exotic plants

Jasper "Jas" Holt — A laid-back fisherman who knows all the local gossip

Dialogue Guidelines:

Answers must never include direct accusations. Only subtle, vague hints.

Characters are not aware of each other's statements or observations. They should not refer to or comment on each other’s stories.

Each character should speak in their natural tone, in 2–3 complete sentences per part.

Responses must feel natural and in-character.

Dialogue should maintain a grounded and realistic tone — avoid over-explaining or dramatic language.

Dialogue context for this round:

{characters[0]} (Murderer): In her Personal Statement, she should give a false alibi and claim she was with {characters[1]}. In her Observation, she should give a vague or unrelated comment — no direct accusations.

{characters[2]}: In his Personal Statement, he was with {characters[1]}. In his Observation, he should comment on something unusual about typical place of {characters[0]} - {CHARACTER_LOCATIONS[characters[0]]} e.g that it was unusually quiet.

{characters[1]}: In her Personal Statement, she was with {characters[2]}. In her Observation, she should mention that {characters[3]} was not at the {CHARACTER_LOCATIONS[characters[3]]} as usual.

{characters[3]}: In his Personal Statement, explain why he wasn’t at the {CHARACTER_LOCATIONS[characters[3]]} that day. In his Observation, mention nothing unusual.

Output Format:
Use the following format for each line:

FirstName:statement#observation
Each part should be a short paragraph (2–3 sentences), natural in tone.

Example:
Marlowe: I spent the afternoon cataloging my seed collection and testing soil samples by the river. Didn't leave my tent all day—too many rare specimens to sort through#Funny thing—I passed by Sylvia’stent just before sunset, and I didn’t hear any movement inside at all, even though she such a workaholic and works everyday.

Do not include anything else in the response. No headers, footers, or notes. Just the lines of dialogue.
"""

def generate_dialogues():
    print("generating dialogues...")
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": SYSTEM_PROMPT
            }
        ]
    )

    raw_text = completion.choices[0].message.content
    dialogues = {}

    for line in raw_text.strip().split("\n"):
        if line.strip() == "":
            continue
        if ":" in line:
            name, content = line.split(":", 1)
            statement, observation = content.strip().split("#", 1)
            dialogues[name.strip()] = {
                "statement": statement.strip(),
                "observation": observation.strip()
            }
    print("Done!")
    return dialogues






def get_actual_murderer():
    return characters[0]