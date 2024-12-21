from time import perf_counter
import httpx
from config import settings
from openai import OpenAI, RateLimitError
import pandas as pd
import string

httpxClient = httpx.Client(verify=False)
client = OpenAI(
    http_client=httpxClient,
    api_key=settings.OPENAI_API_KEY,
)

eval_result_list = ['FULLY ACCURATE', 'MOSTLY ACCURATE', 'PARTIALLY ACCURATE', 'MOSTLY INACCURATE', 'FULLY INACCURATE']


def evaluate_response(
    problem: str, correct_solution: str, predicted_solution: str, model_id: str = "gpt-4-0125-preview"
):
    messages = [
        {
            "role": "system",
            "content": """You are evaluating solutions to textbook problems given by a language model. 
            Given a 'PROBLEM', 'CORRECT SOLUTION', and 'LANGUAGE MODEL RESPONSE', you rate the 'LANGUAGE MODEL RESPONSE' and detect whether it is a satisfactory response to the 'PROBLEM'. 
            Your answer should be a single rating from 5 options: ['FULLY ACCURATE', 'MOSTLY ACCURATE', 'PARTIALLY ACCURATE', 'MOSTLY INACCURATE', 'FULLY INACCURATE'] . 
            It does not matter whether 'LANGUAGE MODEL RESPONSE' is verbose or terse, only its accuracy matters.
            """
        },
        {
            "role": "user",
            "content": f"<<PROBLEM>> {problem}"
        },
        {
            "role": "user",
            "content": f"<<CORRECT SOLUTION>> {correct_solution}"
        },
        {
            "role": "user",
            "content": f"<<LANGUAGE MODEL RESPONSE>> {predicted_solution}"
        }
    ]
    try:
        t1_start = perf_counter()
        # print(messages)
        response = client.chat.completions.create(
            model=model_id, messages=messages, max_tokens=300
        )
        t1_stop = perf_counter()
        print(f"Time taken to execute single ChatGPT request: {t1_stop - t1_start}")
        tmp_result = response.choices[0].message.content
        tmp_result = tmp_result.strip(string.punctuation)
        if tmp_result.upper() in eval_result_list:
            return tmp_result, tmp_result.upper()
        else:
            return tmp_result, "UNDEFINED"
    except RateLimitError as ex:
        return "", "RATE LIMIT ERROR"
    except Exception as ex:
        print(ex)
        return "", "FAILED"


if __name__ == "__main__":
    df = pd.read_csv("llama_predictions_openstax_test_dataset.csv")
    start_string = "<s> [INST] "
    end_string = " [/INST] "
    df["problem_cleaned"] = df["question"].apply(lambda x: x[len(start_string):-len(end_string)])
    llama_scores_gpt4 = []
    llama_responses_raw = []
    for i, row in df.iterrows():
        gpt4_response = evaluate_response(
            problem=row["problem_cleaned"],
            correct_solution=row["actual responses"],
            predicted_solution=row["llama_anyscale_api_predictions"]
        )
        llama_responses_raw.append(gpt4_response[0])
        llama_scores_gpt4.append(gpt4_response[1])
    df["llama_scores_gpt4"] = llama_scores_gpt4
    df["llama_scores_gpt4_raw"] = llama_responses_raw
    df.to_csv("llama_predictions_openstax_test_dataset_complete.csv")

