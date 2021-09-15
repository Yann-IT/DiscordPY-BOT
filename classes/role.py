class Role:
    current = 0
    Names = []

    def __init__(self, icon, name, num, description):
        self.name = name
        self.icon = icon
        self.num = num
        self.description = description

    def add(self, username):
        self.current += 1
        self.Names.append(username)

    def remove(self, username):
        if self.current - 1 >= 0:
            self.current -= 1
            del self.Names[self.Names.index(username)]
