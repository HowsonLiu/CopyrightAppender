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

    def __init__(self):
        pass

    def CheckFileExist(self):
        if os.path.exists(self.ini_path) is False:
            print('ini配置文件不存在')
            return -1
        if os.path.exists(self.new_copyright_path) is False:
            print('Copyright文件不存在')
            return -1
        return 0

    def ReadIni(self):
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

    def Run(self):
        print('你要处理的文件夹为: ' + os.path.abspath('..'))
        self.ForeachDirAppend('..')

    def ForeachDirAppend(self, path):
        for item in os.listdir(path):
            item = os.path.join(path, item)
            if os.path.isdir(item):
                print('Dir ' + item)
                self.ForeachDirAppend(item)
            else:
                print('File ' + item)

    def Work(self):
        self.ReadIni()
        print(self.suffix)
        print(self.apply_file)
        print(self.skip_file)
        self.Run()


ca = CopyrightAppender()
ca.Work()
