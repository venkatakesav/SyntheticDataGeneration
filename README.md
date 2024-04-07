# 1. **Separate Concerns**: The current code has multiple responsibilities, such as fetching responses, processing responses, and managing file operations. We can separate these concerns into different classes or modules.

# 2. **Create a `DocumentProcessor` Class**: This class will be responsible for the core functionality of processing a document and generating question-answer pairs.
#    - The class will have methods for fetching responses, processing responses, and generating unique question-answer pairs.
#    - It will also have methods for managing file operations, such as checking if a file has been processed and marking a file as processed.

# 3. **Create a `ResponseFetcher` Class**: This class will be responsible for fetching responses from the Anthropic API using the provided API keys.
#    - The class will have a method for fetching responses for a given prompt and file.
#    - It will handle the logic of rotating through the API keys and retrying on errors.

# 4. **Create a `QuestionAnswerPairGenerator` Class**: This class will be responsible for processing the fetched responses and generating the question-answer pairs.
#    - The class will have methods for counting the question-answer pairs and generating unique question-answer pairs.
#    - It will also handle the formatting of the output.

# 5. **Create a `FileManager` Class**: This class will be responsible for managing the file operations, such as checking if a file has been processed and marking a file as processed.
#    - The class will have methods for checking if a file has been processed and marking a file as processed.

# 6. **Refactor the Main Logic**: The main logic of the script will now be simplified and will use the created classes and their methods to perform the overall task.

# Here's the refactored code: