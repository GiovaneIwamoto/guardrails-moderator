def treat_input(user_input: str):
    #TODO: develop logic here 
    return "treat_using_regex"

# Main function receives text_input from API param and calls treat_input
def main(params: dict):
    text_input = params.get('text_input')
    treated_response = treat_input(text_input)
    
    return treated_response
