"""
创建简单的程序图标
使用 PIL 库生成一个带有 f(x) 文字的图标
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_icon():
        """创建一个简单的图标"""
        # 创建 256x256 的图像
        size = 256
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形背景
        margin = 20
        draw.ellipse([margin, margin, size-margin, size-margin], 
                     fill=(52, 152, 219, 255))  # 蓝色
        
        # 绘制文字 f(x)
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            # 如果找不到字体，使用默认字体
            font = ImageFont.load_default()
        
        text = "f(x)"
        # 获取文字边界框
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 居中绘制文字
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 10
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # 保存为 PNG
        img.save('icon.png', 'PNG')
        print("✅ 已创建 icon.png")
        
        # 尝试转换为 ICO
        try:
            # 创建多个尺寸的图标
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save('icon.ico', format='ICO', sizes=sizes)
            print("✅ 已创建 icon.ico")
        except Exception as e:
            print(f"⚠️  无法创建 .ico 文件: {e}")
            print("   请使用在线工具将 icon.png 转换为 icon.ico")
    
    if __name__ == "__main__":
        print("🎨 正在创建图标...")
        create_icon()
        print("\n完成！图标文件已保存。")

except ImportError:
    print("❌ 需要安装 Pillow 库")
    print("   运行: pip install Pillow")
    print("\n或者使用在线工具创建图标：")
    print("   https://convertio.co/zh/png-ico/")
