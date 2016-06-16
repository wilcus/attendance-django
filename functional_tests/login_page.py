from page_objects import PageObject, PageElement


class LoginPage(PageObject):
    username = PageElement(id_='id_username')
    password = PageElement(name='password')
    login = PageElement(css='input[type="submit"]')
