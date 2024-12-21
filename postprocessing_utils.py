import execjs
import re
import subprocess
import os
from lxml import etree
import html2text
from bs4 import BeautifulSoup


def remove_tag_attributes_soup(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')

    # Remove attributes from all tags
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            del tag[attr]

    # Return the modified HTML string
    return str(soup)


def remove_tag_attributes(html_string):
    # Define the pattern to match HTML tags with attributes
    pattern = r'<(\w+)\s[^>]*>'
    # Use re.sub to replace each matched tag with only the tag name
    modified_html = re.sub(pattern, lambda match: '<' + match.group(1) + '>', html_string)
    return modified_html


def html_to_plain_text(html_string):
    # Create an instance of the HTML2Text converter
    converter = html2text.HTML2Text()
    # Convert HTML to plain text
    plain_text = converter.handle(html_string)
    # Modify the plain text to replace "\n1. ", "\n2. ", ... with "\nA. ", "\nB. ", ...
    plain_text = re.sub(r'(\d+)\. ', lambda match: chr(int(match.group(1)) + 64) + '. ', plain_text)
    return plain_text


def mathml2latex_xsl(equation: str):
    """Convert MathML to Latex
    ref: https://github.com/oerpub/mathconverter
    """
    xslt_file = os.path.join('mmltex.xsl')
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    equation = str(newdom)
    equation = equation.replace('$', '').strip()
    return equation


def mathml2latex_jslib(mathml_string: str) -> str:
    js_code = f"""
    const MathML2LaTeX = require('mathml2latex');
    const mathmlHtml = '{mathml_string}';
    var latex = MathML2LaTeX.convert(mathmlHtml);
    """
    ctx = execjs.compile(js_code)
    result = ctx.eval('latex')
    return result


def mathml2latex_texmath(mathml_content: str):
    process = subprocess.Popen(['/Users/4760393/.local/bin/texmath', '--from', 'mathml', '--to', 'tex'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    latex_output, _ = process.communicate(mathml_content.encode('utf-8'))
    return latex_output.decode('utf-8')


def clean_string_legacy(raw_text: str):
    pattern = re.compile(r'<div[^>]*>|</div>', flags=re.IGNORECASE)
    # Remove <div> tags and get content in between
    content_between_divs = re.sub(pattern, '', raw_text)
    pattern = re.compile(r'<p[^>]*>|</p>', flags=re.IGNORECASE)
    content_with_stripped_p_tags = re.sub(pattern, '', content_between_divs)
    text_and_span_list = re.split(r'(<span[^>]*>.*?</span>)', content_with_stripped_p_tags)
    return_list = []
    for item in text_and_span_list:
        if item.strip():
            if "<span" in item or "</span>" in item:
                # print(item.strip())
                # item_processed = item.replace("<mrow>", "<mrow>")
                try:
                    return_list.append(mathml2latex_texmath(item.strip()))
                except RuntimeError as e:
                    return_list.append(item.strip())
            else:
                return_list.append(html_to_plain_text(item.strip()))
    return " ".join(return_list)


def split_math_and_non_math(input_string):
    # Define the regex pattern to match <math> tags and non-math content
    pattern = r'(<math>(?:.|\n)*?</math>)|(.*?)(?=<math>|$)'

    # Use re.findall to find all matches of the pattern in the input string
    parts = re.findall(pattern, input_string, re.DOTALL)

    # Extract the non-empty matches and return as a list of strings
    result = [part[0] or part[1] for part in parts if any(part)]
    return result


def process_math_tags(text: str):
    # Parse the HTML string
    soup = BeautifulSoup(text, 'html.parser')
    # text_and_math_list = re.split(r'(<math[^>]*>.*?</math>)', text)
    # # print(text_and_math_list)
    return_list = []
    for element in soup.children:
        if element.name == "math":
            tex_output = mathml2latex_texmath(str(element))
            if len(tex_output) > 0:
                return_list.append(tex_output)
            else:
                print(f"TexMath failed for `{str(element)}`")
                return_list.append(str(element))
        else:
            return_list.append(str(element))
    return " ".join(return_list)


def clean_string(raw_text: str):
    pattern = re.compile(r'<div[^>]*>|</div>', flags=re.IGNORECASE)
    content_between_divs = re.sub(pattern, '', raw_text)
    pattern = re.compile(r'<p[^>]*>|</p>', flags=re.IGNORECASE)
    content_with_stripped_p_tags = re.sub(pattern, '', content_between_divs)
    pattern = re.compile(r'<span[^>]*>|</span>', flags=re.IGNORECASE)
    content_with_stripped_p_and_span_tags = re.sub(pattern, '', content_with_stripped_p_tags)
    processed_text = process_math_tags(content_with_stripped_p_and_span_tags)
    return remove_tag_attributes(html_to_plain_text(processed_text)).replace("\n", " ")


# print(html_to_plain_text('<a> <em style="italics" weight="bold"> g </em> </a>'))
# with open("datasets/english/university-physics-volume-1.json") as fp:
#     json_file = json.loads(fp.read())
# # print(json_file)
# for entry in json_file[-5:]:
#     # print(entry["problem"])
#     # print(entry["solution"])
#     print({"problem_cleaned": clean_string(entry["problem"])})
#     # print({"solution_cleaned": clean_string(entry["solution"])})

# print(clean_string('<ol id="eip-id1169866436811" type="A"><li>Until 2025.</li><li>Until 2079.</li><li>Until 2110.</li></ol> Solution B. <math> Hello </math> <a href="www.google.com" class="high-sdvser"> <em style="italics" weight="bold"> g </em>'))
#
# print(clean_string('hello \n <math> (some mathml html content <msup> 3 <mathml>) </math> world!'))
#
#
# print(clean_string("""Yeast converts glucose to ethanol and carbon dioxide during anaerobic fermentation as depicted in the simple chemical equation here:<br/>
#
# <math display="block">
# <semantics>
# <mrow>
# <mrow>
# <mtext>glucose</mtext>
# <mspace width="0.2em"></mspace>
# <mo stretchy="false">⟶</mo>
# <mspace width="0.2em"></mspace>
# <mtext>ethanol</mtext>
# <mo>+</mo>
# <mtext>carbon dioxide</mtext>
# </mrow>
# </mrow>
# <annotation-xml encoding="MathML-Content">
# <mrow>
# <mtext>glucose</mtext>
# <mspace width="0.2em"></mspace>
# <mo stretchy="false">⟶</mo>
# <mspace width="0.2em"></mspace>
# <mtext>ethanol</mtext>
# <mo>+</mo>
# <mtext>carbon dioxide</mtext>
# </mrow>
# </annotation-xml>
# </semantics>
# </math>
#
# (a) If 200.0 g of glucose is fully converted, what will be the total mass of ethanol and carbon dioxide produced?
# (b) If the fermentation is carried out in an open container, would you expect the mass of the container and contents after fermentation to be less than, greater than, or the same as the mass of the container and contents before fermentation? Explain.
# (c) If 97.7 g of carbon dioxide is produced, what mass of ethanol is produced?"""))