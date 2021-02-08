__version__ = "2.0.2"

try:
    from .school import School
    from .class_unit import ClassUnit
    from .group import Group
    from .teacher import Teacher
    from .student_profile import StudentProfile
    from .client import Client
except ModuleNotFoundError:
    print("Error, while module parsing")
