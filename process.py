import streamlit as st
from stqdm import stqdm
import os
import subprocess
import re
from git import Repo
import requests
import stat
import numpy as np

@st.cache_data
def output(gpt_answer, uid):
    # Obtain username
    id = os.path.split(uid)[1]
    result=[]
    
    # Find ChatGPT mentioning any repository and create URL
    for i in os.listdir(uid):
        if(re.search(i,gpt_answer)):
            result.append(f"https://github.com/{id}/{i}")
    
    return result

@st.cache_data
def call_chatgpt(query, key):
    # THis code calls OpenAI passing it the query, telling the model to figure out the most complex repository
    header = st.header("Calling ChatGPT")

    if os.path.isfile("keys"):
        import keys
        key = keys.openai_key
    
    message_list=[{"role": "user", "content": "Tell me the most complex repository from this data and justify your answer: "+ query}]

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.9,
        "messages": message_list
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
}


    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200:
        content = [choice['message']['content'] for choice in response_json['choices']]
        print(content)
        st.success(f"Sucessfully called ChatGPT")        

        return content[0]

    else:
        st.error(f"Request failed with status code {response.status_code}: {response_json}")
        return None

@st.cache_data
def get_repo_summary(uid, exclude):
    from subprocess import run
    import subprocess
    
    header = st.header("Fetching Summaries")
    solutions=[]

    # Call cloc to generate summaries for each repository
    for i in stqdm(os.listdir(uid)):
        # output = run(f"cloc {os.path.join(uid,i)}", capture_output=True).stdout.decode()
        path_to_repo = os.path.join(uid,i)
        output = subprocess.getstatusoutput(f"./cloc {path_to_repo} --exclude-ext={exclude}")
        if output[0]==0:
            solutions.append(parse_cloc_output(output[1], i))
        else:
            st.write(output)
    
    return solutions

@st.cache_data
def get_query(solutions):
    # All summaries are merged and converted to string form to give to OpenAI
    query = ""
    for i in solutions:

        for key, value in i['Summary'].items():
            # print(f"{key}: {value}")
            query+= f"{key}: {value}\n"
            
        for lang, info in i['Language Breakdown'].items():
            query+= f"{lang}: Files- {info['Files']}, Blank- {info['Blank']}, Comment- {info['Comment']}, Code- {info['Code']}\n"
        # print("\n\n\n\n")
        query+= "\n\n"
    
    st.success(f"Fetched Summaries")        

    return query




@st.cache_data

def parse_cloc_output(output, name):
    # Recieves string output from cloc and converts response into structured data
    
    output = re.sub(' +', ' ', output)
    output = re.sub('\r', '\n', output)
    output = output.strip().split('\n')
    lines=[]
    lines = [line.strip() if line != '' else None for line in lines]
    
    for line in output:
        if line!="":
            lines.append(line.strip())
    
    total_files = None
    unique_files = None
    ignored_files = None
    try:
        total_files = int(lines[0].split()[0])
    except:
        None
    
    idx = 0
    
    for i in range(len(lines)):
        x = lines[i].split()
        if len(x)>=2 and x[1] == "unique":
            unique_files = int(x[0])
        if len(x)>=3 and x[2] == "ignored":
            ignored_files = int(x[0])
        if lines[i].startswith("-"):
            if idx == 0:
                idx = i
            else:
                idx = i+1
                break
    
                
    lang_breakdown = {}
    for line in range(idx, len(lines)):
        if lines[line].startswith("-"):
            break
        lang_info = lines[line].split()
        lang_name = " ".join(lang_info[0:-4])
        lang_data = {
            'Files': int(lang_info[-4]),
            'Blank': int(lang_info[-3]),
            'Comment': int(lang_info[-2]),
            'Code': int(lang_info[-1])
        }
        lang_breakdown[lang_name] = lang_data

    
    return {
        'Summary': {
            'Name': name,
            # 'Total Files': total_files,
            # 'Unique Files': unique_files,
            # 'Ignored Files': ignored_files
        },
        'Language Breakdown': lang_breakdown
    }



def download_data(response, uid):
    
    # All repositories that are forks are ignored
    data = []
    for i in response:
        if i['fork']== False:
            data.append(i)
    
    # repositories are downloaded
    header = st.header("Fetching Repositories")
    for i in stqdm(data):
        # Repo.clone_from(i['clone_url'], os.path.join(os.getcwd(), uid, i['name']))
        try:
            Repo.clone_from(i['clone_url'], os.path.join(os.getcwd(), uid, i['name']))
        except:
            repo_name = i["name"]
    
    st.success(f"Fetched {len(os.listdir(uid))} Repositories")        
    
def rmtree():
    # clears all repositories from all users 
    for root, dirs, files in os.walk("data", topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    st.success(f"Successfully deleted all data")            