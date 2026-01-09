import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()

class GenericHelper(object):
    @staticmethod
    def get_openai_client():
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    def get_anthropic_client():
        return Anthropic()

