


import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

from Common import logger
from Common.dir_config import screenshot_dir


class BasePage:

    # 包含了PageObjects当中，用到所有的selenium底层方法。
    # 还可以包含通用的一些元素操作，如alert,iframe,windows...
    # 还可以自己额外封装一些web相关的断言
    # 实现日志记录、实现失败截图

    def __init__(self,driver:WebDriver):
        self.driver = driver

    # 等待元素可见
    def wait_eleVisible(self,loc,img_doc="",timeout=30,frequency=0.5):
        logging.info("等待元素 {} 可见。".format(loc))
        # 起始等待的时间 datetime
        start = datetime.datetime.now()
        try:
            WebDriverWait(self.driver,timeout,frequency).until(EC.visibility_of_element_located(loc))
        except:
            # 日志
            logging.exception("等待元素可见失败：")
            # 截图 - 哪一个页面哪一个操作导致的失败。+ 当前时间
            self.save_web_screenshot(img_doc)
            raise
        else:
            # 结束等待的时间
            end = datetime.datetime.now()
            logging.info("开始等待时间点：{}，结束等待时间点：{}，等待时长为：{}".format(start, end, end - start))

    # 等待元素存在
    def wait_eleExists(self,loc,img_doc="",timeout=30,frequency=0.5):
        """
        :param loc:
        :param img_doc:
        :param timeout:
        :param frequency:
        :return:
        """
        logging.info("等待元素 {} 存在。".format(loc))
        # 起始等待的时间 datetime
        start = datetime.datetime.now()
        try:
            WebDriverWait(self.driver,timeout,frequency).until(EC.presence_of_all_elements_located(loc))
        except:
            # 日志
            logging.exception("等待元素存在失败：")
            # 截图 - 哪一个页面哪一个操作导致的失败。+ 当前时间
            self.save_web_screenshot(img_doc)
            raise
        else:
            # 结束等待的时间
            end = datetime.datetime.now()
            logging.info("开始等待时间点：{}，结束等待时间点：{}，等待时长为：{}".format(start, end, end - start))

    # 查找一个元素
    def get_element(self,loc,img_doc=""):
        """
        :param loc: 元素定位。以元组的形式。(定位类型、定位时间)
        :param img_doc: 失败截图的命名说明。例如：登陆页面_输入用户名
        :return: WebElement对象。
        """
        logging.info("查找 {} 中的元素 {} ".format(img_doc,loc))
        try:
            ele = self.driver.find_element(*loc)
            return ele
        except:
            # 日志
            logging.exception("查找元素失败")
            # 截图
            self.save_web_screenshot(img_doc)
            raise

    def click_element(self,loc,img_doc,timeout=30,frequency=0.5):
        """
        实现了，等待元素可见，找元素，然后再去点击元素。
        :param loc: 元组形式的元素定位表达式
        :param img_doc: 失败截图的文件命名
        :return: 无
        """
        # 1、等待元素可见
        self.wait_eleVisible(loc,img_doc,timeout,frequency)
        # 2、找元素
        ele = self.get_element(loc,img_doc)
        # 3、再操作
        logging.info(" 点击元素 {}".format(loc))
        try:
            ele.click()
        except:
            # 日志
            logging.exception("点击元素失败")
            # 截图
            self.save_web_screenshot(img_doc)
            raise

    def input_text(self,loc,img_doc,*args,timeout=30,frequency=0.5):
        """
        等待元素可见，找到元素，并在元素中输入文本信息。
        :param loc: 元组形式的元素定位表达式
        :param img_doc: 执行失败时，截图的文件命名。
        :param timeout: 等待元素的超时上限。
        :param frequency: 等待元素可见时，轮询周期。
        :param args: 输入操作中，可以输入多个值。也可以组合按键。
        :return: 无
        """
        # 1、等待元素可见
        self.wait_eleVisible(loc,img_doc,timeout,frequency)
        # 2、找元素
        ele = self.get_element(loc,img_doc)
        # 3、再操作
        logging.info(" 给元素 {} 输入文本内容:{}".format(loc,args))
        try:
            ele.send_keys(*args)
        except:
            # 日志
            logging.exception("元素输入操作失败")
            # 截图
            self.save_web_screenshot(img_doc)
            raise

    def get_element_attribute(self,loc,attr_name,img_doc,timeout=30,frequency=0.5):
        """
        等待元素存在、查找元素、再获取元素的某个属性值。
        :param loc: 元组形式的元素定位表达
        :param attr_name: 要获取的 元素的属性名称
        :param img_doc: 失败截图的文件命名
        :param timeout: 等待元素存在的超时上限。
        :param frequency: 等待元素存在时的，轮询周期。
        :return: 元素的属性值。
        """
        # 等待元素存在
        self.wait_eleExists(loc,img_doc,timeout,frequency)
        # 查找元素
        ele = self.get_element(loc,img_doc)
        # 获取属性
        try:
            attr_value =  ele.get_attribute(attr_name)
        except:
            # 日志
            logging.exception("获取元素属性失败")
            # 截图
            self.save_web_screenshot(img_doc)
            raise
        else:
            logging.info("获取元素 {} 的属性 {} 值为:{}".format(loc, attr_name, attr_value))
            return attr_value

    def get_element_text(self,loc,img_doc,timeout=30,frequency=0.5):
        """
        等待元素存在、查找元素、再获取元素的文本内容。
        :param loc: 元组形式的元素定位表达
        :param img_doc: 失败截图的文件命名
        :param timeout: 等待元素存在的超时上限。
        :param frequency: 等待元素存在时的，轮询周期。
        :return: 元素的文本内容
        """

        # 等待元素存在
        self.wait_eleExists(loc,img_doc,timeout,frequency)
        # 获取元素
        ele = self.get_element(loc, img_doc)
        # 获取属性
        try:
            text = ele.text
        except:
            # 日志
            logging.exception("获取元素文本值失败")
            # 截图
            self.save_web_screenshot(img_doc)
            raise
        else:
            logging.info("获取元素 {} 的文件值为:{}".format(loc, text))
            return text

    # 实现网页截图操作
    def save_web_screenshot(self,img_doc):
        #  页面_功能_时间.png
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filepath = "{}_{}.png".format(img_doc,now)
        try:
            self.driver.save_screenshot(screenshot_dir +"/" + filepath)
            logging.info("网页截图成功。图片存储在：{}".format(screenshot_dir +"/" + filepath))
        except:
            logging.exception("网页截屏失败！")


    # iframe切换
    def switch_to_iframe(self,iframe_pref,img_doc,timeout=30):
        """
        :param iframe_pref:
        :param img_doc:
        :param timeout:
        :return:
        """
        """
        等待iframe可用，并切换进去。
        :param iframe_pref: iframe的标识。支持下标、定位元组、WebElement对象、name属性
        :return: 无
        """
        try:
            WebDriverWait(self.driver,timeout).until(EC.frame_to_be_available_and_switch_to_it(iframe_pref))
        except:
            # 日志
            logging.exception("切换到 {} 的iframe元素：{} 失败！".format(img_doc,iframe_pref))
            # 截图
            self.save_web_screenshot(img_doc)
            raise
        else:
            time.sleep(0.5)
            logging.info("切换到 {} 的iframe元素：{} 成功！可以对新的html页面操作了！".format(img_doc,iframe_pref))


# select下拉列表

# 上传操作 -

# windows切换