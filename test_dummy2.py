class Student:
    def __init__(self, first_name):
        self.first_name = first_name

    # define getter method
    @property
    def get_name(self):
        return self.first_name


# create a new Student object
student = Student("Monica")

# access the first name using data property
print(student.first_name)  # Monica

# access the first name using getter property
print(student.get_name)  # Monica
