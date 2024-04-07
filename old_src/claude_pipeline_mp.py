import os
import anthropic
import base64
import httpx
import json
import re

diversity_number = 3

all_api_keys = [Rahul, Pravin, Rahul1, Sushant, Shourya3, Shourya4, Vatsa1, Vatsa2, Jhanvi3, Ashrith, Akka, Rohit, Veda_Nivas, Jhanvi4]


client = anthropic.Anthropic(api_key = Rahul)

PROMPT_7 = '''
Imagine you are a human annotator, tasked with generating a Visual Question Answering benchmark dataset for CIRCULAR documents. You need to cover each and every part of the document and generate as many question answer pairs as possible. The question's answers should be obtained from the document itself, directly, that is, EXTRACTIVE type questions. And they should span the ENTIRE DOCUMENT, no part should be left out. GENERATE ATLEAST 30 Questions per document. 

The output should be in this Format:
Here are 30 question-answer pairs based on the information provided in the image:
1. <Question> : <Answer> 
2. <Question> : <Answer>
.....
30. <Question> : <Answer> 
'''

PROMPT_filter = '''

Given below are 4 sets of Question and Answer pairs given by you for a document. 4 sets of question answer pairs are generated by prompting the same document with the same prompt. Question and answers in each set could be different from the other set. Give me a set of 40 UNIQUE question-answer pairs from all the 4 sets based on the context of the question-answer pair. 

The input is in the format 
<QNO>. <pair['question']> : <pair['answer']>\n. 
Here QNO is the question number. pair['question'] is the question and pair['answer'] is the answer.  

Give me UNIQUE question-answer pairs in the below json format.

Here is a set of 40 unique question-answer pairs based on the context provided:
{
    [
        {'id':1,
         'question:<QUESTION>',
         'answer':<ANSWER> 
        },
        {'id':2,
         'question:<QUESTION>',
         'answer':<ANSWER> 
        },
        ....
        {'id':40,
         'question:<QUESTION>',
         'answer':<ANSWER> 
        }
    ]

} 

'''

# Define your API keys
api_keys = [Rahul, Pravin, Rahul1, Sushant, Shourya3, Shourya4, Vatsa1, Vatsa2, Jhanvi3, Ashrith, Akka, Rohit, Veda_Nivas, Jhanvi4]

def get_counted_responses(all_responses):
    print("Getting counted question answer pairs...")
    counted_qa_pairs = ""
    count=0
    q_and_a = []
    for response in all_responses:
        file_name = response["file"]
        id_file = response["id"]
        content = response["message"]
        # Remove the \\n
        try:
            content = content.replace("\\n", "\n")
            content = content.split('[{"text": ')[-1].split(', "type": "text"')[0]
            content = content.split('Here are 30 question-answer pairs based on the information provided in the image:')[1].strip()
        except:
            continue
        # q_and_a = []

        answer = ""
        for line in content.split("\n"):
            if line.strip() == "":
                continue

            if line[0].isdigit():
                if answer != "":
                    # If answer starts with Answer:
                    if answer.startswith("Answer:"):
                        answer = answer[7:].strip()

                    # Remove the first number from the question
                    question = question.split(".")[1].strip()          

                    q_and_a.append({
                        "question": question,
                        "answer": answer
                    })
                    answer = ""

                if "?" in line:
                    # The seperator is the number of the question and also the ? mark
                    seperator = line.index("?") + 1
                    question = line[:seperator]
                    answer = line[seperator + 1:] + answer
                    answer.strip().strip(":")
            else:
                answer = line + answer
        # print(q_and_a)
         
    for pair in q_and_a:
        count+=1
        counted_qa_pairs += f"{count}. {pair['question']} : {pair['answer']}\n"
    print(counted_qa_pairs)
    print("\n")
    return counted_qa_pairs

# Function to get response using multiple API keys
def get_response(prompt, file, api_keys):
    print(f"Getting response for {file}")
    all_responses = []
    for key in api_keys:
        print("Using API key", key)
        skip_key = False
        client = anthropic.Anthropic(api_key=key)
        with open(file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
            for i in range(diversity_number):
                print(f"Prompting for the {i+1}th time")
                try:
                    response = client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=4000,
                        temperature=0,
                        system=PROMPT_7,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/png",
                                            "data": image_data
                                        }
                                    }
                                ]
                            }
                        ]
                    )
                    dictt = {
                        "file": file,
                        "message": response.json(),
                        "id": i
                    }
                    all_responses.append(dictt)
                except Exception as e:
                    print(f"Error in getting response with API key {key}: {e}")
                    # Pop the Key from the array
                    if "request_too_large" in str(e):
                        print("Request is too large")
                        return []
                    api_keys.pop(api_keys.index(key))
                    skip_key = True
                    break
            if skip_key:
                continue
            else:
                break
    return all_responses

