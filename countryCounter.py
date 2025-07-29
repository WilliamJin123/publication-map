from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
import time


load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

def process_batch(batch):

    

    prompt = f"""
    I have a list of author affiliation strings. Each new url represents a new article, and each article has a list of authors with their affiliations. The affiliations may include the country of the institution, but they are not consistently formatted.
    Some affiliations include the full country name, some abbreviate it, and some omit it but include a well-known institution or city.

    Your task:
        For each line, determine the country of the affiliation (infer it if not explicitly stated).  
        Then, count how many times each country appears in this list.  
        Output only a JSON object where the keys are country names (in English, fully spelled out) and the values are the counts.  
        If you cannot confidently infer a country for a line, ignore it and do not include it in the count.
        
        Here is the list of affiliations:
        {batch}


    Output only the JSON object and nothing else. Do not include any explanations or additional text, especially avoid giving me python coide or any other programming language code. Do not explain your reasoning, just provide the JSON output with the country counts.
    """


    client = genai.Client(api_key=API_KEY)


    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[
            types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
        ]
        
    )
    
    candidate = response.candidates[0]
    if not candidate.content or not candidate.content.parts:
        raise RuntimeError("No content returned by Gemini model for this batch.")

    output_text = candidate.content.parts[0].text
    return output_text


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


if __name__ == "__main__":
    if not API_KEY:
        raise ValueError("API_KEY not set. Please set it in your environment variables.")
    
    
    with open("files/author_data.csv", "r", encoding="utf-8") as f:
        all_affiliations = [line.strip() for line in f if line.strip()]    
       
        batch_start = 16
        for i, batch in enumerate(chunks(all_affiliations, batch_size)):
            if i < batch_start-1:
                continue
            time.sleep(3)
            output = open("mapData.txt", "a", encoding="utf-8")
            result = process_batch(batch)
            print(f"Batch {i+1}:")
            output.write(f"Batch {i+1}:\n")
            print(result)
            output.write(result + "\n")
            output.close()
            
        
    