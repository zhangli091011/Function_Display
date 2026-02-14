@echo off
chcp 65001 >nul
echo ========================================
echo   数学函数计算器 - 简易打包
echo   （不需要 Inno Setup）
echo ========================================
echo.

REM 检查 PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装 PyInstaller...
    pip install pyinstaller
)

echo 🚀 开始打包...
echo.

REM 打包命令
pyinstaller --name=数学函数计算器 ^
            --windowed ^
            --onefile ^
            --add-data=README.md;. ^
            --add-data=使用说明.md;. ^
            --hidden-import=PyQt5 ^
            --hidden-import=matplotlib ^
            --hidden-import=numpy ^
            main.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 打包完成！
echo ========================================
echo.
echo 📁 可执行文件: dist\数学函数计算器.exe
echo.
echo 💡 现在可以：
echo    1. 测试运行: dist\数学函数计算器.exe
echo    2. 分发文件: 将 dist 文件夹打包成 ZIP
echo.

REM 创建分发包
echo 📦 正在创建分发包...
if exist "数学函数计算器_v1.0.zip" del "数学函数计算器_v1.0.zip"

REM 复制文件到临时目录
if exist temp_dist rmdir /s /q temp_dist
mkdir temp_dist
copy "dist\数学函数计算器.exe" temp_dist\
copy "README.md" temp_dist\
copy "使用说明.md" temp_dist\
copy "快速参考.md" temp_dist\
copy "示例集合.md" temp_dist\

REM 创建启动说明
echo 数学函数计算器 > temp_dist\启动说明.txt
echo ================== >> temp_dist\启动说明.txt
echo. >> temp_dist\启动说明.txt
echo 双击运行: 数学函数计算器.exe >> temp_dist\启动说明.txt
echo. >> temp_dist\启动说明.txt
echo 首次运行可能需要几秒钟加载。 >> temp_dist\启动说明.txt
echo. >> temp_dist\启动说明.txt
echo 详细使用说明请查看: 使用说明.md >> temp_dist\启动说明.txt

REM 使用 PowerShell 压缩
powershell -command "Compress-Archive -Path temp_dist\* -DestinationPath 数学函数计算器_v1.0.zip -Force"

if exist "数学函数计算器_v1.0.zip" (
    echo ✅ 分发包已创建: 数学函数计算器_v1.0.zip
    rmdir /s /q temp_dist
) else (
    echo ⚠️  无法创建 ZIP 文件，请手动压缩 temp_dist 文件夹
)

echo.
pause
