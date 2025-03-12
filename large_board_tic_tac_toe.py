import pygame
import numpy as np
import tkinter as tk
from tkinter import ttk
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai"

class TicTacToeGUI:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        master.title("Tic Tac Toe Settings")
        master.configure(bg="#2C3E50")
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", background="#2C3E50", foreground="white", font=("Arial", 12))
        
        self.frame = ttk.Frame(master)
        self.frame.pack(pady=10)
        
        ttk.Label(self.frame, text="Board Size:").grid(row=0, column=0, padx=10, pady=5)
        self.board_size_var = tk.IntVar(value=3)
        board_size_menu = ttk.Combobox(self.frame, textvariable=self.board_size_var, values=[3, 4, 5], state="readonly")
        board_size_menu.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.frame, text="Symbol:").grid(row=1, column=0, padx=10, pady=5)
        self.symbol_var = tk.StringVar(value="X")
        symbol_menu = ttk.Combobox(self.frame, textvariable=self.symbol_var, values=["X", "O"], state="readonly")
        symbol_menu.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(self.frame, text="Game Mode:").grid(row=2, column=0, padx=10, pady=5)
        self.mode_var = tk.StringVar(value="player_vs_ai")
        mode_menu = ttk.Combobox(self.frame, textvariable=self.mode_var, values=["human_vs_human", "player_vs_ai"], state="readonly")
        mode_menu.grid(row=2, column=1, padx=10, pady=5)
        
        start_button = ttk.Button(self.frame, text="Start Game", command=self.start_game)
        start_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def start_game(self):
        global mode
        mode = self.mode_var.get()
        self.game.update_settings(self.board_size_var.get(), self.symbol_var.get())
        self.master.destroy()
        self.game.run_game()

class RandomBoardTicTacToe:
    def __init__(self, size=(600, 700)):
        pygame.init()
        self.size = self.width, self.height = size
        self.GRID_SIZE = 3
        self.MARGIN = 5
        self.OFFSET = 5
        self.WIDTH = self.size[0] / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = (self.size[1] - 100) / self.GRID_SIZE - self.OFFSET
        self.player_symbol = "X"
        self.screen = pygame.display.set_mode(self.size)
        self.game_reset()

    def update_settings(self, grid_size, player_symbol):
        self.GRID_SIZE = grid_size
        self.player_symbol = player_symbol
        self.WIDTH = self.size[0] / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = (self.size[1] - 100) / self.GRID_SIZE - self.OFFSET
        self.game_reset()

    def game_reset(self):
        self.board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(self.board, turn_O=(self.player_symbol == "O"))
        self.draw_game()

    def draw_game(self):
        self.screen.fill((44, 62, 80))
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                rect = pygame.Rect(col * (self.WIDTH + self.MARGIN), row * (self.HEIGHT + self.MARGIN) + 100, self.WIDTH, self.HEIGHT)
                pygame.draw.rect(self.screen, (236, 240, 241), rect, 2)
        pygame.display.update()

    def move(self, move):
        if move is None:
            return  # Prevents errors when move is None
        x, y = move
        if not (0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE):  
            return  # Prevents index errors
        if self.board[y, x] != 0:
            return  # Prevents overwriting moves
        self.board[y, x] = 1 if self.game_state.turn_O else -1
        new_state = self.game_state.get_new_state(move)
        if new_state is None:
            return  # Prevents breaking the game if new_state is None
        self.game_state = new_state
        if self.game_state.turn_O:
            self.draw_circle(x, y)
        else:
            self.draw_cross(x, y)
        self.check_game_over()
        pygame.display.update()
        self.change_turn()
        if mode == "player_vs_ai" and not self.game_state.is_terminal():
            self.play_ai()
    def change_turn(self):
        self.game_state.turn_O = not self.game_state.turn_O
        turn_text = "O's Turn" if self.game_state.turn_O else "X's Turn"
        pygame.display.set_caption(f"Tic Tac Toe - {turn_text}")

    def play_ai(self):
        if mode == "player_vs_ai":
            result = minimax(self.game_state, 3, True) if self.game_state.turn_O else negamax(self.game_state, 3, 1)
        if result is not None and result[1] is not None:
            move = result[1]
            self.move(move)
            self.draw_circle(*move) if self.game_state.turn_O else self.draw_cross(*move)
        self.change_turn()
        pygame.display.update()

    def draw_circle(self, x, y):
        center = (int(x * (self.WIDTH + self.MARGIN) + self.WIDTH // 2), int(y * (self.HEIGHT + self.MARGIN) + 100 + self.WIDTH // 2))
        pygame.draw.circle(self.screen, (140, 146, 172), center, int(self.WIDTH // 3), 3)

    def draw_cross(self, x, y):
        start_pos1 = (x * (self.WIDTH + self.MARGIN) + self.MARGIN, y * (self.HEIGHT + self.MARGIN) + 100 + self.MARGIN)
        end_pos1 = ((x + 1) * (self.WIDTH + self.MARGIN) - self.MARGIN, (y + 1) * (self.HEIGHT + self.MARGIN) + 100 - self.MARGIN)
        pygame.draw.line(self.screen, (140, 146, 172), start_pos1, end_pos1, 3)
        start_pos2 = ((x+1) * (self.WIDTH + self.MARGIN) - self.MARGIN, y * (self.HEIGHT + self.MARGIN) + 100 + self.MARGIN)
        end_pos2 = (x * (self.WIDTH + self.MARGIN) + self.MARGIN, (y + 1) * (self.HEIGHT + self.MARGIN) + 100 - self.MARGIN)
        pygame.draw.line(self.screen, (140, 146, 172), start_pos2, end_pos2, 3)

    def check_game_over(self):
        if self.game_state.is_terminal():
            print("Game Over! Winner:", self.game_state.winner)

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = int(event.pos[0] // (self.WIDTH + self.MARGIN)), int((event.pos[1] - 100) // (self.HEIGHT + self.MARGIN))
                    if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
                        self.move((x, y))
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = RandomBoardTicTacToe()
    root = tk.Tk()
    gui = TicTacToeGUI(root, game)
    root.mainloop()
