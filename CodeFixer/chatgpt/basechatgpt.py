from abc import ABC, abstractmethod
import os
import traceback
from openai import OpenAI
from CodeFixer.utils.logutil import setup_logger
from CodeFixer.config.basecfg import BaseCfg



cfg = BaseCfg()

class BaseChatGPT(ABC):
    def __init__(self, model: str, bug: str):
        self.history = []
        self.client = OpenAI()
        self.model = model
        self.bug = bug
        self.step = 0
        self.logger = setup_logger('gpt_interactions', os.path.join(cfg.log_dir, 'gpt',  f"{bug}.log"))

    def send_message(self, ep: int=0):
        self.logger.info("发送的消息如下：")
        for mes in self.history:
            self.logger.info(mes['role'])
            self.logger.info(mes['content'])
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            stream=False,
            n=cfg.epochs,
        )
        try:
            for epoch, choice in enumerate(response.choices):
                res = choice.message.content
                self.logger.info("\n----------------------------------------------------------------------")
                self.logger.info(res)
                self.logger.info("\n----------------------------------------------------------------------")
                self.save_ans(self.bug, epoch+1, self.step, res, ep)
        except Exception as e:
            self.logger.error(e)
            # 获取堆栈跟踪信息
            stack_trace = traceback.format_exc()
            self.logger.error(f"{self.bug}b 出现了异常")
            self.logger.error(e)
            self.logger.error("堆栈跟踪信息: %s", stack_trace)

    @abstractmethod
    def save_ans(self, bug: str, res_epoch: int, step: int, res: str, ep: int):
        """
        提取chagpt的信息保存
        """
        pass

    def add_message(self, message, sender="user",):
        # self.history.append({"role": 'system', "content": self.system_message})
        self.history.append({"role": sender, "content": message})

    def get_last_message(self):
        return self.history[-1] if self.history else None

    def get_full_history(self):
        return self.history
    
    def clear(self):
        self.history = []