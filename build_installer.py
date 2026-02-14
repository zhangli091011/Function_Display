"""
打包脚本 - 生成 Windows 安装包
功能：使用 PyInstaller 打包程序，并生成 Inno Setup 安装脚本
"""
import os
import sys
import subprocess
import shutil

def clean_build():
    """清理旧的构建文件"""
    print("🧹 清理旧的构建文件...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   已删除: {dir_name}")
    
    # 删除 .spec 文件
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"   已删除: {spec_file}")

def build_executable():
    """使用 PyInstaller 打包可执行文件"""
    print("\n📦 开始打包可执行文件...")
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=数学函数计算器',
        '--windowed',  # 不显示控制台窗口
        '--onefile',   # 打包成单个文件
        '--icon=icon.ico',  # 图标（如果有）
        '--add-data=README.md;.',
        '--add-data=使用说明.md;.',
        '--add-data=快速参考.md;.',
        '--add-data=示例集合.md;.',
        '--hidden-import=PyQt5',
        '--hidden-import=matplotlib',
        '--hidden-import=numpy',
        'main.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ 未找到 PyInstaller，请先安装：pip install pyinstaller")
        return False

def create_inno_setup_script():
    """创建 Inno Setup 安装脚本"""
    print("\n📝 创建 Inno Setup 安装脚本...")
    
    script_content = """
; 数学函数计算器 - Inno Setup 安装脚本
; 自动生成于 build_installer.py

#define MyAppName "数学函数计算器"
#define MyAppVersion "1.0"
#define MyAppPublisher "数学教学工具开发组"
#define MyAppExeName "数学函数计算器.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=数学函数计算器_安装程序_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\\{#MyAppExeName}

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加图标:"; Flags: unchecked

[Files]
Source: "dist\\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "使用说明.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "快速参考.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "示例集合.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{group}\\使用说明"; Filename: "{app}\\使用说明.md"
Name: "{group}\\卸载 {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "立即运行 {#MyAppName}"; Flags: nowait postinstall skipifsilent
"""
    
    with open('installer_script.iss', 'w', encoding='utf-8-sig') as f:
        f.write(script_content)
    
    print("✅ Inno Setup 脚本已创建: installer_script.iss")

def main():
    """主函数"""
    print("=" * 60)
    print("  数学函数计算器 - 安装包构建工具")
    print("=" * 60)
    
    # 步骤 1：清理
    clean_build()
    
    # 步骤 2：打包可执行文件
    if not build_executable():
        print("\n❌ 构建失败，请检查错误信息")
        sys.exit(1)
    
    # 步骤 3：创建 Inno Setup 脚本
    create_inno_setup_script()
    
    print("\n" + "=" * 60)
    print("✅ 构建完成！")
    print("=" * 60)
    print("\n📁 输出文件：")
    print("   - 可执行文件: dist\\数学函数计算器.exe")
    print("   - Inno Setup 脚本: installer_script.iss")
    print("\n📌 下一步操作：")
    print("   1. 测试可执行文件: 运行 dist\\数学函数计算器.exe")
    print("   2. 生成安装包: 使用 Inno Setup 编译 installer_script.iss")
    print("   3. 安装 Inno Setup: https://jrsoftware.org/isdl.php")
    print("\n💡 提示：")
    print("   - 如需添加图标，请准备 icon.ico 文件")
    print("   - 安装包将生成在 installer_output 目录")

if __name__ == "__main__":
    main()
