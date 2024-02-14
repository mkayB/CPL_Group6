import re

keywords = ['CONSTANTS', 'VARIABLES', 'DEFINE', 'READ', 'DISPLAY', 'INPUT', 'RETURN', 'IF', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE', 'MBREAK', 'MEXIT']
operators = ['+', '-', '*', '/', '=', ':', '(', ')', ',', ';']

patterns = [
    (r'\b[a-zA-Z_]\w*\b', 'IDENTIFIER'),  # Matches identifiers
    (r'\b=\b', 'EQOP'),  # Matches the equals operator
    (r'\bTUNSIGNED|CHAR|INTEGER|MVOID\b', 'DATA_TYPE'),  # Matches data types
    (r'\[', 'LB'),  # Matches left square bracket
    (r'\]', 'RB'),  # Matches right square bracket
    (r'\+', 'PLUS'),  # Matches plus operator
    (r'-', 'MINUS'),  # Matches minus operator
    (r'\*', 'STAR'),  # Matches multiplication operator
    (r'/', 'DIVOP'),  # Matches division operator
    (r'RELOP', 'RELOP'),  # Placeholder for your relational operator
    (r',', 'COMMA'),  # Matches comma
    (r';', 'SEMICOLON'),  # Matches semicolon
    (r'\{', 'LB_BRACE'),  # Matches left brace
    (r'\}', 'RB_BRACE'),  # Matches right brace
    (r'\(', 'LP'),  # Matches left parenthesis
    (r'\)', 'RP'),  # Matches right parenthesis
    (r'MVOID', 'MVOID'),  # Matches MVOID
    (r'PBEGIN', 'PBEGIN'),  # Matches PBEGIN
    (r'ENDFUN', 'ENDFUN'),  # Matches ENDFUN
    (r'MTRUE', 'MTRUE'),  # Matches MTRUE
    (r'MFALSE', 'MFALSE'),  # Matches MFALSE
    (r'\d+', 'INTEGER'),  # Match integers
    (r'"(?:\\.|[^"])*"', 'STRING'),  # Match strings
    (r'\s+', None),  # Match whitespace (to be ignored)
]

