import os
import glob
import sys
import argparse
from typing import List, Tuple

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='文件批量重命名工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
    python multiRename.py                 # 默认模式：字幕文件跟随视频文件名称
    python multiRename.py --mode vid      # 字幕文件跟随视频文件名称
    python multiRename.py --mode sub      # 视频文件跟随字幕文件名称

支持的文件格式:
    视频: .mp4, .mkv, .avi, .mov, .wmv
    字幕: .ass, .srt, .ssa

注意事项:
    1. 程序会在当前目录下查找视频和字幕文件
    2. 确保视频文件和字幕文件数量相等
    3. 重命名操作会生成 revert.py 用于回滚操作
    4. 详细日志保存在 log.txt'''
    )
    parser.add_argument('--mode', choices=['vid', 'sub'], default='vid',
                       help='重命名模式：vid(跟随视频文件) 或 sub(跟随字幕文件)')
    return parser.parse_args()

# 在文件顶部添加支持的文件格式定义
VIDEO_EXTENSIONS = ['*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv']
SUBTITLE_EXTENSIONS = ['*.ass', '*.srt', '*.ssa']

def find_files() -> Tuple[List[str], List[str]]:
    """
    查找当前目录下的视频文件和字幕文件
    
    Returns:
        Tuple[List[str], List[str]]: 返回两个列表，分别包含视频和字幕文件的路径
    """
    # 查找所有支持的视频和字幕文件
    video_files = []
    subtitle_files = []
    
    # 收集所有视频文件
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(glob.glob(ext))
    
    # 收集所有字幕文件
    for ext in SUBTITLE_EXTENSIONS:
        subtitle_files.extend(glob.glob(ext))
    
    # 按文件名排序
    video_files.sort()
    subtitle_files.sort()
    
    # 将信息写入日志文件
    with open('log.txt', 'w', encoding='utf-8') as f:
        f.write("找到以下视频文件：\n")
        for video in video_files:
            f.write(f"- {os.path.basename(video)}\n")
        
        f.write("\n找到以下字幕文件：\n")
        for sub in subtitle_files:
            f.write(f"- {os.path.basename(sub)}\n")
        
        f.write(f"\n总计找到 {len(video_files)} 个视频文件和 {len(subtitle_files)} 个字幕文件\n")
    
    return video_files, subtitle_files

def rename_files(video_files: List[str], subtitle_files: List[str], follow_video: bool) -> None:
    """
    根据指定模式重命名文件
    
    Args:
        video_files: 视频文件列表
        subtitle_files: 字幕文件列表
        follow_video: 是否跟随视频文件名
    """
    source_files = video_files if follow_video else subtitle_files
    target_files = subtitle_files if follow_video else video_files
    
    # 准备回滚脚本的内容
    revert_script = [
        "import os",
        "\ndef revert_rename():",
        "    rename_operations = ["
    ]
    
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write("\n重命名操作日志：\n")
        
        for i, (source, target) in enumerate(zip(source_files, target_files)):
            source_name = os.path.basename(source)
            source_ext = os.path.splitext(target)[1]  # 保持目标文件的扩展名
            new_name = os.path.splitext(source_name)[0] + source_ext
            new_path = os.path.join(os.path.dirname(target), new_name)
            old_name = os.path.basename(target)
            
            try:
                # 检查是否存在同名文件
                if os.path.exists(new_path) and new_path != target:
                    f.write(f"警告：文件 {new_name} 已存在，跳过重命名\n")
                    print(f"警告：文件 {new_name} 已存在，跳过重命名")
                    continue
                
                # 执行重命名
                os.rename(target, new_path)
                f.write(f"成功：{old_name} -> {new_name}\n")
                
                # 添加回滚操作到脚本
                revert_script.append(f"        ('{new_name}', '{old_name}'),")
                
            except Exception as e:
                f.write(f"错误：重命名 {old_name} 失败: {str(e)}\n")
                print(f"错误：重命名 {old_name} 失败")
    
    # 完成回滚脚本
    revert_script.extend([
        "    ]",
        "    ",
        "    for new_name, old_name in rename_operations:",
        "        try:",
        "            os.rename(new_name, old_name)",
        "            print(f'已回滚: {new_name} -> {old_name}')",
        "        except Exception as e:",
        "            print(f'回滚失败 {new_name}: {str(e)}')",
        "",
        "if __name__ == '__main__':",
        "    print('开始回滚重命名操作...')",
        "    revert_rename()",
        "    print('回滚操作完成')"
    ])
    
    # 写入回滚脚本
    with open('revert.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(revert_script))

def main():
    args = parse_args()
    followVidIdc = args.mode == 'vid'
    
    video_files, subtitle_files = find_files()
    print(f"文件信息已保存到 log.txt")
    print(f"重命名模式：{'跟随视频文件' if followVidIdc else '跟随字幕文件'}")
    
    # 检查文件数量是否匹配
    if len(video_files) != len(subtitle_files):
        print("\n错误：视频文件和字幕文件数量不匹配！")
        print("请确保目录中有相同数量的视频和字幕文件。")
        sys.exit(1)
    
    # 执行重命名操作
    rename_files(video_files, subtitle_files, followVidIdc)
    print("\n重命名操作完成，详细日志已保存到 log.txt")

if __name__ == "__main__":
    main()