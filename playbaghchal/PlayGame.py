import pygame
from pygame.locals import *
import os
from importlib import resources 
from .button import Button
import random

asset_path = resources.files("playbaghchal") / "assets"

class TigerGame:
    def __init__(self):
        pygame.init()
        self.screen_height = 700
        self.screen_width = 700
        self.line_width = 4
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tiger Goat Game')
        self.win_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.win_surface.fill((0, 0, 0, 130))
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.placeholder_color = (200, 200, 200)
        self.font = pygame.font.SysFont(None, 40)
        self.turn = "Goats"
        self.game_over = False
        self.winner = ""
        self.game_start = False
        self.tigers_cornered = 0
        self.goats_captured = 0
        self.goats_outside = 20
        self.tiger_img = pygame.image.load(os.path.join(asset_path, "tiger.png")).convert_alpha()
        self.goat_img = pygame.image.load(os.path.join(asset_path,"goat.png")).convert_alpha()
        self.quit_img = pygame.image.load(os.path.join(asset_path,"Quit.png")).convert_alpha()
        self.start_img = pygame.image.load(os.path.join(asset_path,"Start.png")).convert_alpha()
        self.tiger_win_img = pygame.image.load(os.path.join(asset_path,"Tiger_win.png")).convert_alpha()
        self.goat_win_img = pygame.image.load(os.path.join(asset_path,"Goat_win.png")).convert_alpha()
        self.play_again_img = pygame.image.load(os.path.join(asset_path,"Play_Again.png")).convert_alpha()
        self.forest_img = pygame.image.load(os.path.join(asset_path,"forest.png")).convert_alpha()
        self.wood_img = pygame.image.load(os.path.join(asset_path,"wood.png")).convert_alpha()
        self.tiger_img = pygame.transform.scale(self.tiger_img, (50, 50))
        self.goat_img = pygame.transform.scale(self.goat_img, (60, 60))
        self.bg_image = pygame.transform.scale(self.forest_img, (self.screen_width, self.screen_height))
        self.bg_image_game = pygame.transform.scale(self.wood_img, (self.screen_width, self.screen_height))
        self.start_button = Button(200, 200, self.start_img, 0.5)
        self.quit_button = Button(200, 450, self.quit_img, 0.5)
        self.tiger_win_button = Button(30, 200, self.tiger_win_img, 0.5)
        self.goat_win_button = Button(50, 200, self.goat_win_img, 0.5)
        self.play_again_button = Button(100, 300, self.play_again_img, 0.5)
        self.human_img = pygame.image.load(os.path.join(asset_path, "HumanvsHuman.png")).convert_alpha()
        self.ai_img = pygame.image.load(os.path.join(asset_path, "HumanvsAI.png")).convert_alpha()
        self.easy_img = pygame.image.load(os.path.join(asset_path, "easy.png")).convert_alpha()
        self.medium_img = pygame.image.load(os.path.join(asset_path, "medium.png")).convert_alpha()
        self.advanced_img = pygame.image.load(os.path.join(asset_path, "advance.png")).convert_alpha()
        # self.human_img = pygame.image.load(os.path.join('assets', "HumanvsHuman.png")).convert_alpha()
        # self.ai_img = pygame.image.load(os.path.join('assets', "HumanvsAI.png")).convert_alpha()
        # self.easy_img = pygame.image.load(os.path.join('assets', "easy.png")).convert_alpha()
        # self.medium_img = pygame.image.load(os.path.join('assets', "medium.png")).convert_alpha()
        # self.advanced_img = pygame.image.load(os.path.join('assets', "advance.png")).convert_alpha()
        self.human_button = Button(10, 200, self.human_img, 0.5)
        self.ai_button = Button(80, 300, self.ai_img, 0.5)
        self.easy_button = Button(250, 150, self.easy_img, 0.5)
        self.medium_button = Button(200, 250, self.medium_img, 0.5)
        self.advanced_button = Button(160, 350, self.advanced_img, 0.5)
        self.tiger_pos = [(0, 0), (0, 4), (4, 0), (4, 4)]
        self.goats = []
        self.board = [['' for _ in range(5)] for _ in range(5)]
        for pos in self.tiger_pos:
            self.board[pos[0]][pos[1]] = 'T'
        self.placeholders = []
        self.moves = {
            (0, 0): [(0, 1), (1, 0), (1, 1)], 
            (0, 1): [(0, 0), (1, 1), (0, 2)], 
            (0, 2): [(0, 1), (1, 1), (1, 2), (1, 3), (0, 3)],
            (0, 3): [(0, 2), (1, 3), (0, 4)], 
            (0, 4): [(0, 3), (1, 3), (1, 4)], 
            (1, 0): [(0, 0), (1, 1), (2, 0)],
            (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            (1, 2): [(0, 2), (1, 1), (1, 3), (2, 2)],
            (1, 3): [(0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 2), (2, 3), (2, 4)],
            (1, 4): [(0, 4), (1, 3), (2, 4)],
            (2, 0): [(1, 0), (1, 1), (2, 1), (3, 0), (3, 1)],
            (2, 1): [(2, 0), (1, 1), (2, 2), (3, 1)],
            (2, 2): [(1, 1), (1, 2), (1, 3), (2, 1), (3, 1), (3, 2), (2, 3), (3, 3)],
            (2, 3): [(2, 2), (1, 3), (2, 4), (3, 3)],
            (2, 4): [(1, 3), (2, 3), (1, 4), (3, 3), (3, 4)],
            (3, 0): [(2, 0), (3, 1), (4, 0)],
            (3, 1): [(2, 0), (3, 0), (2, 1), (2, 2), (3, 2), (4, 0), (4, 1), (4, 2)],
            (3, 2): [(2, 2), (3, 1), (4, 2), (3, 3)],
            (3, 3): [(2, 2), (3, 2), (2, 3), (2, 4), (3, 4), (4, 2), (4, 3), (4, 4)],
            (3, 4): [(3, 3), (2, 4), (4, 4)],
            (4, 0): [(3, 0), (3, 1), (4, 1)],
            (4, 1): [(4, 0), (3, 1), (4, 2)],
            (4, 2): [(4, 1), (3, 1), (3, 2), (3, 3), (4, 3)],
            (4, 3): [(4, 2), (4, 4), (3, 3)],
            (4, 4): [(4, 3), (3, 3), (3, 4)]
        }
        self.jumps = {
            (0, 0): [(0, 2), (2, 0), (2, 2)],
            (0, 1): [(0, 3), (2, 1)],
            (0, 2): [(0, 0), (0, 4), (2, 0), (2, 2), (2, 4)],
            (0, 3): [(0, 1), (2, 3)],
            (0, 4): [(0, 2), (2, 2), (2, 4)],
            (1, 0): [(3, 0), (1, 2)],
            (1, 1): [(3, 1), (1, 3),(3, 3)],
            (1, 2): [(1, 0), (1, 4),(3, 2)],
            (1, 3): [(1, 1), (3, 1), (3, 3)],
            (1, 4): [(1, 2), (3, 4)],
            (2, 0): [(0, 0), (0, 2), (2, 2), (4, 0), (4, 2)],
            (2, 1): [(0, 1), (4, 1), (2, 3)],
            (2, 2): [(0, 0), (0, 2), (0, 4), (2, 0), (2, 4), (4, 0), (4, 2), (4, 4)],
            (2, 3): [(0, 3), (2, 1), (4, 3)],
            (2, 4): [(0, 2), (0, 4), (4, 2), (2, 2), (4, 4)],
            (3, 0): [(1, 0), (3, 2)],
            (3, 1): [(1, 1), (1, 3), (3, 3)],
            (3, 2): [(1, 2), (3, 0), (3, 4)],
            (3, 3): [(1, 1), (3, 1), (1, 3)],
            (3, 4): [(3, 2), (1, 4)],
            (4, 0): [(2, 0), (2, 2), (4, 2)],
            (4, 1): [(2, 1), (4, 3)],
            (4, 2): [(2, 0), (2, 2), (2, 4), (4, 0), (4, 4)],
            (4, 3): [(4, 1), (2, 3)],
            (4, 4): [(2, 2), (2, 4), (4, 2)]
        }
        self.click_pos = []
        self.game_mode = "Human"
        self.ai_level = "Easy"
        self.as_goat_img = pygame.image.load(os.path.join(asset_path, "asGoat.png")).convert_alpha()
        self.as_tiger_img = pygame.image.load(os.path.join(asset_path, "asTiger.png")).convert_alpha()
        self.as_goat_button = Button(200, 250, self.as_goat_img, 0.5)
        self.as_tiger_button = Button(190, 350, self.as_tiger_img, 0.5)
        self.player_side = "Goats"  # Default

    def draw_board(self):
        color = (50, 50, 50)
        spacing = 120
        self.screen.blit(self.bg_image_game, (0, 0)) # bg = 'burlywood4'  # self.screen.fill(bg)
        for x in range(1, 6):
            # rows and columns
            pygame.draw.line(self.screen, color, (spacing, spacing * x),
                            (self.screen_width-100, spacing * x), self.line_width)
            pygame.draw.line(self.screen, color, (spacing * x, spacing),
                            (spacing * x, self.screen_height-100), self.line_width)
        # diagonal lines
        pygame.draw.line(self.screen, color, (spacing, spacing),
                        (self.screen_height-100, spacing * 5), self.line_width)
        pygame.draw.line(self.screen, color, (spacing, spacing*5),
                        (self.screen_width-100, spacing), self.line_width)

        # secondary diagonal lines
        pygame.draw.line(self.screen, color, (spacing, spacing * 3),
                        (spacing * 3, spacing), self.line_width)
        pygame.draw.line(self.screen, color, (spacing * 3, self.screen_height - 100),
                        (self.screen_width - 100, spacing * 3), self.line_width)
        pygame.draw.line(self.screen, color, (spacing * 3, spacing),
                        (self.screen_height - 100, spacing * 3), self.line_width)
        pygame.draw.line(self.screen, color, (spacing, spacing * 3),
                        (spacing * 3, self.screen_height - 100), self.line_width)

        # Draw the placeholders and store their positions
        self.placeholders.clear()
        for row in range(5):
            for col in range(5):
                center_x = spacing * col + spacing
                center_y = spacing * row + spacing
                pygame.draw.circle(self.screen, self.placeholder_color,
                                (center_x, center_y), 15)
                self.placeholders.append((center_x, center_y, row, col))

        # Draw the tigers and goats on the self.board
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == 'T':
                    self.screen.blit(self.tiger_img, (spacing * col + spacing -
                                23, spacing * row + spacing - 24))
                elif self.board[row][col] == 'G':
                    self.screen.blit(self.goat_img, (spacing * col + spacing -
                                30, spacing * row + spacing - 28))

        # Draw the turn text
        turn_text = self.font.render(f'{self.turn} Turn!', True, self.black)
        self.screen.blit(turn_text, (300, 50))


    def draw_stats(self, tigers_cornered, goats_captured, goats_outside):
        font = pygame.font.SysFont(None, 25)
        # Render the text
        tigers_text = font.render(
            f'TIGERS CORNERED: {tigers_cornered}/4', True, self.black)
        goats_text = font.render(
            f'GOATS CAPTURED: {goats_captured}/20', True, self.black)
        outside_text = font.render(
            f'GOATS OUTSIDE: {goats_outside}/20', True, self.black)

        # Display the text on the self.screen
        self.screen.blit(tigers_text, (250, self.screen_height - 80))
        self.screen.blit(goats_text, (250, self.screen_height - 50))
        self.screen.blit(outside_text, (250, self.screen_height - 20))

    def is_valid_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        if not (0 <= x2 < 5 and 0 <= y2 < 5):
            return False  # Out of bounds
        if self.board[x2][y2] != '':
            return False  # Not an empty spot
        if (x2, y2) in self.moves[(x1, y1)]:
            return True  # Adjacent move
        return False

    def is_valid_jump(self, start, end):
        x1, y1 = start
        x2, y2 = end
        if not (0 <= x2 < 5 and 0 <= y2 < 5):
            return False  # Out of bounds
        if self.board[x2][y2] != '':
            return False  # Not an empty spot
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        if self.board[mid_x][mid_y] != 'G':
            return False  # No goat to jump over
        if (x2, y2) in self.jumps[(x1, y1)]:
            return True  # Valid jump
        return False

    def move_tiger(self, start, end):
        ismove = self.is_valid_move(start, end)
        isjump = self.is_valid_jump(start, end)
        if ismove or isjump:
            x1, y1 = start
            x2, y2 = end
            self.board[x1][y1] = ''
            self.board[x2][y2] = 'T'
            self.tiger_pos.remove((x1, y1))
            self.tiger_pos.append((x2, y2))
            if not ismove:
                if isjump:
                    mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                    self.board[mid_x][mid_y] = ''  # Remove jumped goat
                    self.goats.remove((mid_x, mid_y))
                    self.goats_captured += 1
                    if self.goats_captured == 6:
                        self.game_over = True
                        self.winner = 'Tigers'
            return True
        return False

    def move_goat(self, start, end):
        if self.is_valid_move(start, end):
            x1, y1 = start
            x2, y2 = end
            self.board[x1][y1] = ''
            self.board[x2][y2] = 'G'
            self.goats.append((x2, y2))
            self.goats.remove((x1, y1))
            return True
        return False

    def place_goat(self, position):
        x, y = position
        if self.board[x][y] == '':
            self.board[x][y] = 'G'
            self.goats.append((x, y))
            self.goats_outside -= 1
            return True
        return False

    def is_trap_tiger(self):
        self.tigers_cornered = 0
        for pos in self.tiger_pos:
            for move in self.moves[pos] + self.jumps[pos]:
                if self.board[move[0]][move[1]] == '':
                    break
            else: # if all moves are blocked(if break is not executed)
                self.tigers_cornered += 1
        if self.tigers_cornered == 4:
            self.game_over = True
            self.winner = 'Goats'
            return True
        return False 

    def ai_move(self):
        if self.ai_level == "Easy":
            self.ai_move_easy()
        elif self.ai_level == "Medium":
            self.ai_move_medium()
        elif self.ai_level == "Advanced":
            self.ai_move_advanced()

    def ai_move_easy(self):
        # Random valid move for tiger
        moves = []
        for pos in self.tiger_pos:
            for move in self.moves[pos]:
                if self.board[move[0]][move[1]] == '':
                    moves.append((pos, move))
            for jump in self.jumps[pos]:
                if self.is_valid_jump(pos, jump):
                    moves.append((pos, jump))
        if moves:
            start, end = random.choice(moves)
            self.move_tiger(start, end)
            self.turn = "Goats"

    def ai_move_medium(self):
        # Prefer jumps (captures), else random move
        jumps = []
        moves = []
        for pos in self.tiger_pos:
            for jump in self.jumps[pos]:
                if self.is_valid_jump(pos, jump):
                    jumps.append((pos, jump))
            for move in self.moves[pos]:
                if self.board[move[0]][move[1]] == '':
                    moves.append((pos, move))
        if jumps:
            start, end = random.choice(jumps)
            self.move_tiger(start, end)
        elif moves:
            start, end = random.choice(moves)
            self.move_tiger(start, end)
        self.turn = "Goats"

    def ai_move_advanced(self):
        # Minimax algorithm for best move
        best_score = float('-inf')
        best_move = None
        for pos in self.tiger_pos:
            for move in self.moves[pos]:
                if self.board[move[0]][move[1]] == '':
                    score = self.minimax(self.board, self.tiger_pos, self.goats, pos, move, depth=2, maximizing=True)
                    if score > best_score:
                        best_score = score
                        best_move = (pos, move)
            for jump in self.jumps[pos]:
                if self.is_valid_jump(pos, jump):
                    score = self.minimax(self.board, self.tiger_pos, self.goats, pos, jump, depth=2, maximizing=True)
                    if score > best_score:
                        best_score = score
                        best_move = (pos, jump)
        if best_move:
            start, end = best_move
            self.move_tiger(start, end)
            self.turn = "Goats"

    def minimax(self, board, tigers, goats, start, end, depth, maximizing):
        # Simple evaluation: difference in goats captured
        # You can improve this function for better AI
        temp_board = [row[:] for row in board]
        temp_tigers = tigers[:]
        temp_goats = goats[:]
        # Simulate move
        temp_board[start[0]][start[1]] = ''
        temp_board[end[0]][end[1]] = 'T'
        temp_tigers.remove(start)
        temp_tigers.append(end)
        goats_captured = self.goats_captured
        if self.is_valid_jump(start, end):
            mid_x, mid_y = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
            temp_board[mid_x][mid_y] = ''
            if (mid_x, mid_y) in temp_goats:
                temp_goats.remove((mid_x, mid_y))
            goats_captured += 1
        if depth == 0:
            return goats_captured
        # For brevity, only evaluate tiger moves
        return goats_captured

    def run(self):
        run = True
        while run:
            if not self.game_start:
                # Main menu: choose Human or AI
                self.screen.blit(self.bg_image, (0, 0))
                self.human_button.draw(self.screen)
                self.ai_button.draw(self.screen)
                self.quit_button.draw(self.screen)
                font = pygame.font.SysFont(None, 100)
                title_text = font.render("Bagh-Chal", True, self.black)
                self.screen.blit(title_text, (170, 10))
                mode_text = self.font.render("Choose Game Mode:", True, self.white)
                self.screen.blit(mode_text, (200, 200))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if self.human_button.draw(self.screen):
                        self.game_mode = "Human"
                        self.game_start = True
                    if self.ai_button.draw(self.screen):
                        # Show difficulty selection screen
                        selecting = True
                        while selecting:
                            self.screen.blit(self.bg_image, (0, 0))
                            diff_text = self.font.render("Select AI Difficulty:", True, self.white)
                            self.screen.blit(diff_text, (200, 150))
                            self.easy_button.draw(self.screen)
                            self.medium_button.draw(self.screen)
                            self.advanced_button.draw(self.screen)
                            pygame.display.update()
                            for event2 in pygame.event.get():
                                if event2.type == pygame.QUIT:
                                    run = False
                                    selecting = False
                                if self.easy_button.draw(self.screen):
                                    self.ai_level = "Easy"
                                    selecting = False
                                if self.medium_button.draw(self.screen):
                                    self.ai_level = "Medium"
                                    selecting = False
                                if self.advanced_button.draw(self.screen):
                                    self.ai_level = "Advanced"
                                    selecting = False
                        # Side selection screen
                        side_selecting = True
                        while side_selecting:
                            self.screen.blit(self.bg_image, (0, 0))
                            side_text = self.font.render("Choose Your Side:", True, self.white)
                            self.screen.blit(side_text, (200, 250))
                            self.as_goat_button.draw(self.screen)
                            self.as_tiger_button.draw(self.screen)
                            pygame.display.update()
                            for event3 in pygame.event.get():
                                if event3.type == pygame.QUIT:
                                    run = False
                                    side_selecting = False
                                if self.as_goat_button.draw(self.screen):
                                    self.player_side = "Goats"
                                    self.game_mode = "AI"
                                    self.game_start = True
                                    side_selecting = False
                                if self.as_tiger_button.draw(self.screen):
                                    self.player_side = "Tigers"
                                    self.game_mode = "AI"
                                    self.game_start = True
                                    side_selecting = False
                    if self.quit_button.draw(self.screen):
                        run = False
                continue
            self.draw_board()
            self.draw_stats(self.tigers_cornered, self.goats_captured, self.goats_outside)
            if self.game_over:
                if self.winner == 'Tigers':
                    self.tiger_win_button.draw(self.win_surface)
                    self.screen.blit(self.win_surface, (0, 0))
                elif self.winner == 'Goats':
                    self.goat_win_button.draw(self.win_surface)
                    self.screen.blit(self.win_surface, (0, 0))
                self.play_again_button.draw(self.win_surface)
                self.quit_button.draw(self.win_surface)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if self.quit_button.draw(self.screen):
                        run = False
                    if self.play_again_button.draw(self.screen):
                        self.game_over = False
                        self.winner = 0
                        self.game_start = True
                        self.tigers_cornered = 0
                        self.goats_captured = 0
                        self.goats_outside = 20
                        self.turn = "Goats"
                        self.tiger_pos = [(0, 0), (0, 4), (4, 0), (4, 4)]
                        self.goats = []
                        self.board = [['' for _ in range(5)] for _ in range(5)]
                        for pos in self.tiger_pos:
                            self.board[pos[0]][pos[1]] = 'T'
                pygame.display.update()
                continue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if not self.game_over:
                    if self.game_mode == "AI":
                        # AI plays as opposite of player_side
                        if self.turn == "Tigers" and self.player_side == "Goats" and not self.game_over:
                            self.ai_move()
                            self.is_trap_tiger()
                        elif self.turn == "Goats" and self.player_side == "Tigers" and not self.game_over:
                            # Need to implement ai_move for goats
                            pass
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        for center_x, center_y, row, col in self.placeholders:
                            if (mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2 <= 15 ** 2:
                                if self.turn == 'Goats':
                                    if self.board[row][col] == '' and self.goats_outside > 0:
                                        if self.place_goat((row, col)):
                                            self.turn = 'Tigers'
                                    elif self.goats_outside == 0:
                                        if len(self.click_pos) == 0 and self.board[row][col] == 'G':
                                            self.click_pos.append((row, col))
                                        elif len(self.click_pos) == 1 and self.board[row][col] == '':
                                            self.click_pos.append((row, col))
                                            if self.move_goat(*self.click_pos):
                                                self.click_pos.clear()
                                                self.turn = 'Tigers'
                                            else:
                                                self.click_pos.pop()
                                        elif len(self.click_pos) == 1 and self.board[row][col] == 'G':
                                            self.click_pos.clear()
                                            self.click_pos.append((row, col))
                                        else:
                                            self.click_pos.clear()
                                    self.is_trap_tiger()
                                elif self.turn == 'Tigers':
                                    if len(self.click_pos) == 0 and self.board[row][col] == 'T':
                                        self.click_pos.append((row, col))
                                    elif len(self.click_pos) == 1 and self.board[row][col] == '':
                                        self.click_pos.append((row, col))
                                        if self.move_tiger(*self.click_pos):
                                            self.click_pos.clear()
                                            self.turn = 'Goats'
                                        else:
                                            self.click_pos.pop()
                                    elif len(self.click_pos) == 1 and self.board[row][col] == 'T':
                                        self.click_pos.clear()
                                        self.click_pos.append((row, col))
                                    else:
                                        self.click_pos.clear()
            if self.turn == "Tigers" and self.game_mode == "AI" and not self.game_over:
                self.ai_move()
                self.is_trap_tiger()
            pygame.display.update()
        pygame.quit()


def start_game():
    game = TigerGame()
    game.run()

start_game()