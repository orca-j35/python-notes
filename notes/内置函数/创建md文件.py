import os.path
while True:
    file_name = input("文件名:")
    file = file_name + ".md"
    if os.path.exists(file):
        print("已包含该文件，不会自动覆盖")
    else:
        with open(file_name+".md", "w") as file_objc:
            file_objc.write("# "+ file_name)
