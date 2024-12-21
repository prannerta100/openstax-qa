from bs4 import BeautifulSoup


def split_math_and_non_math(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Initialize lists to store math and non-math content
    math_content = []
    non_math_content = []
    
    # Iterate through all elements in the parsed HTML
    for element in soup.children:
        # Check if the element is a <math> tag
        if element.name == 'math':
            # Append the entire element as math content
            math_content.append(str(element))
        else:
            # Append the element's string representation as non-math content
            non_math_content.append(str(element))
    
    return non_math_content, math_content

# Example usage
html_string = 'hello \n <math attr1="asd" attr2="def"> (some mathml html content) </math> world!'
non_math_content, math_content = split_math_and_non_math(html_string)
print("Non-math content:", non_math_content)
print("Math content:", math_content)

