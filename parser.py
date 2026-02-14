"""
语法分析器（Parser）
功能：将 Token 序列转换为抽象语法树（AST）
使用递归下降解析法，遵循运算优先级
"""
from lexer import Token, TokenType

class ASTNode:
    """抽象语法树节点基类"""
    pass

class NumberNode(ASTNode):
    """数字节点"""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"

class VariableNode(ASTNode):
    """变量节点"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"

class BinaryOpNode(ASTNode):
    """二元运算节点"""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"

class UnaryOpNode(ASTNode):
    """一元运算节点（如负号）"""
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.op} {self.operand})"

class FunctionNode(ASTNode):
    """函数节点"""
    def __init__(self, name, args):
        self.name = name
        self.args = args  # 参数列表
    
    def __repr__(self):
        return f"Func({self.name}, {self.args})"

class Parser:
    """语法分析器"""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
    
    def error(self, msg="语法分析错误"):
        """抛出错误"""
        raise Exception(f"{msg} at token {self.current_token}")
    
    def advance(self):
        """移动到下一个 Token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
    
    def parse(self):
        """解析入口"""
        return self.expression()
    
    def expression(self):
        """表达式：处理加减法（最低优先级）"""
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.type
            self.advance()
            node = BinaryOpNode(node, op, self.term())
        
        return node
    
    def term(self):
        """项：处理乘除法"""
        node = self.power()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token.type
            self.advance()
            node = BinaryOpNode(node, op, self.power())
        
        return node
    
    def power(self):
        """幂运算：处理 ^ 运算符（右结合）"""
        node = self.factor()
        
        if self.current_token.type == TokenType.POWER:
            self.advance()
            # 右结合：a^b^c = a^(b^c)
            node = BinaryOpNode(node, TokenType.POWER, self.power())
        
        return node
    
    def factor(self):
        """因子：处理数字、变量、函数、括号、一元运算符"""
        token = self.current_token
        
        # 一元负号
        if token.type == TokenType.MINUS:
            self.advance()
            return UnaryOpNode(TokenType.MINUS, self.factor())
        
        # 一元正号
        if token.type == TokenType.PLUS:
            self.advance()
            return self.factor()
        
        # 数字
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        # 变量 x
        if token.type == TokenType.VARIABLE:
            self.advance()
            return VariableNode(token.value)
        
        # 常数 π
        if token.type == TokenType.PI:
            self.advance()
            return NumberNode('π')
        
        # 常数 e
        if token.type == TokenType.E:
            self.advance()
            return NumberNode('e')
        
        # 括号表达式
        if token.type == TokenType.LPAREN:
            self.advance()
            node = self.expression()
            if self.current_token.type != TokenType.RPAREN:
                self.error("缺少右括号")
            self.advance()
            return node
        
        # 函数调用
        if token.type in (TokenType.SIN, TokenType.COS, TokenType.LOG):
            return self.function_call()
        
        self.error(f"无效的因子: {token}")
    
    def function_call(self):
        """函数调用：sin(x), cos(x), log(a, x)"""
        func_name = self.current_token.type
        self.advance()
        
        if self.current_token.type != TokenType.LPAREN:
            self.error("函数调用缺少左括号")
        self.advance()
        
        args = []
        
        # 解析参数
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.expression())
            
            # log 函数需要两个参数：log(a, x)
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                args.append(self.expression())
        
        if self.current_token.type != TokenType.RPAREN:
            self.error("函数调用缺少右括号")
        self.advance()
        
        return FunctionNode(func_name, args)
