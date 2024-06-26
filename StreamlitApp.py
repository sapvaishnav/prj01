import os
import json
import traceback
import pandas as pd 
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGEnerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
from langchain.callbacks import get_openai_callback

file_path = 'Response.json'
RESPONSE_JSON=""
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    with open(file_path, 'r') as file:
        try:
            RESPONSE_JSON = json.load(file)        
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            
else:
    print(f"File '{file_path}' does not exist or is empty.")


st.title("MCQ Generator Application")
if True :
    with st.form("User_Input"):
        #file uploader
        uploaded_file=st.file_uploader("Upload a PDF file or txt file")
        #input mcq number
        mcq_count=st.number_input("No. of MCQs : ",min_value=3,max_value=50)
        #subject 
        subject=st.text_input("Enter Subject Name : ",max_chars=30)
        #Quiz Tone
        quiz_tone=st.text_input("Enter Quiz Tone : ",max_chars=10,placeholder="Simple")
        #Button
        create_button=st.form_submit_button("Create MCQs")
        
        
        if create_button and uploaded_file is not None and mcq_count and subject and quiz_tone :
            with st.spinner("...Loading"):
                try:
                    text=read_file(uploaded_file)
                    print(f"text : {text}")
                    #Count Tokens and the cost of API
                    if False :
                        with get_openai_callback() as cb:
                            response=generate_evaluate_chain(
                                {
                                    "text":text,
                                    "number":mcq_count,
                                    "subject":subject,
                                    "tone":quiz_tone,
                                    "response_json":json.dumps(RESPONSE_JSON)
                                }
                            )
                except Exception as e:
                    traceback.print_exception(type(e),e,e.__traceback__)
                    st.error("Error")
                    
                else:
                     if False :
                        print(f"Total Token : {cb.total_tokens}")
                        print(f"Prompt Token : {cb.prompt_tokens}")
                        print(f"Completion Token : {cb.completion_tokens}")
                        print(f"Total Cost : {cb.total_cost}")
                        if isinstance(response,dict):
                            quiz=response.get("quiz",None)
                            if quiz is not None:
                                table_data=get_table_data(quiz)
                                if table_data is not None:
                                    df=pd.DataFrame(table_data)
                                    df.index=df.index+1 
                                    st.table(df)
                                    #Display the review in  a text box as well
                                    st.text_area(label="Review",value=response["review"])
                                else:
                                    st.error("Error in the table data")
                        else:
                            st.write(response)               




