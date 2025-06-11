import os
import shutil


def make_new_file(file_name, text):
    if not os.path.exists(file_name):
        with open(os.getcwd() + '\\' + file_name, 'w') as file:
            file.write(text)
    else:
        return


if __name__ == "__main__":
    current_dir = os.getcwd()
    if not os.path.exists(current_dir + "\\file_managment"):
        os.mkdir(current_dir + '\\file_managment')
    os.chdir(current_dir + "\\file_managment")
    make_new_file('text1.txt', 'Hello!')
    make_new_file('text2.txt', 'Hello world!')
    print(os.listdir())

    if os.path.exists('text1.txt'):
        os.remove("text1.txt")
    else:
        print("Файл не найден")
    if not os.path.exists("new_dir"):
        os.mkdir(os.getcwd() + "\\new_dir")
    os.replace("text2.txt",os.path.join("new_dir","text2.txt"))
    os.chdir("..")
    shutil.rmtree("file_managment")