from uuid import UUID

class TVShow:
    def __init__(self, id: UUID, name: str, first_air_date: str, overview: str, user_id: UUID):
        self.id = id
        self.name = name
        self.first_air_date = first_air_date
        self.overview = overview
        self.user_id = user_id
