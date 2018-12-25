import os
import configparser

class CopyrightAppender:
    ini_path = './CopyrightAppender.ini'
    new_copyright_path = './Copyright.txt'
    old_copyright_path = './.oldCopyright'

    c_style_suffix = ['.c', '.cpp', '.h']
    python_style_suffix = ['.py']
    ini_style_suffix = ['.ini']

    suffix = []
    apply_file = []
    skip_file = []
    skip_dir = []

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

    def Run(self):
        print('你要处理的文件夹为: ' + os.path.abspath('..'))
        self.__foreach_dir_append('..')

    def __foreach_dir_append(self, path):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                if item not in self.skip_dir:
                    print(full_path + '不跳过')
                    self.__foreach_dir_append(full_path)
                else:
                    print(full_path + ' 已跳过')
            else:
                if item not in self.skip_file:
                    if item in self.apply_file or item.endswith(tuple(self.suffix)):
                        print(full_path + ' 已添加')


    def Work(self):
        self.__read_ini()
        print(self.suffix)
        print(self.apply_file)
        print(self.skip_file)
        print(self.skip_dir)
        self.Run()


ca = CopyrightAppender()
ca.Work()
