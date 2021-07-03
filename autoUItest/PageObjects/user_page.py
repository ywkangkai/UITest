

from Common.basepage import BasePage
from PageLocators.userPage_locator import UserPageLocator as loc

class UserPage(BasePage):

    # 获取用户余额
    def get_user_leftMoney(self):
        # 获取个人可用余额的文本内容
        text = self.get_element_text(loc.user_leftMoney,"个人页面_获取用户余额")
        # 截取数字部分 - 分隔符为 元
        return text.strip("元")

    # 获取第一条投资记录的时间、投资金额、收益金额 -- 扩展
    # def get_first_investRecord_info(self):
    #     pass