# Function to get unique question-answer pairs
def get_unique_qa_pairs(counted_qa_pairs, file_path):
    print("Getting unique question answer pairs...")
    response = []
    for key in api_keys:
        print("Using API key", key)
        skip_key = False
        client = anthropic.Anthropic(api_key=key)
        with open(file_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
            response = []
            try:
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=4000,
                    temperature=0,
                    system="Consider yourself to be a human annotator, and you are tasked to produce a visual question answering dataset. You've received question and answer pairs from other annotators and your task is to prepare a final dataset which has both diversity and representation. Give the final output question answer pairs. Also make sure the question answer pairs, are relevant to the given circular.\n\nGenerate at least 40 Pairs of Questions\nThe FORMAT of your output should be as follows:\nHere are 40 question-answer pairs based on the input, \n1. <Question> <Answer>\n2. <Question> <Answer>\n3. <Question> <Answer>\n......\n40. <Question> <Answer>",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Here are the question-answer pairs based on the information provided in the image:\n{counted_qa_pairs}"
                                },
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": image_data
                                    }
                                }
                            ]
                        }
                    ]
                    )
                if "error" in str(response):
                    if "request_too_large" in str(response):
                        print("Request is too large")
                        break
                    api_keys.pop(api_keys.index(key))
                    print("Error in response")
                    continue
                else:
                    break
            except Exception as e:
                print(f"Error in getting response with API key {key}: {e}")
                if "request_too_large" in str(e):
                    print("Request is too large")
                    return []
                # Pop the Key from the array
                api_keys.pop(api_keys.index(key))
                skip_key = True
                continue
            if skip_key:
                api_keys.pop(api_keys.index(key))
                continue
    return response


# Function to check if a file has already been processed
def is_file_processed(file_name, processed_files_file):
    if not os.path.exists(processed_files_file):
        return False
    with open(processed_files_file, "r") as f:
        processed_files = f.read().splitlines()
        return file_name in processed_files

# Function to mark a file as processed
def mark_file_processed(file_name, processed_files_file):
    with open(processed_files_file, "a") as f:
        f.write(file_name + "\n")

# Define your data folder and processed files file
data_folder = "Split_Images/middle_page"
processed_files_file = "processed_files_mp.txt"

# Get a list of all files in the data folder
files = os.listdir(data_folder)

# Open the JSON file, and see if the file is already in it?
# with open("first_page_50_2.json", "r") as f:
#     json_list_prev = json.load(f)

json_list = []

# Create a JSON file to store the unique question-answer pairs

# Open the JSON file in append mode before the loop starts
with open("middle_page.json", "a") as f:
    # Iterate through each file in the data folder
    for file in files:
        # Skip files that are not PNG images or have been processed before
        if not file.endswith(".png") or is_file_processed(file, processed_files_file):
            continue

        # Construct the full path to the file
        file_path = os.path.join(data_folder, file)

        # Perform the processing for the current file
        all_responses = get_response(PROMPT_7, file_path, api_keys)
        counted_qa_pairs = get_counted_responses(all_responses)
        response_unique_qa_pairs = get_unique_qa_pairs(counted_qa_pairs, file_path)

        if len(api_keys) == 0:
            print("All API keys have been exhausted")
            api_keys = all_api_keys.copy()

        # Mark the file as processed
        mark_file_processed(file, processed_files_file)

        # Extract and save the unique question-answer pairs to a text file
        try:
            content = response_unique_qa_pairs.json()
        except:
            continue

        # Save the unique question-answer pairs to a JSON file
        content = content.split('[{"text": ')[-1].split('\",\"type\":\"text\"}]')[0]
        # Index of 1.
        pattern = r'\d+\.\s+(.*?):\s+(.*?)(?=\d+\.\s|$)'

        # Use findall to extract all question-answer pairs
        qa_pairs = re.findall(pattern, content)

        qa_list = []

        # Print the extracted pairs
        for index, (question, answer) in enumerate(qa_pairs, start=1):
            qa_list.append({
                "question": question,
                "answer": answer
            })

        json_list.append({
            "file_name": file,
            "question_answer_pairs": qa_list
        })



        # Write the data to the file within the loop
        json.dump(json_list, f, indent=4)
        # Reset the json_list for the next iteration
        json_list = []