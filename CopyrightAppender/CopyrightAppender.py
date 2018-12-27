import os
import configparser
import re
import chardet

# TODO 编码格式判断

class CopyrightAppender:
    ini_path = './CopyrightAppender.ini'
    new_copyright_path = './Copyright.txt'
    old_copyright_path = './.oldCopyright'  # 标志是否存在

    # 相同类型注释的后缀
    c_style_suffix = ['.c', '.cpp', '.h', '.java', '.php', '.js']
    python_style_suffix = ['.py']
    ini_style_suffix = ['.ini']

    suffix = []
    apply_file = []
    skip_file = []
    skip_dir = []

    # Copyright.txt文件每一行文字的列表
    copyright_text_line = []
    # Copyright.txt的编码格式
    copyright_text_encode = ''

    success_file = []
    clean_file_count = 0
    clean_path = '..'

    def __init__(self):
        pass

    def __check_file_exist(self):
        if os.path.exists(self.ini_path) is False:
            print('ini配置文件不存在')
            return -1
        if os.path.exists(self.new_copyright_path) is False:
            print('Copyright文件不存在')
            return -1
        return 0

    def __read_ini(self):
        conf = configparser.ConfigParser()
        conf.read(self.ini_path, encoding='utf-8')
        if conf.has_section('suffix'):
            for k, v in conf.items('suffix'):
                if v not in self.suffix:
                    self.suffix.append(v)
        if conf.has_section('applyfile'):
            for k, v in conf.items('applyfile'):
                if v not in self.apply_file:
                    self.apply_file.append(v)
        if conf.has_section('skipfile'):
            for k, v in conf.items('skipfile'):
                if v not in self.skip_file:
                    self.skip_file.append(v)
                if v in self.apply_file:
                    self.apply_file.remove(v)
                    print(v + ' 在配置中有冲突，以跳过处理')
        if conf.has_section('skipdir'):
            for k, v in conf.items('skipdir'):
                if v not in self.skip_dir:
                    self.skip_dir.append(v)

    def __read_copyright(self):
        with open(self.new_copyright_path) as file:
            self.copyright_text_line = file.readlines()
        with open(self.new_copyright_path, 'rb') as file:
            data = file.read()
            self.copyright_text_encode = chardet.detect(data)

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

    def _after_append(self):
        if len(self.success_file) > 0:
            with open(self.old_copyright_path, 'w') as file:
                pass
            print('成功添加 ' + str(len(self.success_file)) + ' 个文件\n')

    def __choose_append_style(self, path):
        for suffix in self.c_style_suffix:
            if path.endswith(suffix):
                self.__append_c(path)
                return
        for suffix in self.python_style_suffix:
            if path.endswith(suffix):
                self.__append_py(path)
                return
        for suffix in self.ini_style_suffix:
            if path.endswith(suffix):
                self.__append_ini(path)
                return
        self.__append_text(path)

    def _clean_files(self):
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

    def _after_clean(self):
        if os.path.exists(self.old_copyright_path):
            os.remove(self.old_copyright_path)
        print('成功清除 ' + str(self.clean_file_count) + ' 个文件\n')
        self.clean_file_count = 0

    def __choose_clean_style(self, path):
        for suffix in self.c_style_suffix:
            if path.endswith(suffix):
                return self.__clean_c(path)
        for suffix in self.python_style_suffix:
            if path.endswith(suffix):
                return self.__clean_py(path)
        for suffix in self.ini_style_suffix:
            if path.endswith(suffix):
                return self.__clean_ini(path)
        return self.__clean_text(path)

# ------------------------------------------C类型注释---------------------------------------------
    def __comment_on_c(self):
        c_comment = []
        for line in self.copyright_text_line:
            c_comment.append(' *' + line)
        c_comment.insert(0, '/**\n')
        c_comment.append('\n */')
        c_comment.append('\n\n/*Add by CopyrightAppender*/\n')
        return ''.join(c_comment)

    def __append_c(self, path):
        copyright_text = self.__comment_on_c()
        with open(path, 'r+') as file:
            oldtext = file.read()
            file.seek(0)
            file.write(copyright_text)
            file.write(oldtext)

    def __clean_c(self, path):
        copyright_text = self.__comment_on_c()
        with open(path, 'r') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, '')
            with open(path, 'w') as file:
                file.write(text)
            return True
        return False

# -------------------------------------------------------------------------------------------------

