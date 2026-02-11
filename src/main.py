#!/usr/bin/env python3

import random
import time
import json
import os
import base64
import colorama
from colorama import Fore, Back, Style


def typewriter_effect(text, delay=0.05, color=Fore.WHITE):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()


class RussianRouletteGame:
    def __init__(self):
        self.balance = 100
        self.xp = 0
        self.level = 1
        self.xp_to_level = 100
        self.save_file = "savegame.dat"
        self.settings_file = "settings.json"
        
        self.typewriter_enabled = True
        self.auto_save_enabled = True
        self.auto_save_interval = 60
        
        self.load_settings()
        
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.typewriter_enabled = settings.get('typewriter_enabled', True)
                    self.auto_save_enabled = settings.get('auto_save_enabled', True)
                    self.auto_save_interval = settings.get('auto_save_interval', 60)
            except:
                pass
    
    def save_settings(self):
        settings = {
            'typewriter_enabled': self.typewriter_enabled,
            'auto_save_enabled': self.auto_save_enabled,
            'auto_save_interval': self.auto_save_interval
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except:
            pass
    
    def encrypt_data(self, data):
        json_str = json.dumps(data)
        encoded_bytes = base64.b64encode(json_str.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    def decrypt_data(self, encrypted_data):
        try:
            decoded_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            json_str = decoded_bytes.decode('utf-8')
            return json.loads(json_str)
        except:
            return None
    
    def load_game(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    encrypted_data = f.read()
                
                data = self.decrypt_data(encrypted_data)
                if data is not None:
                    self.balance = data.get('balance', 100)
                    self.xp = data.get('xp', 0)
                    self.level = data.get('level', 1)
                    self.xp_to_level = data.get('xp_to_level', 100)
                    self.print_with_color("Игра загружена!", Fore.GREEN)
                    return True
                else:
                    self.print_with_color("Ошибка при загрузке игры (неверный формат данных).", Fore.RED)
                    return False
            except:
                self.print_with_color("Ошибка при загрузке игры.", Fore.RED)
                return False
        else:
            self.print_with_color("Сохранений не найдено.", Fore.YELLOW)
            return False
    
    def save_game(self):
        data = {
            'balance': self.balance,
            'xp': self.xp,
            'level': self.level,
            'xp_to_level': self.xp_to_level
        }
        
        encrypted_data = self.encrypt_data(data)
        
        try:
            with open(self.save_file, 'w') as f:
                f.write(encrypted_data)
            self.print_with_color("Игра сохранена!", Fore.GREEN)
            return True
        except:
            self.print_with_color("Ошибка при сохранении игры.", Fore.RED)
            return False
    
    def print_with_color(self, text, color=Fore.WHITE):
        if self.typewriter_enabled:
            typewriter_effect(text, color=color)
        else:
            print(color + text)
    
    def print_with_typewriter(self, text):
        if self.typewriter_enabled:
            typewriter_effect(text)
        else:
            print(text)
    
    def display_menu(self):
        print(f"\n{Fore.CYAN}Баланс: ${self.balance} | Уровень: {self.level} | XP: {self.xp}/{self.xp_to_level}")
        print(Fore.MAGENTA + "-"*50)
        print(Fore.LIGHTYELLOW_EX + "1. Играть в Русскую Рулетку")
        print(Fore.LIGHTBLUE_EX + "2. Магазин")
        print(Fore.LIGHTGREEN_EX + "3. Статистика")
        print(Fore.LIGHTRED_EX + "4. Чит-коды")
        print(Fore.LIGHTCYAN_EX + "5. Сохранить игру")
        print(Fore.LIGHTMAGENTA_EX + "6. Загрузить игру")
        print(Fore.LIGHTWHITE_EX + "7. Настройки")
        print(Fore.LIGHTYELLOW_EX + "8. Выход")
        print(Fore.MAGENTA + "-"*50)
    
    def display_settings_menu(self):
        while True:
            print(f"\n{Fore.CYAN}--- НАСТРОЙКИ ---")
            print(f"{Fore.LIGHTYELLOW_EX}1. Типографский эффект: {'Вкл' if self.typewriter_enabled else 'Выкл'}")
            print(f"{Fore.LIGHTBLUE_EX}2. Интервал автосохранения: {self.auto_save_interval//60} мин")
            print(f"{Fore.LIGHTGREEN_EX}3. Автосохранение: {'Вкл' if self.auto_save_enabled else 'Выкл'}")
            print(f"{Fore.LIGHTRED_EX}4. Сбросить все настройки")
            print(f"{Fore.LIGHTWHITE_EX}5. Назад в меню")
            print(Fore.CYAN + "----------------")
            
            choice = input("Выберите опцию: ")
            
            if choice == "1":
                self.typewriter_enabled = not self.typewriter_enabled
                status = "включен" if self.typewriter_enabled else "выключен"
                self.print_with_color(f"Типографский эффект {status}", Fore.GREEN)
                
            elif choice == "2":
                if not self.auto_save_enabled:
                    self.print_with_color("Автосохранение отключено. Сначала включите его.", Fore.RED)
                    continue
                    
                try:
                    mins = int(input("Введите интервал автосохранения в минутах (1-60): "))
                    if 1 <= mins <= 60:
                        self.auto_save_interval = mins * 60
                        self.print_with_color(f"Интервал автосохранения установлен на {mins} мин", Fore.GREEN)
                    else:
                        self.print_with_color("Интервал должен быть от 1 до 60 минут!", Fore.RED)
                except ValueError:
                    self.print_with_color("Введите корректное число!", Fore.RED)
                    
            elif choice == "3":
                self.auto_save_enabled = not self.auto_save_enabled
                status = "включено" if self.auto_save_enabled else "выключено"
                self.print_with_color("Автосохранение {}".format(status), Fore.GREEN)
                    
            elif choice == "4":
                confirm = input("Вы уверены? (y/n): ").lower()
                if confirm == 'y':
                    self.typewriter_enabled = True
                    self.auto_save_enabled = True
                    self.auto_save_interval = 60
                    self.save_settings()
                    self.print_with_color("Настройки сброшены", Fore.GREEN)
                else:
                    self.print_with_color("Сброс отменен", Fore.YELLOW)
                    
            elif choice == "5":
                break
            else:
                self.print_with_color("Неверный выбор!", Fore.RED)
        
        self.save_settings()
    
    def russian_roulette(self):
        if self.balance <= 0:
            self.balance = 10
            self.print_with_color("\nУ вас закончились деньги! Но мы дали вам $10, чтобы вы могли продолжить играть!", Fore.YELLOW)
        
        print(f"\nВаш текущий баланс: ${self.balance}")
        
        while True:
            try:
                bet = int(input("Введите ставку (минимум $1): $"))
                if bet <= 0:
                    print("Ставка должна быть больше 0!")
                    continue
                if bet > self.balance:
                    print("У вас недостаточно средств!")
                    continue
                break
            except ValueError:
                print("Пожалуйста, введите корректное число!")
        
        while True:
            try:
                player_pick = int(input("Выберите число от 1 до 10: "))
                if 1 <= player_pick <= 10:
                    break
                else:
                    print("Пожалуйста, выберите число от 1 до 10!")
            except ValueError:
                print("Пожалуйста, введите корректное число!")
        
        self.print_with_color("\nБарабан заряжается...", Fore.YELLOW)
        time.sleep(1)
        self.print_with_color("Барабан крутится...", Fore.CYAN)
        time.sleep(1)
        
        result = random.randint(1, 10)
        self.print_with_color(f"Барабан останавливается на камере {result}", Fore.MAGENTA)
        time.sleep(0.5)
        
        if player_pick == result:
            self.print_with_color("БАХ! К сожалению, сегодня не ваш день...", Fore.RED)
            self.print_with_color("GAME OVER", Fore.RED)
            self.balance -= bet
            self.xp += 5
        else:
            self.print_with_color("Фух! Вы выжили! Повезло!", Fore.GREEN)
            winnings = bet * 2
            self.print_with_color(f"Вы выиграли ${winnings}!", Fore.GREEN)
            self.balance += winnings
            self.xp += 10
        
        self.check_level_up()
        
        print(f"Новый баланс: ${self.balance}")
        
        if self.auto_save_enabled:
            self.save_game()
    
    def check_level_up(self):
        if self.xp >= self.xp_to_level:
            self.level += 1
            self.xp -= self.xp_to_level
            self.xp_to_level = int(self.xp_to_level * 1.5)
            self.print_with_color(f"\n🎉 ПОЗДРАВЛЯЕМ! Вы достигли уровня {self.level}! 🎉", Fore.LIGHTYELLOW_EX)
    
    def shop(self):
        while True:
            print(f"\n{Fore.LIGHTBLUE_EX}Магазин - Баланс: ${self.balance}")
            print(f"{Fore.LIGHTYELLOW_EX}1. Дополнительная жизнь - $50 (увеличивает шансы на выживание)")
            print(f"{Fore.LIGHTGREEN_EX}2. Удвоитель ставки - $75 (удваивает ваш следующий выигрыш)")
            print(f"{Fore.LIGHTCYAN_EX}3. Секретный патрон - $100 (уменьшает шанс проигрыша)")
            print(f"{Fore.LIGHTMAGENTA_EX}4. Щит безопасности - $150 (позволяет пережить один проигрыш)")
            print(f"{Fore.LIGHTWHITE_EX}5. Счастливое число - $200 (увеличивает шансы на выигрыш)")
            print(f"{Fore.LIGHTRED_EX}6. Бонусный раунд - $300 (дает дополнительную попытку)")
            print(f"{Fore.LIGHTYELLOW_EX}7. Золотой билет - $500 (гарантирует выигрыш в следующей игре)")
            print(f"{Fore.LIGHTBLUE_EX}8. Кристальный шар - $750 (предсказывает следующее число)")
            print(f"{Fore.LIGHTRED_EX}9. БОЖЕСТВЕННЫЙ РЕЖИМ - $-123456789 (получить БОЖЕСТВЕННЫЙ РЕЖИМ)")
            print(f"{Fore.LIGHTMAGENTA_EX}10. Назад в меню")
            print(f"{Fore.LIGHTCYAN_EX}----------------")
            
            choice = input("Выберите опцию: ")
            
            if choice == "1":
                if self.balance >= 50:
                    self.balance -= 50
                    self.print_with_color("Вы купили дополнительную жизнь!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "2":
                if self.balance >= 75:
                    self.balance -= 75
                    self.print_with_color("Вы купили удвоитель ставки!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "3":
                if self.balance >= 100:
                    self.balance -= 100
                    self.print_with_color("Вы купили секретный патрон!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "4":
                if self.balance >= 150:
                    self.balance -= 150
                    self.print_with_color("Вы купили щит безопасности!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "5":
                if self.balance >= 200:
                    self.balance -= 200
                    self.print_with_color("Вы купили счастливое число!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "6":
                if self.balance >= 300:
                    self.balance -= 300
                    self.print_with_color("Вы купили бонусный раунд!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "7":
                if self.balance >= 500:
                    self.balance -= 500
                    self.print_with_color("Вы купили золотой билет!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "8":
                if self.balance >= 750:
                    self.balance -= 750
                    self.print_with_color("Вы купили кристальный шар!", Fore.GREEN)
                else:
                    self.print_with_color("Недостаточно средств!", Fore.RED)
                    
            elif choice == "9":
                self.balance += abs(-123456789)
                self.print_with_color("ПОЗДРАВЛЯЕМ! Вы получили БОЖЕСТВЕННЫЙ РЕЖИМ!", Fore.LIGHTRED_EX)
                self.print_with_color("Вам добавлено $123456789!", Fore.LIGHTRED_EX)
                self.print_with_color("Теперь вы богаты beyond imagination!", Fore.LIGHTRED_EX)
                    
            elif choice == "10":
                break
            else:
                self.print_with_color("Неверный выбор!", Fore.RED)
    
    def show_stats(self):
        self.print_with_color(f"\n--- СТАТИСТИКА ИГРОКА ---", Fore.LIGHTCYAN_EX)
        self.print_with_color(f"Уровень: {self.level}", Fore.LIGHTYELLOW_EX)
        self.print_with_color(f"XP: {self.xp}/{self.xp_to_level}", Fore.LIGHTGREEN_EX)
        self.print_with_color(f"Баланс: ${self.balance}", Fore.LIGHTBLUE_EX)
        self.print_with_color(f"Выживаемость: {(self.xp // 10) * 2}%", Fore.LIGHTMAGENTA_EX)
        self.print_with_color("------------------------", Fore.LIGHTWHITE_EX)
    
    def show_cheats(self):
        print(f"\n{Fore.LIGHTRED_EX}--- ЧИТ-КОДЫ ---")
        print("Введите код чтобы активировать чит:")
        print("1337 - +1000$")
        print("GODMODE - Уровень 10")
        print("LUCKY - +500 XP")
        print("RICH - +5000$")
        print("NOLOSS - Следующая игра = победа")
        print("INSTAWIN - Мгновенный уровень")
        print("RESET - Сбросить все")
        print("UNLOCK - Открыть все предметы в магазине")
        print("LUCKY7 - Установить следующее число на 7")
        print("NOSURPRISE - Отключить случайные события")
        print("Назад - вернуться в меню")
        print("----------------")
        
        code = input("Введите чит-код: ").upper()
        
        if code == "1337":
            self.balance += 1000
            self.print_with_color("Добавлено $1000 к балансу!", Fore.GREEN)
        elif code == "GODMODE":
            self.level = 10
            self.print_with_color("Установлен 10 уровень!", Fore.GREEN)
        elif code == "LUCKY":
            self.xp += 500
            self.print_with_color("Добавлено 500 XP!", Fore.GREEN)
        elif code == "RICH":
            self.balance += 5000
            self.print_with_color("Добавлено $5000 к балансу!", Fore.GREEN)
        elif code == "NOLOSS":
            self.print_with_color("Следующая игра будет выигрышной!", Fore.GREEN)
        elif code == "INSTAWIN":
            self.xp = self.xp_to_level
            self.print_with_color("Мгновенный уровень активирован!", Fore.GREEN)
        elif code == "RESET":
            self.balance = 100
            self.xp = 0
            self.level = 1
            self.xp_to_level = 100
            self.print_with_color("Все сброшено!", Fore.YELLOW)
        elif code == "UNLOCK":
            self.balance += 10000
            self.print_with_color("Открыты все предметы! Добавлено $10000!", Fore.GREEN)
        elif code == "LUCKY7":
            self.print_with_color("Следующее число будет 7! (эффект временный)", Fore.GREEN)
        elif code == "NOSURPRISE":
            self.print_with_color("Случайные события отключены! (эффект временный)", Fore.GREEN)
        else:
            self.print_with_color("Неверный чит-код!", Fore.RED)
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Выберите опцию: ")
            
            if choice == "1":
                self.russian_roulette()
            elif choice == "2":
                self.shop()
            elif choice == "3":
                self.show_stats()
            elif choice == "4":
                self.show_cheats()
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                self.load_game()
            elif choice == "7":
                self.display_settings_menu()
            elif choice == "8":
                self.print_with_color("Спасибо за игру в Cuddly Chainsaw! До свидания!", Fore.LIGHTGREEN_EX)
                break
            else:
                self.print_with_color("Неверный выбор!", Fore.RED)


def main():
    colorama.init(autoreset=True)
    
    game = RussianRouletteGame()
    game.run()


if __name__ == "__main__":
    main()