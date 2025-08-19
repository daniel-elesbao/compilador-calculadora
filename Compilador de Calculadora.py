#Compilador de Calculadora
#Trabalho de Compiladores

import re
import sys
import argparse
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any
from abc import ABC, abstractmethod

# ======================== LEXER ========================

class TokenType(Enum):
    # Literais
    NUMERO = "NUMERO"
    IDENTIFICADOR = "IDENTIFICADOR"
    
    # Operadores aritméticos
    MAIS = "MAIS"
    MENOS = "MENOS"
    VEZES = "VEZES"
    DIVIDIR = "DIVIDIR"
    POTENCIA = "POTENCIA"
    
    # Operador de atribuição
    IGUAL = "IGUAL"
    
    # Delimitadores
    PARENTESESESQ = "PARENTESES ESQUERDO"
    PARENTESESDIR = "PARENTESES DIREITO"
    PONTOEVIRGULA = "PONTO E VIRGULA"
    
    # Palavras-chave
    LEIA = "LEIA"
    IMPRIMA = "IMPRIMA"
    
    # Especiais
    EOF = "FIM DE ARQUIVO"
    NEWLINE = "NOVA LINHA"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class LexicalError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro léxico na linha {line}, coluna {column}: {message}")

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char() in ' \t\r':
            self.advance()
    
    def read_number(self) -> str:
        result = ""
        start_column = self.column
        
        while self.current_char() is not None and self.current_char().isdigit():
            result += self.current_char()
            self.advance()
        
        if self.current_char() == '.':
            result += self.current_char()
            self.advance()
            
            if self.current_char() is None or not self.current_char().isdigit():
                raise LexicalError("Número decimal mal formado", self.line, start_column)
            
            while self.current_char() is not None and self.current_char().isdigit():
                result += self.current_char()
                self.advance()
        
        return result
    
    def read_identifier(self) -> str:
        result = ""
        
        # Primeiro caractere deve ser letra ou underscore
        if self.current_char().isalpha() or self.current_char() == '_':
            result += self.current_char()
            self.advance()
        
        # Caracteres seguintes podem ser letras, dígitos ou underscore
        while (self.current_char() is not None and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            result += self.current_char()
            self.advance()
        
        return result
    
    def tokenize(self) -> List[Token]:
        keywords = {
            'leia': TokenType.LEIA,
            'imprima': TokenType.IMPRIMA
        }
        
        while self.current_char() is not None:
            char = self.current_char()
            
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                continue
            
            if char.isdigit():
                number = self.read_number()
                self.tokens.append(Token(TokenType.NUMERO, number, self.line, self.column - len(number)))
                continue
            
            if char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = keywords.get(identifier.lower(), TokenType.IDENTIFICADOR)
                self.tokens.append(Token(token_type, identifier, self.line, self.column - len(identifier)))
                continue
            
            # Operadores e delimitadores
            token_map = {
                '+': TokenType.MAIS,
                '-': TokenType.MENOS,
                '*': TokenType.VEZES,
                '/': TokenType.DIVIDIR,
                '^': TokenType.POTENCIA,
                '=': TokenType.IGUAL,
                '(': TokenType.PARENTESESESQ,
                ')': TokenType.PARENTESESDIR,
                ';': TokenType.PONTOEVIRGULA
            }
            
            if char in token_map:
                self.tokens.append(Token(token_map[char], char, self.line, self.column))
                self.advance()
                continue
            
            # Caractere inválido
            raise LexicalError(f"Caractere inválido: '{char}'", self.line, self.column)
        
        # Adiciona token EOF
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    # ======================== PARSER ========================

class ASTNode(ABC):
    pass

@dataclass
class NumberNode(ASTNode):
    value: float

@dataclass
class VariableNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class AssignmentNode(ASTNode):
    variable: str
    expression: ASTNode

@dataclass
class ReadNode(ASTNode):
    variable: str

@dataclass
class PrintNode(ASTNode):
    expression: ASTNode

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

class SyntaxError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Erro sintático na linha {token.line}, coluna {token.column}: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, "", 0, 0)
    
    def expect(self, token_type: TokenType) -> Token:
        if self.current_token.type != token_type:
            raise SyntaxError(f"Esperado {token_type.value}, encontrado {self.current_token.type.value}", 
                            self.current_token)
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> ProgramNode:
        return self.program()
    
    def program(self) -> ProgramNode:
        statements = []
        self.skip_newlines()
        
        while self.current_token.type != TokenType.EOF:
            stmt = self.statement()
            statements.append(stmt)
            
            if self.current_token.type == TokenType.PONTOEVIRGULA:
                self.advance()
            
            self.skip_newlines()
        
        return ProgramNode(statements)
    
    def statement(self) -> ASTNode:
        if self.current_token.type == TokenType.LEIA:
            return self.read_stmt()
        elif self.current_token.type == TokenType.IMPRIMA:
            return self.print_stmt()
        elif (self.current_token.type == TokenType.IDENTIFICADOR and 
              self.pos + 1 < len(self.tokens) and 
              self.tokens[self.pos + 1].type == TokenType.IGUAL):
            return self.assignment()
        else:
            return self.expression()
    
    def assignment(self) -> AssignmentNode:
        var_token = self.expect(TokenType.IDENTIFICADOR)
        self.expect(TokenType.IGUAL)
        expr = self.expression()
        return AssignmentNode(var_token.value, expr)
    
    def read_stmt(self) -> ReadNode:
        self.expect(TokenType.LEIA)
        self.expect(TokenType.PARENTESESESQ)
        var_token = self.expect(TokenType.IDENTIFICADOR)
        self.expect(TokenType.PARENTESESDIR)
        return ReadNode(var_token.value)
    
    def print_stmt(self) -> PrintNode:
        self.expect(TokenType.IMPRIMA)
        self.expect(TokenType.PARENTESESESQ)
        expr = self.expression()
        self.expect(TokenType.PARENTESESDIR)
        return PrintNode(expr)
    
    def expression(self) -> ASTNode:
        node = self.term()
        
        while self.current_token.type in [TokenType.MAIS, TokenType.MENOS]:
            op_token = self.current_token
            self.advance()
            right = self.term()
            node = BinaryOpNode(node, op_token.value, right)
        
        return node
    
    def term(self) -> ASTNode:
        node = self.power()
        
        while self.current_token.type in [TokenType.VEZES, TokenType.DIVIDIR]:
            op_token = self.current_token
            self.advance()
            right = self.power()
            node = BinaryOpNode(node, op_token.value, right)
        
        return node
    
    def power(self) -> ASTNode:
        node = self.factor()
        
        # Potenciação é associativa à direita
        if self.current_token.type == TokenType.POTENCIA:
            op_token = self.current_token
            self.advance()
            right = self.power()  # Recursão à direita para associatividade
            node = BinaryOpNode(node, op_token.value, right)
        
        return node
    
    def factor(self) -> ASTNode:
        token = self.current_token
        
        if token.type in [TokenType.MAIS, TokenType.MENOS]:
            self.advance()
            node = self.factor()
            return UnaryOpNode(token.value, node)
        
        elif token.type == TokenType.PARENTESESESQ:
            self.advance()
            node = self.expression()
            self.expect(TokenType.PARENTESESDIR)
            return node
        
        elif token.type == TokenType.NUMERO:
            self.advance()
            return NumberNode(float(token.value))
        
        elif token.type == TokenType.IDENTIFICADOR:
            self.advance()
            return VariableNode(token.value)
        
        else:
            raise SyntaxError(f"Token inesperado: {token.type.value}", token)
    
