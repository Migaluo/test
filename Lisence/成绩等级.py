#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s\'s score is %s'%(self.name,self.score))

    def return_grand(self):
        if self.score == 100:
            return 'S'
        elif self.score > 90:
            return 'A'
        elif self.score >80:
            return 'B'
        elif self.score >70:
            return 'C'
        elif self.score >60:
            return 'D'
        else:
            return 'Bad'

