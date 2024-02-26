from abc import ABC, abstractmethod
import json
import os
from CodeFixer.chatgpt import BaseChatGPT
from CodeFixer.models.analysis import Analysis
from CodeFixer.program.project import Project
from CodeFixer.db import baseSession
from CodeFixer.config import tems
from CodeFixer.config import BaseCfg as cfg


class Template(ABC):
    def __init__(self, p: Project):
        self.system_mes = ""
        self.user_mes = ""
        # self.marker = cfg.marker[0]
        # self.tem_name = 'T5'
        self.p = p

    @abstractmethod
    def make_template(self, ep: int=0):
        pass

    
    # def get_template(self):
    #     return self.system_mes, self.user_mes
    
    def tell_gpt(self, gpt: BaseChatGPT):
        if self.system_mes != "":
            gpt.add_message(self.system_mes, 'system')
        gpt.add_message(self.user_mes)


class AnalysisTemplate(Template):
    def make_template(self, ep:int =0):
        p = self.p
        method = p.fail_test.split('::')[1]
        print(p.bug_code)
        if p.bug_type() == 1 or p.bug_type() == 2 or p.bug_type() == 3 or p.bug_type() == 4:
            code_list = p.bug_code.splitlines()
            fault_line = ""
            for line in code_list:
                if line.startswith('- '):
                    if fault_line != "":
                        fault_line += '\n'
                    fault_line += line
            sub_fault_line = fault_line.replace('- ', '')
            code = p.bug_code.replace(fault_line, (len(sub_fault_line) - len(sub_fault_line.lstrip()))*' ' +cfg.marker[0] + '\n' + sub_fault_line)
            if p.bug_type() == 1:
                self.user_mes = tems['T8']['user'] % (cfg.language, code, sub_fault_line, method ,p.error_test_lines.strip(), p.test_error_mes)
            if p.bug_type() == 2 or p.bug_type() == 3 or p.bug_type() == 4:
                self.user_mes = tems['T10']['user'] % (cfg.language, code, sub_fault_line, method ,p.error_test_lines.strip(), p.test_error_mes)
        # if p.bug_type() == 4:
        #     self.user_mes = tems['T12']['user'] % (cfg.language, p.bug_code, method ,p.error_test_lines.strip(), p.test_error_mes)
            

    
class patchTemplate(Template):
    def make_template(self, ep: int=0):
        try:
            p = self.p
            code_list = p.bug_code.splitlines()
            fault_line = ""
            for line in code_list:
                if line.startswith('- '):
                    if fault_line != "":
                        fault_line += '\n'
                    fault_line += line
            sub_fault_line = fault_line.replace('- ', '')
            code = p.bug_code.replace(fault_line, (len(sub_fault_line) - len(sub_fault_line.lstrip()))*' ' +cfg.marker[1])
            with baseSession() as session:
                query = session.query(Analysis).filter(Analysis.bug == p.name)
                result = query.all()
                print("开始测试")
                if p.bug_type() == 1:
                    self.system_mes = tems['T9']['system'] % (cfg.patch_num)
                    self.user_mes = tems['T9']['user'] % (cfg.language, code, sub_fault_line, result[ep].analysis)
                if p.bug_type() == 2 or p.bug_type() == 3 or p.bug_type() == 4:
                    self.system_mes = tems['T11']['system'] % (cfg.patch_num)
                    self.user_mes = tems['T11']['user'] % (cfg.language, code, sub_fault_line, result[ep].analysis)
                # if p.bug_type() == 4:
                #     self.system_mes = tems['T13']['system']
                #     self.user_mes = tems['T13']['user'] % (cfg.language, code, result[ep].analysis)
        except Exception as e:
            print(e)
            # print(self.system_mes)
            # print(self.user_mes)
    


# class LineTemplate(Template):
#     # 针对单行修改的模板
#     def make_template(self, bug_code: str, test_line: str, error_mes: str):
#         code_list = bug_code.splitlines()
#         for line in code_list:
#             if line.startswith('- '):
#                 fault_line = line
#         code = bug_code.replace(fault_line, self.marker)
#         fault_line = fault_line.replace('- ', '')
#         self.system_mes = tems['T5']['system'] % cfg['patch_num']
#         self.user_mes = tems['T5']['user'] % (code, fault_line, test_line, error_mes)


# class EngTemplate(Template):
#     # 针对单行修改的模板
#     def make_template(self, bug_code: str, test_line: str, error_mes: str, method: str):
#         code_list = bug_code.splitlines()
#         for line in code_list:
#             if line.startswith('- '):
#                 fault_line = line
#         code = bug_code.replace(fault_line, self.marker)
#         fault_line = fault_line.replace('- ', '')
#         self.system_mes = tems['T1']['system'] % cfg['patch_num']
#         self.user_mes = tems['T1']['user'] % (code, fault_line, method, test_line, error_mes)


# class EngAddTemplate(Template):
#     # 针对单行添加的模板
#     def make_template(self, bug_code: str, test_line: str, error_mes: str, method: str):
#         code_list = bug_code.splitlines()
#         for line in code_list:
#             if line.startswith('- '):
#                 fault_line = line
#         code = bug_code.replace(fault_line, self.marker + '\n' + fault_line)
#         rep_line = fault_line.replace('- ', '')
#         code = code.replace(fault_line, rep_line)
#         fault_line = "    "
#         self.system_mes = tems['T1']['system'] % cfg['patch_num']
#         self.user_mes = tems['T1']['user'] % (code, fault_line, method, test_line.strip(), error_mes)

# class EngChunkTemplate(Template):
#     # 针对单块的模板
#     def make_template(self, bug_code: str, test_line: str, error_mes: str, method: str):
#         code_list = bug_code.splitlines()
#         fault_line = []
#         for index, line in enumerate(code_list):
#             if line.startswith('- '):
#                 fault_line.append(line.replace('- ', ''))
#                 if self.marker not in code_list:
#                     code_list[index] = self.marker
#                 else:
#                     code_list[index] = ""
#         code = ""
#         for l in code_list:
#             if l != "":
#                 code += l + '\n'
#         # code = "\n".join(code_list)
#         # code = code.replace('\n\n')
#         fault_lines = "\n".join(fault_line)
#         self.system_mes = tems['T2']['system'] % cfg['patch_num']
#         # self.system_mes = tems['T2']['system']
#         self.user_mes = tems['T2']['user'] % (code, fault_lines, method, test_line.strip(), error_mes)

# class EngAddChunkTemplate(Template):
#     # 针对单块添加的模板
#     def make_template(self, bug_code: str, test_line: str, error_mes: str, method: str):
#         code_list = bug_code.splitlines()
#         for line in code_list:
#             if line.startswith('- '):
#                 fault_line = line
#         code = bug_code.replace(fault_line, self.marker + '\n' + fault_line)
#         rep_line = fault_line.replace('- ', '')
#         code = code.replace(fault_line, rep_line)
#         fault_line = "    "
#         self.system_mes = tems['T2']['system'] % cfg['patch_num']
#         self.user_mes = tems['T2']['user'] % (code, fault_line, method, test_line.strip(), error_mes)