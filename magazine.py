from datetime import timezone


# The Magazine Object
class Magazine:
    # Init an empty object.
    def __init__(self):
        self.id = None
        self.url = None
        self.title = None
        self.description = None
        self.snapshot = None
        self.category = None
        self.tags = set()
        self.language = None
        self.created_at = None
        self.updated_at = None

    # parso object to json.
    def to_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "snapshot": self.snapshot,
            "createdAt": self.created_at.replace(tzinfo=timezone.utc).timestamp() * 1000,
            "updatedAt": self.updated_at.replace(tzinfo=timezone.utc).timestamp() * 1000,
            "category": self.category,
            "tags": list(self.tags),
            "language": self.language
        }


# The builder of Magazine
class MagazineBuilder:
    # Init an empty magazine.
    def __init__(self):
        self.magazine = Magazine()

    # set a magazine id.
    def set_id(self, value):
        self.magazine.id = value

    # set a magazine url
    def set_url(self, value):
        self.magazine.url = value

    # set a magazine title
    def set_title(self, value):
        self.magazine.title = value

    # set a magazine description
    def set_description(self, value):
        self.magazine.description = value

    # set a magazine snapshot
    def set_snapshot(self, value):
        self.magazine.snapshot = value

    # set a magazine category
    def set_category(self, value):
        self.magazine.category = value

    # set a magazine tags
    def set_tags(self, value):
        self.magazine.tags = value

    # set a magazine language
    def set_language(self, value):
        self.magazine.language = value

    # set a magazine created at.
    def set_created_at(self, value):
        self.magazine.created_at = value

    # set a magazine created at.
    def set_updated_at(self, value):
        self.magazine.updated_at = value
