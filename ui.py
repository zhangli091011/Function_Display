"""
用户界面（UI）
功能：使用 PyQt5 构建图形界面
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit, QTextEdit, 
                             QLabel, QSplitter)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, format_result
from derivative import Derivative, ast_to_string
from plotter import FunctionPlotter

class CalculatorWindow(QMainWindow):
    """计算器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_ast = None  # 当前函数的 AST
        self.derivative_ast = None  # 导函数的 AST
        self.result_index = 0  # 结果显示索引（用于多次按 = 切换显示）
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("数学函数计算器 - 教学版")
        self.setGeometry(100, 100, 1200, 800)
        
        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧：输入和按钮区域
        left_panel = self.create_left_panel()
        
        # 右侧：绘图区域
        right_panel = self.create_right_panel()
        
        # 使用分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
    
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 函数输入区
        layout.addWidget(QLabel("函数输入 f(x) ="))
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("例如: x^2 + sin(x)")
        layout.addWidget(self.function_input)
        
        # x 值输入区
        layout.addWidget(QLabel("x 值（数值计算用）"))
        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("例如: 3.14 或 pi")
        layout.addWidget(self.x_input)
        
        # 输出显示区
        layout.addWidget(QLabel("计算结果"))
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setMaximumHeight(150)
        layout.addWidget(self.output_display)
        
        # 按钮区域
        button_grid = self.create_button_grid()
        layout.addLayout(button_grid)
        
        layout.addStretch()
        return panel
    
    def create_button_grid(self):
        """创建按钮网格"""
        grid = QGridLayout()
        
        # 数字按钮
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 0), ('.', 3, 1), ('x', 3, 2),
        ]
        
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.insert_text(t))
            grid.addWidget(btn, row, col)
        
        # 运算符按钮
        operators = [
            ('+', 0, 3), ('-', 1, 3), ('*', 2, 3), ('/', 3, 3),
            ('^', 0, 4), ('(', 1, 4), (')', 2, 4),
        ]
        
        for text, row, col in operators:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.insert_text(t))
            grid.addWidget(btn, row, col)
        
        # 函数按钮
        func_row = 4
        func_buttons = [
            ('sin', 0), ('cos', 1), ('log', 2), ('π', 3), ('e', 4)
        ]
        
        for text, col in func_buttons:
            btn = QPushButton(text)
            if text in ['sin', 'cos', 'log']:
                btn.clicked.connect(lambda checked, t=text: self.insert_function(t))
            else:
                btn.clicked.connect(lambda checked, t=text: self.insert_text(t))
            grid.addWidget(btn, func_row, col)
        
        # 功能按钮
        control_row = 5
        self.calc_btn = QPushButton('= 计算')
        self.calc_btn.clicked.connect(self.calculate)
        grid.addWidget(self.calc_btn, control_row, 0, 1, 2)
        
        self.plot_btn = QPushButton('绘图')
        self.plot_btn.clicked.connect(self.plot_function)
        grid.addWidget(self.plot_btn, control_row, 2, 1, 2)
        
        self.clear_btn = QPushButton('清除')
        self.clear_btn.clicked.connect(self.clear_all)
        grid.addWidget(self.clear_btn, control_row, 4)
        
        # 求导按钮
        deriv_row = 6
        self.deriv_btn = QPushButton('求导')
        self.deriv_btn.clicked.connect(self.compute_derivative)
        grid.addWidget(self.deriv_btn, deriv_row, 0, 1, 2)
        
        self.plot_deriv_btn = QPushButton('绘制导函数')
        self.plot_deriv_btn.clicked.connect(self.plot_derivative)
        grid.addWidget(self.plot_deriv_btn, deriv_row, 2, 1, 3)
        
        # 光标移动按钮
        cursor_row = 7
        left_btn = QPushButton('←')
        left_btn.clicked.connect(self.move_cursor_left)
        grid.addWidget(left_btn, cursor_row, 0)
        
        right_btn = QPushButton('→')
        right_btn.clicked.connect(self.move_cursor_right)
        grid.addWidget(right_btn, cursor_row, 1)
        
        backspace_btn = QPushButton('退格')
        backspace_btn.clicked.connect(self.backspace)
        grid.addWidget(backspace_btn, cursor_row, 2, 1, 3)
        
        # 版权提示
        copyright_row = 8
        copyright_label = QLabel('© 2026 数学函数计算器 - 教学版  by 张力 Zennon')
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: gray; font-size: 14px;")
        grid.addWidget(copyright_label, copyright_row, 0, 2, 5)
        return grid
    
    def create_right_panel(self):
        """创建右侧绘图面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        layout.addWidget(QLabel("函数图像"))
        
        # 创建 Matplotlib 画布
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # 初始化绘图器
        self.plotter = FunctionPlotter(self.canvas)
        
        # 清除图像按钮
        clear_plot_btn = QPushButton('清除图像')
        clear_plot_btn.clicked.connect(self.clear_plot)
        layout.addWidget(clear_plot_btn)
        
        return panel
    
    # ========== 按钮事件处理 ==========
    
    def insert_text(self, text):
        """在光标位置插入文本"""
        cursor_pos = self.function_input.cursorPosition()
        current_text = self.function_input.text()
        new_text = current_text[:cursor_pos] + text + current_text[cursor_pos:]
        self.function_input.setText(new_text)
        self.function_input.setCursorPosition(cursor_pos + len(text))
        self.function_input.setFocus()
    
    def insert_function(self, func_name):
        """插入函数（自动添加括号）"""
        self.insert_text(func_name + '(')
    
    def move_cursor_left(self):
        """光标左移"""
        pos = self.function_input.cursorPosition()
        if pos > 0:
            self.function_input.setCursorPosition(pos - 1)
        self.function_input.setFocus()
    
    def move_cursor_right(self):
        """光标右移"""
        pos = self.function_input.cursorPosition()
        if pos < len(self.function_input.text()):
            self.function_input.setCursorPosition(pos + 1)
        self.function_input.setFocus()
    
    def backspace(self):
        """删除光标前的字符"""
        cursor_pos = self.function_input.cursorPosition()
        if cursor_pos > 0:
            current_text = self.function_input.text()
            new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
            self.function_input.setText(new_text)
            self.function_input.setCursorPosition(cursor_pos - 1)
        self.function_input.setFocus()
    
    def clear_all(self):
        """清除所有输入"""
        self.function_input.clear()
        self.x_input.clear()
        self.output_display.clear()
        self.current_ast = None
        self.derivative_ast = None
        self.result_index = 0
    
    def clear_plot(self):
        """清除图像"""
        self.plotter.clear()
    
    # ========== 核心功能 ==========
    
    def parse_expression(self, expr_text):
        """解析表达式为 AST"""
        try:
            # 预处理：将 π 和 pi 统一
            expr_text = expr_text.replace('π', 'pi')
            
            # 词法分析
            lexer = Lexer(expr_text)
            tokens = lexer.tokenize()
            
            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            
            return ast
        except Exception as e:
            self.show_error(f"表达式解析错误: {str(e)}")
            return None
    
    def parse_x_value(self, x_text):
        """解析 x 的值"""
        if not x_text:
            return None
        
        try:
            # 处理特殊常数
            x_text = x_text.strip().lower()
            if x_text == 'pi' or x_text == 'π':
                import math
                return math.pi
            elif x_text == 'e':
                import math
                return math.e
            else:
                return float(x_text)
        except:
            self.show_error(f"无效的 x 值: {x_text}")
            return None
    
    def calculate(self):
        """计算函数值"""
        expr_text = self.function_input.text().strip()
        if not expr_text:
            self.show_error("请输入函数表达式")
            return
        
        # 解析表达式
        ast = self.parse_expression(expr_text)
        if ast is None:
            return
        
        self.current_ast = ast
        
        # 获取 x 值
        x_text = self.x_input.text().strip()
        x_value = self.parse_x_value(x_text)
        
        if x_value is None:
            self.show_error("请输入有效的 x 值")
            return
        
        # 计算结果
        try:
            evaluator = Evaluator(x_value=x_value)
            result = evaluator.evaluate(ast)
            
            # 格式化输出
            formatted = format_result(result)
            
            output = f"f({x_text}) = {formatted}\n"
            output += f"（小数形式：{result:.6f}）"
            
            self.output_display.setText(output)
            
        except Exception as e:
            self.show_error(f"计算错误: {str(e)}")
    
    def plot_function(self):
        """绘制函数图像"""
        expr_text = self.function_input.text().strip()
        if not expr_text:
            self.show_error("请输入函数表达式")
            return
        
        # 解析表达式
        ast = self.parse_expression(expr_text)
        if ast is None:
            return
        
        self.current_ast = ast
        
        # 绘制函数
        try:
            self.plotter.plot_function(ast, label=f'f(x) = {expr_text}', 
                                      color='blue', linestyle='-')
            self.output_display.setText(f"已绘制函数: f(x) = {expr_text}")
        except Exception as e:
            self.show_error(f"绘图错误: {str(e)}")
    
    def compute_derivative(self):
        """计算导函数"""
        expr_text = self.function_input.text().strip()
        if not expr_text:
            self.show_error("请输入函数表达式")
            return
        
        # 解析表达式
        if self.current_ast is None:
            ast = self.parse_expression(expr_text)
            if ast is None:
                return
            self.current_ast = ast
        
        # 求导
        try:
            derivative_ast = Derivative.differentiate(self.current_ast)
            self.derivative_ast = derivative_ast
            
            # 转换为字符串
            derivative_str = ast_to_string(derivative_ast)
            
            output = f"原函数: f(x) = {expr_text}\n"
            output += f"导函数: f'(x) = {derivative_str}"
            
            self.output_display.setText(output)
            
        except Exception as e:
            self.show_error(f"求导错误: {str(e)}")
    
    def plot_derivative(self):
        """绘制导函数图像"""
        if self.derivative_ast is None:
            # 先计算导函数
            self.compute_derivative()
            if self.derivative_ast is None:
                return
        
        # 绘制导函数
        try:
            expr_text = self.function_input.text().strip()
            derivative_str = ast_to_string(self.derivative_ast)
            
            # 先绘制原函数
            if self.current_ast:
                self.plotter.plot_function(self.current_ast, 
                                          label=f'f(x) = {expr_text}',
                                          color='blue', linestyle='-')
            
            # 再绘制导函数
            self.plotter.plot_function(self.derivative_ast,
                                      label=f"f'(x) = {derivative_str}",
                                      color='red', linestyle='--')
            
            self.output_display.setText(f"已绘制原函数和导函数")
            
        except Exception as e:
            self.show_error(f"绘图错误: {str(e)}")
    
    def show_error(self, message):
        """显示错误信息"""
        self.output_display.setText(f"❌ 错误: {message}")
