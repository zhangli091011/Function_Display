"""
词法分析器（Lexer）
功能：将输入的数学表达式字符串转换为 Token 序列
"""
import re
from enum import Enum, auto

class TokenType(Enum):
    """Token 类型枚举"""
    NUMBER = auto()      # 数字
    VARIABLE = auto()    # 变量 x
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULTIPLY = auto()    # *
    DIVIDE = auto()      # /
    POWER = auto()       # ^
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    SIN = auto()         # sin
    COS = auto()         # cos
    LOG = auto()         # log
    PI = auto()          # π
    E = auto()           # e
    COMMA = auto()       # ,
    EOF = auto()         # 结束符

class Token:
    """Token 类：表示一个词法单元"""
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    """词法分析器"""
    def __init__(self, text):
        self.text = text.replace(' ', '')  # 移除空格
        self.pos = 0
        self.current_char = self.text[0] if self.text else None
    
    def error(self, msg="词法分析错误"):
        """抛出错误"""
        raise Exception(f"{msg} at position {self.pos}")
    
    def advance(self):
        """移动到下一个字符"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset=1):
        """向前查看字符，不移动位置"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def read_number(self):
        """读取数字（支持小数）"""
        num_str = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            num_str += self.current_char
            self.advance()
        return float(num_str)
    
    def read_identifier(self):
        """读取标识符（函数名或变量名）"""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result
    
    def tokenize(self):
        """将输入文本转换为 Token 列表"""
        tokens = []
        
        while self.current_char is not None:
            # 数字
            if self.current_char.isdigit() or self.current_char == '.':
                tokens.append(Token(TokenType.NUMBER, self.read_number()))
            
            # 标识符（函数名、变量、常数）
            elif self.current_char.isalpha():
                identifier = self.read_identifier()
                
                if identifier == 'x':
                    tokens.append(Token(TokenType.VARIABLE, 'x'))
                elif identifier == 'sin':
                    tokens.append(Token(TokenType.SIN))
                elif identifier == 'cos':
                    tokens.append(Token(TokenType.COS))
                elif identifier == 'log':
                    tokens.append(Token(TokenType.LOG))
                elif identifier == 'pi':
                    tokens.append(Token(TokenType.PI))
                elif identifier == 'e':
                    tokens.append(Token(TokenType.E))
                else:
                    self.error(f"未知标识符: {identifier}")
            
            # 运算符和括号
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MULTIPLY))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIVIDE))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TokenType.POWER))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TokenType.COMMA))
                self.advance()
            elif self.current_char == 'π':
                tokens.append(Token(TokenType.PI))
                self.advance()
            else:
                self.error(f"无效字符: {self.current_char}")
        
        tokens.append(Token(TokenType.EOF))
        return tokens
