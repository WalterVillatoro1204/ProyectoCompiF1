import os
import re

class Lexer:
    def __init__(self, file_name):
        # Leer el archivo con el código fuente
        with open(file_name, 'r', encoding='utf-8') as file:
            self.source_code = file.read()

        # Lista para almacenar los tokens
        self.tokens = []
        self.current_position = 0

        # Definir patrones de tokens basados en tu gramática
        self.token_specs = [
            # Sets definidos
            ('LETTER', r'[A-Za-z_]'),  # letter = 'A'..'Z'+'a'..'z'+'_';
            ('DIGIT', r'[0-9]'),       # digit = '0'..'9';
            ('CHARSET', r'[\x20-\xFE]'),  # charset = chr(32)..chr(254);

            # Tokens definidos
            ('NUMBER', r'\d+'),  # number = digit digit*;
            ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),  # identifier = letter (letter|digit)*;
            ('STRING', r'"[^"]*"'),  # String constant

            # Operadores
            ('ASSIGN', r':='),  # Asignación
            ('EQ', r'='),       # Igual
            ('NEQ', r'<>'),     # Diferente
            ('LT', r'<'),       # Menor que
            ('GT', r'>'),       # Mayor que
            ('LTE', r'<='),     # Menor o igual que
            ('GTE', r'>='),     # Mayor o igual que
            ('PLUS', r'\+'),    # Suma
            ('MINUS', r'-'),    # Resta
            ('MUL', r'\*'),     # Multiplicación
            ('DIV', r'DIV'),    # División entera
            ('MOD', r'MOD'),    # Módulo
            ('OR', r'OR'),      # Operador lógico OR
            ('AND', r'AND'),    # Operador lógico AND
            ('NOT', r'NOT'),    # Operador lógico NOT
            ('SEMI', r';'),     # Punto y coma
            ('COMMA', r','),    # Coma
            ('LPAREN', r'\('),  # Paréntesis izquierdo
            ('RPAREN', r'\)'),  # Paréntesis derecho
            ('DOT', r'\.'),     # Punto

            # Epsilon (producción vacía)
            ('EPSILON', r'ε'),

            # Palabras clave
            ('KEYWORD', r'\b(PROGRAM|INCLUDE|CONST|TYPE|VAR|RECORD|ARRAY|OF|PROCEDURE|'
                        r'FUNCTION|IF|THEN|ELSE|FOR|TO|WHILE|DO|EXIT|END|PRINTLN|'
                        r'READLN|CASE|BREAK|DOWNTO|INTEGER|REAL|BOOLEAN|STRING|BEGIN)\b'),

            # Comentarios (multilínea)
            ('COMMENT', r'\(\*.*?\*\)'),

            # Espacios en blanco (se ignoran)
            ('WHITESPACE', r'[ \t]+'),

            # Nueva línea (se ignora)
            ('NEWLINE', r'\n'),

            # Cualquier cosa no válida
            ('MISMATCH', r'.')
        ]
        
        # Compilar las expresiones regulares
        self.token_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self.token_specs))

    def tokenize(self):
        """Convierte el código fuente en una lista de tokens."""
        for mo in self.token_re.finditer(self.source_code):
            kind = mo.lastgroup
            value = mo.group(kind)
            
            # Ignorar comentarios, espacios en blanco y nuevas líneas
            if kind in ['WHITESPACE', 'NEWLINE', 'COMMENT']:
                continue
            
            # Lanzar error si se encuentra un token no válido
            if kind == 'MISMATCH':
                raise RuntimeError(f"Token inesperado: {value}")
            
            # Agregar el token a la lista
            self.tokens.append((kind, value))
        
        return self.tokens

# Prueba del lexer
if __name__ == "__main__":
    # Usa solo el nombre del archivo ya que está en el mismo directorio
    file_path = "GramaticaPY1.txt"

    # Crear una instancia del lexer y analizar tu archivo
    lexer = Lexer(file_path)
    tokens = lexer.tokenize()

    # Imprimir los tokens generados
    print("Tokens generados:")
    for token in tokens:
        print(token)
