import pygame
import math

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WHITE = (255, 255, 255)
FPS = 10

# Define a TextRenderer class to simplify argument passing
class TextRenderer:
    def __init__(self, screen, font, x_start=0, y_start=0, x_separator=10, y_separator=20):
        self.screen = screen
        self.font = font
        self.x_start = x_start
        self.y_start = y_start
        self.x_separator = x_separator
        self.y_separator = y_separator

    def display_text(self, letter):
        text = self.font.render(str(letter), True, WHITE)
        self.screen.blit(text, (self.x_start, self.y_start))
        self.x_start += self.x_separator

    def reset_line(self):
        self.y_start += self.y_separator
        self.x_start = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Spinning Donut')
    font = pygame.font.SysFont('Arial', 18, bold=True)
    clock = pygame.time.Clock()

    # Create an instance of TextRenderer
    text_renderer = TextRenderer(screen, font)

    rows = screen.get_height() // text_renderer.y_separator
    cols = screen.get_width() // text_renderer.x_separator

    A, B = 0, 0  # Rotating animation angles
    theta_spacing = 0.07
    phi_spacing = 0.02
    chars = ".,-~:;=!*#$@"
    x_offset = cols // 2
    y_offset = rows // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        # Reset z-buffer and screen buffer at the start of each frame
        z = [0] * (cols * rows)  # Z-buffer (depth)
        b = [' '] * (cols * rows)  # Screen buffer (characters)

        for j in range(0, 628, int(theta_spacing * 100)):  # θ loop
            for i in range(0, 628, int(phi_spacing * 100)):  # φ loop
                c = math.sin(i)
                d = math.cos(j)
                e = math.sin(A)
                f = math.sin(j)
                g = math.cos(A)
                h = d + 2
                D = 1 / (c * h * e + f * g + 5)
                l = math.cos(i)
                m = math.cos(B)
                n = math.sin(B)
                t = c * h * g - f * e
                x = int(x_offset + 40 * D * (l * h * m - t * n))  # 3D x coordinate after rotation
                y = int(y_offset + 20 * D * (l * h * n + t * m))  # 3D y coordinate after rotation
                o = int(x + cols * y)
                N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))  # luminance index
                if rows > y > 0 and x > 0 and cols > x and D > z[o]:
                    z[o] = D
                    b[o] = chars[N if N > 0 else 0]

        text_renderer.y_start = 0
        for i in range(len(b)):
            A += 0.00004
            B += 0.00002

            if i % cols == 0 and i != 0:
                text_renderer.reset_line()

            text_renderer.display_text(b[i])

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
