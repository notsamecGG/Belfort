import gui, pygame
from gui import CustomRect, Text
from gui import BLACK, WHITE

import agent as am
import sys



# Button Functions
#region
def create_agent():
    url = gui.textField("url")
    a = am.Agent(url)
    raw_html = a.request_collection(url)
    a.parse_NFTs(raw_html)
    a.append_snaphsot()
    a.compare_snapshot()
#endregion



# Mainloop
run = True

button = gui.BorderedRect(CustomRect(0, 0, 200, 100), decorations=[(Text('+').surface, "c")])
buttonClickable = gui.Clickable(button, create_agent)

rect = gui.BorderedRect(CustomRect(0, 0, *gui.WINDOW_SIZE), decorations=[(Text('text').surface, "c")])

agents = []
agents_xmax = 4
agents_ymax = 6

while run:
    gui.window.fill(WHITE)

    # Events
    #region
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            pygame.font.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            WINDOW_SIZE = event.w, event.h

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for clickable in gui.clickables:
                    triggered = clickable.rect.collidepoint(mouse_pos)

                    if triggered:
                        clickable.click()

    #endregion
    
    if gui.callback_queue:
        for callback in gui.callback_queue:
            callback.check()

    gui.window.blits(iter((*rect.draw(), *button.draw())))
    
    for agent in agents:
        gui.window.blits(agent[1])

    pygame.display.flip()