# ======================== INTERPRETER ========================

class RuntimeError(Exception):
    def __init__(self, message: str, node: ASTNode = None):
        self.message = message
        self.node = node
        super().__init__(message)

class Interpreter:
    def __init__(self):
        self.variables: Dict[str, float] = {}
    
    def interpret(self, node: ASTNode) -> Any:
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode):
        raise RuntimeError(f'Nenhum método visit_{node.__class__.__name__}')
    
    def visit_ProgramNode(self, node: ProgramNode) -> None:
        for statement in node.statements:
            result = self.interpret(statement)
            if isinstance(statement, (NumberNode, VariableNode, BinaryOpNode, UnaryOpNode)):
                print(f"Resultado: {result}")
    
    def visit_NumberNode(self, node: NumberNode) -> float:
        return node.value
    
    def visit_VariableNode(self, node: VariableNode) -> float:
        if node.name not in self.variables:
            raise RuntimeError(f"Variável '{node.name}' não foi definida")
        return self.variables[node.name]
    
    def visit_BinaryOpNode(self, node: BinaryOpNode) -> float:
        left = self.interpret(node.left)
        right = self.interpret(node.right)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise RuntimeError("Divisão por zero")
            return left / right
        elif node.operator == '^':
            return left ** right
        else:
            raise RuntimeError(f"Operador desconhecido: {node.operator}")
    
    def visit_UnaryOpNode(self, node: UnaryOpNode) -> float:
        operand = self.interpret(node.operand)
        
        if node.operator == '+':
            return +operand
        elif node.operator == '-':
            return -operand
        else:
            raise RuntimeError(f"Operador desconhecido: {node.operator}")
    
    def visit_AssignmentNode(self, node: AssignmentNode) -> None:
        value = self.interpret(node.expression)
        self.variables[node.variable] = value
        print(f"{node.variable} = {value}")
    
    def visit_ReadNode(self, node: ReadNode) -> None:
        try:
            value = float(input(f"Digite o valor para {node.variable}: "))
            self.variables[node.variable] = value
            print(f"{node.variable} = {value}")
        except ValueError:
            raise RuntimeError("Valor inválido. Digite um número.")
    
    def visit_PrintNode(self, node: PrintNode) -> None:
        value = self.interpret(node.expression)
        print(value)

