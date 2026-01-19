import os
import urllib.parse
import shutil
import re

# 始终扫描当前运行目录
root_dir = '.'
output_file = '_sidebar.md'

def clean_and_rename():
    """
    【预处理】
    1. 去掉文件夹名末尾的 .pdf-UUID 乱码
    2. 将 'full' 重命名为 'full.md'
    """
    print("🧹 正在检查并清洗文件名...")
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        
        # 跳过非文件夹、隐藏文件、以及特定的工程目录
        # 这里把 images 也加入跳过列表，虽然通常 images 在子目录里，但防患未然
        if not os.path.isdir(full_path) or entry.startswith('.') or entry in ['static', 'dist', 'scripts', 'images']:
            continue

        # --- 1. 清洗文件夹名称 ---
        clean_name = re.sub(r'\.pdf-.*', '', entry)
        new_path = os.path.join(root_dir, clean_name)
        
        current_path = full_path
        if entry != clean_name:
            try:
                os.rename(full_path, new_path)
                print(f"   ✨ 重命名文件夹: {entry[:20]}... -> {clean_name}")
                current_path = new_path
            except Exception as e:
                print(f"   ⚠️ 重命名失败 {entry}: {e}")

        # --- 2. 修正内容文件 (full -> full.md) ---
        old_file = os.path.join(current_path, 'full')
        new_file = os.path.join(current_path, 'full.md')
        
        if os.path.exists(old_file) and not os.path.exists(new_file):
            os.rename(old_file, new_file)
            print(f"   📝 添加后缀: {clean_name}/full -> full.md")

def generate_sidebar():
    lines = []
    
    # os.walk 会递归遍历所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # -------------------------------------------------
        # 核心修改：在遍历子目录之前，把不想要的目录剔除
        # 这样 os.walk 就根本不会进入这些目录，也不会把它们印在目录上
        # -------------------------------------------------
        dirs_to_ignore = ['images', 'static', 'dist', 'scripts']
        
        # 使用切片赋值来修改 dirnames，这样会影响 os.walk 的后续行为
        # 移除在这份黑名单里的文件夹，以及所有以 . 开头的隐藏文件夹
        dirnames[:] = [d for d in dirnames if d not in dirs_to_ignore and not d.startswith('.')]
        
        # 排序，保证目录顺序
        dirnames.sort()
        filenames.sort()

        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == '.':
            level = 0
        else:
            level = rel_path.count(os.sep) + 1

        # --- 处理文件夹标题 ---
        if rel_path != '.':
            indent = '  ' * (level - 1)
            folder_name = os.path.basename(dirpath)
            display_name = folder_name.replace('_', ' ')
            
            # 如果该文件夹下有 full.md，则生成链接
            if 'full.md' in filenames:
                file_path = os.path.join(rel_path, 'full.md')
                url_path = file_path.replace('\\', '/')
                encoded_path = urllib.parse.quote(url_path)
                lines.append(f'{indent}* [{display_name}]({encoded_path})')
            else:
                lines.append(f'{indent}* **{display_name}**')

        # --- 处理 Markdown 文件 ---
        for filename in filenames:
            if filename == 'full.md': continue # 已处理
            
            if filename.lower().endswith('.md') and filename.lower() != 'readme.md' and filename != '_sidebar.md':
                indent = '  ' * level
                title = os.path.splitext(filename)[0].replace('_', ' ')
                
                file_path = os.path.join(rel_path, filename)
                if rel_path == '.': file_path = filename
                
                url_path = file_path.replace('\\', '/')
                encoded_path = urllib.parse.quote(url_path)
                
                lines.append(f'{indent}* [{title}]({encoded_path})')

    # 写入 _sidebar.md
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 已生成目录: {os.path.abspath(output_file)}")

    # 检查首页
    readme_file = 'README.md'
    if not os.path.exists(readme_file):
        shutil.copyfile(output_file, readme_file)
        print(f"📄 已生成默认首页")

if __name__ == '__main__':
    clean_and_rename()
    generate_sidebar()