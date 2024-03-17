import os

def generate_markdown_directory_tree(directory, prefix=''):
    output = []
    ignore = set(['node_modules', 'package.json', 'package-lock.json'])  # 無視するファイルやディレクトリのセット

    # ディレクトリ内のアイテムを取得し、無視リストに含まれていないものだけを処理
    items = [item for item in os.listdir(directory) if item not in ignore]
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            # ディレクトリの場合
            if i == len(items) - 1:
                # 最後のアイテムの場合
                output.append(f"{prefix}└── {item}/")
                output.extend(generate_markdown_directory_tree(path, prefix + '    '))
            else:
                output.append(f"{prefix}├── {item}/")
                output.extend(generate_markdown_directory_tree(path, prefix + '│   '))
        else:
            # ファイルの場合
            if i == len(items) - 1:
                output.append(f"{prefix}└── {item}")
            else:
                output.append(f"{prefix}├── {item}")
    return output

if __name__ == "__main__":
    directory_path = input("Enter the project directory path: ")
    markdown_output = generate_markdown_directory_tree(directory_path)

    directory_name = os.path.basename(os.path.normpath(directory_path))
    output_file_path = f"{directory_name}_tree_output.txt"

    with open(output_file_path, "w") as file:
        file.write("\n".join(markdown_output))
    print(f"Directory tree has been saved to {output_file_path}")