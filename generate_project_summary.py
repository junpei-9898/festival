import os
import fnmatch

explicit_ignore_list = ['.github', '.gitignore', 'node_modules', '.DS_Store']  # 例: .log拡張子、tempフォルダ、.DS_Storeファイルを無視

def is_binary(file_path):
    with open(file_path, 'rb') as file:
        return b'\0' in file.read(1024)

def read_file_contents(file_path):
    encodings = ['utf-8', 'shift_jis']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                print(f'Reading file: {file_path}')
                return file.read()
        except UnicodeDecodeError:
            pass
    return ''

def is_ignored(path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns, explicit_ignore_list):
    relative_path = os.path.relpath(path, project_dir)
    basename = os.path.basename(path)
    _, ext = os.path.splitext(basename)

    # 明示的な無視リストに基づくチェック
    for ignore_item in explicit_ignore_list:
        if ignore_item.startswith('.'):  # 拡張子のチェック
            if ext == ignore_item:
                return True
        elif os.sep + ignore_item in path or basename == ignore_item:  # ファイル名またはフォルダ名のチェック
            return True

    # 既存の無視パターンに基づくチェック
    for pattern in gitignore_patterns + summaryignore_patterns + additional_ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            print(f"Ignored: {relative_path} (Pattern: {pattern})")
            return True
    return False

def generate_project_summary(project_dir):
    project_name = os.path.basename(project_dir)
    summary = f'# {project_name}\n\n## Directory Structure\n\n'

    gitignore_patterns = read_gitignore(project_dir)
    print(f"gitignore_patterns: {gitignore_patterns}")
    summaryignore_patterns = read_summaryignore(project_dir)
    print(f"summaryignore_patterns: {summaryignore_patterns}")
    additional_ignore_patterns = ['generate_project_summary.py','.summaryignore', f'{project_name}_project_summary.txt', '.git']

    file_contents_section = "\n## File Contents\n\n"

    def traverse_directory(root, level):
        nonlocal summary, file_contents_section
        indent = '  ' * level
        relative_path = os.path.relpath(root, project_dir)
        if not is_ignored(relative_path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns, explicit_ignore_list):
            summary += f'{indent}- {os.path.basename(root)}/\n'

            subindent = '  ' * (level + 1)
            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                if os.path.isdir(item_path):
                    if not is_ignored(item_path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns, explicit_ignore_list):
                        traverse_directory(item_path, level + 1)
                else:
                    if not is_ignored(item_path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns, explicit_ignore_list):
                        if not is_binary(item_path):
                            summary += f'{subindent}- {item}\n'
                            content = read_file_contents(item_path)
                            if content.strip():
                                # ファイル名をプロジェクト名からの相対パスで表示
                                relative_file_path = os.path.relpath(item_path, project_dir)
                                file_contents_section += f'### {relative_file_path}\n\n```\n{content}\n```\n\n'
                        else:
                            summary += f'{subindent}- {item} (binary file)\n'

    traverse_directory(project_dir, 0)

    with open(f'{project_name}_project_summary.txt', 'w', encoding='utf-8') as file:
        file.write(summary + file_contents_section)

def read_gitignore(project_dir):
    gitignore_path = os.path.join(project_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            expanded_patterns = []
            for pattern in patterns:
                expanded_patterns.append(pattern)
                if '/' in pattern:
                    expanded_patterns.append(pattern.replace('/', '\\'))
                if '\\' in pattern:
                    expanded_patterns.append(pattern.replace('\\', '/'))
            return expanded_patterns
    return []

def read_summaryignore(project_dir):
    summaryignore_path = os.path.join(project_dir, '.summaryignore')
    if os.path.exists(summaryignore_path):
        with open(summaryignore_path, 'r') as file:
            patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            expanded_patterns = []
            for pattern in patterns:
                expanded_patterns.append(pattern)
                if '/' in pattern:
                    expanded_patterns.append(pattern.replace('/', '\\'))
                if '\\' in pattern:
                    expanded_patterns.append(pattern.replace('\\', '/'))
            return expanded_patterns
    return []

if __name__ == '__main__':
    project_directory = input('Enter the project directory path (leave blank for current directory): ')
    if not project_directory:
        project_directory = os.getcwd()
    generate_project_summary(project_directory)