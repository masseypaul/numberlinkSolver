import pygame
import math

colorDict = {
    0: (252, 63, 63),
    1: (101, 252, 63),
    2: (63, 139, 252),
    3: (252, 63, 177),
    4: (215, 252, 63),
    5: (63, 252, 252),
    6: (215, 63, 252),
    7: (252, 177, 63),
    8: (63, 252, 139),
    9: (101, 63, 252),
    10: (252, 120, 63),
    11: (63, 252, 82),
    12: (63, 82, 252),
    13: (252, 63, 120),
}

#%% Square cells

def displayGrid(window,height,width):
    for i in range(height+1):
        pygame.draw.line(window, (0,0,0), (30, 30 + 40*i), (30 + 40*width, 30 + 40*i))
    for j in range(width+1):
        pygame.draw.line(window, (0,0,0), (30 + 40*j, 30), (30 + 40*j, 30 + 40*height))

def display_forbidden(window, forbidden):
    for pos in forbidden:
        pygame.draw.rect(window, (0,0,0), (30+40*pos[1],30+40*pos[0],40,40))

def displayNumber(window, endDict, convertor, end = False):
    myFont = pygame.font.Font("C:\\Windows\\Fonts\\calibri.ttf", 20)
    for key in endDict:
        color = colorDict[key] if key < len(colorDict) else (0,0,0)
        for pos in endDict[key]:
            pygame.draw.rect(window, color, (30+40*pos[1],30+40*pos[0],40,40))
            if end:
                text = convertor[key]
                surface_text = myFont.render(text,True,(0,0,0),color)
                text_rect = surface_text.get_rect()
                text_rect.center = (50+40*pos[1],50+40*pos[0])
                window.blit(surface_text,text_rect)
            
def displayMessage(window,message):
    myFont = pygame.font.Font("C:\\Windows\\Fonts\\calibri.ttf", 20)
    surface_text = myFont.render(message, True, (0,0,0), (255,255,255))
    text_rect = surface_text.get_rect()
    text_rect.center = (400,20)
    window.blit(surface_text,text_rect)


def displayBridge(window, bridges, posBridgeDict, answer):
    for pos in bridges:
        if pos in posBridgeDict:
            for key in posBridgeDict[pos]:
                color = colorDict[key] if key < len(colorDict) else (0,0,0)
                if (pos[0]-1,pos[1]) in answer[key]:
                    pygame.draw.polygon(window, color, [
                        [30+40*pos[1],30+40*pos[0]],
                        [40+40*pos[1],40+40*pos[0]],
                        [60+40*pos[1],40+40*pos[0]],
                        [70+40*pos[1],30+40*pos[0]]
                    ], width = 0)
                    pygame.draw.polygon(window, color, [
                        [30+40*pos[1],70+40*pos[0]],
                        [40+40*pos[1],60+40*pos[0]],
                        [60+40*pos[1],60+40*pos[0]],
                        [70+40*pos[1],70+40*pos[0]]
                    ], width = 0)
                else:
                    pygame.draw.polygon(window, color, [
                        [30+40*pos[1],30+40*pos[0]],
                        [40+40*pos[1],40+40*pos[0]],
                        [60+40*pos[1],40+40*pos[0]],
                        [70+40*pos[1],30+40*pos[0]],
                        [70+40*pos[1],70+40*pos[0]],
                        [60+40*pos[1],60+40*pos[0]],
                        [40+40*pos[1],60+40*pos[0]],
                        [30+40*pos[1],70+40*pos[0]]
                    ], width = 0)
            
        
        # line of separation
        pygame.draw.line(window, (0,0,0), (30+40*pos[1],30+40*pos[0]),(40+40*pos[1],40+40*pos[0]))
        pygame.draw.line(window, (0,0,0), (40+40*pos[1],40+40*pos[0]),(60+40*pos[1],40+40*pos[0]))
        pygame.draw.line(window, (0,0,0), (60+40*pos[1],40+40*pos[0]),(70+40*pos[1],30+40*pos[0]))
        
        pygame.draw.line(window, (0,0,0), (30+40*pos[1],70+40*pos[0]),(40+40*pos[1],60+40*pos[0]))
        pygame.draw.line(window, (0,0,0), (40+40*pos[1],60+40*pos[0]),(60+40*pos[1],60+40*pos[0]))
        pygame.draw.line(window, (0,0,0), (60+40*pos[1],60+40*pos[0]),(70+40*pos[1],70+40*pos[0]))


def displaySquareGame(answer, endDict, convertor,message,bridges, posBridgeDict, forbidden, size):
    pygame.init()
    dimensions = (1000, 650)
    window = pygame.display.set_mode(dimensions)
    running = True
    while running:
        window.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        displayNumber(window, answer, convertor)
        displayNumber(window, endDict, convertor, end=True)
        displayMessage(window, message)
        displayBridge(window, bridges, posBridgeDict, answer)
        display_forbidden(window, forbidden)
        displayGrid(window,size[0],size[1])
        pygame.display.flip()
    pygame.quit()
    
    

#%% Hexagon cells
def displayHexagon(window, x, y, d, color,name=""):
    myFont = pygame.font.Font("C:\\Windows\\Fonts\\calibri.ttf", 20)
    angles = [math.radians(60 * i+30) for i in range(6)]
    vertices = [
        (x + d * math.cos(angle), y + d * math.sin(angle))
        for angle in angles
    ]
    pygame.draw.polygon(window, color, vertices, 0)
    pygame.draw.polygon(window, (0, 0, 0), vertices, 1)
    surface_text = myFont.render(name,True,(0,0,0),color)
    text_rect = surface_text.get_rect()
    text_rect.center = (x,y)
    window.blit(surface_text,text_rect)
    
def displayGridHexa(window, d, height, width, hidden,answer, endDict,convertor, shiftFirstLine = False):
    shift = 1 if shiftFirstLine else 0
    offset = (100, 100)
    horizontal_distance = d * math.sqrt(3)
    vertical_distance = d * 1.5
    for row in range(height):
        for col in range(width):
            if (row,col) not in hidden:
                x = offset[0] + col * horizontal_distance + ((row+shift) % 2) * (horizontal_distance / 2)
                y = offset[1] + row * vertical_distance
                displayHexagon(window, x, y, d, (255, 255, 255))
    for key in endDict:
        color = colorDict[key] if key < len(colorDict) else (0,0,0)
        for pos in endDict[key]:
            x = offset[0] + pos[1] * horizontal_distance + ((pos[0]+shift) % 2) * (horizontal_distance / 2)
            y = offset[1] + pos[0] * vertical_distance
            name = convertor[key]
            displayHexagon(window, x, y, d, color, name=name)
    for key in answer:
        color = colorDict[key] if key < len(colorDict) else (0,0,0)
        for pos in answer[key]:
            x = offset[0] + pos[1] * horizontal_distance + ((pos[0]+shift) % 2) * (horizontal_distance / 2)
            y = offset[1] + pos[0] * vertical_distance
            name = ""
            if pos in endDict[key]:
                name = convertor[key]
            displayHexagon(window, x, y, d, color, name=name)

def displayHexagonGame(answer, endDict, convertor,message,bridges, posBridgeDict, forbidden,shiftFirstLine, size):
    pygame.init()
    dimensions = (1000, 650)
    window = pygame.display.set_mode(dimensions)
    running = True
    while running:
        window.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        displayMessage(window, message)
        displayGridHexa(window, 20, size[0], size[1], forbidden,answer,endDict,convertor, shiftFirstLine=shiftFirstLine)

        pygame.display.flip()
    pygame.quit()


