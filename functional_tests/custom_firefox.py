from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class Firefox(webdriver.Firefox):
    def find_element_by_id(self, element_id):
        WebDriverWait(super(), timeout=30).until(
            lambda driver: driver.find_element_by_id(element_id),
            'Element with id {} not found.'.format(element_id)
        )
        return super().find_element_by_id(element_id)

    def find_element_by_link_text(self, link_text):
        WebDriverWait(super(), timeout=30).until(
            lambda driver: driver.find_element_by_link_text(link_text),
            'Element with text {} not found.'.format(link_text)
        )
        return super().find_element_by_link_text(link_text)
