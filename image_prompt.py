import os
import random
import requests
import json
import datetime  # Import datetime module

def generate_text(prompt, model="tomchat-1dllama", base_url="http://localhost:11434"):  # Replace with your Ollama server address
    url = f"{base_url}/api/generate"
    headers = {'Content-Type': 'application/json'}  # Important: Set the Content-Type header
    data = {
        "model": model,
        "prompt": prompt,
        "stream":False,

    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))  # Use json.dumps()
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()  # Parse the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'response' in locals(): # Corrected typo 'responce' to 'response'
            if response.status_code != 200:
                print(f"Status Code: {response.status_code}")
                print(f"Response Text: {response.text}") # Print the response from the server for debugging
        return None

def get_random_description_from_file(filepath):
    """
    Returns a random line from a given file.
    """
    try:
        with open(filepath, 'r') as f:
            descriptions = [line.strip() for line in f if line.strip()] # Read lines and remove empty ones
            if not descriptions:
                return None # File is empty or contains only empty lines
            return random.choice(descriptions)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None


def get_vibe_description_by_name(vibes_dir, vibe_name):
    """
    Retrieves a random description for a specific vibe name from the vibes directory.
    """
    vibe_file = os.path.join(vibes_dir, f"{vibe_name}.txt")
    return get_random_description_from_file(vibe_file)

def get_season_description_by_name(seasons_dir, season_name):
    """
    Retrieves a random description for a specific season name from the seasons directory.
    """
    season_file = os.path.join(seasons_dir, f"{season_name}.txt")
    return get_random_description_from_file(season_file)


def get_event_description(event_file_path):
    
    return get_random_description_from_file(event_file_path)
    

def get_season_by_time():
    """
    Determines the season based on the current date.
    """
    now = datetime.datetime.now()
    month = now.month
    #if month in [12, 1, 2]: # December, January, February
    return "winter"
    #elif month in [3, 4, 5]: # March, April, May
    #    return "spring"
    #elif month in [6, 7, 8]: # June, July, August
    #    return "summer"
    #else: # September, October, November
    #    return "autumn" # or "fall" if you prefer


def generate_image_prompt_with_vibe_season_event_old(vibe_name, vibes_dir="./vibes", seasons_dir="./seasons", event_file="./events/events.txt"):
    """
    Generates an image prompt using an LLM, incorporating user-specified vibe, time-determined season, and event descriptions.
    The prompt is now assembled directly from vibe, season, and event information.

    Args:
        vibe_name: The name of the vibe to use (user-provided).
        vibes_dir: Directory containing vibe description text files.
        seasons_dir: Directory containing season description text files.
        event_file: Path to the event description text file.

    Returns:
        The generated image prompt as a string, or None if there was an error.
    """

    vibe_description = get_vibe_description_by_name(vibes_dir, vibe_name)
    season_name = get_season_by_time()
    season_description = get_season_description_by_name(seasons_dir, season_name)
    event_description = get_event_description(event_file)

    description_parts = []
    description_parts.append(f"A {vibe_name} scene") # Start with vibe name
    if vibe_description:
        description_parts.append(vibe_description)
    description_parts.append(f"in {season_name}") # Add season name
    if season_description:
        description_parts.append(season_description)
    if event_description:
        description_parts.append(f"featuring {event_description}")

    assembled_description = ", ".join(description_parts) # Join with commas

    assembled_description = f"write a prompt for an image generation language model using the folowing statement, Flynn tower shows like a beacon amid {assembled_description}. Write only the prompt."
    print("--- Assembled Description for LLM Prompt ---")
    
    print(assembled_description)
    print("---")


    llm_response = generate_text(assembled_description) # Pass assembled description as prompt

    if llm_response and 'response' in llm_response: # Check if response is in the dict
        image_prompt = llm_response['response']
        print("--- LLM Generated Image Prompt ---")
        print(image_prompt)
        print("---")
        return image_prompt
    else:
        print("Error: Failed to generate image prompt from LLM.")
        return None

def generate_image_prompt_with_vibe_season_event(vibe_name, vibes_dir="./vibes", seasons_dir="./seasons", event_file="./events/events.txt", page_context_file=None):
    """
    Generates an image prompt using an LLM, incorporating user-specified vibe, time-determined season, event, and page context descriptions.
    """

    vibe_description = get_vibe_description_by_name(vibes_dir, vibe_name)
    season_name = get_season_by_time()
    season_description = get_season_description_by_name(seasons_dir, season_name)
    event_description = get_event_description(event_file)

    description_parts = []
    description_parts.append(f"A {vibe_name} scene")
    if vibe_description:
        description_parts.append(vibe_description)
    description_parts.append(f"in {season_name}")
    if season_description:
        description_parts.append(season_description)
    if event_description:
        description_parts.append(f"featuring {event_description}")

    # Add page context if provided
    if page_context_file:
        page_context_description = get_random_description_from_file(page_context_file)
        if page_context_description:
            description_parts.append(page_context_description)

    assembled_description = ", ".join(description_parts)

    assembled_description = f"write a prompt for an image generation language model using the folowing statement, Flynn tower shows like a beacon amid {assembled_description}. Write only the prompt."
    print("--- Assembled Description for LLM Prompt ---")
    print(assembled_description)
    print("---")

    llm_response = generate_text(assembled_description)

    if llm_response and 'response' in llm_response:
        image_prompt = llm_response['response']
        print("--- LLM Generated Image Prompt ---")
        print(image_prompt)
        print("---")
        return image_prompt
    else:
        print("Error: Failed to generate image prompt from LLM.")
        return None
        
if __name__ == '__main__':
    # Example Usage (Index Page):
    user_vibe_name = "cyberpunk"
    image_prompt = generate_image_prompt_with_vibe_season_event(user_vibe_name)

    if image_prompt:
        print("\n--- Final Image Prompt (Index) ---")
        print(image_prompt)
    else:
        print("\nImage prompt generation failed.")

    # Example Usage (Sub-Page):
    user_vibe_name = "cyberpunk"
    sub_page_context_file = "/home/ttombbab/shadow_kernel/page_context/trails.txt"  # Replace with your sub-page context file
    image_prompt_subpage = generate_image_prompt_with_vibe_season_event(user_vibe_name, page_context_file=sub_page_context_file)

    if image_prompt_subpage:
        print("\n--- Final Image Prompt (Sub-Page) ---")
        print(image_prompt_subpage)
    else:
        print("\nImage prompt generation failed.")
