class School:
    """ Школа """
    id: int = None
    county: str = None
    name: str = None
    shortname: str = None
    ou_types: str = None
    principal: str = None
    comments: str = None
    guid: str = None
    address: str = None
    email: str = None
    site: str = None
    __client = None

    def __init__(self, client, school_id: int):
        """ Конструктор. Требует объект client и ID школы """
        self.__client = client
        data = self.__client.make_request(f"/core/api/schools/{school_id}")
        self.id = data["id"]
        self.county = data["county"]
        self.name = data["name"]
        self.ou_types = data["ou_types"]
        self.principal = data["principal"]
        self.comments = data["comments"]
        self.guid = data["guid"]
        self.address = data["address"]
        self.email = data["email"]
        self.site = data["site"]
