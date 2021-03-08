# 使用超级鹰识别12306验证码，然后使用Selenium登录12306
# 超级鹰：https://www.chaojiying.com/
# 12306: https://kyfw.12306.cn/otn/resources/login.html

import time
import requests
from hashlib import md5

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

# 创建一个参数对象
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
# 设置界面最大化
chrome_options.add_argument('--start-maximized')
# 规避对selenium的检测
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def main():
    # 创建浏览器对象
    browser = webdriver.Chrome(options=chrome_options)
    # 打开12306登录页面
    login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
    browser.get(login_url)
    # 执行js代码，修改selenium标识，绕过网站对selenium的检测
    browser.execute_script('Object.defineProperties(navigator,{webdriver:{get:()=>undefined}})')
    time.sleep(2)
    # 选择“账号登录”
    browser.find_element_by_xpath('//li[@class="login-hd-account"]/a').click()
    time.sleep(2)
    # 将当前页面进行截图且保存
    browser.save_screenshot('page.png')
    # 图片元素
    code_img_ele = browser.find_element_by_id('J-loginImg')
    # 验证码图片左上角坐标 {'x': 1005, 'y': 291}
    location = code_img_ele.location
    print('location：', location)
    # print(location['x'])
    # print(type(location['x']))
    # print('*' * 60)
    # 验证码图片的长和宽 {'height': 190, 'width': 320}
    size = code_img_ele.size
    print('size：', size)
    # print(size['height'])
    # print(type(size['height']))
    # 确定验证码左上角和右下角坐标（裁剪的区域就确定了）
    rangle = (location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height'])
    print('rangle：', rangle)
    # 裁剪验证码区域
    img = Image.open('page.png')
    code_img_name = 'code.png'
    # crop根据指定区域进行图片裁剪（注意：将Windows下“缩放与布局”调整为100%）
    frame = img.crop(rangle)
    frame.save(code_img_name)
    # 将验证码图片提交给超级鹰进行识别
    chaojiying = Chaojiying_Client('username', 'password', 'id')
    im = open('code.png', 'rb').read()
    # 结果示例：56,183|86,94
    result = chaojiying.PostPic(im, 9004)['pic_str']
    print('result：', result)
    # 处理超级鹰返回来的数据
    # 存储即将被点击的点的坐标 [[x1,y1],[x2,y2]]
    all_list = []
    if '|' in result:
        list_1 = result.split('|')
        count_1 = len(list_1)
        for i in range(count_1):
            xy_list = []
            x = int(list_1[i].split(',')[0])
            y = int(list_1[i].split(',')[1])
            xy_list.append(x)
            xy_list.append(y)
            all_list.append(xy_list)
    else:
        xy_list = []
        x = int(result.split(',')[0])
        y = int(result.split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
    print('all_list：', all_list)
    # 输入用户账号
    browser.find_element_by_id('J-userName').send_keys('xxx')
    time.sleep(0.5)
    # 输入用户密码
    browser.find_element_by_id('J-password').send_keys('xxx')
    # 遍历列表，使用动作量对每一个列表元素对应的x,y指定的位置进行操作
    for oli in all_list:
        x = oli[0]
        y = oli[1]
        ActionChains(browser).move_to_element_with_offset(code_img_ele, x, y).click().perform()
        time.sleep(0.5)
    time.sleep(3)
    # 点击登录按钮
    browser.find_element_by_id('J-login').click()
    time.sleep(3)
    # 找到滑块
    slider = browser.find_element_by_xpath('//span[@id="nc_1_n1z"]')
    # 找到滑块轨迹
    track = browser.find_element_by_id('nc_1__scale_text')
    time.sleep(0.5)
    # 滑动滑块
    action = ActionChains(browser)
    action.drag_and_drop_by_offset(slider, track.size['width'], -slider.size['height']).perform()
    time.sleep(5)
    browser.quit()


if __name__ == '__main__':
    main()
