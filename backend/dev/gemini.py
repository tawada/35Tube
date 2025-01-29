import os

import vertexai
from vertexai.generative_models import GenerativeModel

project_id = os.environ["PROJECT_ID"]
location = os.environ["LOCATION"]

vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-1.5-flash-002")
response = model.generate_content(
    "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
)

print(response.text)
