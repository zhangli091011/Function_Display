"""
符号求导器（Derivative）
功能：对 AST 进行符号求导，返回导函数的 AST
支持：幂函数、指数函数、对数函数、三角函数及其复合
"""
import math
from parser import *
from lexer import TokenType

class Derivative:
    """符号求导器"""
    
    @staticmethod
    def differentiate(node, var='x'):
        """
        对 AST 节点求导
        参数：
            node: AST 节点
            var: 求导变量（默认为 'x'）
        返回：导数的 AST 节点
        """
        if isinstance(node, NumberNode):
            # 常数的导数为 0
            return NumberNode(0)
        
        elif isinstance(node, VariableNode):
            # 变量的导数
            if node.name == var:
                return NumberNode(1)
            else:
                return NumberNode(0)
        
        elif isinstance(node, UnaryOpNode):
            # 一元运算：-(f) 的导数为 -(f')
            if node.op == TokenType.MINUS:
                return UnaryOpNode(TokenType.MINUS, 
                                 Derivative.differentiate(node.operand, var))
        
        elif isinstance(node, BinaryOpNode):
            return Derivative._diff_binary_op(node, var)
        
        elif isinstance(node, FunctionNode):
            return Derivative._diff_function(node, var)
        
        else:
            raise Exception(f"无法对节点类型 {type(node)} 求导")
    
    @staticmethod
    def _diff_binary_op(node, var):
        """二元运算求导"""
        left = node.left
        right = node.right
        left_prime = Derivative.differentiate(left, var)
        right_prime = Derivative.differentiate(right, var)
        
        if node.op == TokenType.PLUS:
            # (f + g)' = f' + g'
            return BinaryOpNode(left_prime, TokenType.PLUS, right_prime)
        
        elif node.op == TokenType.MINUS:
            # (f - g)' = f' - g'
            return BinaryOpNode(left_prime, TokenType.MINUS, right_prime)
        
        elif node.op == TokenType.MULTIPLY:
            # (f * g)' = f' * g + f * g'
            term1 = BinaryOpNode(left_prime, TokenType.MULTIPLY, right)
            term2 = BinaryOpNode(left, TokenType.MULTIPLY, right_prime)
            return BinaryOpNode(term1, TokenType.PLUS, term2)
        
        elif node.op == TokenType.DIVIDE:
            # (f / g)' = (f' * g - f * g') / g^2
            numerator_term1 = BinaryOpNode(left_prime, TokenType.MULTIPLY, right)
            numerator_term2 = BinaryOpNode(left, TokenType.MULTIPLY, right_prime)
            numerator = BinaryOpNode(numerator_term1, TokenType.MINUS, numerator_term2)
            denominator = BinaryOpNode(right, TokenType.POWER, NumberNode(2))
            return BinaryOpNode(numerator, TokenType.DIVIDE, denominator)
        
        elif node.op == TokenType.POWER:
            # 幂函数求导需要分情况
            return Derivative._diff_power(left, right, var)
    
    @staticmethod
    def _diff_power(base, exponent, var):
        """
        幂函数求导：f(x)^g(x)
        使用公式：(f^g)' = f^g * (g' * ln(f) + g * f'/f)
        特殊情况：
        - x^n: n * x^(n-1)
        - a^x: a^x * ln(a)
        """
        base_prime = Derivative.differentiate(base, var)
        exp_prime = Derivative.differentiate(exponent, var)
        
        # 检查是否为常数幂：x^n
        if Derivative._is_constant(exponent, var):
            # (f^n)' = n * f^(n-1) * f'
            new_exp = BinaryOpNode(exponent, TokenType.MINUS, NumberNode(1))
            power_part = BinaryOpNode(base, TokenType.POWER, new_exp)
            result = BinaryOpNode(exponent, TokenType.MULTIPLY, power_part)
            return BinaryOpNode(result, TokenType.MULTIPLY, base_prime)
        
        # 检查是否为常数底：a^x
        elif Derivative._is_constant(base, var):
            # (a^g)' = a^g * ln(a) * g'
            ln_base = FunctionNode(TokenType.LOG, [base])
            power_part = BinaryOpNode(base, TokenType.POWER, exponent)
            result = BinaryOpNode(power_part, TokenType.MULTIPLY, ln_base)
            return BinaryOpNode(result, TokenType.MULTIPLY, exp_prime)
        
        # 一般情况：f(x)^g(x)
        else:
            # (f^g)' = f^g * (g' * ln(f) + g * f'/f)
            ln_base = FunctionNode(TokenType.LOG, [base])
            term1 = BinaryOpNode(exp_prime, TokenType.MULTIPLY, ln_base)
            
            f_prime_over_f = BinaryOpNode(base_prime, TokenType.DIVIDE, base)
            term2 = BinaryOpNode(exponent, TokenType.MULTIPLY, f_prime_over_f)
            
            bracket = BinaryOpNode(term1, TokenType.PLUS, term2)
            power_part = BinaryOpNode(base, TokenType.POWER, exponent)
            
            return BinaryOpNode(power_part, TokenType.MULTIPLY, bracket)
    
    @staticmethod
    def _diff_function(node, var):
        """函数求导"""
        if node.name == TokenType.SIN:
            # sin(f)' = cos(f) * f'
            arg = node.args[0]
            arg_prime = Derivative.differentiate(arg, var)
            cos_node = FunctionNode(TokenType.COS, [arg])
            return BinaryOpNode(cos_node, TokenType.MULTIPLY, arg_prime)
        
        elif node.name == TokenType.COS:
            # cos(f)' = -sin(f) * f'
            arg = node.args[0]
            arg_prime = Derivative.differentiate(arg, var)
            sin_node = FunctionNode(TokenType.SIN, [arg])
            neg_sin = UnaryOpNode(TokenType.MINUS, sin_node)
            return BinaryOpNode(neg_sin, TokenType.MULTIPLY, arg_prime)
        
        elif node.name == TokenType.LOG:
            if len(node.args) == 1:
                # ln(f)' = f' / f
                arg = node.args[0]
                arg_prime = Derivative.differentiate(arg, var)
                return BinaryOpNode(arg_prime, TokenType.DIVIDE, arg)
            
            elif len(node.args) == 2:
                # log_a(f)' = f' / (f * ln(a))
                base = node.args[0]
                arg = node.args[1]
                arg_prime = Derivative.differentiate(arg, var)
                
                ln_base = FunctionNode(TokenType.LOG, [base])
                denominator = BinaryOpNode(arg, TokenType.MULTIPLY, ln_base)
                return BinaryOpNode(arg_prime, TokenType.DIVIDE, denominator)
    
    @staticmethod
    def _is_constant(node, var):
        """判断节点是否为常数（不含变量 var）"""
        if isinstance(node, NumberNode):
            return True
        elif isinstance(node, VariableNode):
            return node.name != var
        elif isinstance(node, UnaryOpNode):
            return Derivative._is_constant(node.operand, var)
        elif isinstance(node, BinaryOpNode):
            return (Derivative._is_constant(node.left, var) and 
                   Derivative._is_constant(node.right, var))
        elif isinstance(node, FunctionNode):
            return all(Derivative._is_constant(arg, var) for arg in node.args)
        return False

