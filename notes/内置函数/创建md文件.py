import os.path
while True:
    file_name = input("文件名:")
    file = file_name + ".md"
    if os.path.exists(file):
        print("已包含该文件，不会自动覆盖")
    else:
        with open(file_name + ".md", "w", encoding='utf-8') as file_objc:
            file_objc.write("# " + file_name + '\n')
            file_objc.write(
                "> GitHub@[orca-j35](https://github.com/orca-j35)，"
                "所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库\n"
            )
