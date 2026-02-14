"""
测试脚本：验证计算器核心功能
"""
import math
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, format_result
from derivative import Derivative, ast_to_string

def test_expression(expr, x_value=None):
    """测试表达式解析和计算"""
    print(f"\n{'='*60}")
    print(f"测试表达式: {expr}")
    if x_value is not None:
        print(f"x = {x_value}")
    
    try:
        # 词法分析
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        print(f"Tokens: {[str(t) for t in tokens[:5]]}")  # 只显示前5个
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"AST: {ast}")
        
        # 数值计算
        if x_value is not None:
            evaluator = Evaluator(x_value=x_value)
            result = evaluator.evaluate(ast)
            formatted = format_result(result)
            print(f"结果: {formatted} (小数: {result:.6f})")
        
        # 求导
        derivative_ast = Derivative.differentiate(ast)
        derivative_str = ast_to_string(derivative_ast)
        print(f"导函数: f'(x) = {derivative_str}")
        
        print("✅ 测试通过")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

def main():
    """运行测试"""
    print("数学函数计算器 - 核心功能测试")
    print("="*60)
    
    # 测试用例
    test_cases = [
        ("x^2", 3),
        ("x^2 + sin(x)", math.pi),
        ("2^x", 3),
        ("sin(x) + cos(x)", 0),
        ("log(x)", math.e),
        ("x^3 + 2*x^2 - 5*x + 1", 2),
        ("sin(x^2)", 1),
    ]
    
    for expr, x_val in test_cases:
        test_expression(expr, x_val)
    
    print(f"\n{'='*60}")
    print("所有测试完成！")

if __name__ == "__main__":
    main()
