import anthropic
import base64

from constants import all_api_keys, diversity_number

class ResponseFetcher:
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def get_response(self, prompt, file_path):
        # Move the ResponseFetcher class implementation here
            def get_response(self, prompt, file_path):
        all_responses = []
        for key in self.api_keys:
            try:
                client = anthropic.Anthropic(api_key=key)
                with open(file_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode("utf-8")
                for i in range(diversity_number):
                    response = client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=4000,
                        temperature=0,
                        system=prompt,
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
                        "file": file_path,
                        "message": response.json(),
                        "id": i
                    }
                    all_responses.append(dictt)
            except Exception as e:
                print(f"Error in getting response with API key {key}: {e}")
                if "request_too_large" in str(e):
                    print("Request is too large")
                    self.api_keys.remove(key)
                    if not self.api_keys:
                        self.api_keys = all_api_keys.copy()
                    continue
        return all_responses