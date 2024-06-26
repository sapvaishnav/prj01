import os
import json
from pypdf import PdfReader

def read_file(file):
    """ Read File using file variable"""
    text=""
    
    if file.name.endswith(".pdf"):
        try:
            text = ""
            reader = PdfReader(file)
            number_of_pages = len(reader.pages)
            for page in reader.pages:
                text+=page.extract_text()
             
             
             
             
            print(f"text : {text}")
            return text
        except Exception as e :
            print(f"file.name : {e}")
            return False
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except:
            return False
            

def get_table_data(quiz_str):
    """Get Table data from string"""
    try:
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option} -> {option_value}" for option,option_value in value["options"].items()
                ]
            )
            correct=value["correct"]
            quiz_table_data.append({"MCQ":mcq, "Choices":options, "Correct":correct})
            return quiz_table_data
    except:
        return False