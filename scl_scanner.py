from Token import *
import json
import sys
import re


# Group members (Bri, Briana, Brian, Molly)

def tokenize(line):
    tokens = []
    current = ""
    in_string_comment = False
    inline_comment = False
    token_types = {
        "StringLiteral": r'("[^"]*"|\'[^\']*\')',
        "MultiLineComment": r'/\*.*?\*/',
        "SingleLineComment": r'//.*',
        "Keyword": r'\b(import|implementations|function|main|is|variables|define|of|begin|display|set|input|if|then|else|endif|not|greater|or|equal|return)\b',
        "Identifier": r'[a-zA-Z_]\w*',
        "NumericLiteral": r'\d+(\.\d+)?',
        "Operator": r':|\.|:|,|/|=|>|\*|\)|\('
    }
    regular_expressions = "|".join(f"({regex})" for regex in token_types.values())

    match_objects = re.finditer(regular_expressions, line)

    for match_regex in match_objects:
        token = match_regex.group(0)

        if token.strip() == "":
            continue  # gets rid of whitespaces

        if '//' in token:
            # gets rid of comments
            token = token.split('//')[0].strip()

        tokens.append(token)

    return tokens


def scl_file(name_file):
    try:
        file = open(name_file, 'r')
    except:
        print("no such file or directory: ", name_file)
        exit(2)

    lineArray = []

    inline_comment = False  # makes sure not inside inline comment

    for line in file:
        if 'description' in line:
            inline_comment = True

        if inline_comment:
            if '*/' in line:
                inline_comment = False
            continue  # skips the lines within inline comments
        else:
            if line.startswith("/*"):
                continue  # skips the comment line

            inlineTokens = tokenize(line)

            # removes blank tokens
            inlineTokens = [token for token in inlineTokens if token.strip() != '']

            if inlineTokens:
                lineArray.append(inlineTokens)

    return lineArray


counter = 3000
map = {}

def categorize(token):
    global counter
    keyword_set = set(tokenList["keywords"])
    operator_set = set(tokenList["operators"])
    special_symbol_set = set(tokenList["specialSymbols"])

    if token in keyword_set:
        return {"Type": "Keyword", "id": tokenList["keywords"][token], "value": token}
    elif token in operator_set:
        return {"Type": "Operator", "id": tokenList["operators"][token], "value": token}
    elif token in special_symbol_set:
        return {"Type": "SpecialSymbol", "id": tokenList["specialSymbols"][token], "value": token}

    if re.match(r'^[a-zA-Z_]\w*$', token):
        # Use counter directly without a separate map
        result = {"Type": "Identifier", "id": counter, "value": token}
        counter += 1
        return result
    elif re.match(r'^(?:"|\').*?(?:"|\')$', token) or re.match(r'^[0-9]+(\.[0-9]+)?$', token):
        if token.startswith('"') or token.startswith("'"):
            cleaned_token = token[1:-1].replace('\\"', '"').replace("\\'", "'").replace("\\/", "/")
            return {"Type": "StringLiteral", "id": 5000, "value": cleaned_token}
        else:
            return {"Type": "NumericLiteral", "id": 4000, "value": token}
    elif token in [",", "="]:
        return {"Type": "Operator", "id": 400, "value": token}

    # unknown token if previous conditions are untrue
    return {"Type": "UNKNOWN", "id": 1200, "value": token}



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    sys.Argv = sys.argv

    #input_file_path = sys.Argv[1]
    itemList = scl_file(sys.Argv[1])

    finalList = []

    megaDictionary = {}

    for lineTokens in itemList:
        for token in lineTokens:
            categorized_token = categorize(token)
            newToken = Token(categorized_token["Type"], categorized_token["id"], categorized_token["value"])
            finalList.append(newToken)
            print("New Token created: ", newToken.getData())

        newToken = Token('EndOfStatement', 1000, 'EOS')
        finalList.append(newToken)
        print("New Token created: ", newToken.getData())

    # putting token objects into a dictionary for future JSON file

    loopCounter = 0
    for Token in finalList:
        tokenString = "Token_" + str(loopCounter)

        # make dictionary for token
        tokenInfo = Token.getData()
        tokenDictionary = {
            "Type": tokenInfo[0],
            "id": tokenInfo[1],
            "value": tokenInfo[2]
        }

        # add the token dictionary to the megaDictionary
        megaDictionary[tokenString] = tokenDictionary

        loopCounter += 1

    loopCounter = 0
    for Token in finalList:
        tokenInfo = Token.getData()
        lst = ['Type', tokenInfo[0], 'id', tokenInfo[1], 'value', tokenInfo[2]]


        tokenString = "Token_" + str(loopCounter)

    # creating output JSON file
    json_object = json.dumps(megaDictionary, indent=4)
    with open('OutputTokens.json', 'w') as f:
        f.write(json_object)
