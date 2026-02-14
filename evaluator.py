"""
表达式求值器（Evaluator）
功能：遍历 AST 并计算数值结果
"""
import math
from parser import *
from lexer import TokenType

class Evaluator:
    """表达式求值器"""
    def __init__(self, x_value=None):
        self.x_value = x_value  # 变量 x 的值
        self.symbolic_mode = (x_value is None)  # 是否为符号模式
    
    def evaluate(self, node):
        """递归求值 AST 节点"""
        if isinstance(node, NumberNode):
            return self.eval_number(node)
        elif isinstance(node, VariableNode):
            return self.eval_variable(node)
        elif isinstance(node, BinaryOpNode):
            return self.eval_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self.eval_unary_op(node)
        elif isinstance(node, FunctionNode):
            return self.eval_function(node)
        else:
            raise Exception(f"未知节点类型: {type(node)}")
    
    def eval_number(self, node):
        """求值数字节点"""
        if node.value == 'π':
            return math.pi
        elif node.value == 'e':
            return math.e
        else:
            return node.value
    
    def eval_variable(self, node):
        """求值变量节点"""
        if self.x_value is None:
            raise Exception("变量 x 未赋值")
        return self.x_value
    
    def eval_binary_op(self, node):
        """求值二元运算节点"""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        if node.op == TokenType.PLUS:
            return left + right
        elif node.op == TokenType.MINUS:
            return left - right
        elif node.op == TokenType.MULTIPLY:
            return left * right
        elif node.op == TokenType.DIVIDE:
            if right == 0:
                raise Exception("除数不能为零")
            return left / right
        elif node.op == TokenType.POWER:
            return left ** right
        else:
            raise Exception(f"未知运算符: {node.op}")
    
    def eval_unary_op(self, node):
        """求值一元运算节点"""
        operand = self.evaluate(node.operand)
        
        if node.op == TokenType.MINUS:
            return -operand
        else:
            raise Exception(f"未知一元运算符: {node.op}")
    
    def eval_function(self, node):
        """求值函数节点"""
        if node.name == TokenType.SIN:
            if len(node.args) != 1:
                raise Exception("sin 函数需要 1 个参数")
            arg = self.evaluate(node.args[0])
            return math.sin(arg)
        
        elif node.name == TokenType.COS:
            if len(node.args) != 1:
                raise Exception("cos 函数需要 1 个参数")
            arg = self.evaluate(node.args[0])
            return math.cos(arg)
        
        elif node.name == TokenType.LOG:
            if len(node.args) == 1:
                # log(x) 默认为自然对数
                arg = self.evaluate(node.args[0])
                if arg <= 0:
                    raise Exception("对数函数参数必须大于 0")
                return math.log(arg)
            elif len(node.args) == 2:
                # log(a, x) 表示以 a 为底 x 的对数
                base = self.evaluate(node.args[0])
                arg = self.evaluate(node.args[1])
                if base <= 0 or base == 1:
                    raise Exception("对数底数必须大于 0 且不等于 1")
                if arg <= 0:
                    raise Exception("对数函数参数必须大于 0")
                return math.log(arg, base)
            else:
                raise Exception("log 函数需要 1 或 2 个参数")
        
        else:
            raise Exception(f"未知函数: {node.name}")

def format_result(value, precision=4):
    """
    格式化输出结果
    优先级：整数 > 分数 > π/e 的倍数 > 小数
    """
    # 检查是否接近整数
    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    
    # 检查是否为 π 的倍数
    pi_ratio = value / math.pi
    if abs(pi_ratio - round(pi_ratio)) < 1e-10:
        coef = int(round(pi_ratio))
        if coef == 1:
            return "π"
        elif coef == -1:
            return "-π"
        else:
            return f"{coef}π"
    
    # 检查是否为 e 的倍数
    e_ratio = value / math.e
    if abs(e_ratio - round(e_ratio)) < 1e-10:
        coef = int(round(e_ratio))
        if coef == 1:
            return "e"
        elif coef == -1:
            return "-e"
        else:
            return f"{coef}e"
    
    # 尝试简单分数表示（分母 <= 100）
    for denom in range(2, 101):
        numer = value * denom
        if abs(numer - round(numer)) < 1e-10:
            numer = int(round(numer))
            # 简化分数
            from math import gcd
            g = gcd(abs(numer), denom)
            numer //= g
            denom //= g
            if denom == 1:
                return str(numer)
            return f"{numer}/{denom}"
    
    # 默认返回小数
    return f"{value:.{precision}f}"
