import pandas as pd
from gpt4_answer_scorer import evaluate_response


df = pd.concat([
    pd.read_csv("/Users/4760393/Downloads/testing_sample_Llama-2-7b-hf_finetuned_full_dataset_untrained_model.csv"),
    pd.read_csv("/Users/4760393/Downloads/testing_sample_Llama-2-7b-hf_finetuned_full_dataset_untrained_model (1).csv"),
    pd.read_csv("/Users/4760393/Downloads/testing_sample_Llama-2-7b-hf_finetuned_full_dataset_untrained_model (2).csv")
], axis=0)

llama_responses_raw = []
llama_scores_gpt4 = []
for i, row in df.iterrows():
    gpt4_response = evaluate_response(
        problem=row["question"],
        correct_solution=row["actual responses"],
        predicted_solution=row["predicted responses"]
    )
    llama_responses_raw.append(gpt4_response[0])
    llama_scores_gpt4.append(gpt4_response[1])
df["llama_scores_gpt4"] = llama_scores_gpt4
df["llama_scores_gpt4_raw"] = llama_responses_raw
df.to_csv("llama_untrained_model_scores.csv")