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
        """
        Конструктор:
        param client: Объект класса dnevnik.Client нужен для выолнения запросов
        param class_unit_id: id класса
        """
        self.__client = client
        data = client.make_request(f"/core/api/class_units/{class_unit_id}")
        # Id класса
        self.id: int = data["id"]
        # Имя класса (отображаемое)
        self.display_name: str = data["display_name"]
        # Буква класса
        self.letter: str = data["letter"]
        # Имя класса
        self.name: str = data["name"]
        # Процент учащихся с дополнителтным образованием
        self.ae_percentage: float = data["ae_percentage"]
        # Число учащихся
        self.student_count: int = data["student_count"]
        # Класс домашнего обучения
        self.home_based: bool = data["home_based"]

    @property
    def school(self):
        """
        Школа класса
        """
        return School(self.__client, self.__school_id)
