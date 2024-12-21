import subprocess


def convert_mathml_to_latex(mathml_content):
    # Call the texmath executable with the MathML content as input
    process = subprocess.Popen(['/Users/4760393/.local/bin/texmath', '--from', 'mathml', '--to', 'tex'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    latex_output, _ = process.communicate(mathml_content.encode('utf-8'))
    return latex_output.decode('utf-8')


# Example usage
# mathml_content = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mn>2</mn><mo>+</mo><mfrac><mn>3</mn><mn>4</mn></mfrac></mrow></math>'
mathml_content = '<math display="inline"><semantics><mrow><mrow><mi>g</mi><mo>∘</mo><mi>f</mi></mrow></mrow><annotation-xml encoding="MathML-Content"><mrow><mi>g</mi><mo>∘</mo><mi>f</mi></mrow></annotation-xml></semantics></math>'
latex_output = convert_mathml_to_latex(mathml_content)
print(latex_output)


# def clean_string(raw_text: str):
#     soup = BeautifulSoup(raw_text, 'html.parser')
#     # p_tags = soup.find('div').find_all('p')
#     # raw_text_stripped = " ".join([str(p.contents[0]) for p in p_tags])
#     raw_text_stripped = re.split(r'(<span[^>]*>.*?</span>)', raw_text)
#     raw_text_stripped = re.split(r'(<div[^>]*>.*?</div>)', raw_text_stripped)
#     print(raw_text_stripped)
#     text_and_span_list = re.split(r'(<span[^>]*>.*?</span>)', raw_text_stripped)
#     text_and_span_list = [item.strip() for item in text_and_span_list if item.strip()]
#     return text_and_span_list
#     # clean_text = mathml2latex(raw_text_stripped)
#     # clean_text = re.sub(r'\\text\{([^}]*)\}', r'\1', clean_text)
#     # return clean_text.encode().decode('utf-8')




# string = '<div class="os-problem-container">\n<p id="fs-id1170572213101"><span class="os-math-in-para"><math display="inline"><semantics><mrow><mrow><mi>f</mi><mo>\u2218</mo><mi>g</mi><mo>=</mo><mi>g</mi><mo>\u2218</mo><mi>f</mi><mo>,</mo></mrow></mrow><annotation-xml encoding="MathML-Content"><mrow><mi>f</mi><mo>\u2218</mo><mi>g</mi><mo>=</mo><mi>g</mi><mo>\u2218</mo><mi>f</mi><mo>,</mo></mrow></annotation-xml></semantics></math></span> assuming <em data-effect="italics">f</em> and <em data-effect="italics">g</em> are functions.</p>\n</div>'
# problems_soup = BeautifulSoup(string, 'html.parser')
# os_hasSolution_divs = problems_soup.find('div', class_='os-problem-container').find_all('p')
# print([p.get_text() for p in os_hasSolution_divs])
# print(clean_string(r'<span class=\"os-math-in-para\"><math display=\"inline\"><semantics><mrow><mrow><mrow><mrow><mn>4</mn><mtext>.</mtext><mtext>20 m</mtext><msup><mtext>/s</mtext><mrow><mn>2</mn></mrow></msup></mrow></mrow></mrow></mrow><annotation-xml encoding=\"MathML-Content\"><mrow><mrow><mrow><mn>4</mn><mtext>.</mtext><mtext>20 m</mtext><msup><mtext>/s</mtext><mrow><mn>2</mn></mrow></msup></mrow></mrow></mrow></annotation-xml></semantics></math></span>'))

# from bs4 import BeautifulSoup
#
# html_content = 'Hi how are you? <span class="os-math-in-para"> 2 <msup>2</msup> = 4 </span> is an equation I like.'
#
# # Parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')
# text_and_tag_pairs = []

# # Extract text and tags
# for element in soup.descendants:
#     if isinstance(element, str):
#         text_and_tag_pairs.append(element)
#     else:
#         text_and_tag_pairs.append(str(element))
#
# # Filter out empty strings
# text_and_tag_pairs = [item for item in text_and_tag_pairs if item.strip()]
#
# print(text_and_tag_pairs)

# text_and_tag_pairs = []
#
# # Find all tags in the parsed HTML content
# tags = soup.find_all()
#
# # Initialize a variable to store the previous index
# prev_index = 0
#
# # Iterate over the tags
# for tag in tags:
#     # Get the index of the current tag in the original HTML content
#     curr_index = html_content.find(str(tag), prev_index)
#
#     # If there is text between the previous and current tag, add it to the list
#     if curr_index > prev_index:
#         text_and_tag_pairs.append(html_content[prev_index:curr_index])
#
#     # Add the current tag to the list
#     text_and_tag_pairs.append(str(tag))
#
#     # Update the previous index to the end of the current tag
#     prev_index = curr_index + len(str(tag))
#
# # If there is text after the last tag, add it to the list
# if prev_index < len(html_content):
#     text_and_tag_pairs.append(html_content[prev_index:])
#
# print(text_and_tag_pairs)

# print('<div class="os-problem-container">\n<p id="fs-id1170572213101"><span class="os-math-in-para"><math display="inline"><semantics><mrow><mrow><mi>f</mi><mo>\u2218</mo><mi>g</mi><mo>=</mo><mi>g</mi><mo>\u2218</mo><mi>f</mi><mo>,</mo></mrow></mrow><annotation-xml encoding="MathML-Content"><mrow><mi>f</mi><mo>\u2218</mo><mi>g</mi><mo>=</mo><mi>g</mi><mo>\u2218</mo><mi>f</mi><mo>,</mo></mrow></annotation-xml></semantics></math></span> assuming <em data-effect="italics">f</em> and <em data-effect="italics">g</em> are functions.</p>\n</div>'.encode().decode('utf-8'))


# import re
#
# html_content = 'Hi how are you? <span class="os-math-in-para"> 2 <msup>2</msup> = 4 </span> is an equation I like.'
#
# # Split the HTML content using regex to separate text and tags
# text_and_tag_pairs = re.split(r'(<.*?>)', html_content)
#
# # Filter out empty strings and remove extra whitespace
# text_and_tag_pairs = [item.strip() for item in text_and_tag_pairs if item.strip()]
#
# print(text_and_tag_pairs)


# import re
#
# print(clean_string(
#     '<div><p>Hi how are you? <span class="os-math-in-para"> 2 <msup>2</msup> = 4 </span> is an equation I like.</div></p>'))
#
# # Split the HTML content using regex to separate text and <span> tags
# text_and_span_pairs = re.split(r'(<span[^>]*>.*?</span>)', html_content)
#
# # Filter out empty strings and remove extra whitespace
# text_and_span_pairs = [item.strip() for item in text_and_span_pairs if item.strip()]
#
# print(text_and_span_pairs)


# vi try.json -c ':%s/}\,\n]/}\r]/g' -c ':wq'