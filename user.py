class User:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __str__(self):
        return f"User(name={self.name}, image={self.image})"

    def __repr__(self):
        return f"User(name={self.name}, image={self.image})"

    def set_name(self, name):
        self.name = name

    def set_image(self, image):
        self.image = image