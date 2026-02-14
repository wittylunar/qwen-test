from colorama import Fore
from modules.core import format_number


class UIHandler:
    """Handles all UI and display functionality for the game"""
    
    def __init__(self, game_instance):
        self.game = game_instance

    def display_menu(self):
        print(f"\n{Fore.CYAN}Баланс: ${format_number(self.game.balance)} | Уровень: {self.game.level} | XP: {format_number(self.game.xp)}/{format_number(self.game.xp_to_level)}")
        print(Fore.MAGENTA + "="*60)
        print(Fore.LIGHTYELLOW_EX + "1. Играть в Русскую Рулетку")
        print(Fore.LIGHTBLUE_EX + "2. Режим 'Всё или ничего'")
        print(Fore.LIGHTGREEN_EX + "3. Прогрессивный Джекпот")
        print(Fore.LIGHTCYAN_EX + "4. Бонусный раунд")
        print(Fore.LIGHTMAGENTA_EX + "5. Игра 'Монетка'")
        print(Fore.LIGHTWHITE_EX + "6. Многопользовательская игра")
        print(Fore.LIGHTRED_EX + "7. Магазин")
        print(Fore.LIGHTYELLOW_EX + "8. Статистика")
        print(Fore.LIGHTBLUE_EX + "9. Достижения")
        print(Fore.LIGHTGREEN_EX + "10. Чит-коды (отключены)")
        print(Fore.LIGHTCYAN_EX + "11. Ежедневные задания")
        print(Fore.LIGHTMAGENTA_EX + "12. Сохранить игру")
        print(Fore.LIGHTWHITE_EX + "13. Загрузить игру")
        print(Fore.LIGHTRED_EX + "14. Настройки")
        print(Fore.LIGHTYELLOW_EX + "15. Выход")
        print(Fore.MAGENTA + "="*60)

    def display_settings_menu(self):
        while True:
            try:
                print(f"\n{Fore.CYAN}--- НАСТРОЙКИ ---")
                print(f"{Fore.LIGHTYELLOW_EX}1. Типографский эффект: {'Вкл' if self.game.typewriter_enabled else 'Выкл'}")
                print(f"{Fore.LIGHTBLUE_EX}2. Интервал автосохранения: {self.game.auto_save_interval//60} мин")
                print(f"{Fore.LIGHTGREEN_EX}3. Автосохранение: {'Вкл' if self.game.auto_save_enabled else 'Выкл'}")
                print(f"{Fore.LIGHTCYAN_EX}4. Облачная синхронизация: {'Вкл' if getattr(self.game, 'cloud_sync_enabled', False) else 'Выкл'}")
                print(f"{Fore.LIGHTRED_EX}5. Сбросить все настройки")
                print(f"{Fore.LIGHTWHITE_EX}6. Назад в меню")
                print(Fore.CYAN + "----------------")

                choice = input("Выберите опцию: ")

                if choice == "1":
                    self.game.typewriter_enabled = not self.game.typewriter_enabled
                    status = "включен" if self.game.typewriter_enabled else "выключен"
                    self.game.print_with_color(f"Типографский эффект {status}", Fore.GREEN)

                elif choice == "2":
                    if not self.game.auto_save_enabled:
                        self.game.print_with_color("Автосохранение отключено. Сначала включите его.", Fore.RED)
                        continue

                    try:
                        mins = int(input("Введите интервал автосохранения в минутах (1-60): "))
                        if 1 <= mins <= 60:
                            self.game.auto_save_interval = mins * 60
                            self.game.print_with_color(f"Интервал автосохранения установлен на {mins} мин", Fore.GREEN)
                        else:
                            self.game.print_with_color("Интервал должен быть от 1 до 60 минут!", Fore.RED)
                    except ValueError:
                        self.game.print_with_color("Введите корректное число!", Fore.RED)

                elif choice == "3":
                    self.game.auto_save_enabled = not self.game.auto_save_enabled
                    status = "включено" if self.game.auto_save_enabled else "выключено"
                    self.game.print_with_color("Автосохранение {}".format(status), Fore.GREEN)

                elif choice == "4":
                    self.game.toggle_cloud_sync()

                elif choice == "5":
                    confirm = input("Вы уверены? (y/n): ").lower()
                    if confirm == 'y':
                        self.game.typewriter_enabled = True
                        self.game.auto_save_enabled = True
                        self.game.auto_save_interval = 60
                        self.game.cloud_sync_enabled = False  # Disable cloud sync on reset
                        self.game.save_settings()
                        self.game.print_with_color("Настройки сброшены", Fore.GREEN)
                    else:
                        self.game.print_with_color("Сброс отменен", Fore.YELLOW)

                elif choice == "6":
                    break
                else:
                    self.game.print_with_color("Неверный выбор!", Fore.RED)
            except (EOFError, KeyboardInterrupt):
                self.game.print_with_color("\nВыход из настроек...", Fore.LIGHTRED_EX)
                break

        self.game.save_settings()

    def show_stats(self):
        self.game.print_with_color(f"\n--- СТАТИСТИКА ИГРОКА ---", Fore.LIGHTCYAN_EX)
        self.game.print_with_color(f"Уровень: {format_number(self.game.level)}", Fore.LIGHTYELLOW_EX)
        self.game.print_with_color(f"XP: {format_number(self.game.xp)}/{format_number(self.game.xp_to_level)}", Fore.LIGHTGREEN_EX)
        self.game.print_with_color(f"Баланс: ${format_number(self.game.balance)}", Fore.LIGHTBLUE_EX)
        self.game.print_with_color(f"Выживаемость: {format_number((self.game.xp // 10) * 2)}%", Fore.LIGHTMAGENTA_EX)
        self.game.print_with_color("------------------------", Fore.LIGHTWHITE_EX)

    def show_cheats(self):
        print(f"\n{Fore.LIGHTRED_EX}--- ЧИТ-КОДЫ ---")
        print("Чит-коды были отключены для обеспечения честной игры.")
        print("Развлекайтесь по-настоящему!")
        print("----------------")
        input("Нажмите Enter для возврата в меню...")