import tkinter as tk
import random
import time

class PuzzleGame:
    """Класс реализует игровую логику и интерфейс для игры."""
    def __init__(self, master, size):
        """Инициализирует игру."""
        self.master = master
        self.size = size
        self.tiles = [i for i in range(1, size * size)] + [0]
        self.blank_pos = size * size - 1
        self.start_time = None
        self.move_count = 0
        self.create_widgets()
        self.shuffle_tiles()
        self.update_display()

    def create_widgets(self):
        """Создает графические элементы интерфейса."""
        self.canvas = tk.Canvas(self.master, width=300, height=300)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.timer_label = tk.Label(self.master, text="Время: 0 сек")
        self.timer_label.grid(row=1, column=0)
        self.move_label = tk.Label(self.master, text="Ходы: 0")
        self.move_label.grid(row=2, column=0)
        self.canvas.bind("<Button-1>", self.handle_click)

    def shuffle_tiles(self):
        """Перемешивает плитки для начального поля в игре."""
        for _ in range(1000): # Повторяем 1000 раз для хорошего перемешивания
            random_index = random.randint(0, self.size * self.size - 2)
            if self.is_adjacent(random_index, self.blank_pos):
                self.swap_tiles(random_index, self.blank_pos)

    def update_display(self):
        """Обновляет отображение плиток."""
        self.canvas.delete("all")
        tile_size = 300 // self.size
        for index, tile in enumerate(self.tiles):
            if tile != 0:
                x = (index % self.size) * tile_size
                y = (index // self.size) * tile_size
                self.canvas.create_rectangle(x, y, x + tile_size, y + tile_size,
                                             fill="lightblue")
                self.canvas.create_text(x + tile_size // 2, y + tile_size // 2, text=str(tile),
                                        font=("Arial", 20))

        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Время: {elapsed_time} сек")

        self.move_label.config(text=f"Ходы: {self.move_count}")

    def swap_tiles(self, index1, index2):
        """Меняет местами две плитки и обновляет индекс пустой плитки."""
        if self.tiles[index1] != 0 and self.tiles[index2] == 0:  # Проверка на пустую ячейку
            self.tiles[index1], self.tiles[index2] = self.tiles[index2], self.tiles[index1]
            self.blank_pos = index1
            self.update_display()  # Обновляем дисплей после перемещения

    def handle_click(self, event):
        """Обрабатывает клики мыши на игровом поле."""
        tile_size = 300 // self.size
        x = event.x // tile_size
        y = event.y // tile_size
        clicked_index = y * self.size + x

        # Проверяем, является ли выбранная плитка соседней с пустой и не пустая ли сама нажатая плитка
        if self.is_adjacent(clicked_index, self.blank_pos) and self.tiles[clicked_index] != 0:
            # Если плитка рядом с пустой, меняем их местами
            self.swap_tiles(clicked_index, self.blank_pos)
            self.move_count += 1

            if not self.start_time:
                self.start_time = time.time()

            if self.is_solved():
                self.on_game_won()

    def is_adjacent(self, index1, index2):
        """Проверяет, являются ли две плитки соседними."""
        row1, col1 = divmod(index1, self.size)
        row2, col2 = divmod(index2, self.size)
        return ((row1 == row2 and abs(col1 - col2) == 1) or
                (col1 == col2 and abs(row1 - row2) == 1))

    def is_solved(self):
        """Проверяет, решена ли игра."""
        return self.tiles == [i for i in range(1, self.size * self.size)] + [0]

    def on_game_won(self):
        """Вызывается, когда игра выигрывается."""
        elapsed_time = int(time.time() - self.start_time)
        self.canvas.create_text(150, 150,
                                text=f"Победа!\nВремя: {elapsed_time} сек\nХоды: {self.move_count}",
                                font=("Arial", 20))
        self.canvas.unbind("<Button-1>")

def start_game(size):
    """Запускает игру с заданным размером поля."""
    root = tk.Tk()
    root.title("Пятнашки")
    PuzzleGame(root, size)
    root.mainloop()
