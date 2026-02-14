class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def move(self):
        self.y -= 20
        if self.y < 0:
            self.active = False

class Character:
    def __init__(self):
        self.x = 250
        self.y = 400
        self.power = False
        self.bullets = []

    # Movement
    def move_left(self):
        self.x = max(0, self.x - 20)

    def move_right(self):
        self.x = min(500, self.x + 20)

    def move_up(self):
        self.y = max(0, self.y - 20)

    def move_down(self):
        self.y = min(500, self.y + 20)

    # Power
    def activate_power(self):
        self.power = True

    def deactivate_power(self):
        self.power = False

    # Shooting
    def shoot(self, gesture_fingers):
        if "Thumb" in gesture_fingers and "Pinky" in gesture_fingers:
            self.bullets.append(Bullet(self.x - 10, self.y))
            self.bullets.append(Bullet(self.x + 10, self.y))
        elif gesture_fingers == ["Thumb"]:
            self.bullets.append(Bullet(self.x, self.y))

    # Update bullets
    def update_bullets(self):
        for b in self.bullets:
            b.move()
        self.bullets = [b for b in self.bullets if b.active]