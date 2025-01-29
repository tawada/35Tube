import os

import vertexai
from vertexai.generative_models import GenerativeModel, Part

project_id = os.environ["PROJECT_ID"]
location = os.environ["LOCATION"]

vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-1.5-flash-002")
response = model.generate_content(
    [
        Part.from_uri(
            # "gs://cloud-samples-data/generative-ai/image/scones.jpg",
            "https://storage.googleapis.com/cloud-samples-data/generative-ai/image/scones.jpg",
            mime_type="image/jpeg",
        ),
        "What is shown in this image?",
    ]
)

print(response.text)
