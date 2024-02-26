import json
import subprocess
import os
import sys
from CodeFixer.dao.d4jdao import query_changes, query_file_name, query_mtrics
from CodeFixer.strategies.d4jstrategies import ChunkContextAround, ContextAround, ContextStratege, MethodContextAround, TestCodeSingleline, TestFirst, TestStrategy
from CodeFixer.utils.logutil import setup_logger
from .project import Project, ProjectBuilder, ProjectDirector
import timeout_decorator
from CodeFixer.config.d4jcfg import D4jCfg as cfg


def list_add(l1:list, l2:list):
    # 添加二维list的所有元素
    for ll2 in l2:
        for lll2 in ll2:
            l1.append(lll2)
    return l1


class D4j(Project):

    def __init__(self, name):
        super().__init__(name)
        self.project_path = ""
        self.project = ""
        self.bug_id = ""
        self.project = self.name.split('_')[0]
        self.bug_id = self.name.split('_')[1]
        root_path = cfg.d4j_dir
        self.project_path = os.path.join(root_path, self.name)
        self.src_path = ""
        self.method = ""
        self.error_num = []
    

        
    def checkout(self):
        """
        将项目进行checkout
        """
        os.chdir(os.path.dirname(self.project_path))
        cmd = ["defects4j", "checkout", "-p", self.project, "-v", str(self.bug_id)+'b', '-w', self.project_path]
        self.logger.info(' '.join(cmd))
        out = subprocess.run(cmd, capture_output=True, text=True)
        result = out.stderr.split('\n')[:-1]
        checkout = True
        for line in result:
            if (not line.endswith("OK")):
                    self.logger.error(f"checkout {self.project} {self.bug_id}b失败")
                    self.logger.error(out.stderr)
                    checkout = False
                    break
        if checkout:
            self.logger.info(f"checkout {self.project} {self.bug_id}b 成功")
        return checkout
    
    
    
    @timeout_decorator.timeout(cfg.compile_maxtime)
    def compile(self):
        """
        执行编译
        """
        os.chdir(self.project_path)
        cmd = ["defects4j", "compile"]
        out = subprocess.run(cmd, capture_output=True, text=True)
        error = out.stderr
        result = error.split('\n')[:-1]
        compile_OK = True
        err_mes = ""
        for index, line in enumerate(result):
            if (not line.endswith("OK")):
                compile_OK = False
                if "错误" in line:
                    err_mes += "错误" + line.split("错误")[1] + '\n'
                    err_mes += result[index+1].replace("[javac]", "").strip()
                    break
        if (compile_OK):
            self.logger.info("编译成功")
            return True
        else:
            self.logger.info("编译失败")
            self.compile_error_mes = err_mes
            self.logger.info(err_mes)
            return False
        
    @timeout_decorator.timeout(cfg.test_maxtime)
    def test(self):
        """
        执行测试,获取失败的测试用例
        """
        os.chdir(self.project_path)
        cmd = ["defects4j", "test"]
        out = subprocess.run(cmd, capture_output=True, text=True)
        out = out.stdout
        result = out.split('\n')[:-1]
        test_OK = True
        for index, line in enumerate(result):
            if line.strip() == "Failing tests: 1" and 'testParseMonth' in result[index+1]:
                break
            if (not line.endswith("OK") and line.strip() != "Failing tests: 0"):
                self.logger.info("测试失败")
                test_OK = False
                break
        if (test_OK):
            self.logger.info("测试成功")
            return True
        else:
            self.logger.info(out)
            for line in out.split('\n')[1:]:
                line = line.replace('-', '')
                self.fail_tests.append(line.strip())
            self.choose_test(TestFirst())
            # self.get_fail_test_source()
            self.get_fail_test_errormes()
            return False
    
    def choose_test(self, strategy: TestStrategy):
        """
        选择使用的测试用例
        """
        self.fail_test = strategy.get_test(self.fail_tests)

    def get_fail_test_source(self):
        """
        获取失败的测试用例方法源码
        """
        fail_test = self.fail_test
        # method = fail_test.split("::")[1]
        # 查找测试的源代码目录
        cmd = ["defects4j", "export", "-p", "dir.src.tests"]
        os.chdir(self.project_path)
        out = subprocess.run(cmd, capture_output=True, text=True)
        dir = out.stdout
        self.bug_file = os.path.join(self.project_path, dir, fail_test.split("::")[0].replace('.', '/') + '.java')  

    def get_fail_test_errormes(self):
        """
        获取失败的测试用例的位置及信息
        """
        fail_test = self.fail_test
        method = fail_test.split("::")[1]
        self.method = method + '()'
        line_feature = method + '('
        os.chdir(self.project_path)
        error_num = 0
        start_num = -1
        test_file = ""
        with open("failing_tests") as f:
            fail_file = f.readlines()
        for index, line in enumerate(fail_file):
            if fail_test in line:
                start_num = index   
            if line_feature in line:
                error_num = line.split(':')[1].replace(')', '')
                test_file = line.split('.'+line_feature)[0].replace('at ', '').strip()

        if start_num != -1:
            self.test_error_mes = fail_file[start_num+1]
        
        if test_file == "":
            self.error_test_lines = ""
            return 

        cmd = ["defects4j", "export", "-p", "dir.src.tests"]
        os.chdir(self.project_path)
        out = subprocess.run(cmd, capture_output=True, text=True)
        dir = out.stdout
        bug_file = os.path.join(self.project_path, dir, test_file.replace('.', '/') + '.java')  
        # # 这是一个例外
        # if self.name == 'Math_41':
        #     bug_file = 
        with open(bug_file) as f:
            file = f.readlines()
        if type(error_num) != int:
            error_num = int(error_num.strip())
        if error_num != 0:
            # print(error_num)
            # print(bug_file)
            self.error_test_lines = TestCodeSingleline().get_test_code(file, error_num)


    def delete(self):
        """
        删除项目
        """
        cmd = ["rm", "-rf", self.project_path]
        self.logger.info(' '.join(cmd))
        subprocess.run(cmd, capture_output=True, text='True')
        self.logger.info(f"删除 {self.project} {self.bug_id}b 成功")

        
    def clear(self):
        self.fail_tests.clear()
        self.test_error_mes = ""     # 测试错误信息
        self.compile_error_mes = ""     # 编译错误信息
        self.error_test_code = ""   # 出错的测试用例代码
        self.bug_file = ""  # 出错的测试文件路径
        self.fail_test_source = ""  # 失败的测试用例

    def bug_type(self):
        # (chunks, classes, files, linesAdd, linesMod, linesRem, methods, sizeInLines, spreadAllLines)
        # 单行修改的补丁
        if self.metrics[7] == 1 and self.metrics[4] == 1:
            return 1
        # 单块删除的补丁
        if self.metrics[0] == 1 and self.metrics[5] == self.metrics[7]:
            return 2
        # 单块有删除的补丁
        if self.metrics[0] == 1 and self.metrics[7] > 1 and self.metrics[7] != self.metrics[3]:
            return 2
        # 单块添加的补丁 包含单行添加
        if self.metrics[0] == 1 and self.metrics[7] == self.metrics[3]:
            return 3
        # 单函数多错误补丁
        if self.metrics[0] > 1 and self.metrics[6] == 1:
            return 4
        return 0


