import pygame
import sys
import ast

from const import *
from game import Game
from map import Map
from player import player
import os
from ui import Button
from ui import UIElement

def save_map(squares, folder="maps", overwrite=0):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if overwrite and overwrite > 0:
        filename = os.path.join(folder, f"map_{overwrite}.txt")
    else:
        i = 1
        while True:
            filename = os.path.join(folder, f"map_{i}.txt")
            if not os.path.exists(filename):
                break
            i += 1
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    with open(filename, "w") as f:
        f.write("[\n")
        for row in squares:
            values = [str(square.value) for square in row]
            line = "[" + ",".join(values) + "],\n"
            f.write(line)
        f.write("]\n")

    print(f"Map saved as {filename}")

class Main:
    
    def __init__(self):
        self.IsJumping = False
        self.Died = False
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Final Project: PLATFORMER")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.map = Map(self.screen)
        self.player = player("down")
        self.started = True

        #Hahmon aloituskohta
        self.base_x = GridSize*10
        self.base_y = GridSize*10
        self.offdir = 0
        self.offdiry = 0

        # Hahmo path
        base_dir = os.path.dirname(__file__)
        char_idle = os.path.join(base_dir, "ASSET", "CHARS", "idle.png")
        char_right = os.path.join(base_dir, "ASSET", "CHARS", "char_right.png")
        char_left = os.path.join(base_dir, "ASSET", "CHARS", "char_left.png")
        
        #hahmo image
        img_right = pygame.image.load(char_right)
        img_left = pygame.image.load(char_left)
        img_idle = pygame.image.load(char_idle)
        #hahmo image muuttuja
        self.char_size = max(28, 28)
        self.char_right = pygame.transform.smoothscale(img_right, (self.char_size, self.char_size))
        self.char_left = pygame.transform.smoothscale(img_left, (self.char_size, self.char_size))
        self.char_idle = pygame.transform.smoothscale(img_idle, (self.char_size, self.char_size))


        self.EditorStars = 0
        self.Stars1 = 0
        self.Stars2 = 0
        self.Stars3 = 0
        self.CurrentLevel = 1
        self.AllStars = [self.Stars1, self.Stars2, self.Stars3]

        #UI SETUP
        self.last_clicked_button = None
        self.IsMainMenu = True
        self.IsEditor = False
        self.IsLevels = False
        self.IsInGame = False
        self.Win = False
        self.EditorHelp = False
        

        #LOAD IMAGES
        img_starUI = pygame.image.load('ASSET/UI/star.png')
        img_nostarUI = pygame.image.load('ASSET/UI/blackstar.png')


        img_menubg = pygame.image.load('ASSET/UI/baldjumpermainmenu.png')
        img_levelbg = pygame.image.load('ASSET/UI/levelbg.png')
        img_winscreen = pygame.image.load('ASSET/UI/winscreen.png')

        img_play = pygame.image.load('ASSET/UI/UIplay.png')
        img_editor = pygame.image.load('ASSET/UI/UIeditor.png')
        img_exit = pygame.image.load('ASSET/UI/UIexit.png')
        img_menub = pygame.image.load('ASSET/UI/menub.png')

        img_editortab = pygame.image.load('ASSET/UI/items.png')
        img_editorhelp = pygame.image.load('ASSET/UI/help.png')
        img_editorinfo = pygame.image.load('ASSET/UI/info.png')

        img_map1 = pygame.image.load('ASSET/UI/map1.png')
        img_map2 = pygame.image.load('ASSET/UI/map2.png')
        img_map3 = pygame.image.load('ASSET/UI/map3.png')   
        img_lvl1 = pygame.image.load('ASSET/UI/level1.png')
        img_lvl2 = pygame.image.load('ASSET/UI/level2.png')
        img_lvl3 = pygame.image.load('ASSET/UI/level3.png')

        self.editortab = UIElement(1220, 0, img_editortab, 0.5)
        self.editorhelp = UIElement(0, 0, img_editorhelp, 0.3)
        self.editorinfo = UIElement(0, 690, img_editorinfo, 0.6)

        self.menuscreen = UIElement(0, 0, img_menubg, 0.66667)
        self.levelscreen = UIElement(0, 0, img_levelbg, 0.66667)
        self.winscreen = UIElement(0, 0, img_winscreen, 1.6)

        self.starUI = UIElement(1050, 650, img_starUI, 2)
        self.nostarUI = UIElement(1050, 650, img_nostarUI, 2)
        self.starUI2 = UIElement(1125, 650, img_starUI, 2)
        self.nostarUI2 = UIElement(1125, 650, img_nostarUI, 2)
        self.starUI3 = UIElement(1200, 650, img_starUI, 2)
        self.nostarUI3 = UIElement(1200, 650, img_nostarUI, 2)

        self.WinstarUI = UIElement(400, 300, img_starUI, 5)
        self.WinnostarUI = UIElement(400, 300, img_nostarUI, 5)
        self.WinstarUI2 = UIElement(555, 250, img_starUI, 5)
        self.WinnostarUI2 = UIElement(555, 250, img_nostarUI, 5)
        self.WinstarUI3 = UIElement(700, 300, img_starUI, 5)
        self.WinnostarUI3 = UIElement(700, 300, img_nostarUI, 5)

        self.menuplay = Button(920, 350, img_play, 0.3)
        self.menueditor = Button(970, 440, img_editor, 0.3)
        self.menuexit = Button(1020, 535, img_exit, 0.3)
        self.menubutton = Button(560, 535, img_menub, 0.3)

        self.map1 = Button(90, 50, img_map1, 0.5)
        self.map2 = Button(520, 220, img_map2, 0.5)
        self.map3 = Button(950, 50, img_map3, 0.4)
        self.Level1UI = UIElement(80, 300, img_lvl1, 0.7)
        self.Level2UI = UIElement(510, 480, img_lvl2, 0.7)
        self.Level3UI = UIElement(940, 300, img_lvl3, 0.7)


    def LoadMap(self, map):
        with open(f"maps/map_{map}.txt", 'r', encoding="utf-8") as f: content = f.read()
        chosenmap = ast.literal_eval(content)
        self.map.load_from_list(chosenmap)
        self.started = True
        self.IsLevels = False
        self.IsInGame = True
        self.CurrentLevel = map
        if map == 1:
            self.last_clicked_button = self.map1
        elif map == 2:
            self.last_clicked_button = self.map2
        elif map == 3:
            self.last_clicked_button = self.map3

    def collides_with_tiles(self, rect):
        # return True if rect collides with any non-background tile
        for row in self.map.squares:
            for square in row:

                if square.value != 0 and square.value != 54:
                    tile_rect = pygame.Rect(square.col * GridSize, square.row * GridSize, GridSize, GridSize)
                    if rect.colliderect(tile_rect):
                        if square.value == 55:
                            if self.CurrentLevel == 1:
                                self.Stars1 += 1
                            elif self.CurrentLevel == 2:
                                self.Stars2 += 1
                            elif self.CurrentLevel == 3:
                                self.Stars3 += 1
                            square.value = 0
                            self.AllStars = [self.Stars1, self.Stars2, self.Stars3]
                            return True
                        if square.value == 53:
                            self.Win = True
                            self.IsInGame = False
                            self.last_clicked_button = None
                            if self.AllStars[self.CurrentLevel - 1] < 3:
                                self.AllStars[self.CurrentLevel - 1] = self.AllStars[self.CurrentLevel - 1]
                            return True
                        if not self.IsJumping and square.value != 7 and square.value != 8:
                            return True
                        else:
                            
                            if square.value == 4:
                                return True
                            if square.value == 7 or square.value == 8:
                                self.Died = True
                                return False
                                
                            else:
                                return True
        return False

    def MainLoop(self):
            running = True
            active_tile = 0
            mouse_down = False
            jumpheight = 19
            multiplierheight = 1
            overwrite_mode = False
            import_mode = False
            override_input = ""
            import_input = ""
            IsGrounded = True
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.last_clicked_button = None
                    keys = pygame.key.get_pressed()
                    if (keys[pygame.K_UP] and keys[pygame.K_LEFT]) and IsGrounded == True or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]) and IsGrounded == True:
                        self.IsJumping = True
                        
                    if (keys[pygame.K_UP]) and IsGrounded == True:
                        self.IsJumping = True

                    if keys[pygame.K_LEFT]:
                    #    if keys[pygame.K_UP]:
                    #        self.IsJumping = True
                        self.player.dir = "left"
                    
                    if keys[pygame.K_RIGHT]:
                    #    if keys[pygame.K_UP]:
                    #        self.IsJumping = True
                        self.player.dir = "right"
                        
                    if keys[pygame.K_DOWN]:
                        self.player.dir = "down"   
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_l:
                            self.last_clicked_button = None
                            self.IsMainMenu = True
                            self.IsEditor = False
                            self.IsLevels = False
                            self.IsInGame = False
                            self.Win = False
                        if self.IsEditor:
                            if pygame.K_0 <= event.key <= pygame.K_9 and self.IsEditor:
                                active_tile = event.key - pygame.K_0
                                print("Active tile:", active_tile)
                            if event.key == pygame.K_r:
                                active_tile = 55
                                print("Active tile:", active_tile)
                            if event.key == pygame.K_t:
                                active_tile = 53
                                print("Active tile:", active_tile)
                            if event.key == pygame.K_e:
                                active_tile = 54
                                print("Active tile:", active_tile)
                            if event.key == pygame.K_s and self.IsEditor:
                                if self.map._IsValid():
                                    save_map(self.map.squares)
                                    print("Map saved!")
                                
                            if event.key == pygame.K_d and self.IsEditor:
                                self.map.restore()
                                self.map.draw(self.screen)
                            if event.key == pygame.K_h and self.IsEditor:
                                self.EditorHelp = not self.EditorHelp
                                print("Editor help:", self.EditorHelp)
                                continue
                            if event.key == pygame.K_o:
                                if self.map._IsValid():
                                    overwrite_mode = not overwrite_mode
                                    override_input = ""
                                    print("Override mode:", overwrite_mode)
                                
                                continue
                            if overwrite_mode:
                                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                                    if override_input.isdigit():
                                        idx = int(override_input)
                                        filename = os.path.join("maps", f"map_{idx}.txt")
                                        if os.path.exists(filename):
                                            save_map(self.map.squares, overwrite=idx)
                                            print(f"Overwrote {filename}")
                                        else:
                                            print(f"File {filename} not found — not overwritten")
                                    else:
                                        print("No number entered to override")
                                elif event.key == pygame.K_BACKSPACE:
                                    override_input = override_input[:-1]
                                    print("Override input:", override_input)
                                else:
                                    c = event.unicode
                                    if c.isdigit():
                                        override_input += c
                                        print("Override input:", override_input)
                                continue
                            if event.key == pygame.K_i:
                                import_mode = not import_mode
                                import_input = ""
                                print("Import mode:", import_mode)
                                continue
                            if import_mode:
                                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                                    if import_input.isdigit():
                                        idx = int(import_input)
                                        filename = os.path.join("maps", f"map_{idx}.txt")
                                        if os.path.exists(filename):
                                            with open(filename, 'r', encoding="utf-8") as f: content = f.read()
                                            chosenmap = ast.literal_eval(content)
                                            self.map.load_from_list(chosenmap)
                                            print(f"Imported {filename}")
                                            
                                        else:
                                            print(f"File {filename} not found — not imported")
                                    else:
                                        print("No number entered to import")
                                elif event.key == pygame.K_BACKSPACE:
                                    import_input = import_input[:-1]
                                    print("Import input:", import_input)
                                else:
                                    c = event.unicode
                                    if c.isdigit():
                                        import_input += c
                                        print("Import input:", import_input)
                                continue
                        if event.key == pygame.K_UP and IsGrounded == True:
                            
                            # jump = 64px
                            self.IsJumping = True
                                        

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_down = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_down = False
                    
                #Kokoaikainen pudotus
                #Grounded Checker
                if self.player.dir == "down" or "left" or "right":
                    proposed_offdiry = self.offdiry - 4
                    candidate = pygame.Rect(self.base_x + self.offdir, self.base_y - proposed_offdiry, self.char_size, self.char_size)
                    if not self.collides_with_tiles(candidate):
                        self.offdiry = proposed_offdiry
                        IsGrounded = False
                    else:   
                        IsGrounded = True
                if self.IsJumping:
                    jumpheight -= multiplierheight
                    multiplierheight += 0.001
                    if jumpheight < 1:
                        
                        multiplierheight = 1
                        IsGrounded = False
                        self.IsJumping = False
                    
                    proposed_offdiry = self.offdiry + jumpheight
                    candidate = pygame.Rect(self.base_x + self.offdir, self.base_y - proposed_offdiry, self.char_size, self.char_size)
                    if not self.collides_with_tiles(candidate):
                        self.offdiry = proposed_offdiry
                if mouse_down and self.IsEditor:
                    mx, my = pygame.mouse.get_pos()

                    grid_x = mx // GridSize
                    grid_y = my // GridSize

                    if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                        if active_tile == 55 and self.EditorStars < 3 and self.map.squares[grid_y][grid_x].value != 55:
                            self.EditorStars += 1
                            self.map.squares[grid_y][grid_x].value = active_tile
                            self.map.draw(self.screen)
                        elif active_tile != 55:
                            if self.map.squares[grid_y][grid_x].value == 55:
                                self.EditorStars -= 1
                            self.map.squares[grid_y][grid_x].value = active_tile
                            self.map.draw(self.screen)
                        

                # Jatkuva liike
                
                if self.player.dir == "left" and not self.Win:
                    proposed_offdir = self.offdir - 2
                    candidate = pygame.Rect(self.base_x + proposed_offdir, self.base_y - self.offdiry, self.char_size, self.char_size)
                    if not self.collides_with_tiles(candidate):
                        self.offdir = proposed_offdir
                if self.player.dir == "right" and not self.Win:
                    proposed_offdir = self.offdir + 2
                    candidate = pygame.Rect(self.base_x + proposed_offdir, self.base_y - self.offdiry, self.char_size, self.char_size)
                    if not self.collides_with_tiles(candidate):
                        self.offdir = proposed_offdir
                
                
                
                if self.Died or self.started == True:
                    self.player.dir = "down"
                    self.AllStars[self.CurrentLevel - 1] = 0
                    self.Stars1 = 0
                    self.Stars2 = 0
                    self.Stars3 = 0
                    with open(f"maps/map_{self.CurrentLevel}.txt", 'r', encoding="utf-8") as f: content = f.read()
                    chosenmap = ast.literal_eval(content)
                    self.map.load_from_list(chosenmap)
                    for row in self.map.squares:
                        for square in row:
                            if square.value == 54:
                                self.base_x = GridSize * square.col
                                self.base_y = GridSize * square.row
                                self.offdir = 0
                                self.offdiry = 0
                                
                    self.Died = False
                    self.started = False
                    
                
                self.map.draw(self.screen)
                if jumpheight < 1:
                    jumpheight = 19
                # player piirto
                draw_x = self.base_x + self.offdir
                draw_y = self.base_y - self.offdiry
                if self.IsInGame:
                    if self.player.dir == "left":
                        self.screen.blit(self.char_left, (draw_x, draw_y))
                    elif self.player.dir == "right":
                        self.screen.blit(self.char_right, (draw_x, draw_y))
                    else:
                        self.screen.blit(self.char_idle, (draw_x, draw_y))
                
                if self.map1.clicked and self.IsLevels and self.last_clicked_button != self.map1:
                    self.LoadMap(1)
                if self.map2.clicked and self.IsLevels and self.last_clicked_button != self.map2:
                    self.LoadMap(2)
                if self.map3.clicked and self.IsLevels and self.last_clicked_button != self.map3:
                    self.LoadMap(3)
                if self.menubutton.clicked and self.IsLevels and self.last_clicked_button != self.menubutton:
                    self.IsLevels = False
                    self.IsMainMenu = True
                    self.Win = False
                    self.last_clicked_button = self.menubutton
                #LOAD UIS
                if self.IsInGame:
                    self.nostarUI.draw(self.screen)
                    self.nostarUI2.draw(self.screen)
                    self.nostarUI3.draw(self.screen)
                    if self.AllStars[self.CurrentLevel - 1] == 3:
                        self.starUI3.draw(self.screen)
                        self.starUI2.draw(self.screen)
                        self.starUI.draw(self.screen)
                    elif self.AllStars[self.CurrentLevel - 1] == 2:
                        self.starUI2.draw(self.screen)
                        self.starUI.draw(self.screen)
                    elif self.AllStars[self.CurrentLevel - 1] == 1:
                        self.starUI.draw(self.screen)
                if self.IsMainMenu:
                    self.menuscreen.draw(self.screen)
                    self.menuplay.draw(self.screen)
                    self.menueditor.draw(self.screen)
                    self.menuexit.draw(self.screen)
                if self.menuplay.clicked and self.IsMainMenu and self.last_clicked_button != self.menuplay:
                    self.IsMainMenu = False
                    self.IsLevels = True
                    self.last_clicked_button = self.menuplay
                    
                if self.menueditor.clicked and self.IsMainMenu and self.last_clicked_button != self.menueditor:
                    self.IsEditor = True
                    self.IsMainMenu = False
                    self.last_clicked_button = self.menueditor

                    self.map.restore()
                    self.map.draw(self.screen)
                
                if self.menuexit.clicked and self.IsMainMenu and self.last_clicked_button != self.menuexit:
                    running = False
                    self.last_clicked_button = self.menuexit
                if self.IsEditor and self.EditorHelp:
                    self.editortab.draw(self.screen)
                    self.editorinfo.draw(self.screen)
                    self.editorhelp.draw(self.screen)
                elif self.IsEditor:
                    self.editorhelp.draw(self.screen)
                if self.IsLevels:
                    self.IsMainMenu = False
                    self.levelscreen.draw(self.screen)
                    self.map1.draw(self.screen)
                    self.map2.draw(self.screen)
                    self.map3.draw(self.screen)
                    self.Level1UI.draw(self.screen)
                    self.Level2UI.draw(self.screen)
                    self.Level3UI.draw(self.screen)
                if self.Win:
                    self.winscreen.draw(self.screen)
                    self.WinnostarUI3.draw(self.screen)
                    self.WinnostarUI2.draw(self.screen)
                    self.WinnostarUI.draw(self.screen)
                    if self.AllStars[self.CurrentLevel - 1] == 3:
                        self.WinstarUI3.draw(self.screen)
                        self.WinstarUI2.draw(self.screen)
                        self.WinstarUI.draw(self.screen)
                    elif self.AllStars[self.CurrentLevel - 1] == 2:
                        self.WinstarUI2.draw(self.screen)
                        self.WinstarUI.draw(self.screen)
                    elif self.AllStars[self.CurrentLevel - 1] == 1:
                        self.WinstarUI.draw(self.screen)
                    self.menubutton.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(60)

            pygame.quit()
            sys.exit()


main = Main()
main.MainLoop()
