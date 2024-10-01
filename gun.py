class Gun:
    def __init__(self, name, damage, range, ammo):
        self.name = name
        self.damage = damage
        self.range = range
        self.ammo = ammo

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            return True
        return False

    def reload(self, ammo):
        self.ammo += ammo