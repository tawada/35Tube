import os

import vertexai

from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

# Initialize Vertex AI
project_id = os.environ["PROJECT_ID"]
location = os.environ["LOCATION"]

vertexai.init(project=project_id, location=location)

# Initialize Gemini model
model = GenerativeModel("gemini-1.5-flash-002")

# Define the user's prompt in a Content object that we can reuse in model calls
user_prompt_content = Content(
    role="user",
    parts=[
        Part.from_text("What is the weather like in Boston?"),
    ],
)

# Specify a function declaration and parameters for an API request
function_name = "get_current_weather"
get_current_weather_func = FunctionDeclaration(
    name=function_name,
    description="Get the current weather in a given location",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {"location": {"type": "string", "description": "Location"}},
    },
)

# Define a tool that includes the above get_current_weather_func
weather_tool = Tool(
    function_declarations=[get_current_weather_func],
)

# Send the prompt and instruct the model to generate content using the Tool that you just created
response = model.generate_content(
    user_prompt_content,
    generation_config=GenerationConfig(temperature=0),
    tools=[weather_tool],
)
function_call = response.candidates[0].function_calls[0]
print(function_call)
print(function_call.args)

# Check the function name that the model responded with, and make an API call to an external system
if function_call.name == function_name:
    # Extract the arguments to use in your API call
    location = function_call.args["location"]  # noqa: F841

    # Here you can use your preferred method to make an API request to fetch the current weather, for example:
    # api_response = requests.post(weather_api_url, data={"location": location})

    # In this example, we'll use synthetic data to simulate a response payload from an external API
    api_response = """{ "location": "Boston, MA", "temperature": 38, "description": "Partly Cloudy",
                    "icon": "partly-cloudy", "humidity": 65, "wind": { "speed": 10, "direction": "NW" } }"""

# Return the API response to Gemini so it can generate a model response or request another function call
response = model.generate_content(
    [
        user_prompt_content,  # User prompt
        response.candidates[0].content,  # Function call response
        Content(
            parts=[
                Part.from_function_response(
                    name=function_name,
                    response={
                        "content": api_response,  # Return the API response to Gemini
                    },
                ),
            ],
        ),
    ],
    tools=[weather_tool],
)

# Get the model response
print(response.text)
# Example response:
# The weather in Boston is partly cloudy with a temperature of 38 degrees Fahrenheit.
# The humidity is 65% and the wind is blowing from the northwest at 10 mph.
