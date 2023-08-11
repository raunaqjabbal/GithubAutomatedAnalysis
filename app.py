import requests
import json
import numpy as np
import regex as re
from tqdm import tqdm
import shutil
import os
import stat
import streamlit as st
import keys
from stqdm import stqdm
from git import Repo
from process import parse_cloc_output, download_data, get_query, get_repo_summary, call_chatgpt, output, rmtree

import requests


st.title("Github Automated Analysis")

            

    


uid = st.sidebar.text_input("Enter GitHub Username", value="raunaqjabbal")

openai_key = st.sidebar.text_input("Enter OpenAI Key", value = "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")


col1, col2, col3 = st.sidebar.columns([1,1,1])

with col1:
    button1 = st.button("Run Code!", key="runcode") 
with col2: 
    button2 = st.button("Delete Key", key="delkey")
with col3:
    button3 = st.button("Delete Files", key="delfiles")

if button1:
    github_api_key = keys.github_api_key
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
        uidloc = os.path.join("data", uid)
        if not os.path.exists(uidloc):
            os.mkdir(uidloc)
        download_data(response, uidloc)
        solutions = get_repo_summary(uidloc)
        query = get_query(solutions)
        gpt_answer = call_chatgpt(query, openai_key)
        if gpt_answer:
            result = output(gpt_answer, uidloc)
            st.header("Links:")
            st.write(result)
            st.header("Reason:")
            st.write(gpt_answer)
            
        
        rmtree()
    
if button2:
    openai_key=None

if button3:
    rmtree()
