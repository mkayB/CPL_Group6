from Token import *  # Import Token class from Tokens.py
import json
import sys
import re

def tokenize(line, tokenList):
    tokens = []

    # Define token types and their corresponding regular expressions
    token_types = {
        "StringLiteral": r'("[^"]*"|\'[^\']*\')',
        "MultiLineComment": r'/\*.*?\*/',
        "SingleLineComment": r'//.*',
        "Keyword": r'\b(import|implementations|function|main|is|variables|define|of|begin|display|set|input|if|then|else|endif|not|greater|or|equal|return)\b',
        "Identifier": r'[a-zA-Z_]\w*',
        "NumericLiteral": r'\d+(\.\d+)?',
        "Operator": r':|\.|:|,|/|=|>|\*|\)|\('
    }

    combined_regex = "|".join(f"({regex})" for regex in token_types.values())
    match_objects = re.finditer(combined_regex, line)

    for match_regex in match_objects:
        token = next(filter(None, match_regex.groups()))  # Pick the non-empty match

        if token.strip() == "":
            continue

        token_type = categorize_token(token, tokenList)
        newToken = Token(token_type["Type"], token_type["id"], token)
        tokens.append(newToken)
        print("New Token created:", newToken.getData())

    return tokens

def categorize_token(token, tokenList):
    if token in tokenList["keywords"]:
        return {"Type": "Keyword", "id": tokenList["keywords"][token], "value": token}
    elif re.match(r'^[a-zA-Z_]\w*$', token):
        return {"Type": "Identifier", "id": 4000, "value": token}
    elif re.match(r'^[0-9]+(\.[0-9]+)?$', token):
        return {"Type": "NumericLiteral", "id": 5000, "value": token}
    elif token.startswith('"') or token.startswith("'"):
        cleaned_token = token[1:-1].replace('\\"', '"').replace("\\'", "'").replace("\\/", "/")
        return {"Type": "StringLiteral", "id": 6000, "value": cleaned_token}
    elif token in tokenList["operators"]:
        return {"Type": "Operator", "id": tokenList["operators"][token], "value": token}
    elif token in tokenList["specialSymbols"]:
        return {"Type": "SpecialSymbol", "id": tokenList["specialSymbols"][token], "value": token}
    else:
        return {"Type": "UNKNOWN", "id": 7000, "value": token}

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

            inlineTokens = tokenize(line, tokenList)

            # removes blank tokens
            inlineTokens = [token for token in inlineTokens if token.value.strip() != '']

            if inlineTokens:
                lineArray.append(inlineTokens)

    return lineArray

if __name__ == '__main__':
    sysArgv = "/Users/briannanoel/PycharmProjects/deliverable1/welcome.scl"
    itemList = scl_file(sysArgv)

    finalList = []

    for lineTokens in itemList:
        tokens = tokenize(" ".join(lineTokens), tokenList)
        finalList.extend(tokens)

    megaDictionary = {}

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

    # creating output JSON file
    json_object = json.dumps(megaDictionary, indent=4)
    with open('OutputTokens.json', 'w') as f:
        f.write(json_object)