def ast_to_string(node):
    """将 AST 转换为可读的字符串表达式"""
    if isinstance(node, NumberNode):
        if node.value == 'π':
            return 'π'
        elif node.value == 'e':
            return 'e'
        elif isinstance(node.value, float):
            if node.value == int(node.value):
                return str(int(node.value))
            return str(node.value)
        return str(node.value)
    
    elif isinstance(node, VariableNode):
        return node.name
    
    elif isinstance(node, UnaryOpNode):
        operand_str = ast_to_string(node.operand)
        if node.op == TokenType.MINUS:
            # 如果操作数是复杂表达式，加括号
            if isinstance(node.operand, (BinaryOpNode, FunctionNode)):
                return f"-({operand_str})"
            return f"-{operand_str}"
    
    elif isinstance(node, BinaryOpNode):
        left_str = ast_to_string(node.left)
        right_str = ast_to_string(node.right)
        
        # 根据优先级决定是否加括号
        if node.op == TokenType.PLUS:
            return f"{left_str} + {right_str}"
        elif node.op == TokenType.MINUS:
            # 右侧如果是加减法，需要括号
            if isinstance(node.right, BinaryOpNode) and node.right.op in (TokenType.PLUS, TokenType.MINUS):
                return f"{left_str} - ({right_str})"
            return f"{left_str} - {right_str}"
        elif node.op == TokenType.MULTIPLY:
            # 左右如果是加减法，需要括号
            if isinstance(node.left, BinaryOpNode) and node.left.op in (TokenType.PLUS, TokenType.MINUS):
                left_str = f"({left_str})"
            if isinstance(node.right, BinaryOpNode) and node.right.op in (TokenType.PLUS, TokenType.MINUS):
                right_str = f"({right_str})"
            return f"{left_str} * {right_str}"
        elif node.op == TokenType.DIVIDE:
            if isinstance(node.left, BinaryOpNode) and node.left.op in (TokenType.PLUS, TokenType.MINUS):
                left_str = f"({left_str})"
            if isinstance(node.right, BinaryOpNode):
                right_str = f"({right_str})"
            return f"{left_str} / {right_str}"
        elif node.op == TokenType.POWER:
            if isinstance(node.left, BinaryOpNode):
                left_str = f"({left_str})"
            if isinstance(node.right, BinaryOpNode):
                right_str = f"({right_str})"
            return f"{left_str}^{right_str}"
    
    elif isinstance(node, FunctionNode):
        if node.name == TokenType.SIN:
            return f"sin({ast_to_string(node.args[0])})"
        elif node.name == TokenType.COS:
            return f"cos({ast_to_string(node.args[0])})"
        elif node.name == TokenType.LOG:
            if len(node.args) == 1:
                return f"ln({ast_to_string(node.args[0])})"
            else:
                return f"log({ast_to_string(node.args[0])}, {ast_to_string(node.args[1])})"
    
    return str(node)
