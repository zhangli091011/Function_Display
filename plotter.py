"""
函数绘图器（Plotter）
功能：使用 Matplotlib 绘制函数图像
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from evaluator import Evaluator

class FunctionPlotter:
    """函数绘图器"""
    
    def __init__(self, canvas):
        """
        初始化绘图器
        参数：
            canvas: Matplotlib 画布对象
        """
        self.canvas = canvas
        self.figure = canvas.figure
        self.ax = self.figure.add_subplot(111)
        self.setup_axes()
        self.plots = []  # 存储绘制的曲线
    
    def setup_axes(self):
        """设置坐标轴"""
        self.ax.axhline(y=0, color='k', linewidth=0.5)  # x 轴
        self.ax.axvline(x=0, color='k', linewidth=0.5)  # y 轴
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
    
    def plot_function(self, ast, x_range=(-10, 10), num_points=1000, 
                     label='f(x)', color='blue', linestyle='-'):
        """
        绘制函数图像
        参数：
            ast: 函数的抽象语法树
            x_range: x 的取值范围
            num_points: 采样点数
            label: 曲线标签
            color: 曲线颜色
            linestyle: 线型
        """
        x_values = np.linspace(x_range[0], x_range[1], num_points)
        y_values = []
        
        for x in x_values:
            try:
                evaluator = Evaluator(x_value=x)
                y = evaluator.evaluate(ast)
                # 过滤无效值
                if np.isnan(y) or np.isinf(y):
                    y_values.append(None)
                else:
                    y_values.append(y)
            except:
                y_values.append(None)
        
        # 绘制曲线（自动处理 None 值）
        line, = self.ax.plot(x_values, y_values, label=label, 
                            color=color, linestyle=linestyle, linewidth=2)
        self.plots.append(line)
        
        # 更新图例
        self.ax.legend()
        self.canvas.draw()
    
    def clear(self):
        """清除所有图像"""
        self.ax.clear()
        self.setup_axes()
        self.plots = []
        self.canvas.draw()
    
    def set_range(self, x_range, y_range=None):
        """设置坐标轴范围"""
        self.ax.set_xlim(x_range)
        if y_range:
            self.ax.set_ylim(y_range)
        self.canvas.draw()
