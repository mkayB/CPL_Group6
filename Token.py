# Tokens
tokenList = {
    "keywords":{
        'import': 0,
        'implementations': 1,
        'function': 2,
        'main': 3,
        'return': 4,
        'type': 5,
        'integer': 6,
        'double': 7,
        'char': 8,
        'num': 9,
        'is': 10,
        'variables': 11,
        'define': 12,
        'of': 13,
        'begin': 14,
        'display': 15,
        'set': 16,
        'exit': 17,
        'endfun': 18,
        'symbol': 19,
        'end': 20,
        'input': 21,
        'structures': 22,
        'pointer': 23,
        'head': 24,
        'last': 25,
        'NULL': 26,
        'ChNode': 27,
        'using': 28,
        'reverse': 29,
        'while': 30,
        'endwhile': 31,
        'call': 32,
        'constants': 33,
        'float': 34,
        'array': 35,
        'for': 36,
        'to': 37,
        'do': 38,
        'endfor': 39,
        'forward': 40,
        'setup': 41,
        'declarations': 42,
        'loop': 43,
        'parameters': 44

    },

    "operators": {
        '+': 201,
        '-': 202,
        '*': 203,
        '/': 204,
        '^': 205,
        '>': 206,
        '<': 207,
        '=': 208,
        '(': 209,
        ')': 210,
        '.': 211
    },

    "specialSymbols": {
        ',': 400,
        '.': 401,
    }
}

class Token:
    def __init__(self, type, id, value):
        self.type = type
        self.id = id
        self.value = value

    def getData(self):
        return [self.type, self.id, self.value]
        
