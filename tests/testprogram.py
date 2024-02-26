import traceback
import unittest
from CodeFixer import get_project, QueryChatGPT, D4jChatGPT
from CodeFixer import AnalysisTemplate, patchTemplate
from CodeFixer import PatchValidator, D4jPatchValidator
from CodeFixer.dao.d4jdao import query_add_lines, query_chunks, query_single_line
from CodeFixer.db import baseSession
from CodeFixer.models.fix import Fix

class TestProgram(unittest.TestCase):
    project = 'Math'
    bug_id = 7
    bug = project+'_'+str(bug_id)

    # def test_Build(self):
    #     p = get_project(self.bug)
    #     print(p.bug_code)
    
    # def test_gpt(self):
    #     gpt = QueryChatGPT(self.bug)
    #     gpt.add_message("你是谁")
    #     gpt.send_message()

    # def test_tem(self):
    #     p = get_project(self.bug)
    #     tem = AnalysisTemplate(p)
    #     tem.make_template()
    #     print(tem.user_mes)

    # def test_analysis(self):
    #     p = get_project(self.bug)
    #     tem = AnalysisTemplate(p)
    #     tem.make_template()
    #     gpt = QueryChatGPT(self.bug)
    #     tem.tell_gpt(gpt)
    #     gpt.send_message()

    def test_patch_template(self):
        # sigle_line = query_single_line()
        # single_bugs = [p+'_'+str(b) for p, b in sigle_line]
        # with baseSession() as session:
        #     query = session.query(Fix.bug)
        #     res = query.all()
        # part = [item[0] for item in res]

        # print(part)
        # fixed_line = ''
        # for 
        # print(single_bugs)
        # for bug in single_bugs:
        #     try:
        #         if bug in part:
        #             continue
        # bugs = ['Math_20', 'Math_56', 'Math_91', 'Math_101', 'Mockito_1', 'Mockito_22', 'Mockito_27', 'Mockito_28', 'Time_11', 'Closure_35', 'Closure_59', 'Closure_55', 'Closure_83', 'Closure_82', 'Closure_97', 'Closure_109', 'Closure_111', 'Closure_112', 'Closure_122']
        # bugs = ['Chart_7']
        # res = query_add_lines()
        # bugs = [p + '_' + str(b) for p, b in res]
        # res = query_chunks()
        # bugs = [p + '_' + str(b) for p, b in res]
        bugs = ['Mockito_18']
        print(bugs)
        for bug in bugs:
            try:
                # if not bug.startswith('Time'):
                #     continue
                print(bug)
                p = get_project(bug)
                # 分析
                tem1 = AnalysisTemplate(p)
                tem1.make_template()
                gpt1 = QueryChatGPT(bug)
                tem1.tell_gpt(gpt1)
                gpt1.send_message()
                # 生成
                tem2 = patchTemplate(p)
                gpt2 = D4jChatGPT(bug)
                for ep in range(3):
                    tem2.make_template(ep=ep)
                    tem2.tell_gpt(gpt2)
                    gpt2.send_message(ep=ep+1)
                    gpt2.clear()
                # 补丁验证
                validator = D4jPatchValidator(p)
                if validator.test_patch():
                    print("修复成功")
                else:
                    print("修复失败")
            except Exception as e:
                print(e)
                stack_trace = traceback.format_exc()
                print("堆栈跟踪信息: %s", stack_trace)
    
    # def test_single_bug(self):

        
if __name__ == '__main__':
    unittest.main()