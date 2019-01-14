import re
students = [
    'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Fred', 'Ginny', 'Harriet',
    'Ileana', 'Joseph', 'Kincaid', 'Larry'
]


class Garden(object):
    plant_names = {
        'G': 'Grass',
        'C': 'Clover',
        'R': 'Radishes',
        'V': 'Violets'
    }

    def __init__(self, diagram: str, students=students):
        students.sort()
        pattern = re.compile(r'\w\w')
        self.stu = {
            k: i + j
            for i, j, k in zip(
                *[pattern.findall(i) for i in diagram.splitlines()], students)
        }

    def plants(self, student_name):
        return [Garden.plant_names.get(i) for i in self.stu.get(student_name)]
