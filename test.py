import os
from PIL import Image

def create_gif(input_folder, output_gif, duration=200, loop=0, sort_by='name'):
    """
    将指定文件夹中的图片合成GIF动画
    
    参数:
    input_folder (str): 图片文件夹路径
    output_gif (str): 输出GIF路径
    duration (int): 帧持续时间（毫秒）
    loop (int): 循环次数（0表示无限循环）
    sort_by (str): 排序方式 ['name'按文件名|'date'按修改时间]
    """
    
    try:
        # 获取支持的图片格式列表
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        
        # 获取文件列表并过滤
        files = [f for f in os.listdir(input_folder) 
                if os.path.splitext(f)[1].lower() in valid_extensions]
        
        if not files:
            print("错误：文件夹中没有支持的图片文件（支持.jpg, .jpeg, .png, .bmp, .gif）")
            return

        # 排序文件列表
        if sort_by == 'name':
            files.sort()
        elif sort_by == 'date':
            files.sort(key=lambda x: os.path.getmtime(os.path.join(input_folder, x)))
        else:
            raise ValueError("无效的排序方式，请选择 'name' 或 'date'")

        # 打开所有图片并统一尺寸
        frames = []
        first_image = None
        for file in files:
            img_path = os.path.join(input_folder, file)
            img = Image.open(img_path)
            
            # 统一使用RGB模式（处理透明通道）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 将所有帧调整为第一帧的尺寸
            if first_image is None:
                first_image = img
                frames.append(img)
            else:
                # 修改此处，将 Image.ANTIALIAS 替换为 Image.LANCZOS
                frames.append(img.resize(first_image.size, Image.LANCZOS))

        # 保存GIF
        frames[0].save(
            output_gif,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            optimize=True
        )
        print(f"成功生成GIF：{output_gif}（共{len(frames)}帧）")

    except Exception as e:
        print(f"程序出错：{str(e)}")

if __name__ == "__main__":
    # 配置参数
    input_folder = "./images"       # 图片文件夹路径
    output_gif = "./output.gif"     # 输出GIF路径
    duration = 50                  # 每帧持续时间（毫秒）
    loop = 0                        # 循环次数（0=无限）
    sort_by = 'name'                # 排序方式：'name' 或 'date'

    create_gif(input_folder, output_gif, duration, loop, sort_by)