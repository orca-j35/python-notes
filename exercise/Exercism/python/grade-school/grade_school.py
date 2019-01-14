class School(object):
    def __init__(self):
        self.__db = dict()

    def add_student(self, name, grade):
        self.__db.setdefault(grade, set()).add(name)

    def roster(self):
        return [i for k in sorted(self.__db.keys()) for i in self.grade(k)]

    def grade(self, grade_number):
        return sorted(self.__db.get(grade_number, []))
