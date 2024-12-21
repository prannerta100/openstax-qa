import pandas as pd
from gpt4_answer_scorer import evaluate_response
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# df_llama = pd.read_csv("challenge_arc_Llama-2-7b-hf.csv")
# df_llama_finetuned = pd.read_csv("challenge_arc_Llama-2-7b-hf-openstax.csv")
# df_llemma_finetuned = pd.read_csv("challenge_arc_llemma_7b-openstax.csv")

# responses_raw = []
# scores_gpt4 = []
# for i, row in df_llama.iterrows():
#     gpt4_response = evaluate_response(
#         problem=row["question"],
#         correct_solution=row["AnswerKey"],
#         predicted_solution=row["predicted response"]
#     )
#     responses_raw.append(gpt4_response[0])
#     scores_gpt4.append(gpt4_response[1])
# df_llama["llama_scores_gpt4"] = scores_gpt4
# df_llama["llama_scores_gpt4_raw"] = responses_raw
# df_llama.to_csv("challenge_arc_Llama-2-7b-hf-scored.csv")
#
# responses_raw = []
# scores_gpt4 = []
# for i, row in df_llama_finetuned.iterrows():
#     gpt4_response = evaluate_response(
#         problem=row["question"],
#         correct_solution=row["AnswerKey"],
#         predicted_solution=row["predicted response"]
#     )
#     responses_raw.append(gpt4_response[0])
#     scores_gpt4.append(gpt4_response[1])
# df_llama_finetuned["llama_finetuned_scores_gpt4"] = scores_gpt4
# df_llama_finetuned["llama_finetuned_scores_gpt4_raw"] = responses_raw
# df_llama_finetuned.to_csv("challenge_arc_Llama-2-7b-hf-openstax-scored.csv")

# responses_raw = []
# scores_gpt4 = []
# for i, row in df_llemma_finetuned.iterrows():
#     gpt4_response = evaluate_response(
#         problem=row["question"],
#         correct_solution=row["AnswerKey"],
#         predicted_solution=row["predicted response"]
#     )
#     responses_raw.append(gpt4_response[0])
#     scores_gpt4.append(gpt4_response[1])
# df_llemma_finetuned["llemma_finetuned_scores_gpt4"] = scores_gpt4
# df_llemma_finetuned["llemma_finetuned_scores_gpt4_raw"] = responses_raw
# df_llemma_finetuned.to_csv("challenge_arc_llemma_7b-openstax-scored.csv")

score_dict = {'FULLY ACCURATE': 5, 'MOSTLY ACCURATE': 4, 'PARTIALLY ACCURATE': 3, 'MOSTLY INACCURATE': 2, 'FULLY INACCURATE': 1}
score_names = ['FULLY INACCURATE', 'MOSTLY INACCURATE', 'PARTIALLY ACCURATE', 'MOSTLY ACCURATE', 'FULLY ACCURATE']
df = pd.read_csv("challenge_arc_Llama-2-7b-hf-scored.csv")
scores_llama = df.loc[df['llama_scores_gpt4'].isin(score_names), 'llama_scores_gpt4']
df = pd.read_csv("challenge_arc_Llama-2-7b-hf-openstax-scored.csv")
scores_llama_finetuned = df.loc[df['llama_finetuned_scores_gpt4'].isin(score_names), 'llama_finetuned_scores_gpt4']
df = pd.read_csv("challenge_arc_llemma_7b-openstax-scored.csv")
scores_llemma_finetuned = df.loc[df['llemma_finetuned_scores_gpt4'].isin(score_names), 'llemma_finetuned_scores_gpt4']

print(
    "2-sided pair t test Llama finetuned vs not finetuned",
    stats.ttest_ind(
        scores_llama.apply(lambda x: score_dict[x]),
        scores_llama_finetuned.apply(lambda x: score_dict[x]
    ), equal_var=False)
)

print(
    "2-sided pair t test Llemma finetuned vs Llama finetuned",
    stats.ttest_ind(
        scores_llama_finetuned.apply(lambda x: score_dict[x]),
        scores_llemma_finetuned.apply(lambda x: score_dict[x]
    ), equal_var=False)
)

print(
    "Llama untrained- mean and standard deviations",
    np.mean(scores_llama.apply(lambda x: score_dict[x])),
    np.std(scores_llama.apply(lambda x: score_dict[x]))
)
print(
    "Llama finetuned- mean and standard deviations",
    np.mean(scores_llama_finetuned.apply(lambda x: score_dict[x])),
    np.std(scores_llama_finetuned.apply(lambda x: score_dict[x]))
)

print(
    "Llemma finetuned- mean and standard deviations",
    np.mean(scores_llemma_finetuned.apply(lambda x: score_dict[x])),
    np.std(scores_llemma_finetuned.apply(lambda x: score_dict[x]))
)


plt.figure(figsize=(10,10))
width = 0.2

length_ratio = scores_llama_finetuned.shape[0] / scores_llama.shape[0]
bar_heights = []
for x in score_names:
    if x in scores_llama.value_counts().index:
        bar_heights.append(length_ratio * scores_llama.value_counts()[x])
    else:
        bar_heights.append(0)
plt.bar(np.arange(5) - width, bar_heights, width, label='Llama 7B')

plt.bar(np.arange(5), [scores_llama_finetuned.value_counts()[x] for x in score_names], width, label='Llama 7B Finetuned')

length_ratio = scores_llama_finetuned.shape[0] / scores_llemma_finetuned.shape[0]
bar_heights = []
for x in score_names:
    if x in scores_llama.value_counts().index:
        bar_heights.append(length_ratio * scores_llemma_finetuned.value_counts()[x])
    else:
        bar_heights.append(0)
plt.bar(np.arange(5) + width, bar_heights, width, label='Llemma 7B Finetuned')

plt.xlabel('Score given by GPT 4')
plt.ylabel('Number of answers')
plt.title('Comparing finetuned model scores')
plt.xticks(np.arange(5), score_names)
plt.yscale('log')
plt.legend(loc='best')
plt.savefig('ai2rc-llama-llemma-finetuned-comparison.png')
plt.close()