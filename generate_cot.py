import json
import re
from utils import chat_api

# ================================ #
# Choose from "MATH", "TabMWP", "Creation"
task = "TabMWP"
if task == "MATH":
    fields = ["algebra", "counting_and_probability", "geometry", "intermediate_algebra", "number_theory", "prealgebra", "precalculus"]
    sys_msg = "You are a helpful assistant in answering math competition problems."
elif task == "TabMWP":
    fields = ["tabmwp"]
    sys_msg = "You are a helpful assistant in answering questions with tabular contents."
elif task == "Creation":
    fields = ["CC"]
    sys_msg = "You are a helpful assistant in answering newly defined questions."
else:
    raise Exception("Wrong task name!")
# ================================ #     
start_key = 0
temperature = 0.3
prompt_file = f"{task}/prompt_lib/prompt_cot.md"
gen_func = chat_api
# ================================ #

for field in fields:
    save_file = f"{task}/results/results_{field}_cot.md"
    f = open(save_file, "w")
    f.close()
    
    f = open(prompt_file, "r")
    prompt = f.read().strip()
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
            if task == "Creation":
                env = env.replace("===constants===", line["constant"].strip())
            response = gen_func(env, start_key, sys_msg, temperature)
            
            try:
                res = response.split("Final Answer:")[-1].strip()
            except:
                print("!!! No Correct Format Answer !!!")
                f = open(save_file, "a")
                if task == "TabMWP":
                    f.write("### Table\n" + line["table"] + "\n")
                f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + f"\n\nNo answer found!\nThe correct answer should be {correct_ans}")
                f.write("\n\n=============================split case=============================\n\n")
                f.close()
                exec_err += 1
                continue
            
            have_ans = True
            model_ans = re.findall(r'-?\d+\.?\d*', res)
            if len(model_ans) == 0:
                have_ans = False
            else:
                model_ans = float(model_ans[0])
                        
            if have_ans and model_ans == correct_ans:
                print("~~~ Correct Answer ~~~")
                f = open(save_file, "a")
                if task == "TabMWP":
                    f.write("### Table\n" + line["table"] + "\n")
                f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + f"\n\nCorrect Answer!\nThe correct answer should be {correct_ans}")
                f.write("\n\n=============================split case=============================\n\n")
                f.close()
                correct += 1
            else:
                print("!!! Wrong Answer !!!")
                f = open(save_file, "a")
                if task == "TabMWP":
                    f.write("### Table\n" + line["table"] + "\n")
                f.write("### Question\n" + line["question"] + "\n### Respose\n" + response.strip() + f"\n\nWrong Answer!\nThe correct answer should be {correct_ans}")
                f.write("\n\n=============================split case=============================\n\n")
                f.close()
                wrong += 1
            print("Correct:", correct, "Wrong:", wrong, "Exec Error:", exec_err)
        except:
            exec_err += 1

    f = open(save_file, "a")
    total_num = len(lines)
    f.write("Correct: " + str(correct) + " " + str(correct/total_num * 100) + "\nWrong: " + str(wrong) + " " + str(wrong/total_num * 100) + "\nExec Error: " + str(exec_err) + " " + str(exec_err/total_num * 100) + "\n\n")
    f.close()
