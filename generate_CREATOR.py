import json
import re
from utils import process_code, chat_api, check_code_valid

# ================================ #
# Choose from "MATH", "TabMWP", "Creation"
task = "Creation"
if task == "MATH":
    fields = ["algebra", "counting_and_probability", "geometry", "intermediate_algebra", "number_theory", "prealgebra", "precalculus"]
    sys_msg = "You are a helpful assistant in answering math competition problems."
elif task == "TabMWP":
    fields = ["tabmwp"]
    sys_msg = "You are a helpful assistant in answering questions with tabular contents."
elif task == "Creation":
    fields = ["CC"]
    sys_msg = "You are a helpful assistant in answering newly defined questions."
    # For Creation Challenge, you can choose from "normal", "utilityhint" and "allhint"
    mode = "allhint"
else:
    raise Exception("Wrong task name!")
# ================================ #     
start_key = 0
temperature = 0.3
prompt_creation = f"{task}/prompt_lib/prompt_CREATOR_creation.md"
prompt_decision = f"{task}/prompt_lib/prompt_CREATOR_decision.md"
prompt_rectification = f"{task}/prompt_lib/prompt_rectification.md"
code_file = "code_exec/tmp0"
gen_func = chat_api
rectify_limit = 0
# ================================ #
if mode == "utilityhint":
    prompt_creation = f"{task}/prompt_lib/prompt_CREATOR_creation_utilityhint.md"
    prompt_decision = f"{task}/prompt_lib/prompt_CREATOR_decision_utilityhint.md"
if mode == "allhint":
    prompt_creation = f"{task}/prompt_lib/prompt_CREATOR_creation_allhint.md"
    prompt_decision = f"{task}/prompt_lib/prompt_CREATOR_decision_allhint.md"
# ================================ #

for field in fields:
    save_file = f"{task}/results/results_{field}_CREATOR.md"
    f = open(save_file, "w")
    f.close()
    
    f = open(prompt_creation, "r")
    prompt1 = f.read().strip()
    f.close
    
    f = open(prompt_decision, "r")
    prompt2 = f.read().strip()
    f.close

    f = open(prompt_rectification, "r")
    err_prompt = f.read().strip()
    f.close()

    lines = []
    f = open(f"{task}/dataset/{field}.jsonl", "r")
    all_lines = f.readlines()
    f.close()
    
    for line in all_lines:
        lines.append(json.loads(line.strip()))
    
    correct = 0
    wrong = 0
    exec_err = 0
    one_time_pass = 0
    
    for line in lines:
        try:
            correct_ans = line["answer"]
            
            env1 = prompt1.replace("===qst===", line["question"])
            if task == "TabMWP":
                env1 = env1.replace("===table===", line["table"])
            if task == "Creation":
                env1 = env1.replace("===constants===", line["constant"].strip())
                if mode == "utilityhint":
                    hints = "You might use the following hints about what tool to create:\n"
                    hints += "Utility:\n" + line["utility"].strip() + "\n"
                    env1 = env1.replace("===hints===", hints.strip())
                if mode == "allhint":
                    hints = "You might use the following hints about what tool to create\n"
                    hints += "Utility:\n" + line["utility"].strip() + "\n"
                    hints += "Args:\n" + line["args"].strip() + "\n"
                    hints += "Return:\n" + line["return"].strip() + "\n"
                    env1 = env1.replace("===hints===", hints.strip())
            response1 = gen_func(env1, start_key, sys_msg, temperature=temperature)
            
            tool_time = 0
            while tool_time < 3:
                # check the validity of the tool format
                if (check_code_valid(response1, code_file)):
                    break
                print("!!! Wrong tool format generated !!!")
                response1 = gen_func(env1, start_key, sys_msg, temperature=temperature)
                tool_time += 1
                
            env2 = prompt2.replace("===qst===", line["question"]).replace("===tool===", response1)
            if task == "TabMWP":
                env2 = env2.replace("===table===", line["table"])
            if task == "Creation":
                env2 = env2.replace("===constants===", line["constant"].strip())
                if mode == "utilityhint" or mode == "allhint":
                    env2 = env2.replace("===hints===", hints.strip())
            response2 = gen_func(env2, start_key, sys_msg, temperature=temperature)
            
            # To further enhance the validity of the tool format
            if "```" not in response1:
                response1 = "```python\n" + response1 + "\n```"
            if "```" not in response2:
                response2 = "```python\n" + response2 + "\n```"
            response = response1 + "\n" + response2
            
            time = 0
            while True:
                time += 1
                if_succ, info = process_code(response, code_file)
                
                if not if_succ and time <= rectify_limit:
                    print(f"!!! Error in execution, time {time} !!!")
                    rectify_env = err_prompt.replace("===qst===", line["question"]).replace("===ori===", response).replace("===err===", info)
                    if task == "TabMWP":
                        rectify_env = rectify_env.replace("===table===", line["table"])
                    if task == "Creation":
                        rectify_env = rectify_env.replace("===constants===", line["constant"].strip())
                    response = gen_func(rectify_env, start_key, sys_msg, temperature=temperature)
                    if "```" not in response:
                        response = "```python\n" + response + "\n```"
                    continue
                
                elif not if_succ and time > rectify_limit:
                    print("!!! Times of execution error exceeds limit, skip !!!")
                    f = open(save_file, "a")
                    if task == "TabMWP":
                        f.write("### Table\n" + line["table"] + "\n")
                    f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + "\n\n### Back info:\n" + info.strip() + f"\n\nExceed rectify limit!\nThe correct answer should be {correct_ans}")
                    f.write("\n\n=============================split case=============================\n\n")
                    f.close()
                    exec_err += 1
                    break
                
                elif if_succ:
                    print("~~~ Runing successfully ~~~")
                    model_ans = re.findall(r'-?\d+\.?\d*', info)
                    model_ans = [float(ans) for ans in model_ans]
                    correct_flag = False
                    for ans in model_ans:
                        if round(ans,2) == round(correct_ans,2):
                            print("~~~ Correct Answer ~~~")
                            correct_flag = True
                            f = open(save_file, "a")
                            if task == "TabMWP":
                                f.write("### Table\n" + line["table"] + "\n")
                            f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + "\n\n### Back info:\n" + info.strip() + f"\n\nCorrect Answer!\nThe correct answer should be {correct_ans}")
                            f.write("\n\n=============================split case=============================\n\n")
                            f.close()
                            correct += 1
                            if time == 1:
                                one_time_pass += 1
                                
                    if not correct_flag:
                        print("!!! Wrong Answer !!!")
                        f = open(save_file, "a")
                        if task == "TabMWP":
                            f.write("### Table\n" + line["table"] + "\n")
                        f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + "\n\n### Back info:\n" + info.strip() + f"\n\nWrong Answer!\nThe correct answer should be {correct_ans}")
                        f.write("\n\n=============================split case=============================\n\n")
                        f.close()
                        wrong += 1
                    break
                # T_T you shouldn't reach here
                break
            
            print("Correct:", correct, "Wrong:", wrong, "Exec Error:", exec_err, "One Time Pass:", one_time_pass)
        
        except:
            exec_err += 1
        
    f = open(save_file, "a")
    total_num = correct + wrong + exec_err
    f.write("Correct: " + str(correct) + " " + str(correct/total_num * 100) + "\nWrong: " + str(wrong) + " " + str(wrong/total_num * 100) + "\nExec Error: " + str(exec_err) + " " + str(exec_err/total_num * 100) + "\nOne Time Pass: " + str(one_time_pass) + "\nTotal: " + str(total_num) + "\n\n")
    f.close()
