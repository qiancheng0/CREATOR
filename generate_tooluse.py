import json
import re
from utils import wolfram, web_chat
from grader import grade_answer

# ================================ #
# Choose from "MATH", "TabMWP"
task = "MATH"
if task == "MATH":
    fields = ["algebra", "counting_and_probability", "geometry", "intermediate_algebra", "number_theory", "prealgebra", "precalculus"]
    sys_msg = "You are a helpful assistant in answering math competition problems."
elif task == "TabMWP":
    fields = ["tabmwp"]
    sys_msg = "You are a helpful assistant in answering questions with tabular contents."
else:
    raise Exception("Wrong task name!")
# ================================ #     
start_key = 0
temperature = 0.3
prompt_file = f"{task}/prompt_lib/prompt_tooluse_part1.md"
prompt2_file = f"{task}/prompt_lib/prompt_tooluse_part2.md"
gen_func = web_chat
# ================================ #

for field in fields:
    save_file = f"{task}/results/results_{field}_tooluse_temp{temperature}.md"
    open(save_file, "w").close()
    
    f = open(prompt_file, "r")
    prompt = f.read().strip()
    f.close()

    f = open(prompt2_file, "r")
    prompt_cont = f.read().strip()
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
    
    for line in lines:
        try:
            correct_ans = line["answer"]
            env = prompt.replace("===qst===", line["question"])
            if task == "TabMWP":
                env = env.replace("===table===", line["table"])
            response = gen_func(env, sys_msg, temperature=temperature)
            
            use_wolfram = True
            try:
                st = response.index("WOLFRAM:") + len("WOLFRAM:")
                call = response[st:].strip()
            except:
                print("!!! Error when parsing model output part 1 !!!")
                use_wolfram = False
                
            if use_wolfram:
                wolfram_return = wolfram(call).strip()
            
            if not use_wolfram or wolfram_return == "Error":
                print("!!! Error when calling Wolfram API !!!")
                wolfram_return = "No available information from WalframAlpha.\nPut your final numerical answer after 'Final Answer:'"
            
            if len(wolfram_return) > 1500:
                wolfram_return = wolfram_return[:1500]
            
            env_cont = prompt_cont.replace("===qst===", line["question"]).replace("===res===", response).replace("===wol===", wolfram_return)
            if task == "TabMWP":
                env_cont = env_cont.replace("===table===", line["table"])
            response_cont = gen_func(env_cont, sys_msg, temperature=temperature)
            
            try:
                st = response_cont.index("Final Answer:") + len("Final Answer:")
                generated_ans = response_cont[st:].strip()
            except:
                print("!!! Error when parsing model output part 2 !!!")
                f = open(save_file, "a")
                if task == "TabMWP":
                    f.write("### Table\n" + line["table"] + "\n")
                f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + "\n### Wolfram Return\n" + wolfram_return.strip() + "\n### Response Continue\n" + response_cont + f"\n\nError when parsing model output part 2!\nThe correct answer should be {correct_ans}")
                f.write("\n\n=============================split case=============================\n\n")
                f.close()
                exec_err += 1
                continue
            
            model_ans = re.findall(r'-?\d+\.?\d*', generated_ans)
            model_ans = [float(ans) for ans in model_ans]
            correct_flag = False
            for ans in model_ans:
                if grade_answer(str(ans), str(correct_ans)):
                    print("~~~ Correct Answer ~~~")
                    correct_flag = True
                    f = open(save_file, "a")
                    if task == "TabMWP":
                        f.write("### Table\n" + line["table"] + "\n")
                    f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + "\n### Wolfram Return\n" + wolfram_return.strip() + "\n### Response Continue\n" + response_cont + f"\n\nCorrect Answer!\nThe correct answer should be {correct_ans}")
                    f.write("\n\n=============================split case=============================\n\n")
                    f.close()
                    correct += 1
                    break

            if not correct_flag:
                print("!!! Wrong Answer !!!")
                f = open(save_file, "a")
                if task == "TabMWP":
                    f.write("### Table\n" + line["table"] + "\n")
                f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + "\n### Wolfram Return\n" + wolfram_return.strip() + "\n### Response Continue\n" + response_cont + f"\n\nWrong Answer!\nThe correct answer should be {correct_ans}")
                f.write("\n\n=============================split case=============================\n\n")
                f.close()
                wrong += 1
                
            print("Correct:", correct, "Wrong:", wrong, "Exec Error:", exec_err)
        
        except:
            exec_err += 1

    f = open(save_file, "a")
    total_num = correct + wrong + exec_err
    f.write("Correct: " + str(correct) + " " + str(correct/total_num * 100) + "\nWrong: " + str(wrong) + " " + str(wrong/total_num * 100) + "\nExec Error: " + str(exec_err) + " " + str(exec_err/total_num * 100) + "\n\n")
    f.close()
