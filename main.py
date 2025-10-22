import os
from dotenv import load_dotenv
load_dotenv()

# Assuming these imports work correctly
from models.gemini import generate
from ms_paint import draw_shapes, transcribe_from_mic 

def main():
    print("=== MS PAINT DRAWING TOOL WITH AI ===")
    print("Enter 1. To use voice based commands")
    print("Enter 2. To use text based commands")
    
    # Initialize user_input to None or an empty string
    user_input = None 
    
    choice = input("\nEnter your choice (1 or 2): ")

    if choice == '1':
        print("\n--- VOICE INPUT MODE ---")
        print("Listening for your command...")
        
        command = transcribe_from_mic(timeout=5, phrase_time_limit=10) # Added typical limits
        
        if not command:
            print("No voice command detected. Returning to main menu.")
            return

        print("-" * 40)
        print(f"Transcription: {command}")
        correction = input("Type correction text, or press Enter to confirm: ").strip()
        
        if correction:
            user_input = correction
            print("Correction applied.")
        else:
            user_input = command
            print("Transcription confirmed.")
        print("-" * 40)
        
    elif choice == '2':
        print("\n--- TEXT INPUT MODE ---")
        user_input = input("Enter prompt to draw on MS Paint: ")
        
    else:
        print("\nInvalid choice. Please enter '1' or '2'.")
        return # Exit the function if the choice is invalid

    # --- CORE LOGIC (Only runs if user_input is successfully defined) ---

    if not user_input:
        print("Input command is empty. Cannot generate shapes.")
        return

    print(f"Sending command to AI: '{user_input}'")
    
    try:
        shapes = generate(user_input)
    except Exception as e:
        print(f"Error communicating with AI model: {e}")
        return

    if not isinstance(shapes, list):
        print(f"Model returned invalid format: {type(shapes)}. Expected a list.")
        # If the model gives a string error or non-list, it should be handled
        raise ValueError("Model output was not a list.")

    if len(shapes) == 0:
        print("AI model returned no shapes to draw.")
        return
    
    print("\n--- GENERATED SHAPES ---")
    print(shapes)
    print("------------------------")
    
    try:
        draw_shapes(shapes)
    except ValueError as ve:
        print(f"Drawing Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred during drawing: {e}")


if __name__ == "__main__":
    main()