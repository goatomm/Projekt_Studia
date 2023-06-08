import pygame
import os
import math

pygame.init()

WIDTH, HEIGHT = 750, 750
GROUND_HEIGHT = 50
GRAVITY = 0.2  # Stała siła grawitacji
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE LANDER")

# Ładowanie obrazków
SHIP_IMG = pygame.image.load(os.path.join("assets", "statek.png"))
FLAME_IMG = pygame.image.load(os.path.join("assets", "flame.png"))
FLAME_IMG = pygame.transform.scale(FLAME_IMG, (40, 40))
FLAME_IMG = pygame.transform.flip(FLAME_IMG, False, True)
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Inicjalizacja czcionek
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 36)

class Ship:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.ship_img = SHIP_IMG
        self.flame_img = FLAME_IMG
        self.show_flame = False
        self.flame_timer = 0  # Licznik czasu płomienia
        self.flame_duration = 1000  # Czas trwania płomienia w milisekundach
        self.angle = 0
        self.speed = 5
        self.landed = False  # Zmienna śledząca, czy statek wylądował
        self.successful_landing = False  # Zmienna śledząca, czy lądowanie się powiodło

    def draw(self, window):
        rotated_ship_img = pygame.transform.rotate(self.ship_img, self.angle)
        new_rect = rotated_ship_img.get_rect(center=self.ship_img.get_rect(topleft=(self.position.x, self.position.y)).center)
        window.blit(rotated_ship_img, new_rect.topleft)

        if self.show_flame:
            self.draw_flame(window)

        # Sprawdzamy, czy statek dotyka podłoża
        if self.position.y + self.ship_img.get_height() >= HEIGHT - GROUND_HEIGHT:
            self.velocity.y = 0  # Zatrzymujemy ruch pionowy statku
            self.position.y = HEIGHT - GROUND_HEIGHT - self.ship_img.get_height()  # Ustalamy statkowi pozycję na wysokości podłoża
            if not self.landed:
                self.landed = True
                # Sprawdzamy, czy statek jest w odpowiednim kącie nachylenia do lądowania
                angle_diff = abs(self.angle % 90)  # Różnica między kątem a najbliższą wartością 90 stopni
                max_angle_diff = 90 * 0.2  # Maksymalna dozwolona różnica kąta (20% od 90 stopni)
                if angle_diff <= max_angle_diff:
                    self.successful_landing = True
                else:
                    self.successful_landing = False
                    self.velocity.x = 0  # Zatrzymujemy ruch poziomy statku
        else:
            self.landed = False

    def draw_flame(self, window):
        flame_distance = 60  # Odległość od statku do płomienia
        offset = pygame.math.Vector2(0, flame_distance + self.ship_img.get_height() / 5)  # Offset gdy statek jest zwrócony w górę
        offset.rotate_ip(-self.angle)  # Obracamy offset o kąt statku
        flame_pos = self.position + offset  # Dodajemy offset do pozycji statku

        # Wyśrodkowanie płomienia na statku
        flame_center = (flame_pos.x + self.ship_img.get_width() / 2, flame_pos.y + self.ship_img.get_height() / 2)

        rotated_flame_img = pygame.transform.rotate(self.flame_img, self.angle)
        rotated_rect = rotated_flame_img.get_rect(center=flame_center)
        window.blit(rotated_flame_img, rotated_rect.topleft)

    def toggle_flame(self, state):
        self.show_flame = state
        if state:
            self.flame_timer = pygame.time.get_ticks()  # Resetujemy licznik czasu płomienia

    def rotate_left(self):
        self.angle = (self.angle + 5) % 360

    def rotate_right(self):
        self.angle = (self.angle - 5) % 360

    def move(self):
        radians_angle = math.radians(self.angle + 90)  # Dodajemy 90 stopni
        direction = pygame.math.Vector2(math.cos(radians_angle), -math.sin(radians_angle))  # Odwracamy sinus

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # do przodu
            self.toggle_flame(True)
            self.velocity = self.speed * direction
            self.velocity.y += GRAVITY  # Dodajemy siłę grawitacyjną do składowej pionowej prędkości statku
        else:
            self.toggle_flame(False)
            if not self.landed:
                self.velocity.y += GRAVITY  # Dodajemy siłę grawitacyjną tylko gdy statek nie jest wylądowany

        # Obliczamy nową pozycję, ale jeszcze jej nie zapisujemy
        new_position = self.position + self.velocity

        # Sprawdzamy kolizję z podłożem
        if new_position.y + self.ship_img.get_height() > HEIGHT - GROUND_HEIGHT:
            new_position.y = HEIGHT - GROUND_HEIGHT - self.ship_img.get_height()
            if not self.landed:
                self.velocity.y = 0  # Zatrzymujemy ruch pionowy statku
                # Sprawdzamy, czy statek jest w odpowiednim kącie nachylenia do lądowania
                angle_diff = abs(self.angle % 90)  # Różnica między kątem a najbliższą wartością 90 stopni
                max_angle_diff = 90 * 0.2  # Maksymalna dozwolona różnica kąta (20% od 90 stopni)
                if angle_diff <= max_angle_diff:
                    self.successful_landing = True
                else:
                    self.successful_landing = False
                    self.velocity.x = 0  # Zatrzymujemy ruch poziomy statku

        # Ograniczamy pozycję statku do granic ekranu
        if new_position.x < 0:
            new_position.x = 0
        elif new_position.x > WIDTH - self.ship_img.get_width():
            new_position.x = WIDTH - self.ship_img.get_width()

        # Aktualizujemy pozycję statku na nową pozycję
        self.position = new_position

def main_menu():
    run = True

    while run:
        WIN.fill((0, 0, 0))
        title_text = FONT.render("SPACE LANDER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        WIN.blit(title_text, title_rect)

        play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(WIN, (255, 255, 255), play_button)
        play_text = FONT.render("Graj", True, (0, 0, 0))
        play_text_rect = play_text.get_rect(center=play_button.center)
        WIN.blit(play_text, play_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    run = False
                    main_game()

    pygame.quit()

def main_game():
    run = True
    FPS = 60

    player = Ship(300, HEIGHT - GROUND_HEIGHT - 50)  # Ustalamy początkową pozycję statku na wysokości podłoża

    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # lewo
            player.rotate_left()
        elif keys[pygame.K_d]:  # prawo
            player.rotate_right()

        player.move()

        WIN.blit(BG, (0, 0))
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))  # Rysowanie podłoża
        player.draw(WIN)

        # Wyświetlanie komunikatu o lądowaniu
        if player.landed:
            if player.successful_landing:
                text = "Udane lądowanie!"
            else:
                text = "Nieudane lądowanie. Zbyt duży kąt nachylenia."
            text_surface = FONT.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WIN.blit(text_surface, text_rect)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
