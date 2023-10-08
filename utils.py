import openai
import subprocess
import requests
import xmltodict

WolframAlpha_Key = "{Wolfram_Key}"
key_pool = []
f = open("keys.txt", "r")
lines = f.readlines()
f.close()

for line in lines:
    key_pool.append(line.strip())
key_num = len(key_pool)

# Use ChatGPT API provided by OpenAI
def web_chat(usr_msg, system_msg, temperature=0.3):
    try_num = 0
    while try_num < key_num:
        try_num += 1
        try:
            openai.api_key = key_pool[try_num % key_num]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": usr_msg},
                ],
                temperature=temperature,
                max_tokens=1024,
            )
            return response["choices"][0]["message"]["content"].strip()
        except:
            pass
    raise Exception("API key exhausted")


# Use Text-Davinci-003 API provided by OpenAI
def davinci_api(message, current_key, temperature=0.3):
    # print("~~~ In Davinci ~~~")
    try_num = 0
    while try_num < key_num:
        try_num += 1
        try:
            openai.api_key = key_pool[(try_num+current_key) % key_num]
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message,
                temperature=temperature,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response["choices"][0]["text"].strip()
        except:
            pass
    raise Exception("API key exhausted")


# Execute the code in PoT method / during Execution Stage
def process_code(code, code_file="code_exec/tmp0"):
    try:
        code_pieces = []
        while "```python" in code:
            st_idx = code.index("```python") + 10
            end_idx = code.index("```", st_idx)
            code_pieces.append(code[st_idx:end_idx].strip())
            code = code[end_idx+3:].strip()
        if len(code_pieces) == 0:
            return False, "No code found"
        else:
            code = "\n\n".join(code_pieces)
            f = open(f"{code_file}.py", "w")
            f.write(code)
            f.close()
            result = subprocess.run(
                ['python', f'{code_file}.py'], capture_output=True, check=False, text=True, timeout=1)
            if result.returncode != 0:
                error_msg = result.stderr.strip()
                msgs = error_msg.split("\n")
                new_msgs = []
                want_next = False
                for m in msgs:
                    if "Traceback" in m:
                        new_msgs.append(m)
                    elif m == msgs[-1]:
                        new_msgs.append(m)
                    elif code_file in m:
                        st = m.index('"/') + 1
                        ed = m.index(f'/{code_file}.py') + 1
                        clr = m[st:ed]
                        m = m.replace(clr, "")
                        new_msgs.append(m)
                        want_next = True
                    elif want_next:
                        new_msgs.append(m)
                        want_next = False
                error_msg = "\n".join(new_msgs)
                return False, error_msg.strip()
            else:
                output = result.stdout
                # print("Code Run successfully!")
                return True, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Timeout detected in running subprocess"
    except Exception as e:
        return False, "Unknown error in running subprocess"


# Check the validity of the code
def check_code_valid(code, code_file="code_exec/tmp0"):
    try:
        code_pieces = []
        while "```python" in code:
            st_idx = code.index("```python") + 10
            end_idx = code.index("```", st_idx)
            code_pieces.append(code[st_idx:end_idx].strip())
            code = code[end_idx+3:].strip()
        if len(code_pieces) == 0:
            return False
        else:
            code = "\n\n".join(code_pieces)
            f = open(f"{code_file}.py", "w")
            f.write(code)
            f.close()
            result = subprocess.run(
                ['python', f'{code_file}.py'], check=True, timeout=1)
            if result.returncode != 0:
                return False
            return True
    except Exception as e:
        return False
    

# Call the Wolfram API under Tool Use setting
def wolfram(query):
    try:
        URL = "https://api.wolframalpha.com/v2/query"
        wolfram_id = WolframAlpha_Key
        input_qst = query.strip()
        params = {'appid': wolfram_id, "input": input_qst, "format": "plaintext"}
        response = requests.get(URL, params=params)
        json_data = xmltodict.parse(response.text)

        rets = json_data["queryresult"]['pod']

        cleaned_rets = []
        blacklist = ["@src", "@scanner", "@id", "@position", "@error", "@numsubpods", "@width", "@height", "@type", "@themes","@colorinvertable", "expressiontypes"]
                
        def filter_dict(d, blacklist):
            if isinstance(d, dict):
                return {k: filter_dict(v, blacklist) for k, v in d.items() if k not in blacklist}
            elif isinstance(d, list):
                return [filter_dict(i, blacklist) for i in d]
            else:
                return d

        for ret in rets:
            ret = filter_dict(ret, blacklist=blacklist)
            if "@title" in ret:
                if ret["@title"] == "Input" or ret["@title"] == "Result":
                    cleaned_rets.append(ret)

        return str(cleaned_rets)
    except:
        return "Error"