from openai import OpenAI
from time import perf_counter
import pandas as pd
from transformers import AutoTokenizer
from huggingface_hub import HfApi, HfFolder
import json


client = OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = "..."
)

token = '...'
# set api for login and save token
api=HfApi(token=token)
# api.set_access_token(token)
folder = HfFolder()
folder.save_token(token)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", trust_remote_code=True)
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

test_dataset = pd.read_csv("testing_sample_Llama-2-7b-hf_finetuned_full_dataset_scored.csv")

problem_list = list(test_dataset["question"])
solution_list = list(test_dataset["actual responses"])
batch_size_for_evaluation = 4

length_ratios = [int(tokenizer(solution_list[i], return_tensors="pt")["input_ids"].shape[1]) / int(
    tokenizer(problem_list[i], return_tensors="pt")["input_ids"].shape[1]) for i in range(len(problem_list))]
mean_length_ratio = sum(length_ratios) / len(problem_list)
input_batches = [problem_list[i:(i+batch_size_for_evaluation)] for i in range(0, len(problem_list), batch_size_for_evaluation)]

predictions = []
for i, batch in enumerate(input_batches):
    print("Batch number", i)
    # Tokenize the batch of input texts
    input_ids = tokenizer(batch, return_tensors="pt", padding=True)
    # Generate text for the batch
    start_index = i * batch_size_for_evaluation
    stop_index = min(len(problem_list), (i + 1) * batch_size_for_evaluation)
    for j in range(start_index, stop_index):
        print(problem_list[j])
        t_start = perf_counter()
        completion = client.completions.create(
            model="meta-llama/Llama-2-7b-chat-hf",
            prompt=problem_list[j],
            max_tokens=int(mean_length_ratio * input_ids["input_ids"].shape[1]),
            temperature=1.0
        )
        print(perf_counter() - t_start, " seconds")
        predictions.append(completion.model_dump()['choices'][0]['text'])
    # Decode the generated output

test_dataset["llama_anyscale_api_predictions"] = predictions
print(predictions)

test_dataset.to_csv("llama_predictions_openstax_test_dataset.csv")
with open("llama_predictions_openstax_test_dataset.json", "w") as f:
    json.dump(test_dataset.to_json(orient="records"), f)
