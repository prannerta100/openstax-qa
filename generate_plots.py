import pandas as pd
import matplotlib.pyplot as plt
combined_df = pd.read_json("openstax_processed_data.json")
combined_df.drop_duplicates(subset=["problem_cleaned", "solution_cleaned"], inplace=True)
print(combined_df.columns)
"            But if the language used in 'LANGUAGE MODEL RESPONSE' is not the same as the language of the 'PROBLEM', you should always answer 'FULLY INACCURATE'."
# book_field_mapping = pd.read_csv("book_field_mapping.csv")
# field_counts = pd.merge(combined_df, book_field_mapping, on="book", how="inner")["field"].value_counts().sort_index()
# plt.bar(["Business", "Humanities", "Math", "Science", "Social Sciences"], field_counts.values)
# plt.yscale('log')
# plt.ylabel("Number of unique problem-solution pairs")
# plt.savefig("field_distribution.png")
# plt.show()

# language_counts = combined_df["language"].value_counts().sort_index()
# plt.bar(["English", "Spanish", "Polish"], language_counts.values)
# plt.yscale('log')
# plt.ylabel("Number of unique problem-solution pairs")
# plt.savefig("language_distribution.png")
# plt.show()



# filename = "testing_sample_llemma_7b_finetuned_full_dataset.csv"
# df = pd.read_csv(filename)
# df["gpt4_score_A"] = df.apply(lambda row: evaluate_response(row["question"], row["actual responses"], row["predicted responses A"])[1], axis=1)
# df["gpt4_score_B"] = df.apply(lambda row: evaluate_response(row["question"], row["actual responses"], row["predicted responses B"])[1], axis=1)
#
# df.to_csv(filename.split(".")[0] + "_scored.csv")