# -----------------------------------------Python类型注释------------------------------------------

    # 两个返回值，第一个是字符串，第二个是行列表
    def __comment_on_py(self):
        py_comment = []
        for line in self.copyright_text_line:
            py_comment.append('# ' + line)
        py_comment.append('\n\n# Add by CopyrightAppender\n')
        return ''.join(py_comment), py_comment

    # python不能直接插入第一行，有可能有特殊注释，特殊注释一般在一二行，我只对一二行进行判断
    def __append_py(self, path):
        copyright_text, copyright_text_line = self.__comment_on_py()
        with open(path, 'r+') as file:
            file_line = file.readlines()
            insert_num = 0
            if len(file_line) >= 1:
                # 第一行通常是编译器路径
                if re.compile('^#!').search(file_line[0]) is not None:
                    insert_num += 1
                # 第二行是编码格式 https://blog.csdn.net/xld_19920728/article/details/80534146
                if re.compile('^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)').search(file_line[0]) is not None:
                    insert_num += 1
                if len(file_line) >= 2 and re.compile('^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)').search(file_line[1]) is not None:
                    insert_num += 1
            for t in reversed(copyright_text_line):
                file_line.insert(insert_num, t)
            file.seek(0)
            file.write(''.join(file_line))

    def __clean_py(self, path):
        copyright_text, copyright_text_line = self.__comment_on_py()
        with open(path, 'r') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, '')
            with open(path, 'w') as file:
                file.write(text)
            return True
        return False

# -------------------------------------------------------------------------------------------------

# ----------------------------------------ini类型注释-----------------------------------------------

    def __comment_on_ini(self):
        ini_comment = []
        for line in self.copyright_text_line:
            ini_comment.append(';' + line)
        ini_comment.append('\n\n;Add by CopyrightAppender\n')
        return ''.join(ini_comment)

    def __append_ini(self, path):
        copyright_text = self.__comment_on_ini()
        with open(path, 'r+') as file:
            oldtext = file.read()
            file.seek(0)
            file.write(copyright_text)
            file.write(oldtext)

    def __clean_ini(self, path):
        copyright_text = self.__comment_on_ini()
        with open(path, 'r') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, '')
            with open(path, 'w') as file:
                file.write(text)
            return True
        return False

# ------------------------------------------------------------------------------------------------

# ----------------------------------------txt类型注释-----------------------------------------------

    def __comment_on_text(self):
        text_comment = []
        for line in self.copyright_text_line:
            text_comment.append(line)
        text_comment.append('\n\nAdd by CopyrightAppender\n')
        return ''.join(text_comment)

    def __append_text(self, path):
        copyright_text = self.__comment_on_text()
        with open(path, 'r+') as file:
            oldtext = file.read()
            file.seek(0)
            file.write(copyright_text)
            file.write(oldtext)

    def __clean_text(self, path):
        copyright_text = self.__comment_on_text()
        with open(path, 'r') as file:
            text = file.read()
        if copyright_text in text:
            text = text.replace(copyright_text, '')
            with open(path, 'w') as file:
                file.write(text)
            return True
        return False

# ------------------------------------------------------------------------------------------------

    def run(self):
        if self.__check_file_exist() != 0:
            return

        self.__read_ini()
        if len(self.apply_file) == 0 and len(self.suffix) == 0:
            print('没有要处理的文件和后缀')
            return

        self.__read_copyright()
        if len(self.copyright_text_line) == 0:
            print('Copyright.txt 是空的')
            return

        print('你要处理的文件夹为: ' + os.path.abspath(self.clean_path) + ' , 不是的话快按×')
        os.system('pause')
        if os.path.exists(self.old_copyright_path):
            answer = ''
            while(answer not in ['y', 'n']):
                print('检测到有旧的 Copyright, 是否清理 (y/n)')
                answer = input()
                if answer == 'y':
                    self.__foreach_dir_clean(self.clean_path)
                    self._after_clean()
                    break
                elif answer == 'n':
                    break
        answer = ''
        while(answer not in ['a', 'c']):
            print('你想要做的是: append or clean (a/c)')  # 右上角退出
            answer = input()
            if answer == 'a':
                self.__foreach_dir_append(self.clean_path)
                self._after_append()
            elif answer == 'c':
                self._clean_files()
                self._after_clean()
            answer = ''

ca = CopyrightAppender()
ca.run()
