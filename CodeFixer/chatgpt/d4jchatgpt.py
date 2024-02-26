import re
from CodeFixer.models import Answer
from CodeFixer.chatgpt.basechatgpt import BaseChatGPT
from CodeFixer.models.analysis import Analysis
from CodeFixer.config.d4jcfg import D4jCfg as cfg
from CodeFixer.db import baseSession


def extract_triple_quotes(text: str):
    text = text.replace('```java', '```')
    # 使用正则表达式找到所有三引号之间的内容
    matches = re.findall(r"```(.*?)```", text, re.DOTALL)
    # 将找到的匹配项转换为整数，并返回这个列表
    return [match for match in matches]


class D4jChatGPT(BaseChatGPT):
    def __init__(self, bug: str):
        super().__init__(cfg.model2, bug)

    def save_ans(self, bug: str, res_epoch: int, step: int, res: str, ep: int):
        res = list(extract_triple_quotes(res))
        if len(res) > cfg.patch_num/2: 
            for index, r in enumerate(res):
                with baseSession() as session:
                    session.add(Answer(bug=bug, epoch=(res_epoch-1)*cfg.patch_num+index+1, step=step, answer=r, analysis_epoch=ep))
        else:
            self.logger.info("生成的补丁数量有问题，请检查！")