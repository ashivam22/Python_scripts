def mean(value):
    if type(value) == dict:
        the_mean = sum(value.values()) / len(value)
    else:
        the_mean = sum(value)/len(value)

    return the_mean

monday_temperatures = [9.8,2.4,4.5]
student_grades = {"Marry":9.1, "bhaiko":4.4, "jijaji":7.5}

print(mean(monday_temperatures))