from page_objects import PageObject, PageElement, MultiPageElement


class RegisterStudentPage(PageObject):
    checkboxes = MultiPageElement(xpath="//input[@type='checkbox']")
    submit_button = PageElement(name="submit")

    def register(self, student):
        student_chekbox = [checkbox for checkbox in self.checkboxes if checkbox.get_attribute("value") == student][0]
        student_chekbox.click()
        self.submit_button.click()