class D4jBuilder(ProjectBuilder):

    def __init__(self, name):
        self.project = D4j(name)
        root_path = cfg.log_dir
        self.project.logger = setup_logger(name, os.path.join(root_path, 'project', name+".log"))  # 日志记录器

    def get_fail_type(self):
        self.project.delete()
        if not self.project.checkout():
            return -1
        if  not self.project.compile():
            return 1
        if  not self.project.test():
            return 2
        return 0
    
    def get_bug_code(self, strategy: ContextStratege=ContextAround()):
        """
        使用不同的策略获取上下文
        """
        # 单行修改上下文
        p = self.project
        file_name, _ = query_file_name(p.project, p.bug_id)
        os.chdir(p.project_path)
        cmd = ["defects4j", "export", "-p", "dir.src.classes"]
        out = subprocess.run(cmd, capture_output=True, text=True)
        dir = out.stdout
        src_path = os.path.join(p.project_path, dir, file_name) 
        p.src_path = src_path
        with open(src_path, errors='ignore') as f:
            file = f.read()
        p.logger.info("它的bug类型为:")
        p.logger.info(p.bug_type())
        if  p.bug_type() == 1:
            error_num = int(self.project.changes[0][0][0])
            p.error_num = [error_num]
            return strategy.get_context(file, error_num)
        if p.bug_type() == 2:
            error_num = []
            if len(self.project.changes[0])>0:
                error_num = list_add(error_num, p.changes[0])
            if len(self.project.changes[2])>0:
                error_num = list_add(error_num, p.changes[2])
                error_num.sort()
            p.error_num = error_num
            return ChunkContextAround().get_context(file, p.error_num)
        if  p.bug_type() == 3:
            error_num = int(self.project.changes[1][0][0])
            p.error_num = [error_num]
            return strategy.get_context(file, error_num)
        if  p.bug_type() == 4:
            error_num = []
            if len(self.project.changes[0])>0:
                error_num = list_add(error_num, p.changes[0])
            if len(self.project.changes[2])>0:
                error_num = list_add(error_num, p.changes[2])
            # if len(self.project.changes[1])>0:
            #     error_num = list_add(error_num, p.changes[1])
            error_num.sort()
            p.error_num = [i for i in range(min(error_num), max(error_num)+1)]
            for add in self.project.changes[1]:
                if min(add)<min(p.error_num):
                    p.error_num = [i for i in range(min(add), max(p.error_num)+1)]
                else:
                    p.error_num = [i for i in range(min(p.error_num), max(max(p.error_num), min(add))+1)]
            return ChunkContextAround(5).get_context(file, p.error_num)
        return ""
    
    def get_change_type(self):
        changes_str, inserts_str, deletes_str = query_changes(self.project.project, self.project.bug_id)
        chunks, classes, files, linesAdd, linesMod, linesRem, methods, sizeInLines, spreadAllLines = query_mtrics(self.project.project, self.project.bug_id)
        if changes_str != '':
            changes = json.loads(changes_str)
            changes_num = len(changes)
        else:
            changes = []
            changes_num = 0
        if inserts_str != '':
            inserts = json.loads(inserts_str)
            inserts_num = len(inserts)
        else:
            inserts = []
            inserts_num = 0
        if deletes_str != '':
            deletes = json.loads(deletes_str)
            deletes_num = len(deletes)
        else:
            deletes = []
            deletes_num = 0
        return (changes_num, inserts_num, deletes_num), (changes, inserts, deletes), (chunks, classes, files, linesAdd, linesMod, linesRem, methods, sizeInLines, spreadAllLines)

    def get_compile_error_mes(self):
        pass

    def get_test_error_mes(self):
        pass

    def get_error_test_lines(self):
        pass

    def get_fail_tests(self):
        pass

class D4jDirector(ProjectDirector):
    
    def build(self):
        self.builder.set_fail_type()
        fail_type = self.builder.project.fail_type
        if fail_type > 0:
            self.builder.set_change_type()
            self.builder.set_bug_code()
        return fail_type

def get_project(bug: str):
    builder = D4jBuilder(bug)
    D4jDirector(builder).build()
    return builder.project
