import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


print(num_tokens_from_string("""You are evaluating solutions to textbook problems given by a language model. 
            Given a 'PROBLEM', 'CORRECT SOLUTION', and 'LANGUAGE MODEL RESPONSE', you rate the 'LANGUAGE MODEL RESPONSE' and detect whether it is a satisfactory response to the 'PROBLEM'. 
            Your answer should be a single rating from 5 options: ['FULLY ACCURATE', 'MOSTLY ACCURATE', 'PARTIALLY ACCURATE', 'MOSTLY INACCURATE', 'FULLY INACCURATE'] . 
            It does not matter whether 'LANGUAGE MODEL RESPONSE' is verbose or terse, only its accuracy matters.""", "cl100k_base"))