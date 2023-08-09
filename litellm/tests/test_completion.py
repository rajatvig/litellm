import sys, os
import traceback
from dotenv import load_dotenv
load_dotenv()
import os
sys.path.insert(0, os.path.abspath('../..'))  # Adds the parent directory to the system path
import pytest
import litellm
from litellm import embedding, completion
# from infisical import InfisicalClient

# litellm.set_verbose = True
# litellm.secret_manager_client = InfisicalClient(token=os.environ["INFISICAL_TOKEN"])

user_message = "Hello, whats the weather in San Francisco??"
messages = [{ "content": user_message,"role": "user"}]

def logger_fn(user_model_dict):
    print(f"user_model_dict: {user_model_dict}")

def test_completion_claude():
    try:
        response = completion(model="claude-instant-1", messages=messages, logger_fn=logger_fn)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_claude_stream():
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "how does a court case get to the Supreme Court?"}
        ]
        response = completion(model="claude-2", messages=messages, stream=True)
        # Add any assertions here to check the response
        for chunk in response:
            print(chunk['choices'][0]['delta']) # same as openai format
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_hf_api():
    try:
        user_message = "write some code to find the sum of two numbers"
        messages = [{ "content": user_message,"role": "user"}]
        response = completion(model="stabilityai/stablecode-completion-alpha-3b-4k", messages=messages, hugging_face=True)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_cohere():
    try:
        response = completion(model="command-nightly", messages=messages, max_tokens=500)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_cohere_stream():
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "how does a court case get to the Supreme Court?"}
        ]
        response = completion(model="command-nightly", messages=messages, stream=True, max_tokens=50)
        # Add any assertions here to check the response
        for chunk in response:
            print(chunk['choices'][0]['delta']) # same as openai format
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_openai():
    try:
        response = completion(model="gpt-3.5-turbo", messages=messages)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_openai_with_optional_params():
    try:
        response = completion(model="gpt-3.5-turbo", messages=messages, temperature=0.5, top_p=0.1, user="ishaan_dev@berri.ai")
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_openrouter():
    try:
        response = completion(model="google/palm-2-chat-bison", messages=messages, temperature=0.5, top_p=0.1, user="ishaan_dev@berri.ai")
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_openai_with_more_optional_params():
    try:
        response = completion(model="gpt-3.5-turbo", messages=messages, temperature=0.5, top_p=0.1, n=2, max_tokens=150, presence_penalty=0.5, frequency_penalty=-0.5, logit_bias={123: 5}, user="ishaan_dev@berri.ai")
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_openai_with_stream():
    try:
        response = completion(model="gpt-3.5-turbo", messages=messages, temperature=0.5, top_p=0.1, n=2, max_tokens=150, presence_penalty=0.5, stream=True, frequency_penalty=-0.5, logit_bias={27000: 5}, user="ishaan_dev@berri.ai")
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_openai_with_functions():
    function1 = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    ]
    try:
        response = completion(model="gpt-3.5-turbo", messages=messages, functions=function1)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_azure():
    try:
        response = completion(model="gpt-3.5-turbo", deployment_id="chatgpt-test", messages=messages, azure=True)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

# Replicate API endpoints are unstable -> throw random CUDA errors -> this means our tests can fail even if our tests weren't incorrect. 
def test_completion_replicate_llama_stream():
    model_name = "replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1"
    try:
        response = completion(model=model_name, messages=messages, stream=True)
        # Add any assertions here to check the response
        for result in response:
            print(result)
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_replicate_stability_stream():
    model_name = "stability-ai/stablelm-tuned-alpha-7b:c49dae362cbaecd2ceabb5bd34fdb68413c4ff775111fea065d259d577757beb"
    try:
        response = completion(model=model_name, messages=messages, stream=True, replicate=True)
        # Add any assertions here to check the response
        for chunk in response:
            print(chunk['choices'][0]['delta'])
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


# Replicate API endpoints are unstable -> throw random CUDA errors -> this means our tests can fail even if our tests weren't incorrect. 
# [TODO] improve our try-except block to handle for these
# def test_completion_replicate_llama():
#     model_name = "replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1"
#     try:
#         response = completion(model=model_name, messages=messages, max_tokens=500)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         print(f"in replicate llama, got error {e}")
#         pass
#         if e == "FunctionTimedOut":
#             pass
#         else:
#             pytest.fail(f"Error occurred: {e}")

def test_completion_replicate_stability():
    model_name = "stability-ai/stablelm-tuned-alpha-7b:c49dae362cbaecd2ceabb5bd34fdb68413c4ff775111fea065d259d577757beb"
    try:
        response = completion(model=model_name, messages=messages, replicate=True)
        # Add any assertions here to check the response
        for result in response:
            print(result)
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

######## Test TogetherAI ########
def test_completion_together_ai():
    model_name = "togethercomputer/mpt-30b-chat"
    try:
        response = completion(model=model_name, messages=messages, together_ai=True)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")