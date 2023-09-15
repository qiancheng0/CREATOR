import json
import re
from utils import process_code, chat_api

# ================================ #
task = "Tooltransfer"
# Choose the mode from "normal" and "hint"
mode = "normal"
# ================================ #
start_key = 0
temperature = 0.3
prompt1 = open(f"{task}/prompt_lib/prompt_CREATOR_creation.md", "r").read().strip()
prompt2 = open(f"{task}/prompt_lib/prompt_CREATOR_decision.md", "r").read().strip()
prompt_t = open(f"{task}/prompt_lib/prompt_tool_transfer.md", "r").read().strip()
err_prompt = open(f"{task}/prompt_lib/prompt_rectification.md", "r").read().strip()
save_file = f"{task}/results/results_tooltransfer_test.md"
code_file = "code_exec/tmp0"
gen_func = chat_api
sys_msg = "You are a helpful assistant in answering questions with tools."
# ================================ #
if mode == "hint":
    prompt1 = open("ToolTransfer/prompt_lib/prompt_CREATOR_creation_hint.md", "r").read().strip()
# ================================ #

bad_exec = 0
good_ans = 0
bad_ans = 0
good_transfer = 0
good_transfer_time = 0
all_transfer_data = []
all_separate_correct = []

f = open(save_file, "w")
f.close()

f = open("ToolTransfer/dataset/transfer_300.jsonl", "r")
lines = f.readlines()
f.close()

