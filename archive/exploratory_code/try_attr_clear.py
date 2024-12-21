from bs4 import BeautifulSoup

def remove_tag_attributes(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Remove attributes from all tags
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            del tag[attr]
    
    # Return the modified HTML string
    return str(soup)

# Example usage
html_string = '<em class="italic">g</em>'
modified_html = remove_tag_attributes(html_string)
print(modified_html)

