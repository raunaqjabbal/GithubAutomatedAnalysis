import requests
import json
import numpy as np
import regex as re
from tqdm import tqdm
import shutil
import os
import stat
import streamlit as st
from stqdm import stqdm
from git import Repo
from process import parse_cloc_output, download_data, get_query, get_repo_summary, call_chatgpt, output, rmtree

import requests


st.title("Github Automated Analysis")

            

os.system("chmod 777 cloc")

st.sidebar.header("How it works...")
st.sidebar.text("All GitHub repositories that aren't forks are cloned.")
st.sidebar.text("Summary for all repositories are generated using cloc.")
st.sidebar.text("These summaries are processed, aggregated and sent to GPT 3.5")
st.sidebar.text("Answer is extracted and response is shown.")
st.sidebar.text("Deployed on Google Cloud Run.")


st.sidebar.text("Least number of tokens are sent to OpenAI")
st.sidebar.text("Since the code is public, I'll be deleting keys on 15/8/2023.")
st.sidebar.text("Sorry for the inconvinence!")



st.sidebar.header("Form")
uid = st.sidebar.text_input("Enter GitHub Username", value="raunaqjabbal")

exclude = st.sidebar.text_input("Enter file extensions to exclude", value="xlsx,csv,md")



openai_key = st.sidebar.text_input("Enter OpenAI Key")

github_api_key = st.sidebar.text_input("Enter GitHub Key")

col1, col2, col3 = st.sidebar.columns([1,1,1])

with col1:
    button1 = st.button("Run Code!", key="runcode") 
with col2: 
    button2 = st.button("Delete Keys", key="delkey")
with col3:
    button3 = st.button("Delete Files", key="delfiles")

if button1:
    headers = {
        # 'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_api_key}',
        # 'X-GitHub-Api-Version': '2022-11-28',
    }

    response = requests.get(f'https://api.github.com/users/{uid}/repos', headers=headers)
    response = json.loads(response.text)
    if isinstance(response,dict):
        st.error("Error while getting repositories. Please try again.")
        st.write(response)
    else:
        # Continure if proper response is recieved from GitHub API
        uidloc = os.path.join("data", uid)
        if not os.path.exists(uidloc):
            os.mkdir(uidloc)
            
        # Download repositories from GitHub
        download_data(response, uidloc)
        
        # Obtain summaries
        solutions = get_repo_summary(uidloc, exclude)
        print(np.array(solutions))
        
        # Process and compress summaries to get query
        query = get_query(solutions)
        
        # Call OpenAI API
        gpt_answer = call_chatgpt(query, openai_key)
        
        if gpt_answer:
            # Extract result
            result = output(gpt_answer, uidloc)
            st.header("Links:")
            st.write(result)
            st.header("Reason:")
            st.write(gpt_answer)
            
        
        # rmtree()
    
if button2:
    openai_key = None
    github_api_key = None

if button3:
    rmtree()