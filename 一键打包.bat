@echo off
chcp 65001 >nul
echo ========================================
echo   数学函数计算器 - 一键打包工具
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 检查 PyInstaller 是否安装
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 安装失败
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller 已就绪
echo.

REM 运行打包脚本
echo 🚀 开始打包...
echo.
python build_installer.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 打包完成！
echo ========================================
echo.
echo 📁 可执行文件位置: dist\数学函数计算器.exe
echo 📝 安装脚本位置: installer_script.iss
echo.
echo 💡 下一步：
echo    1. 测试可执行文件
echo    2. 使用 Inno Setup 编译安装脚本
echo.
pause
