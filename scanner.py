# from Token import *  # Import Token class from Tokens.py
# import json
# import sys
# import re

# def tokenize(line, tokenList):
#     tokens = []

#     # Define token types and their corresponding regular expressions
#     token_types = {
#         "StringLiteral": r'("[^"]*"|\'[^\']*\')',
#         "MultiLineComment": r'/\*.*?\*/',
#         "SingleLineComment": r'//.*',
#         "Keyword": r'\b(import|implementations|function|main|is|variables|define|of|begin|display|set|input|if|then|else|endif|not|greater|or|equal|return)\b',
#         "Identifier": r'[a-zA-Z_]\w*',
#         "NumericLiteral": r'\d+(\.\d+)?',
#         "Operator": r':|\.|:|,|/|=|>|\*|\)|\('
#     }

#     combined_regex = "|".join(f"({regex})" for regex in token_types.values())
#     match_objects = re.finditer(combined_regex, line)

#     for match_regex in match_objects:
#         token = next(filter(None, match_regex.groups()))  # Pick the non-empty match

#         if token.strip() == "":
#             continue

#         token_type = categorize_token(token, tokenList)
#         newToken = Token(token_type["Type"], token_type["id"], token)
#         tokens.append(newToken)
#         print("New Token created:", newToken.getData())

#     return tokens

# def categorize_token(token, tokenList):
#     if token in tokenList["keywords"]:
#         return {"Type": "Keyword", "id": tokenList["keywords"][token], "value": token}
#     elif re.match(r'^[a-zA-Z_]\w*$', token):
#         return {"Type": "Identifier", "id": 4000, "value": token}
#     elif re.match(r'^[0-9]+(\.[0-9]+)?$', token):
#         return {"Type": "NumericLiteral", "id": 5000, "value": token}
#     elif token.startswith('"') or token.startswith("'"):
#         cleaned_token = token[1:-1].replace('\\"', '"').replace("\\'", "'").replace("\\/", "/")
#         return {"Type": "StringLiteral", "id": 6000, "value": cleaned_token}
#     elif token in tokenList["operators"]:
#         return {"Type": "Operator", "id": tokenList["operators"][token], "value": token}
#     elif token in tokenList["specialSymbols"]:
#         return {"Type": "SpecialSymbol", "id": tokenList["specialSymbols"][token], "value": token}
#     else:
#         return {"Type": "UNKNOWN", "id": 7000, "value": token}

# def scl_file(name_file):
#     try:
#         file = open(name_file, 'r')
#     except:
#         print("no such file or directory: ", name_file)
#         exit(2)

#     lineArray = []

#     inline_comment = False  # makes sure not inside inline comment

#     for line in file:
#         if 'description' in line:
#             inline_comment = True

#         if inline_comment:
#             if '*/' in line:
#                 inline_comment = False
#             continue  # skips the lines within inline comments
#         else:
#             if line.startswith("/*"):
#                 continue  # skips the comment line

#             inlineTokens = tokenize(line, tokenList)

#             # removes blank tokens
#             inlineTokens = [token for token in inlineTokens if token.value.strip() != '']

#             if inlineTokens:
#                 lineArray.append(inlineTokens)

#     return lineArray

# if __name__ == '__main__':
#     sysArgv = "/Users/briannanoel/PycharmProjects/deliverable1/welcome.scl"
#     itemList = scl_file(sysArgv)

#     finalList = []

#     for lineTokens in itemList:
#         tokens = tokenize(" ".join(lineTokens), tokenList)
#         finalList.extend(tokens)

#     megaDictionary = {}

#     loopCounter = 0
#     for Token in finalList:
#         tokenString = "Token_" + str(loopCounter)

#         # make dictionary for token
#         tokenInfo = Token.getData()
#         tokenDictionary = {
#             "Type": tokenInfo[0],
#             "id": tokenInfo[1],
#             "value": tokenInfo[2]
#         }

#         # add the token dictionary to the megaDictionary
#         megaDictionary[tokenString] = tokenDictionary

#         loopCounter += 1

#     # creating output JSON file
#     json_object = json.dumps(megaDictionary, indent=4)
#     with open('OutputTokens.json', 'w') as f:
#         f.write(json_object)

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

    # group together all regular expressions
    #regular_expressions = r'("[^"]*"|\'[^\']*\')|(/\*.*?\*/)|(//.*)|(\b(import|implementations|function|main|is|variables|define|of|begin|display|set|input|if|then|else|endif|not|greater|or|equal|return)\b)|([a-zA-Z_]\w*)|(\d+(\.\d+)?)|(:|\.|:|,|/|=|>|\*|\)|\()'

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


# categorizes tokens
def categorize(token):
    global counter

    if token in tokenList["keywords"]:
        return {"Type": "Keyword", "id": tokenList["keywords"][str(token)], "value": token}
    elif re.match(r'^[a-zA-Z_]\w*$', token):
        # increment ID's
        # gives every identifier an unique id
        if token in map:
            return {"Type": "Identifier", "id": map[token], "value": token}

        result = {"Type": "Identifier", "id": counter, "value": token}
        map[token] = counter
        counter += 1
        return result
    elif re.match(r'^[0-9]+(\.[0-9]+)?$', token):
        return {"Type": "NumericLiteral", "id": 4000, "value": token}
    elif token.startswith('"') or token.startswith("'"):
        #gets rid of extra quotes
        cleaned_token = token[1:-1].replace('\\"', '"').replace("\\'", "'").replace("\\/", "/")
        return {"Type": "StringLiteral", "id": 5000, "value": cleaned_token}
    elif token in [",", "="]:
        return {"Type": "Operator", "id": 400, "value": token}
    elif token in tokenList["operators"]:
        return {"Type": "Operator", "id": tokenList["operators"][str(token)], "value": token}
    elif token == ":":
        return {"Type": "VariableDeclaration", "id": 6002, "value": token}
    # additional conditions for other kinds of tokens

    # unknown token if previous conditions are untrue
    return {"Type": "UNKNOWN", "id": 1200, "value": token}


if __name__ == '__main__':
    sysArgv = "/Users/briannanoel/PycharmProjects/deliverable1/welcome.scl"

    itemList = scl_file(sysArgv)

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
