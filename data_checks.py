import pandas as pd
import re
import html2text

def html_to_plain_text(html_string):
    # Create an instance of the HTML2Text converter
    converter = html2text.HTML2Text()
    # Convert HTML to plain text
    plain_text = converter.handle(html_string)
    # Modify the plain text to replace "\n1. ", "\n2. ", ... with "\nA. ", "\nB. ", ...
    plain_text = re.sub(r'(\d+)\. ', lambda match: chr(int(match.group(1)) + 64) + '. ', plain_text)
    return plain_text

def find_html_tags(html_string):
    # Define the regular expression pattern to match HTML tags
    pattern = r'<\s*([a-zA-Z]+)[^>]*>'
    # Use re.findall to find all matches of the pattern in the string
    matched_tags = re.findall(pattern, html_string)
    return matched_tags


df_list = []

df = pd.read_json("openstax_processed_data.json", orient="records")
tag_set = set()
for _, row in df.iterrows():
    tags = find_html_tags(row["problem_cleaned"]) + find_html_tags(row["solution_cleaned"])
    for tag in tags:
        tag_set.add(tag)
print("Tags found: ", sorted(list(tag_set)))
print(df.loc[df["problem_cleaned"].str.contains("<B") | df["solution_cleaned"].str.contains("<B") | df["problem_cleaned"].str.contains("B>") | df["solution_cleaned"].str.contains("B>")].shape)
print(df.loc[df["problem_cleaned"].str.contains("<R") | df["solution_cleaned"].str.contains("<R") | df["problem_cleaned"].str.contains("R>") | df["solution_cleaned"].str.contains("R>")].shape)
print(df.loc[df["problem_cleaned"].str.contains("<t") | df["solution_cleaned"].str.contains("<t") | df["problem_cleaned"].str.contains("t>") | df["solution_cleaned"].str.contains("t>")].shape)
print(df.loc[df["problem_cleaned"].str.contains("<a") | df["solution_cleaned"].str.contains("<a") | df["problem_cleaned"].str.contains("a>") | df["solution_cleaned"].str.contains("a>")].shape)


# df.drop_duplicates(subset=["problem_cleaned", "solution_cleaned"], inplace=True)
# df["problem_cleaned"] = df["problem_cleaned"].astype(str)
# df["solution_cleaned"] = df["solution_cleaned"].astype(str)
# df = df.loc[~df["problem_cleaned"].str.contains("<a") & ~df["solution_cleaned"].str.contains("<a")]
# df = df.loc[~df["problem_cleaned"].str.contains("<figure") & ~df["solution_cleaned"].str.contains("<figure")]
# df = df.loc[~df["problem_cleaned"].str.contains("<img") & ~df["solution_cleaned"].str.contains("<img")]
# print(df.shape)
# print(df["book"].value_counts())
# df["guanaco_style_prompt_responses"] = "<s>[INST]" + df["problem_cleaned"] + " [/INST] " + df[
#     "solution_cleaned"] + " </s>"
# df.to_csv(f"~/{language}_dataset_modified.csv")
# df_list.append(df)
# pd.concat(df_list, axis=0).to_csv("~/consolidated_dataset_modified.csv")
