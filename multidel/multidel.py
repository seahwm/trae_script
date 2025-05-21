import os
import glob
import sys
from typing import List

def delete_files(pattern: str) -> List[str]:
    """删除匹配指定模式的文件
    
    Args:
        pattern: 文件匹配模式，例如 "*.ts.ass"
        
    Returns:
        已删除文件的列表
    """
    deleted_files = []
    
    # 获取匹配的文件列表
    matched_files = glob.glob(pattern)
    
    if not matched_files:
        print(f"没有找到匹配 '{pattern}' 的文件")
        return deleted_files
    
    # 显示将要删除的文件
    print(f"将要删除以下文件:")
    for file in matched_files:
        print(f"- {file}")
    
    # 询问用户确认
    confirm = input("确认删除这些文件? (y/N): ").lower()
    if confirm != 'y':
        print("操作已取消")
        return deleted_files
    
    # 执行删除
    for file in matched_files:
        try:
            os.remove(file)
            deleted_files.append(file)
            print(f"已删除: {file}")
        except Exception as e:
            print(f"删除 {file} 时出错: {e}")
    
    return deleted_files

def main():
    if len(sys.argv) != 2:
        print("使用方法: python multidel.py <文件模式>")
        print("示例: python multidel.py *.ts.ass")
        sys.exit(1)
    
    pattern = sys.argv[1]
    delete_files(pattern)

if __name__ == "__main__":
    main()