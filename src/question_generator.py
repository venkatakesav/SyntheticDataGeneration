class QuestionAnswerPairGenerator:
    def get_counted_responses(self, all_responses):
        counted_qa_pairs = ""
        count = 0
        q_and_a = []
        for response in all_responses:
            content = response["message"]
            try:
                content = content.replace("\\n", "\n")
                content = content.split('[{"text": ')[-1].split(', "type": "text"')[0]
                content = content.split('Here are 30 question-answer pairs based on the information provided in the image:')[1].strip()
            except:
                continue
            answer = ""
            for line in content.split("\n"):
                if line.strip() == "":
                    continue
                if line[0].isdigit():
                    if answer != "":
                        if answer.startswith("Answer:"):
                            answer = answer[7:].strip()
                        question = question.split(".")[1].strip()
                        q_and_a.append({
                            "question": question,
                            "answer": answer
                        })
                        answer = ""
                    if "?" in line:
                        separator = line.index("?") + 1
                        question = line[:separator]
                        answer = line[separator + 1:] + answer
                        answer.strip().strip(":")
                    else:
                        answer = line + answer
        for pair in q_and_a:
            count += 1
            counted_qa_pairs += f"{count}. {pair['question']} : {pair['answer']}\n"
        return counted_qa_pairs

    def get_unique_qa_pairs(self, counted_qa_pairs, file_path):
        response = []
        for key in all_api_keys:
            try:
                client = anthropic.Anthropic(api_key=key)
                with open(file_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode("utf-8")
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
                        all_api_keys.remove(key)
                        if not all_api_keys:
                            all_api_keys.extend(all_api_keys)
                    print("Error in response")
                    continue
                else:
                    break
            except Exception as e:
                print(f"Error in getting response with API key {key}: {e}")
                if "request_too_large" in str(e):
                    print("Request is too large")
                    all_api_keys.remove(key)
                    if not all_api_keys:
                        all_api_keys.extend(all_api_keys)
                    continue
        return response