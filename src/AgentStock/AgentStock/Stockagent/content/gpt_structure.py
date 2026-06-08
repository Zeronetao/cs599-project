import json
import random
import openai
import time
from timeout_decorator import timeout
from .utils import *
from ..database_utils import round_two_decimal, trans_url
import os
from pathlib import Path
from openai import OpenAI
import re
import PIL.Image
import google.generativeai as genai

# proxy_url = 'http://127.0.0.1'
# proxy_port = '18081'

# 禁用代理设置，直接连接API
# os.environ['http_proxy'] = f'{proxy_url}:{proxy_port}'
# os.environ['https_proxy'] = f'{proxy_url}:{proxy_port}'
openai.api_key = ""


def temp_sleep(seconds=0.1):  # 进一步减少等待时间从0.1秒到0.01秒
    time.sleep(seconds)


def ChatGPT_single_request(prompt):
    temp_sleep()

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]


# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================


def GPT4_request(prompt):
    """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
    temp_sleep()

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return completion["choices"][0]["message"]["content"]

    except:
        print("ChatGPT ERROR")
        return "ChatGPT ERROR"

def qwen_request(prompt):
    try:
        openai = OpenAI(
    api_key="sk-01955ed7b6f6406bb4e5ce528fe68882",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

        chat_completion = openai.chat.completions.create(
            model="qwen-vl-max",
            messages=[{"role": "user", "content": prompt}],
            #temperature=1.5
)
        return chat_completion.choices[0].message.content

    except:
        print("ChatGPT ERROR!")
        return "ChatGPT ERROR"

def qwenvl_vision(prompt, image_url1, image_url2, image_url3, image_url4, image_url5 ):#
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key="sk-4a5c652a71954c55ada74abfed16dcb5",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-vl-max",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                    {
                      "role": "user",
                      "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url","image_url": {"url": image_url1,},},
                        {"type": "image_url","image_url": {"url": image_url2,},},
                        {"type": "image_url","image_url": {"url": image_url3,},},
                        {"type": "image_url","image_url": {"url": image_url4,},},
                        {"type": "image_url","image_url": {"url": image_url5,},},
                      ],
                    }
                  ],
            )
        return completion.choices[0].message.content
    except:
        print("ChatGPT ERROR!")
        return "ChatGPT ERROR"

def qwenvl(prompt):#
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key="sk-273c8acde88b4f53972c8cc707cccdeb",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-vl-max",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                    {
                      "role": "user",
                      "content": [
                        {"type": "text", "text": prompt},
                      ],
                    }
                  ],
            )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT ERROR! qwenvl API调用失败: {str(e)}")
        return "ChatGPT ERROR"


def gemini(prompt):
    GOOGLE_API_KEY='AIzaSyDVQRVLHUwu4nrAbrl6inun24y1Q4gp4rc'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    generation_config = {
    "temperature": 1.4
}
    response = model.generate_content(prompt)#, generation_config=generation_config)
    #response = model.generate_content([prompt])
    return response.text 
 
def gemini_3images_request(prompt, image_url1,image_url2,image_url3,image_url4,image_url5):
    GOOGLE_API_KEY='AIzaSyDDmfx3iQCjCzf4vP-b4qO_XYVnaQzYOgY'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([prompt,image_url1,image_url2,image_url3,image_url4,image_url5])
    return response.text

import os
def GPT4o_3images_request(prompt, image_url1, image_url2, image_url3, image_url4, image_url5 ):#
    try:
        client = os.getenv("OPENAI_API_KEY", "")
        chat_completion = client.chat.completions.create(
              model="gpt-4o-mini-2024-07-18",#"gpt-4o-mini-2024-07-18",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url","image_url": {"url": image_url1,},},
                    {"type": "image_url","image_url": {"url": image_url2,},},
                    {"type": "image_url","image_url": {"url": image_url3,},},
                    {"type": "image_url","image_url": {"url": image_url4,},},
                    {"type": "image_url","image_url": {"url": image_url5,},},
                  ],
                }
              ],
              #max_tokens=300,
           # temperature=0.5,
            )
        return chat_completion.choices[0].message.content

    except:
        print("ChatGPT ERROR")
        return "ChatGPT ERROR"
    
    
def ChatGPT_request(prompt):
    try:
        client = OpenAI( api_key = openai_api_key )#gpt-3.5-turbo
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18", messages=[{"role" : "user", "content": prompt}],
             #temperature=0.5,
        )
       # print(completion)
        return completion.choices[0].message.content
    except:
        print("ChatGPT ERROR!")
        return "ChatGPT ERROR"

def liama3_request(prompt):
    try:
        openai = OpenAI(
    api_key="3YLqqmXgWY0igz6oLObgSRe7hANhpu4G",
    base_url="https://api.deepinfra.com/v1/openai",
)

        chat_completion = openai.chat.completions.create(
    model="meta-llama/Meta-Llama-3-70B-Instruct",
    messages=[{"role": "user", "content": prompt}],
)
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"ChatGPT ERROR! liama3_request API调用失败: {str(e)}")
        return "ChatGPT ERROR"
        
def deepseek3v(prompt):
   # client = OpenAI(api_key="sk-5db9f88610024e958eb224fb160e718e", base_url="https://api.deepseek.com")
    client = OpenAI(
    api_key="euYxF1xblcpXY6abm6rmDHLfWdMlprnH",
    base_url="https://api.deepinfra.com/v1/openai",
)

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",#"deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    print(response)
    return response.choices[0].message.content
    
def deepseek3v_3image(prompt, image_url1, image_url2, image_url3, image_url4, image_url5):
    #client = OpenAI(api_key="sk-9153795d09cd41beba5dfbe702d584ce", base_url="https://api.deepseek.com")
    client = OpenAI(
    api_key="euYxF1xblcpXY6abm6rmDHLfWdMlprnH",
    base_url="https://api.deepinfra.com/v1/openai",
)
    content = f"{prompt}\nImage: {image_url1}\nImage: {image_url2}\nImage: {image_url3}\nImage: {image_url4}\nImage: {image_url5}"
    messages = [
        {"role": "user", "content": content},
    ]
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",#"deepseek-chat",
        messages=messages,
        stream=False
    )
    print(response)
    return response.choices[0].message.content
    
@timeout(50)
def send_request(prompt):
    curr_gpt_response = ChatGPT_request(prompt).strip()
    return curr_gpt_response


def ChatGPT_3images_generate_response(
    person_id,
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt +="\n   - Provided stock information visualizations.\n"
    prompt = '"""\n' + prompt + '\n"""\n'
    prompt += (
        f"Output the response to the prompt above in json. {special_instruction}\n"
    )
    prompt += "Please only provide the response in the following format:\n"
    prompt += '{"output": "' + str(example_output) + '"}'
    
    if verbose:
        print("CHAT GPT PROMPT")
        print(prompt)
    # eventlet.monkey_patch()

    for i in range(repeat):
        try:
            url1="stock_A_price.jpg"
            url2="stock_B_price.jpg"
            url3="stock_C_price.jpg"
            url4="plot_order.jpg"
            url5="plot_person{}_order.jpg".format(person_id)
            url1=trans_url(url1)
            url2=trans_url(url2)
            url3=trans_url(url3)
            url4=trans_url(url4)
            url5=trans_url(url5)
            
            curr_gpt_response=qwenvl_vision(prompt, url1, url2, url3, url4, url5).strip()
                
            #curr_gpt_response = liama3_request(prompt).strip()
            curr_gpt_response = re.sub(r'\s{3,}', '\n', curr_gpt_response).replace("\n","\\n")
            curr_gpt_response = curr_gpt_response.replace('(', '').replace(')', '')
            curr_gpt_response = curr_gpt_response.replace('[', '').replace(']', '')
            begin_index=curr_gpt_response.find("{")+1
            end_index = curr_gpt_response.rfind("}")
            curr_gpt_response = curr_gpt_response[begin_index:end_index]
            curr_gpt_response = curr_gpt_response.strip("\\n") 
            curr_gpt_response='{'+curr_gpt_response+'}'
            curr_gpt_response = curr_gpt_response.replace('(\n\\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('(\\n\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('(\\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('\\n\\n', '\\n').replace('\\n\\n)', '\\n')
            curr_gpt_response = curr_gpt_response.replace('(', '').replace(')', '')
            curr_gpt_response = curr_gpt_response.replace('(\n\\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('(\\n\n', '').replace('\\n)', '')
            print(curr_gpt_response)
            curr_gpt_response = json.loads(curr_gpt_response)["output"]

            if verbose:
                print("---GPT Response---")
                print(curr_gpt_response)
                print("---end of GPT Response---")
            #print("func_validate",func_validate(curr_gpt_response, prompt=prompt))
            if func_validate(curr_gpt_response, prompt=prompt):
                return func_clean_up(curr_gpt_response, prompt=prompt)

            if verbose:
                print("---- repeat count: \n", i, curr_gpt_response)
                print(curr_gpt_response)
        except Exception as e:
            print(f"GPT connection error: {str(e)}")
            pass
    return False


def ChatGPT_safe_generate_response(
    person_id,
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt = '"""\n' + prompt + '\n"""\n'
    prompt += (
        f"Output the response to the prompt above in json. {special_instruction}\n"
    )
    prompt += "Please only provide the response in the following format:\n"
    prompt += '{"output": "' + str(example_output) + '"}'
    
    if verbose:
        print("CHAT GPT PROMPT")
        print(prompt)
    # eventlet.monkey_patch()

    for i in range(repeat):
        try:
            if person_id in [1,5,7,9,11]:
                print("liama3_request",person_id)
                curr_gpt_response = liama3_request(prompt).strip()
            else:
                print("qwenvl",person_id)
                curr_gpt_response = qwenvl(prompt).strip()
                
            
            #if person_id in [0,1]:
             #   curr_gpt_response = gemini(prompt).strip()
            #else:
             #   curr_gpt_response = liama3_request(prompt).strip()
           # curr_gpt_response = gemini(prompt).strip()
            #curr_gpt_response = gemini_3images_request(prompt,sample_file_1,sample_file_2).strip()
           # curr_gpt_response = GPT4o_3images_request(prompt,url1,url2).strip()
            #curr_gpt_response = qwen_3images_request(prompt,url1,url2).strip()
            curr_gpt_response = qwenvl(prompt).strip()
           # curr_gpt_response = ChatGPT_request(prompt).strip()#.replace("\n","")
           # curr_gpt_response = liama3_request(prompt).strip()
            #curr_gpt_response = deepseek3v(prompt).strip()
            curr_gpt_response = re.sub(r'\s{3,}', '\n', curr_gpt_response).replace("\n","\\n")
            curr_gpt_response = curr_gpt_response.replace('(', '').replace(')', '')
            curr_gpt_response = curr_gpt_response.replace('[', '').replace(']', '')
            begin_index=curr_gpt_response.find("{")+1
            end_index = curr_gpt_response.rfind("}")
            curr_gpt_response = curr_gpt_response[begin_index:end_index]
            curr_gpt_response = curr_gpt_response.strip("\\n") 
            curr_gpt_response='{'+curr_gpt_response+'}'
            curr_gpt_response = curr_gpt_response.replace('(\n\\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('(\\n\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('(\\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('\\n\\n', '\\n').replace('\\n\\n)', '\\n')
            curr_gpt_response = curr_gpt_response.replace('(', '').replace(')', '')
            curr_gpt_response = curr_gpt_response.replace('(\n\\n', '').replace('\\n)', '')
            curr_gpt_response = curr_gpt_response.replace('(\\n\n', '').replace('\\n)', '')
            print(curr_gpt_response)
            curr_gpt_response = json.loads(curr_gpt_response)["output"]
            
        
            if verbose:
                print("---GPT Response---")
                print(curr_gpt_response)
                print("---end of GPT Response---")
            #print("func_validate",func_validate(curr_gpt_response, prompt=prompt))
            if func_validate(curr_gpt_response, prompt=prompt):
                return func_clean_up(curr_gpt_response, prompt=prompt)
        
            if verbose:
                print("---- repeat count: \n", i, curr_gpt_response)
                print(curr_gpt_response)
        except Exception as e:
            print(f"GPT connection error: {str(e)}")
            pass
    return False


def ChatGPT_safe_generate_response_OLD(
    prompt,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    if verbose:
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat):
        try:
            curr_gpt_response = ChatGPT_request(prompt).strip()
            if func_validate(curr_gpt_response, prompt=prompt):
                return func_clean_up(curr_gpt_response, prompt=prompt)
            if verbose:
                print(f"---- repeat count: {i}")
                print(curr_gpt_response)
                print("~~~~")

        except:
            pass
    print("FAIL SAFE TRIGGERED")
    return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================


def GPT_request(prompt, gpt_parameter):
    """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
    temp_sleep()
    try:
        response = openai.Completion.create(
            model=gpt_parameter["engine"],
            prompt=prompt,
            temperature=gpt_parameter["temperature"],
            max_tokens=gpt_parameter["max_tokens"],
            top_p=gpt_parameter["top_p"],
            frequency_penalty=gpt_parameter["frequency_penalty"],
            presence_penalty=gpt_parameter["presence_penalty"],
            stream=gpt_parameter["stream"],
            stop=gpt_parameter["stop"],
        )
        return response.choices[0].text
    except:
        print("TOKEN LIMIT EXCEEDED")
        return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file):
    """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
    if type(curr_input) == type("string"):
        curr_input = [curr_input]
    curr_input = [str(round_two_decimal(i)) for i in curr_input]

    f = open(prompt_lib_file, "r")
    prompt = f.read()
    f.close()
    for count, i in enumerate(curr_input):
        prompt = prompt.replace(f"!<INPUT {count}>!", i)
    if "<commentblockmarker>###</commentblockmarker>" in prompt:
        prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
    return prompt.strip()


def safe_generate_response(
    prompt,
    gpt_parameter,
    repeat=5,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    if verbose:
        print(prompt)

    for i in range(repeat):
        curr_gpt_response = GPT_request(prompt, gpt_parameter)
        if func_validate(curr_gpt_response, prompt=prompt):
            return func_clean_up(curr_gpt_response, prompt=prompt)
        if verbose:
            print("---- repeat count: ", i, curr_gpt_response)
            print(curr_gpt_response)
            print("~~~~")
    return fail_safe_response


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    if not text:
        text = "this is blank"
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]


if __name__ == "__main__":
    gpt_parameter = {
        "engine": "text-davinci-003",
        "max_tokens": 50,
        "temperature": 0,
        "top_p": 1,
        "stream": False,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ['"'],
    }
    curr_input = ["driving to a friend's house"]
    prompt_lib_file = "prompt_template/test_prompt_July5.txt"
    prompt = generate_prompt(curr_input, prompt_lib_file)

    def __func_validate(gpt_response):
        if len(gpt_response.strip()) <= 1:
            return False
        if len(gpt_response.strip().split(" ")) > 1:
            return False
        return True

    def __func_clean_up(gpt_response):
        cleaned_response = gpt_response.strip()
        return cleaned_response

    output = safe_generate_response(
        prompt, gpt_parameter, 5, "rest", __func_validate, __func_clean_up, True
    )

    print(output)
