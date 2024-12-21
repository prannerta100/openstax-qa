import json

html_content = '<div class="example">Content inside div</div>'

# Create a dictionary with the HTML content
data = {"html_content": html_content}

# Write the dictionary to a JSON file
with open("output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
