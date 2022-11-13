import os
from selenium import webdriver
from time import sleep
import pytesseract
from PIL import Image, ImageEnhance
from selenium.webdriver.common.by import By

# 验证码位置
left = 644
top = 447
right = left + 175
bottom = top + 64


# 验证码处理
def image_process(img):
    img = img.convert('RGBA')
    img = img.convert('L')
    img = ImageEnhance.Contrast(img)
    img = img.enhance(2.0)
    threshold = 80
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    img = img.point(table, '1')
    return img


driver = webdriver.Edge('msedgedriver.exe')
driver.get("http://zlapp.fudan.edu.cn/site/ncov/fudanDaily")
sleep(2)
now_handle = driver.current_window_handle
driver.switch_to.window(now_handle)

# login 等待3s响应
driver.find_element(value="username").clear()
driver.find_element(value="password").clear()
driver.find_element(value="username").send_keys("YOURID")
driver.find_element(value="password").send_keys("YOURPASSWORD")
driver.find_element(value="idcheckloginbtn").click()
sleep(3)

# 验证码可能会识别错误，因此要加入循环多次
while True:
    # 填报在校与位置获取
    driver.find_element(by=By.CLASS_NAME, value='wapat-btn').click()
    driver.find_element(by=By.XPATH,
                        value='/html/body/div[1]/div/div[1]/section/div[4]/ul/li[4]/div/div/div[1]').click()
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]/section/div[4]/ul/li[6]/div/input').click()
    # 位置获取比较慢 所以多等一会.....
    sleep(7)

    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]/section/div[5]/div/a').click()
    driver.find_element(by=By.XPATH, value='//*[@id="wapcf"]/div/div[2]/div[2]').click()
    sleep(3)
    driver.get_screenshot_as_file("D:\screenImg.png")
    # 从文件读取截图，截取验证码位置再次保存
    img = Image.open("D:\screenImg.png").crop((left, top, right, bottom))
    img = image_process(img)
    code = pytesseract.image_to_string(img).replace(" ", "")
    os.remove("D:\screenImg.png")
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div[1]/input').send_keys(code)
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div[3]').click()

    te = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[4]/div/p/span').text
    if "错误" in te:
        driver.refresh()
        sleep(2)
    else:
        driver.quit()
        break
