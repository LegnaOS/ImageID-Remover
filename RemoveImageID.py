import sys
import os
import piexif
from tqdm import tqdm

# 从命令行参数获取文件夹路径，如果没有参数，则使用当前工作目录
folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

# 获取文件夹下所有文件
all_files = os.listdir(folder_path)

# 使用tqdm函数遍历文件夹下的所有文件
for filename in tqdm(all_files, desc="处理进度", ncols=70):
    # 检查文件是否为 JPEG 图片
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        # 获取图片的完整路径
        image_path = os.path.join(folder_path, filename)
        
        # 输出正在处理的文件名
        print(f"正在处理文件：{image_path}")
        
        try:
            # 加载图片的Exif信息
            exif_dict = piexif.load(image_path)

            # 修改ImageID
            exif_dict["0th"][piexif.ImageIFD.ImageID] = b""
            exif_dict["Exif"][piexif.ExifIFD.ImageUniqueID] = b""
            # 生成新的Exif字节数据
            exif_bytes = piexif.dump(exif_dict)

            # 将新的Exif数据写回图片
            piexif.insert(exif_bytes, image_path)
            
            # 输出处理成功的信息
            print(f"成功处理文件：{image_path}")
        except Exception as e:
            # 输出处理失败的信息
            print(f"处理文件失败：{image_path}，错误信息：{str(e)}")