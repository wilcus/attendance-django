from page_objects import MultiPageElement, PageObject


class CourseListPage(PageObject):
    links_courses = MultiPageElement(css=".courses a")

    @property
    def course_list(self):
        course_list = map(lambda link_course: link_course.text, self.links_courses)
        return course_list