# ======================== COMPILADOR ========================

class CalculatorCompiler:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.interpreter = Interpreter()
    
    def compile_and_run(self, source_code: str):
        """Compila e executa o código fonte"""
        try:
            print("=== ANÁLISE LÉXICA ===")
            self.lexer = Lexer(source_code)
            tokens = self.lexer.tokenize()
            
            print("Tokens encontrados:")
            for i, token in enumerate(tokens):
                if token.type != TokenType.EOF:
                    print(f"{i+1:2}: {token.type.value:12} '{token.value}' (linha {token.line}, coluna {token.column})")
            print()
            
            # Análise sintática
            print("=== ANÁLISE SINTÁTICA ===")
            self.parser = Parser(tokens)
            ast = self.parser.parse()
            print("Análise sintática concluída com sucesso!")
            print()
            
            # Execução
            print("=== EXECUÇÃO ===")
            self.interpreter.interpret(ast)
            
        except (LexicalError, SyntaxError, RuntimeError) as e:
            print(f"ERRO: {e}")
            return False
        except Exception as e:
            print(f"ERRO INTERNO: {e}")
            return False
        
        return True
    
    def run_interactive(self):
        print("=== CALCULADORA INTERATIVA ===")
        print("Digite 'sair' para sair")
        print("Exemplos:")
        print("  x = 10")
        print("  y = x + 5")
        print("  imprima(x * y)")
        print("  leia(z)")
        print()
        
        while True:
            try:
                line = input("calc> ").strip()
                if line.lower() in ['quit', 'exit', 'sair', 'end', 'fim', 'stop', 'break', 'return'] :
                    break
                if not line:
                    continue
                
                self.compile_and_run(line)
                print()
                
            except KeyboardInterrupt:
                print("\nSaindo...")
                break
            except EOFError:
                break
            
    
    def run_file(self, filename: str):
        """Executa arquivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                source_code = file.read()
            
            print(f"=== EXECUTANDO ARQUIVO: {filename} ===")
            success = self.compile_and_run(source_code)
            
            if success:
                print("\nExecução concluída com sucesso!")
            else:
                print("\nExecução falhou!")
                sys.exit(1)
                
        except FileNotFoundError:
            print(f"ERRO: Arquivo '{filename}' não encontrado")
            sys.exit(1)
        except Exception as e:
            print(f"ERRO ao ler arquivo: {e}")
            sys.exit(1) 

def main():
    parser = argparse.ArgumentParser(description='Compilador de Calculadora')
    parser.add_argument('file', nargs='?', help='Arquivo para executar')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Modo interativo')
    
    args = parser.parse_args()
    
    compiler = CalculatorCompiler()
    
    if args.file:
        compiler.run_file(args.file)
    elif args.interactive:
        compiler.run_interactive()
    else:
        compiler.run_interactive()

if __name__ == "__main__":
    main()