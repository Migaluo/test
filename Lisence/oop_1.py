class Student(object):
    def __init__(self,name,score):
        self.name = name
        self.score = score

    def Get_score(self):
        return self.score


    def Get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'

bart = Student('bart',59)
sun = Student('simon',90)
print(bart.Get_score(),bart.Get_grade())