for line in lines:
    print("======================new question begin========================")
    data = json.loads(line)
    # ========= hints ======== (can apply / not apply based on the mode chosen)
    hints = f"create a tool based on the following introduction:\n{data['intro'].strip()}"
    # ========================
    env = prompt1
    
    separate_correct = 0
    useful_tools = []
    
    print("Answering problems one by one...")
    for i in range(3):
        print("in problem", i)
        answer = data[f"ans{i+1}"]
        question = data[f"scn{i+1}"]
        env = env.replace("===problem===", question).replace("===hints===", hints)
        res = gen_func(env, start_key, sys_msg, temperature=temperature)

        try:
            tool_code = res.split("```python")[1].split("```")[0].strip()
            
            env_cont = prompt2
            env_cont = env_cont.replace("===problem===", question).replace("===hints===", hints).replace("===tool===", tool_code)
            res_cont = gen_func(env_cont, start_key, sys_msg, temperature=temperature)
            call_code = res_cont.split("```python")[1].split("```")[0].strip()
            
            response = "```python\n" + tool_code + "\n\n" + call_code + "\n```"
            
            if_succ, info = process_code(response, code_file)
            if not if_succ:
                raise Exception(info)
            else:
                print("~~~ Runing successfully ~~~")
                model_ans = re.findall(r'-?\d+\.?\d*', info)
                model_ans = [float(ans) for ans in model_ans]
                correct_flag = False
                for ans in model_ans:
                    if round(ans,2) == round(answer,2):
                        print("~~~ Correct Answer ~~~")
                        correct_flag = True
                        f = open(save_file, "a")
                        f.write("### Problem\n" + question.strip() + "\n### Response\n" + response.strip() + "\n\n### Return Info\n" + info.strip() + f"\n\nCorrect Answer!\nThe correct answer should be {answer}")
                        f.write("\n\n=============================split line=============================\n\n")
                        f.close()
                        good_ans += 1
                        separate_correct += 1
                        useful_tools.append({"tool": "```python\n" + tool_code + "\n```", "num": i})
                        break
                if not correct_flag:
                    print("!!! Wrong Answer !!!")
                    f = open(save_file, "a")
                    f.write("### Problem\n" + question.strip() + "\n### Response\n" + response.strip() + "\n\n### Return Info\n" + info.strip() + f"\n\nWrong Answer!\nThe correct answer should be {answer}")
                    f.write("\n\n=============================split line=============================\n\n")
                    f.close()
                    bad_ans += 1
        except Exception as e:
            bad_exec += 1
            print("!!! Bad Execution !!!")
            f = open(save_file, "a")
            f.write("Met Unknown Error! Stop!")
            f.write("\n\n=============================split line=============================\n\n")
            f.close()
            
        if i == 2:
            f = open(save_file, "a")
            f.write(f"Separate Correct: {separate_correct}")
            f.write("\n\n=============================split line=============================\n\n")
            f.close()
    
    f = open(save_file, "a")
    f.write(f"Separate Correct: {separate_correct}")
    f.write("\n\n=============================split line=============================\n\n")
    f.write("\n\n=============================begin transfer test=============================\n\n")
    f.close()
    
    all_separate_correct.append(separate_correct)
    print("Bad Execution: ", bad_exec, "Good Answer: ", good_ans, "Bad Answer: ", bad_ans)
    print("======================Test transfer begin========================")
    print(f"Begin Test Useful Tools, total number: {len(useful_tools)}")
    
    success_rate = []
    for tool in useful_tools:
        success_transfer = 0
        for i in range(3):
            if i == tool["num"]:
                continue
            answer = data[f"ans{i+1}"]
            question = data[f"scn{i+1}"]
            
            env_cont = prompt_t
            tool_code = tool["tool"]
            env_cont = env_cont.replace("===problem===", question).replace("===hints===", hints).replace("===tool===", tool_code)
            res_cont = gen_func(env_cont, start_key, sys_msg, temperature=temperature)
            try:    
                call_code = res_cont.split("```python")[1].split("```")[0].strip()
                tool_code = tool_code.split("```python")[1].split("```")[0].strip()
                
                response = "```python\n" + tool_code + "\n\n" + call_code + "\n```"
                
                if_succ, info = process_code(response, code_file)
                if not if_succ:
                    raise Exception(info)
                else:
                    print("~~~ Runing successfully ~~~")
                    model_ans = re.findall(r'-?\d+\.?\d*', info)
                    model_ans = [float(ans) for ans in model_ans]
                    correct_flag = False
                    for ans in model_ans:
                        if round(ans,2) == round(answer,2):
                            print("~~~ Transfer Correct Answer ~~~")
                            correct_flag = True
                            f = open(save_file, "a")
                            f.write("### Problem\n" + question.strip() + "\n### Response\n" + response.strip() + "\n\n### Return Info\n" + info.strip() + f"\n\nCorrect Transfer Answer!\nThe correct answer should be {answer}")
                            f.write("\n\n=============================split line=============================\n\n")
                            f.close()
                            success_transfer += 1
                            break
                    if not correct_flag:
                        print("!!! Wrong Answer !!!")
                        f = open(save_file, "a")
                        f.write("### Problem\n" + question.strip() + "\n### Response\n" + response.strip() + "\n\n### Return Info\n" + info.strip() + f"\n\nWrong Transfer Answer!\nThe correct answer should be {answer}")
                        f.write("\n\n=============================split line=============================\n\n")
                        f.close()
            except:
                print("!!! Transfer Bad Execution !!!")
                f = open(save_file, "a")
                f.write("Met Unknown Error! Stop! Bad Transfer Parsing!")
                f.write("\n\n=============================split line=============================\n\n")
                f.close()
        
        success_rate.append(success_transfer)

    success_transfer = max(success_rate) if len(success_rate) > 0 else 0
    if len(success_rate) > 0:
        good_transfer_time += 1
    # originally self success!
    good_transfer += (success_transfer + 1)
    all_transfer_data.append(success_rate)
    
    f = open(save_file, "a")
    f.write("\n\n============================end transfer test=============================\n\n")
    f.close()

f = open(save_file, "a")
f.write(f"Good Answer: {good_ans}\nBad Answer: {bad_ans}\nBad Execution: {bad_exec}\n")
f.write(f"Good Transfer: {good_transfer}\nGood Transfer Time: {good_transfer_time}\n")
f.write(f"Transfer Data:\n{str(all_transfer_data)}\n")
f.write(f"Separate Correct:\n{str(all_separate_correct)}\n")
f.close()