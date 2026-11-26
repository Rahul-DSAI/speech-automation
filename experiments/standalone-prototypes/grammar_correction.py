import google.generativeai as genai

class GoogleGeminiAPI:
    def __init__(self, api_key, model_name="models/gemini-1.0-pro-latest"):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None

    def gcp_config(self):
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_model(self):
        try:
            self.gcp_config()
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_text(self, prompt, text):
        try:
            if not self.model:
                self.load_model()
            response = self.model.generate_content(prompt + text)
            return response.text
        except Exception as e:
            print(f"generate_text:: {e}")
            return None

def correct_grammar(api_key, text):
    prompt = '''
        You are a highly knowledgeable language teacher with in-depth expertise in multiple languages, including their grammar, pronunciation, and vocabulary. Your role is to teach language learners how to speak fluently and accurately in any language they choose...
        '''
    gemini_api = GoogleGeminiAPI(api_key)
    return gemini_api.generate_text(prompt, text)
