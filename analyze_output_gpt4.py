import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from scipy import stats

score_dict = {'FULLY ACCURATE': 5, 'MOSTLY ACCURATE': 4, 'PARTIALLY ACCURATE': 3, 'MOSTLY INACCURATE': 2, 'FULLY INACCURATE': 1}
score_names = ['FULLY INACCURATE', 'MOSTLY INACCURATE', 'PARTIALLY ACCURATE', 'MOSTLY ACCURATE', 'FULLY ACCURATE']
# LANGUAGE = "pl"

df = pd.read_csv("llama_untrained_model_scores.csv")
scores_llama = df.loc[df['llama_scores_gpt4'].isin(score_names), 'llama_scores_gpt4']

df = pd.read_csv("llama_predictions_openstax_test_dataset_complete.csv")
# df = df.loc[df["language"] == LANGUAGE]
scores_llama_A = df.loc[df['gpt4_score_A'].isin(score_names), 'gpt4_score_A'] #apply(lambda x: score_dict[x])
scores_llama_B = df.loc[df['gpt4_score_B'].isin(score_names), 'gpt4_score_B'] #apply(lambda x: score_dict[x])

df = pd.read_csv("testing_sample_llemma_7b_finetuned_full_dataset_scored.csv")
# df = df.loc[df["language"] == LANGUAGE]
scores_llemma_A = df.loc[df['gpt4_score_A'].isin(score_names), 'gpt4_score_A'] #apply(lambda x: score_dict[x])
scores_llemma_B = df.loc[df['gpt4_score_B'].isin(score_names), 'gpt4_score_B'] #apply(lambda x: score_dict[x])

# Mean and standard deviations of responses
# print("Llama- mean and standard deviations", np.mean(scores_llama.apply(lambda x: score_dict[x])), np.std(scores_llama.apply(lambda x: score_dict[x])))
scores_llama_trained_combined = pd.concat([scores_llama_A, scores_llama_B], axis=0)
scores_llemma_trained_combined = pd.concat([scores_llemma_A, scores_llemma_B], axis=0)

print(
    "2-sided pair t test Llama finetuned vs not finetuned",
    stats.ttest_ind(
        scores_llama.apply(lambda x: score_dict[x]),
        scores_llemma_trained_combined.apply(lambda x: score_dict[x]
    ), equal_var=False)
)

print(
    "2-sided pair t test Llemma finetuned vs Llama finetuned",
    stats.ttest_ind(
        scores_llama_trained_combined.apply(lambda x: score_dict[x]),
        scores_llemma_trained_combined.apply(lambda x: score_dict[x]
    ), equal_var=False)
)

print(
    "Llama untrained- mean and standard deviations",
    np.mean(scores_llama.apply(lambda x: score_dict[x])),
    np.std(scores_llama.apply(lambda x: score_dict[x]))
)
print(
    "Llama finetuned- mean and standard deviations",
    np.mean(scores_llama_trained_combined.apply(lambda x: score_dict[x])),
    np.std(scores_llama_trained_combined.apply(lambda x: score_dict[x]))
)

print(
    "Llemma finetuned- mean and standard deviations",
    np.mean(scores_llemma_trained_combined.apply(lambda x: score_dict[x])),
    np.std(scores_llemma_trained_combined.apply(lambda x: score_dict[x]))
)


plt.figure(figsize=(10,10))
width = 0.2

length_ratio = scores_llama_trained_combined.shape[0] / scores_llama.shape[0]
plt.bar(np.arange(5) - width, [length_ratio * scores_llama.value_counts()[x] for x in score_names], width, label='Llama 7B')
plt.bar(np.arange(5), [scores_llama_trained_combined.value_counts()[x] for x in score_names], width, label='Llama 7B Finetuned')
length_ratio = scores_llama_trained_combined.shape[0] / scores_llemma_trained_combined.shape[0]
plt.bar(np.arange(5) + width, [length_ratio * scores_llemma_trained_combined.value_counts()[x] for x in score_names], width, label='Llemma 7B Finetuned')
plt.xlabel('Score given by GPT 4')
plt.ylabel('Number of answers')
plt.title('Comparing finetuned model scores')
plt.xticks(np.arange(5), score_names)
plt.yscale('log')
plt.legend(loc='best')
plt.savefig('llama-llemma-finetuned-comparison.png')
plt.close()

# plt.bar(np.arange(5) - width / 2, [scores_llemma_A.value_counts()[x] for x in score_names], width, label='Beam 1')
# plt.bar(np.arange(5) + width / 2, [scores_llemma_B.value_counts()[x] for x in score_names], width, label='Beam 2')
# plt.xlabel('Score given by GPT 4')
# plt.ylabel('Number of answers')
# plt.title('Comparing finetuned model scores- Llemma 7B trained model')
# plt.xticks(np.arange(5), score_names)
# plt.yscale('log')
# plt.legend(loc='best')
# plt.savefig('llemma-finetuned-comparison-beams.png')

# plt.bar(np.arange(5) - width / 2, [scores_llama_A.value_counts()[x] for x in score_names], width, label='Llama 7B')
# plt.bar(np.arange(5) + width / 2, [scores_llemma_A.value_counts()[x] for x in score_names], width, label='Llemma 7B finetuned')
# plt.xlabel('Score given by GPT 4')
# plt.ylabel('Number of answers')
# plt.title('Comparing finetuned model scores')
# plt.savefig('llemma-llama-finetuned-comparison.png')


# xticks()
# First argument - A list of positions at which ticks should be placed
# Second argument -  A list of labels to place at the given locations

# Finding the best position for legends and putting it




# b1 = plt.barh(0, scores_llama_A.index, scores_llama_A.values, label="LLama-2 Finetuned Model")
# b2 = plt.barh(1, scores_llemma_A.index, scores_llemma_A.values, label="LLemma Finetuned Model")
# plt.show()

# f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
# ax1.bar(scores_llama_A.index, scores_llemma_A.values, alpha=0.2)
# ax1.bar(scores_llemma_A, alpha=0.2)
# ax1.set_title('Sharing X axis')
# ax2.bar(scores_llama_B, alpha=0.5)
# ax2.bar(scores_llemma_B, alpha=0.5)

# # plotting histograms
# plt.hist(data['petal_length'],
#          label='petal_length')
#
# plt.hist(data['sepal_length'],
#          label='sepal_length')
#
# plt.legend(loc='upper right')
# plt.title('Overlapping')
plt.show()
#
# print(
#     .value_counts(normalize=True),
#     df.loc[df['gpt4_score_B'] != 'FAILED', 'gpt4_score_B'].value_counts(normalize=True),
# )
#
# df = pd.read_csv("")
# print(
#     df.loc[df['gpt4_score_A'] != 'FAILED', 'gpt4_score_A'].value_counts(normalize=True),
#     df.loc[df['gpt4_score_B'] != 'FAILED', 'gpt4_score_B'].value_counts(normalize=True),
# )