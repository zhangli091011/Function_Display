@echo off
chcp 65001 >nul
echo ========================================
echo   数学函数计算器 - 启动程序
echo ========================================
echo.

echo 正在检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo Python 环境正常
echo.

echo 正在启动计算器...
python main.py

if errorlevel 1 (
    echo.
    echo [错误] 程序启动失败
    echo 可能原因：
    echo 1. 缺少依赖包，请运行: pip install -r requirements.txt
    echo 2. 代码文件损坏
    echo.
    pause
)
