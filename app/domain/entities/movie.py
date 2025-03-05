from uuid import UUID

class Movie:
    def __init__(self, id: UUID, title: str, release_date: str, overview: str, user_id: UUID):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.overview = overview
        self.user_id = user_id
