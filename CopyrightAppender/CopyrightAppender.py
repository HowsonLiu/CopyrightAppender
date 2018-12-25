import os
import configparser

class CopyrightAppender:
    ini_path = './CopyrightAppender.ini'
    new_copyright_path = './Copyright.txt'

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

    def Run(self):
        print('你要处理的文件夹为: ' + os.path.abspath('..'))
        self.__foreach_dir_append('..')

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
                        print('文件 ' + full_path + ' 已添加')
                else:
                    print('文件 ' + full_path + ' 已跳过')

    def __choose_append_style(self, path):
        for suffix in self.c_style_suffix:
            if path.endswith(suffix):
                self.__append_c(path)
                return
        for suffix in self.python_style_suffix:
            if path.endswith(suffix):
                self.__comment_on_py()
                return
        for suffix in self.ini_style_suffix:
            if path.endswith(suffix):
                self.__comment_on_ini()
                return
        self.__comment_on_text()

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


    def __comment_on_py(self):
        py_comment = []
        for line in self.copyright_text_line:
            py_comment.append('# ' + line)
        py_comment.append('\n\n# Add by CopyrightAppender\n')
        print(''.join(py_comment))

    def __comment_on_ini(self):
        ini_comment = []
        for line in self.copyright_text_line:
            ini_comment.append(';' + line)
        ini_comment.append('\n\n;Add by CopyrightAppender\n')
        print(''.join(ini_comment))

    def __comment_on_text(self):
        text_comment = []
        for line in self.copyright_text_line:
            text_comment.append(line)
        text_comment.append('\n\nAdd by CopyrightAppender\n')
        print(''.join(text_comment))

    def Work(self):
        if self.__check_file_exist() == 0:
            self.__read_copyright()
            self.__read_ini()
            self.Run()


ca = CopyrightAppender()
ca.Work()
