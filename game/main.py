from puzzle_game import start_game

if __name__ == "__main__":
    """Главная функция игры.Запрашивает у пользователя уровень сложности и запускает игру."""
    while True:
        level = input("Выберите уровень сложности (2, 3, 4): ")
        if level in ['2', '3', '4']:
            start_game(int(level))
            break
        else:
            print("Неверный уровень. Пожалуйста, выберите 2, 3 или 4:")
