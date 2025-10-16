import os

from dotenv import load_dotenv
load_dotenv()

from models.gemini import generate
from ms_paint import draw_shapes

def main():
    user_input = input("enter prompt to draw on MS Paint: ")

    shapes = generate(user_input)

    if not isinstance(shapes, list):
        raise ValueError("Model output was not a list.")

    if len(shapes) == 0:
        print("No shapes to draw.")
        return
    print(shapes)
    draw_shapes(shapes)

if __name__ == "__main__":
    main()