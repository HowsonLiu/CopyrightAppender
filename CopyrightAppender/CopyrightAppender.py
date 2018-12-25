import os
import configparser

class CopyrightAppender:
    ini_path = './CopyrightAppender.ini'
    new_copyright_path = './Copyright.txt'
    old_copyright_path = './.oldCopyright'

    # 相同类型注释的后缀
    c_style_suffix = ['.c', '.cpp', '.h', '.java', '.php', '.js']
    python_style_suffix = ['.py']
    ini_style_suffix = ['.ini']

    suffix = []
    apply_file = []
    skip_file = []
    skip_dir = []

    copyright_text = ''

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
        file = open(self.new_copyright_path)
        self.copyright_text = file.read()
        file.close()
        print(self.copyright_text)

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
                        self.__choose_append_style(item)
                        print('文件 ' + full_path + ' 已添加')
                else:
                    print('文件 ' + full_path + ' 已跳过')

    def __choose_append_style(self, name):
        for suffix in self.c_style_suffix:
            if name.endswith(suffix):
                print(name + ' c-style')
                return
        for suffix in self.python_style_suffix:
            if name.endswith(suffix):
                print(name + ' python-style')
                return
        for suffix in self.ini_style_suffix:
            if name.endswith(suffix):
                print(name + ' ini-style')
                return
        print(name + ' txt-style')


    def Work(self):
        if self.__check_file_exist() == 0:
            self.__read_copyright()


ca = CopyrightAppender()
ca.Work()
