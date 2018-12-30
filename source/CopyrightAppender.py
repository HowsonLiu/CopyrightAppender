import os
import configparser
import re
import time

# 别跟老夫说什么编码不编码的，老夫代码就一个字，干！
# 管他什么编码，统统使用单字节读取写入，出现乱码调一下格式就好了

class CopyrightAppender:
    conf = None

    INI_PATH = './CopyrightAppender.ini'
    COPYRIGHT_PATH = './Copyright.txt'

    # 相同类型注释的后缀
    C_STYLE_SUFFIX = ['.c', '.cpp', '.h', '.java', '.php', '.js']
    PYTHON_STYLE_SUFFIX = ['.py']
    INI_STYLE_SUFFIX = ['.ini']

    # ini中的标签名
    SKIP_DIR = 'skipdir'
    SKIP_FILE = 'skipfile'
    APPLY_FILE = 'applyfile'
    SUFFIX = 'suffix'
    USED_FOLDER = 'usedfolder'

    suffix = []
    apply_file = []
    skip_file = []
    skip_dir = []

    # Copyright.txt文件每一行文字的列表
    copyright_text_line = []

    success_file = []
    clean_file_count = 0
    clean_path = '..'
    clean_abs_path = ''
    ini_clean_path = ''

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(self.INI_PATH, encoding='utf-8')
        if self.conf.has_section(self.USED_FOLDER) is False:
            self.conf.add_section(self.USED_FOLDER)
            self.conf.write(open(self.INI_PATH, 'w'))
        self.clean_abs_path = os.path.abspath(self.clean_path)
        self.ini_clean_path = self.clean_abs_path.replace(':', '').lower() # configParse在写的时候自动转换成小写，而且不能有:

    def __check_file_exist(self):
        if os.path.exists(self.INI_PATH) is False:
            print('ini配置文件不存在')
            return -1
        if os.path.exists(self.COPYRIGHT_PATH) is False:
            print('Copyright文件不存在')
            return -1
        return 0

    def __read_ini(self):
        if self.conf.has_section(self.SUFFIX):
            for k, v in self.conf.items(self.SUFFIX):
                if v not in self.suffix:
                    self.suffix.append(v)
        if self.conf.has_section(self.APPLY_FILE):
            for k, v in self.conf.items(self.APPLY_FILE):
                if v not in self.apply_file:
                    self.apply_file.append(v)
        if self.conf.has_section(self.SKIP_FILE):
            for k, v in self.conf.items(self.SKIP_FILE):
                if v not in self.skip_file:
                    self.skip_file.append(v)
                if v in self.apply_file:
                    self.apply_file.remove(v)
                    print(v + ' 在配置中有冲突，以跳过处理')
        if self.conf.has_section(self.SKIP_DIR):
            for k, v in self.conf.items(self.SKIP_DIR):
                if v not in self.skip_dir:
                    self.skip_dir.append(v)

    def __read_copyright(self):
        with open(self.COPYRIGHT_PATH, 'rb') as file:
            self.copyright_text_line = file.readlines()

    def __foreach_dir_append(self, path):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                if item not in self.skip_dir:
                    self.__foreach_dir_append(full_path)
                else:
                    print('文件夹 ' + full_path + ' 已跳过')
            else:
                if item not in self.skip_file:
                    if item in self.apply_file or item.endswith(tuple(self.suffix)):
                        self.__choose_append_style(full_path)
                        if full_path not in self.success_file:
                            self.success_file.append(full_path)
                        print('文件 ' + full_path + ' 已添加')
                else:
                    print('文件 ' + full_path + ' 已跳过')

    def __after_append(self):
        if len(self.success_file) > 0:
            self.conf.set(self.USED_FOLDER, self.ini_clean_path, '1')
            self.conf.write(open(self.INI_PATH, 'w'))
            print('成功添加 ' + str(len(self.success_file)) + ' 个文件\n')

    def __choose_append_style(self, path):
        for suffix in self.C_STYLE_SUFFIX:
            if path.endswith(suffix):
                self.__append_c(path)
                return
        for suffix in self.PYTHON_STYLE_SUFFIX:
            if path.endswith(suffix):
                self.__append_py(path)
                return
        for suffix in self.INI_STYLE_SUFFIX:
            if path.endswith(suffix):
                self.__append_ini(path)
                return
        self.__append_text(path)

    def __clean_files(self):
        if len(self.success_file) > 0:
            for file in self.success_file:
                if self.__choose_clean_style(file):
                    self.clean_file_count += 1
                    print('文件 ' + file + ' 已清理')
            self.success_file = []
        else:
            self.__foreach_dir_clean(self.clean_path)

    def __foreach_dir_clean(self, path):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                if item not in self.skip_dir:
                    self.__foreach_dir_clean(full_path)
                else:
                    print('文件夹 ' + full_path + ' 已跳过')
            else:
                if item not in self.skip_file:
                    if item in self.apply_file or item.endswith(tuple(self.suffix)):
                        if self.__choose_clean_style(full_path):
                            self.clean_file_count += 1
                            print('文件 ' + full_path + ' 已清理')
                else:
                    print('文件 ' + full_path + ' 已跳过')

    def __after_clean(self):
        self.conf.set(self.USED_FOLDER, self.ini_clean_path, '0')
        self.conf.write(open(self.INI_PATH, 'w'))
        print('成功清除 ' + str(self.clean_file_count) + ' 个文件\n')
        self.clean_file_count = 0

    def __choose_clean_style(self, path):
        for suffix in self.C_STYLE_SUFFIX:
            if path.endswith(suffix):
                return self.__clean_c(path)
        for suffix in self.PYTHON_STYLE_SUFFIX:
            if path.endswith(suffix):
                return self.__clean_py(path)
        for suffix in self.INI_STYLE_SUFFIX:
            if path.endswith(suffix):
                return self.__clean_ini(path)
        return self.__clean_text(path)

