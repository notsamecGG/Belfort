from typing import Sequence, Tuple
import pygame
import time


pygame.init()
pygame.font.init()


# Colors
#region
WHITE = 255, 255, 255
BLACK = 0, 0, 0
#endregion


# Window setup
#region
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
icon = pygame.Surface((10, 10))
icon.fill((WHITE))


pygame.display.set_icon(icon)
pygame.display.set_caption('App')
window = pygame.display.set_mode(WINDOW_SIZE) #, pygame.RESIZABLE)
#endregion


# Font setup
#region
FONT = "arial"
#endregion


# Geometries
#region
class CustomRect:
    def __init__(self, *args) -> None:
        if len(args) == 4:
            self.left = args[0]
            self.top = args[1]
            self.width = args[2]
            self.height = args[3]
        
        elif len(args) == 1:
            self.left = args[0].left
            self.top = args[0].top
            self.width = args[0].width
            self.height = args[0].height

        else:
            self.left = 1
            self.top = 1
            self.width = 1
            self.height = 1
    
    
    @property
    def dimesions(self) -> Tuple[int, int, int, int]:
        return (self.top, self.left, self.width, self.height)

    
    @property
    def coords(self) -> Tuple[int, int]:
        return (self.top, self.left)

    
    @property
    def wh(self) -> Tuple[int, int]:
        return (self.width, self.height)

    
    def resize(self, x_coeficient, y_coeficient):
        self.left *= x_coeficient
        self.width *= x_coeficient
        self.top *= y_coeficient
        self.height *= y_coeficient


    def center_rect(self, other, include_pos=True):
        left = (self.width - other.width) / 2
        top = (self.height - other.height) / 2

        if include_pos:
            left += self.top
            top += self.left

        return (left, top)
    


class Shape:
    def __init__(self, rect: CustomRect, color, decorations: list[pygame.Surface, Tuple[int, int] or str]=[]):
        '''decorations insert as [(pygame.Surface, (coords))]'''
        self.rect = rect
        self.color = color

        if decorations:
            final_decors = []
            for decor_tuple in decorations:
                if decor_tuple[1] == "c":
                    position = self.rect.center_rect(CustomRect(decor_tuple[0].get_rect()))
                    decor_tuple = (decor_tuple[0], position)
                
                final_decors.append(decor_tuple)
            self.decorations = final_decors
        else:
           self.decorations = tuple(decorations)


    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(*self.rect.dimesions)



class BorderedRect(Shape):
    def __init__(self, rect: CustomRect, border_width=5, color: Tuple = WHITE, border_color: Tuple =BLACK, decorations: list[pygame.Surface, Tuple[int, int] or str]=[]) -> None:
        # recalculate center sizes
        self.x_coeficient = 1
        self.y_coeficient = 1

        c_rect = self.generate_center_rect(rect, border_width)

        self.rect = rect
        self.b_color = border_color
        self.b_width = border_width

        self.c_rect = c_rect
        self.color = color

        border, center = self.generate_surfaces()
        self.border = border
        self.center = center

        super().__init__(rect, color, decorations)
        

    def generate_surfaces(self) -> Tuple[pygame.Surface, pygame.Surface]:
        '''Generate pygame.Surface for border, center with valid params'''
        border = pygame.Surface(self.rect.wh)
        border.fill(self.b_color)
        center = pygame.Surface(self.c_rect.wh)
        center.fill(self.color)

        return border, center


    def generate_center_rect(self, rect, border_width) -> CustomRect:
        c_left = rect.left + border_width
        c_top = rect.top + border_width
        c_width = rect.width - 2 * border_width
        c_height = rect.height - 2 * border_width
        c_rect = CustomRect(c_left * self.x_coeficient, c_top * self.y_coeficient,\
            c_width * self.x_coeficient, c_height * self.y_coeficient)

        return c_rect
    

    def resize(self, x_coeficient, y_coeficient):
        self.x_coeficient = x_coeficient
        self.y_coeficient = y_coeficient

        self.c_rect = self.generate_center_rect(self.rect, self.b_width)


    def draw(self) -> Sequence[Tuple[pygame.Surface, Tuple[int, int]], ]:
        self.border, self.center = self.generate_surfaces()
        return ((self.border, self.rect.coords), (self.center, self.c_rect.coords), *self.decorations)

    
    @property
    def surface(self) -> pygame.Surface:
        surface = pygame.Surface(self.rect.wh)
        surface.blits(self.draw())

        return surface



class Text:
    def __init__(self, text: str, font:str=FONT, font_size:int=32, color=BLACK) -> None:
        self.text = text
        self.color = color
        self.font = font
        self.font_size = font_size


    @property
    def surface(self) -> pygame.Surface:
        font = pygame.font.SysFont(self.font, self.font_size)
        return font.render(self.text, False, self.color)
#endregion


# Functionable
#region
callback_queue = []
class Callback:
    def __init__(self, pause, func) -> None:
        '''pause(ms)'''
        
        global callback_queue

        self.end = time.time_ns() + pause * 1e6
        self.func = func

        callback_queue.append(self)

    def check(self):
        if self.end <= time.time_ns():
            self.func()

            global callback_queue
            callback_queue.remove(self)



clickables = []
class Clickable:
    def __init__(self, parent: Shape, func) -> None:
        self.parent = parent
        self.rect = parent.get_rect()
        self.func = func

        global clickables
        clickables.append(self)
    
    def click(self):
        print(self, ' clicked')
        self.parent.color = tuple(x - y for x, y in zip(self.parent.color, (81, 64, 22)))
        self.func()
        Callback(50, self.unshade)

    def unshade(self):
        self.parent.color = tuple(x + y for x, y in zip(self.parent.color, (81, 64, 22)))

    def delete(self):
        global clickables
        clickables.remove(self)

    def __del__(self):
        self.delete()




def textField(hint: str) -> str:
    return str(input(hint + ': '))
#endregion


# if __name__ == '__main__':
#     # Mainloop
#     run = True

#     button = BorderedRect(CustomRect(0, 0, 200, 100), decorations=[(Text('+').surface, "c")])
#     buttonClickable = Clickable(button, create_agent)

#     rect = BorderedRect(CustomRect(0, 0, *WINDOW_SIZE), decorations=[(Text('text').surface, "c")])

#     agents = []
#     agents_xmax = 4
#     agents_ymax = 6

#     while run:
#         window.fill(WHITE)

#         # Events
#         #region
#         mouse_pos = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#                 pygame.font.quit()
#                 sys.exit()

#             if event.type == pygame.VIDEORESIZE:
#                 WINDOW_SIZE = event.w, event.h

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     for clickable in clickables:
#                         triggered = clickable.rect.collidepoint(mouse_pos)

#                         if triggered:
#                             clickable.click()

#         #endregion
        
#         if callback_queue:
#             for callback in callback_queue:
#                 callback.check()

#         window.blits(iter((*rect.draw(), *button.draw())))
        
#         for agent in agents:
#             window.blits(agent[1])

#         pygame.display.flip()