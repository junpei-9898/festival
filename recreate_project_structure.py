import os

def read_file_contents(file_path):
    encodings = ['utf-8', 'shift_jis', 'euc-jp', 'iso-2022-jp']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            pass
    return ''

def recreate_project(summary_file):
    with open(summary_file, 'r', encoding='utf-8') as file:
        summary_data = file.read()

    lines = summary_data.split('\n')
    project_name = lines[0].lstrip('# ').strip()
    os.makedirs(project_name, exist_ok=True)
    current_dir = project_name

    file_contents = {}
    binary_files = []
    current_file = ''

    for line in lines[1:]:
        if line.startswith('- '):
            item = line.lstrip('- ').strip()
            if item.endswith('/'):
                current_dir = os.path.join(current_dir, item[:-1])
                os.makedirs(current_dir, exist_ok=True)
            else:
                file_path = os.path.join(current_dir, item)
                if '(binary file)' in line:
                    binary_files.append(file_path)
                    open(file_path, 'wb').close()
                else:
                    file_contents[file_path] = ''  # ここでファイルパスを初期化
        elif line.startswith('### '):
            current_file = os.path.join(current_dir, line.lstrip('### ').strip())
            if current_file not in file_contents:  # 新しいファイルパスが辞書にない場合は追加
                file_contents[current_file] = ''
        elif line.startswith('```'):
            pass
        else:
            if current_file:  # current_fileが空文字列でないことを確認
                if current_file not in file_contents:  # セーフティチェック
                    file_contents[current_file] = ''
                file_contents[current_file] += line + '\n'
            else:
                # current_fileが空文字列の場合の処理（例：警告を出力）
                print("Warning: Trying to add content without a current file set.")


    for file_path, content in file_contents.items():
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

if __name__ == '__main__':
    summary_file = input('Enter the project summary file path: ')
    recreate_project(summary_file)
