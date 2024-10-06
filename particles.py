import pyray

class Particle:
    def __init__(self, x, y, vx, vy, speed, lifespan, size, color, shape):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed = speed
        self.lifespan = lifespan
        self.size = size
        self.color = color
        self.alpha = self.color[-1]
        self.shape = shape

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update(self, delta_time):
        self.x += self.vx * self.speed * delta_time
        self.y += self.vy * self.speed * delta_time
        if self.alpha > 0 and self.lifespan > 0:
            self.alpha -= (255 / self.lifespan * delta_time)
            self.lifespan -= delta_time

    def draw(self):
        if self.alpha > 0:
            r, g, b, _ = self.color  # Unpack the color tuple
            color = pyray.Color(r, g, b, round(self.alpha))
            if self.shape == 'circle':
                pyray.draw_circle(int(self.x), int(self.y), self.size, color)
            elif self.shape == 'square':
                pyray.draw_rectangle(int(self.x) - self.size, int(self.y) - self.size, self.size * 2, self.size * 2, color)
            elif self.shape == 'triangle':
                pyray.draw_triangle(
                    pyray.Vector2(self.x, self.y - self.size),
                    pyray.Vector2(self.x - self.size, self.y + self.size),
                    pyray.Vector2(self.x + self.size, self.y + self.size),
                    color
                )

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, vx, vy, speed, lifespan, size, color, shape):
        self.particles.append(Particle(x, y, vx, vy, speed, lifespan, size, color, shape))

    def apply_force_to_all(self, fx, fy):
        for particle in self.particles:
            particle.apply_force(fx, fy)

    def update(self, delta_time):
        for particle in self.particles:
            particle.update(delta_time)
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()