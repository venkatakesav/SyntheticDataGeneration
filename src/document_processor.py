import os
import json

from response_fetcher import ResponseFetcher
from qa_pair_generator import QuestionAnswerPairGenerator
from file_manager import FileManager
from constants import PROMPT_7

class DocumentProcessor:
    def __init__(self, data_folder, processed_files_file, json_file="middle_page.json"):
        self.data_folder = data_folder
        self.processed_files_file = processed_files_file
        self.response_fetcher = ResponseFetcher(all_api_keys)
        self.qa_pair_generator = QuestionAnswerPairGenerator()
        self.file_manager = FileManager()
        self.json = json_file

    def process_documents(self):
        files = os.listdir(self.data_folder)
        with open(self.json, "a") as f:
            for file in files:
                if not file.endswith(".png") or self.file_manager.is_file_processed(file, self.processed_files_file):
                    continue
                file_path = os.path.join(self.data_folder, file)
                all_responses = self.response_fetcher.get_response(PROMPT_7, file_path)
                counted_qa_pairs = self.qa_pair_generator.get_counted_responses(all_responses)
                response_unique_qa_pairs = self.qa_pair_generator.get_unique_qa_pairs(counted_qa_pairs, file_path)
                try:
                    content = response_unique_qa_pairs.json()
                    content = content.split('[{"text": ')[-1].split('\",\"type\":\"text\"}]')[0]
                    pattern = r'\d+\.\s+(.*?):\s+(.*?)(?=\d+\.\s|$)'
                    qa_pairs = re.findall(pattern, content)
                    qa_list = []
                    for index, (question, answer) in enumerate(qa_pairs, start=1):
                        qa_list.append({
                            "question": question,
                            "answer": answer
                        })
                    json.dump([{
                        "file_name": file,
                        "question_answer_pairs": qa_list
                    }], f, indent=4)
                except:
                    continue
                self.file_manager.mark_file_processed(file, self.processed_files_file)