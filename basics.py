
""" 
import datetime
mynow = datetime.datetime.now()
print("The date and time is:", datetime.datetime.now())
print(datetime.datetime.now())
print(mynow)

mynumber = 10
mytext = "Hello"

print(mynumber,mytext)
------------------------------------------------------ 

student_grades = [9.1,8.8,7.5]
student_grades = {"Marry":9.1,"Sim":8.8, "John":7.5}

mysum= sum(student_grades.values())
length=len(student_grades)
mean = mysum/length
print(mean)  

--------------------------------------------------------
student_grades = [9.8,1.3,9.3]

my_sum = sum(student_grades)
length = len(student_grades)
mean = mysum/length
print(mean)
========================================================

def mean(mylist):
    the_mean = sum(mylist)/len(mylist)
    return the_mean

print(mean([1,4,5]))
---------------------------------------------------------
"""
def mean(myList)
    
    the_mean=sum(mylist)/len(mylist)
    return the_mean

mymean = mean([1,2,3,4])
print(mymean+10)