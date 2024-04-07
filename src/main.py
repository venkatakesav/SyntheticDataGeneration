import anthropic
import base64
import json
import re

import os
from src.document_processor import DocumentProcessor
from src.constants import all_api_keys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process documents.")
    parser.add_argument("--data_folder", type=str, help="Path to the data folder.")
    parser.add_argument("--processed_files_file", type=str, help="Path to the processed files file.")
    parser.add_argument("--json_file", type=str, help="Path to the JSON file.")
    args = parser.parse_args()

    document_processor = DocumentProcessor(args.data_folder, args.processed_files_file)
    document_processor.process_documents()
