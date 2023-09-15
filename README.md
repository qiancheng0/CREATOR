# CREATOR

We release here the code for most of the main experiments in paper *CREATOR: Tool Creation for Disentangling Abstract and Concrete Reasoning of Large Language Models*, including the code of our framework and various baselines. We also release two new datasets: Creation Challenge and Tool Transfer here. Please refer to our paper for more details.

## Preparation

Please first install the packages needed for the experiment through

```shell
pip install -r requirements.txt
```

We will use the API from OpenAI to complete our experiment, so please put your OpenAI API key in file `keys.txt` before the experiment. If you have more than one API key, please put one key in a line (our code supports the polling of keys).

In the tool use setting, we will also use the WolframAlpha API. Please put the WolframAlpha API key at the beginning of `utils.py`, replacing the `{Wolfram_Key}`.

All the datasets, including MATH, TabMWP, Creation Challenge and Tool Transfer dataset are provided in advance in corresponding folders.

## Main Experiments

All the codes are under the root folder. In the main experiment, we utilize three datasets, including two existing benchmarks, MATH and TabMWP, and one new dataset, Creation Challenge. We construct a folder for the experiment on each dataset. Each folder contains the dataset prepared in advance, and the prompt library that we will utilize to inspire the LLM's ability.

### CREATOR setting

Please run `generate_CREATOR.py` for the CREATOR framework setting. In the code, please first choose one task from MATH, TabMWP and Creation Challenge. Specially, for Creation Challenge, you can choose from "normal", "utility hint" and "all hint" to reproduce our experiment on the role of hints for CREATOR framework.

The meaning of other hyper-parameters are illustrated below.

```python
# The index of the OpenAI API key that we start to utilize
start_key = 0
# The temperature of the LLM we apply in generation
temperature = 0.3
# The path to the prompt file
prompt_creation = f"{task}/prompt_lib/prompt_CREATOR_creation.md"
prompt_decision = f"{task}/prompt_lib/prompt_CREATOR_decision.md"
prompt_rectification = f"{task}/prompt_lib/prompt_rectification.md"
# The file where we conduct execution
code_file = "code_exec/tmp0"
# The LLM we use, we also provide Text-Davinci-003 API in utils
gen_func = chat_api
# The upper bound of the rounds of rectification
rectify_limit = 0
```

You can also change the saving path. After a successful execution, the results will be recorded in the `results` folder for each dataset.

### ToolCreate (Whole) setting

We do not disentangle the tool creation and decision in this stage. Please run `generate_toolcreate_whole.py` for this setting. Besides dataset, different modes can also be chosen under this setting. Other hyper-parameters keep the same meaning with the CREATOR setting.

### CoT and PoT setting

Please run `generate_cot.py` and `generate_pot.py` for these two settings respectively. Under the chain-of-thought (CoT) and program-of-thought (PoT), we do not have hint modes any more. You can choose which dataset to conduct the experiments. Other hyper-parameters keep the same meaning with the CREATOR setting.

### Tool Use setting

Please run `generate_tooluse.py` to conduct experiments under tool-using setting. We leverage WolframAlpha as external API for the LLM to utilize. Under this setting, we test on MATH and TabMWP, and do not apply hint modes. Other hyper-parameters keep the same meaning with the CREATOR setting.

## Tool Transfer

We also provide the codes and dataset about tool transfer in the discussion part of our paper. Same as the main experiment, we create a folder specifically for this experiment, and prepare the prompts and dataset in advanced.

Please run `test_transfer.py` to reproduce our experiments. There are two modes that could be chosen, including "normal" and "hint". The meaning of all the other hyper-parameters are same as the CREATOR setting in our main experiment.

## Acknowledgement