from student import Student

class CourseGroup:
  def __init__(self, student, classmates):
    self.student = student
    self.classmates = classmates # Список объектов класса Student

  def __str__(self):
    classmates_str = ", ".join([str(classmate) for classmate in self.classmates])
    return f"{self.student} учится вместе с: {classmates_str}"