# ------------------------------------------C类型注释---------------------------------------------
    def __comment_on_c(self):
        c_comment = []
        for line in self.copyright_text_line:
            c_comment.append(b' *' + line)
        c_comment.insert(0, b'/**\n')
        c_comment.append(b'\n */')
        c_comment.append(b'\n\n/*Add by CopyrightAppender*/\n')
        return b''.join(c_comment)

    def __append_c(self, path):
        copyright_text = self.__comment_on_c()
        with open(path, 'rb+') as file:
            oldtext = file.read()
            file.seek(0)
            file.write(copyright_text)
            file.write(oldtext)

    def __clean_c(self, path):
        copyright_text = self.__comment_on_c()
        with open(path, 'rb') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, b'')
            with open(path, 'wb') as file:
                file.write(text)
            return True
        return False

# -------------------------------------------------------------------------------------------------

# -----------------------------------------Python类型注释------------------------------------------

    # 两个返回值，第一个是字符串，第二个是行列表
    def __comment_on_py(self):
        py_comment = []
        for line in self.copyright_text_line:
            py_comment.append(b'# ' + line)
        py_comment.append(b'\n\n# Add by CopyrightAppender\n')
        return b''.join(py_comment), py_comment

    # python不能直接插入第一行，有可能有特殊注释，特殊注释一般在一二行，我只对一二行进行判断
    def __append_py(self, path):
        copyright_text, copyright_text_line = self.__comment_on_py()
        with open(path, 'rb+') as file:
            file_line = file.readlines()
            insert_num = 0
            if len(file_line) >= 1:
                # 第一行通常是编译器路径
                if re.compile(b'^#!').search(file_line[0]) is not None:
                    insert_num += 1
                # 第二行是编码格式 https://blog.csdn.net/xld_19920728/article/details/80534146
                if re.compile(b'^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)').search(file_line[0]) is not None:
                    insert_num += 1
                if len(file_line) >= 2 and re.compile(b'^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)').search(file_line[1]) is not None:
                    insert_num += 1
            for t in reversed(copyright_text_line):
                file_line.insert(insert_num, t)
            file.seek(0)
            file.write(b''.join(file_line))

    def __clean_py(self, path):
        copyright_text, copyright_text_line = self.__comment_on_py()
        with open(path, 'rb') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, b'')
            with open(path, 'wb') as file:
                file.write(text)
            return True
        return False

# -------------------------------------------------------------------------------------------------

# ----------------------------------------ini类型注释-----------------------------------------------

    def __comment_on_ini(self):
        ini_comment = []
        for line in self.copyright_text_line:
            ini_comment.append(b';' + line)
        ini_comment.append(b'\n\n;Add by CopyrightAppender\n')
        return b''.join(ini_comment)

    def __append_ini(self, path):
        copyright_text = self.__comment_on_ini()
        with open(path, 'rb+') as file:
            oldtext = file.read()
            file.seek(0)
            file.write(copyright_text)
            file.write(oldtext)

    def __clean_ini(self, path):
        copyright_text = self.__comment_on_ini()
        with open(path, 'rb') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, b'')
            with open(path, 'wb') as file:
                file.write(text)
            return True
        return False

# ------------------------------------------------------------------------------------------------

# ----------------------------------------txt类型注释-----------------------------------------------

    def __comment_on_text(self):
        text_comment = []
        for line in self.copyright_text_line:
            text_comment.append(line)
        text_comment.append(b'\n\nAdd by CopyrightAppender\n')
        return b''.join(text_comment)

    def __append_text(self, path):
        copyright_text = self.__comment_on_text()
        with open(path, 'rb+') as file:
            oldtext = file.read()
            file.seek(0)
            file.write(copyright_text)
            file.write(oldtext)

    def __clean_text(self, path):
        copyright_text = self.__comment_on_text()
        with open(path, 'rb') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, b'')
            with open(path, 'wb') as file:
                file.write(text)
            return True
        return False

# ------------------------------------------------------------------------------------------------

    def run(self):
        print('CopyrightAppender')
        if self.__check_file_exist() != 0:
            time.sleep(1)
            return

        self.__read_ini()
        if len(self.apply_file) == 0 and len(self.suffix) == 0:
            print('没有要处理的文件和后缀')
            time.sleep(1)
            return

        self.__read_copyright()
        if len(self.copyright_text_line) == 0:
            print('Copyright.txt 是空的')
            time.sleep(1)
            return

        print('你要处理的文件夹是: ' + os.path.abspath(self.clean_path))
        os.system('pause')
        answer = ''

        if self.ini_clean_path in self.conf.options(self.USED_FOLDER) and \
                self.conf.get(self.USED_FOLDER, self.ini_clean_path) == '1':
            while answer not in ('y', 'n'):
                print('检测到有旧的 Copyright, 是否清理 (y/n)')
                answer = input()
            if answer == 'y':
                self.__foreach_dir_clean(self.clean_path)
                self.__after_clean()
        while answer not in ('a', 'c'):
            print('你想要做的是: append or clean (a/c)')  # 右上角退出
            answer = input()
            if answer == 'a':
                self.__foreach_dir_append(self.clean_path)
                self.__after_append()
            elif answer == 'c':
                self.__clean_files()
                self.__after_clean()
            answer = ''

ca = CopyrightAppender()
ca.run()