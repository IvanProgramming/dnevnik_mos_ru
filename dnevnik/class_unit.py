from dnevnik import School


class ClassUnit:
    """Объект класса"""
    __client = None
    id: int = None
    display_name: str = None
    letter: str = None
    name: str = None
    student_count: int = None
    ae_percentage: float = None
    home_based: bool = None

    __school_id: id = None

    def __init__(self, client, class_unit_id: int):
        self.__client = client
        data = client.make_request(f"/core/api/class_units/{class_unit_id}")
        self.id = data["id"]
        self.display_name = data["display_name"]
        self.letter = data["letter"]
        self.name = data["name"]
        self.ae_percentage = data["ae_percentage"]
        self.student_count = data["student_count"]
        self.home_based = data["home_based"]

    @property
    def school(self):
        return School(self.__client, self.__school_id)
