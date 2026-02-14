@echo off
chcp 65001 >nul
echo ========================================
echo   数学函数计算器 - 依赖安装
echo ========================================
echo.

echo 正在检查 Python 环境...
python --version
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请从 https://www.python.org/ 下载并安装 Python 3.7+
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    echo 请检查网络连接或尝试使用国内镜像源：
    echo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   依赖安装完成！
echo ========================================
echo.
echo 现在可以运行 启动程序.bat 来启动计算器
echo.
pause
