from page_objects import PageObject, MultiPageElement


class ListStudentPage(PageObject):
    # ul > li
    li_students = MultiPageElement(class_name="registered--item")

    @property
    def students_registered(self):
        students_registered = map(lambda li_student: li_student.text, self.li_students)
        return students_registered
