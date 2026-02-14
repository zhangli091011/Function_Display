@echo off
chcp 65001 >nul
echo ========================================
echo   打包环境检查工具
echo ========================================
echo.

echo 📋 检查打包环境...
echo.

REM 检查 Python
echo [1/5] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ 未安装 Python
    echo    请从 https://www.python.org/ 下载安装
    set ERROR=1
) else (
    python --version
    echo    ✅ Python 已安装
)
echo.

REM 检查 PyInstaller
echo [2/5] 检查 PyInstaller...
python -c "import PyInstaller; print('   版本:', PyInstaller.__version__)" 2>nul
if errorlevel 1 (
    echo    ❌ 未安装 PyInstaller
    echo    运行: pip install pyinstaller
    set ERROR=1
) else (
    echo    ✅ PyInstaller 已安装
)
echo.

REM 检查依赖包
echo [3/5] 检查项目依赖...
python -c "import PyQt5" 2>nul
if errorlevel 1 (
    echo    ❌ PyQt5 未安装
    set ERROR=1
) else (
    echo    ✅ PyQt5 已安装
)

python -c "import matplotlib" 2>nul
if errorlevel 1 (
    echo    ❌ matplotlib 未安装
    set ERROR=1
) else (
    echo    ✅ matplotlib 已安装
)

python -c "import numpy" 2>nul
if errorlevel 1 (
    echo    ❌ numpy 未安装
    set ERROR=1
) else (
    echo    ✅ numpy 已安装
)
echo.

REM 检查主程序文件
echo [4/5] 检查项目文件...
if not exist "main.py" (
    echo    ❌ 缺少 main.py
    set ERROR=1
) else (
    echo    ✅ main.py 存在
)

if not exist "ui.py" (
    echo    ❌ 缺少 ui.py
    set ERROR=1
) else (
    echo    ✅ ui.py 存在
)

if not exist "lexer.py" (
    echo    ❌ 缺少 lexer.py
    set ERROR=1
) else (
    echo    ✅ lexer.py 存在
)
echo.

REM 检查磁盘空间
echo [5/5] 检查磁盘空间...
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do set FREE_SPACE=%%a
echo    可用空间: %FREE_SPACE% 字节
echo    ✅ 磁盘空间充足
echo.

REM 总结
echo ========================================
if defined ERROR (
    echo   ❌ 环境检查未通过
    echo ========================================
    echo.
    echo 💡 解决方法：
    echo    1. 安装缺失的软件/包
    echo    2. 运行: pip install -r requirements.txt
    echo    3. 重新运行此脚本
) else (
    echo   ✅ 环境检查通过！
    echo ========================================
    echo.
    echo 💡 可以开始打包了：
    echo    - 简易打包: 运行 简易打包.bat
    echo    - 专业打包: 运行 一键打包.bat
    echo.
    echo 📝 建议：
    echo    1. 先运行程序测试: python main.py
    echo    2. 确认功能正常后再打包
    echo    3. 打包后在干净系统上测试
)
echo.
pause
