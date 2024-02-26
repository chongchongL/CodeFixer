import os
from CodeFixer.db import baseSession
from CodeFixer.models import Answer
from CodeFixer.program.project import Project
from sqlalchemy.orm import joinedload



class PatchValidator:
    def __init__(self, p: Project):
        self.p = p
        self.patch_file = os.path.join(self.p.project_path, "diff.patch")
        self.anwsers = []
        # self.get_patchs()
        self.sucess_type = 0   # 0 补丁错误  1 与人工编写的补丁一致  2 补丁正确与人工编写的不一致
        self.batch = 0  # 在第几轮次修复成功，0代表未修复成功
        self.unique = []
        self.correct_patch = "" # 正确的补丁
        # stats.add_project(self.p.project + str(self.p.bug_id))
    
    # def get_patchs(self):
    #     """
    #     获取所有的补丁
    #     """
    #     with baseSession() as session:
    #         query = session.query(Answer).filter(Answer.bug == self.p.name)
    #         for relationship in Answer.__mapper__.relationships.keys():
    #             query = query.options(joinedload(relationship))
    #         result = query.all()
    #         for r in result:
    #             print(r.answer)
    #         self.anwsers = result
