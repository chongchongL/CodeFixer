from CodeFixer.chatgpt.basechatgpt import BaseChatGPT
from CodeFixer.db import baseSession
from CodeFixer.models.analysis import Analysis
from CodeFixer.config.basecfg import BaseCfg as cfg


class QueryChatGPT(BaseChatGPT):

    def __init__(self, bug: str):
        super().__init__(cfg.model1, bug)

    def save_ans(self, bug: str, res_epoch: int, step: int, res: str, ep: int):
        with baseSession() as session:
            session.add(Analysis(bug=bug, epoch=res_epoch, step=step, analysis=res))
    