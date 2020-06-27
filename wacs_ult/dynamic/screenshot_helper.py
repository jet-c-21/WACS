# coding: utf-8
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver

from wacs_ult.public.save_tool import SaveTool


class ScreenshotHelper:
    def __init__(self, driver: webdriver, screenshot_save_path: str):
        self.scroll_delay = 0.3
        self.driver = driver
        self.screenshot_save_path = screenshot_save_path
        self.result = False


    def launch(self):
        image = self.fetch(self.driver)
        if image:
            SaveTool.save_screenshot(self.screenshot_save_path, image)
            self.result = True
        else:
            print('ss error')

    def fetch(self, driver: webdriver) -> Image:
        device_pixel_ratio = driver.execute_script('return window.devicePixelRatio')
        total_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        viewport_height = driver.execute_script('return window.innerHeight')
        total_width = driver.execute_script('return document.body.offsetWidth')
        viewport_width = driver.execute_script("return document.body.clientWidth")

        try:
            assert (viewport_width == total_width)
        except AssertionError as e:
            print('screen: ', e)

        # scroll the page, take screenshots and save screenshots to slices
        offset = 0
        slices = {}
        while offset < total_height:
            if offset + viewport_height > total_height:
                offset = total_height - viewport_height

            driver.execute_script('window.scrollTo({0}, {1})'.format(0, offset))
            time.sleep(self.scroll_delay)

            img = Image.open(BytesIO(driver.get_screenshot_as_png()))
            slices[offset] = img

            offset = offset + viewport_height

        # combine image slices
        stitched_image = Image.new('RGB', (total_width * device_pixel_ratio, total_height * device_pixel_ratio))
        for offset, image in slices.items():
            stitched_image.paste(image, (0, offset * device_pixel_ratio))

        return stitched_image
