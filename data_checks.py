import pandas as pd
import re
import html2text


# class CustomHTML2Text(html2text.HTML2Text):
#     def handle_list(self, list, state):
#         if 'A' in list.get('type', ''):
#             self.list_item_prefix = 'A. '
#         elif 'a' in list.get('type', ''):
#             self.list_item_prefix = 'a. '
#         elif '1' in list.get('type', ''):
#             self.list_item_prefix = '1. '
#         elif 'I' in list.get('type', ''):
#             self.list_item_prefix = 'I. '
#         elif 'i' in list.get('type', ''):
#             self.list_item_prefix = 'i. '
#         else:
#             self.list_item_prefix = '• '

# Example usage
# def html_to_plain_text(html_string):
#     # Create an instance of the CustomHTML2Text converter
#     converter = html2text.HTML2Text()
#     # Convert HTML to plain text
#     plain_text = converter.handle(html_string)
#     return plain_text


def html_to_plain_text(html_string):
    # Create an instance of the HTML2Text converter
    converter = html2text.HTML2Text()
    # Convert HTML to plain text
    plain_text = converter.handle(html_string)
    # Modify the plain text to replace "\n1. ", "\n2. ", ... with "\nA. ", "\nB. ", ...
    plain_text = re.sub(r'(\d+)\. ', lambda match: chr(int(match.group(1)) + 64) + '. ', plain_text)
    return plain_text

print(html_to_plain_text("""<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
</table>"""))


# Example usage
# html_string = "\\frac{3}{4}" #'<ol id="eip-id1169866436811" type="A"><li>Until 2025.</li><li>Until 2079.</li><li>Until 2110.</li></ol>'
# plain_text = html_to_plain_text(html_string)
# print(plain_text)
#
# html_string = '<ol id="eip-id1169866436811" type="A"><li>Until 2025.</li><li>Until 2079.</li><li>Until 2110.</li></ol> Solution B.'
# print('<<Out>>', html_to_plain_text(html_string))


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
