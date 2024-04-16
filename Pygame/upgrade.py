import pygame
class upgrade(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((20, 20))  # Power-up sprite size
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_boost = 0
        self.multi_shot = False
        self.penetration = False
        self.size_increase = 1  # Default size increase factor
        # Add more attributes as needed for other power-up types
    def activate(self,player):
        if self.speed_boost > 0:
            self.activate_speed_boost(player)
        if self.multi_shot:
            self.activate_multi_shot(player)
        if self.penetration:
            self.activate_penetration(player)
        self.increase_bullet_size(player)

    def activate_speed_boost(self, player):
        # Stub method for applying speed boost
        pass

    def activate_multi_shot(self, player):
        # Stub method for activating multi-shot ability
        pass

    def activate_penetration(self, player):
        # Stub method for activating penetration ability
        pass

    def increase_bullet_size(self, player):
        # Stub method for increasing bullet size
        pass

    def update(self):
        # You can add movement logic here if power-ups move on the screen
        pass