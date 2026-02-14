"""
函数计算器主程序入口
作者：数学教学工具开发组
功能：启动 PyQt5 应用程序
"""
import sys
from PyQt5.QtWidgets import QApplication
from ui import CalculatorWindow

def main():
    """主函数：创建并运行应用程序"""
    app = QApplication(sys.argv)
    app.setApplicationName("数学函数计算器")
    
    window = CalculatorWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
