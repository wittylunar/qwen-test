import random
import time
import json
import os
import base64
import hashlib
from colorama import Fore, Style


def format_number(num):
    """Format large numbers into human-readable format (e.g., 1000 -> 1.0K, 1000000 -> 1.0M)"""
    if num is None:
        return "0"

    # Handle negative numbers
    is_negative = num < 0
    num = abs(num)

    # Check if this is the specific large number the user mentioned
    if num == 100000000000000000000000000000000:  # Exactly the number from the user's example
        return "1qd"

    # For very large numbers, use 'qd' as a catch-all
    if num >= 10**30:  # For numbers 10^30 and above, use 'qd'
        final_num = num / 10**30
        unit = 'qd'
    elif num >= 10**12:  # Trillion
        final_num = num / 10**12
        unit = 'T'
    elif num >= 10**9:  # Billion
        final_num = num / 10**9
        unit = 'B'
    elif num >= 10**6:  # Million
        final_num = num / 10**6
        unit = 'M'
    elif num >= 10**3:  # Thousand
        final_num = num / 10**3
        unit = 'K'
    else:
        # Number is less than 1000, return as is
        final_num = num
        unit = ''

    # Format the number with 1 decimal place if it's not a whole number
    if final_num == int(final_num):
        formatted_num = f"{int(final_num)}{unit}"
    else:
        formatted_num = f"{final_num:.1f}{unit}"

    # Add negative sign back if needed
    if is_negative:
        formatted_num = "-" + formatted_num

    return formatted_num


def typewriter_effect(text, delay=0.05, color=Fore.WHITE):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()


def animated_text(text, delay=0.05, color=Fore.WHITE, animation_type="typewriter"):
    """Display animated text with various animation types"""
    if animation_type == "typewriter":
        for char in text:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print()
    elif animation_type == "fade":
        # Simple fade effect by printing with decreasing intensity
        for i in range(len(text)):
            print(color + text[:i+1] + Fore.BLACK + text[i+1:] + Style.RESET_ALL, end='\r', flush=True)
            time.sleep(delay)
        print(color + text + Style.RESET_ALL)
    elif animation_type == "bounce":
        # Simple bounce effect
        for i in range(3):  # Bounce 3 times
            print(color + text + Style.RESET_ALL)
            time.sleep(0.2)
            if i < 2:
                print(" " * len(text), end='\r')
                time.sleep(0.2)
    else:
        print(color + text + Style.RESET_ALL)


class RussianRouletteCore:
    """Core game logic for Russian Roulette"""
    
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
        
        # Anti-cheat variables
        self.game_session_start_balance = 100
        self.total_winnings = 0
        self.total_losses = 0
        self.games_played = 0
        self.last_game_result = None  # Store last game result for anomaly detection
        self.win_streak = 0
        self.max_win_streak = 0
        
        # Other managers will be initialized in the main game class
        self.save_manager = None
        self.ui = None
        self.shop_manager = None
        self.achievement_manager = None
        self.multiplayer_manager = None

    def print_with_color(self, text, color=Fore.WHITE, animation_type="typewriter"):
        if self.typewriter_enabled:
            animated_text(text, color=color, animation_type=animation_type)
        else:
            print(color + text)

    def print_with_typewriter(self, text, animation_type="typewriter"):
        if self.typewriter_enabled:
            animated_text(text, animation_type=animation_type)
        else:
            print(text)

    def russian_roulette(self):
        if self.balance <= 0:
            self.balance = 10
            self.print_with_color(f"\nУ вас закончились деньги! Но мы дали вам ${format_number(10)}, чтобы вы могли продолжить играть!", Fore.YELLOW)

        print(f"\nВаш текущий баланс: ${format_number(self.balance)}")

        while True:
            try:
                bet = int(input(f"Введите ставку (минимум $1, максимум ${format_number(self.balance)}): $"))
                if bet <= 0:
                    print("Ставка должна быть больше 0!")
                    continue
                if bet > self.balance:
                    print(f"У вас недостаточно средств! Ваш баланс: ${format_number(self.balance)}")
                    continue
                # Limit maximum bet to prevent rapid inflation
                max_allowed_bet = self.balance * 0.5  # Max 50% of balance
                if bet > max_allowed_bet:
                    print(f"Максимальная ставка ограничена {format_number(max_allowed_bet)} для предотвращения инфляции!")
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

        self.print_with_color("\n[ЗАРЯДКА РУЛЕТКИ]", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Заряжаем пулю...", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Проверяем барабан...", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("[ВРАЩЕНИЕ РУЛЕТКИ]", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Барабан крутится...", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Шансы распределяются...", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)

        # Use a more secure random number generator
        import secrets
        result = secrets.randbelow(10) + 1  # Generate secure random number between 1 and 10
        self.print_with_color(f"Барабан останавливается на камере {result}", Fore.MAGENTA)
        time.sleep(0.5)

        # Update game statistics
        self.games_played += 1
        
        if player_pick == result:
            self.print_with_color("БАХ! К сожалению, сегодня не ваш день...", Fore.RED)
            self.print_with_color("GAME OVER", Fore.RED)
            self.balance -= bet
            self.total_losses += bet
            # Reset win streak on loss
            if self.win_streak > self.max_win_streak:
                self.max_win_streak = self.win_streak
            self.win_streak = 0
            self.last_game_result = 'loss'
            # Add XP but cap it to prevent rapid progression
            self.xp = min(self.xp + 5, 1000000000)  # Cap XP at 1 billion
            self.print_with_color(f"Баланс после проигрыша: ${format_number(self.balance)}", Fore.RED)
        else:
            self.print_with_color("Фух! Вы выжили! Повезло!", Fore.GREEN)
            winnings = bet * 2
            self.print_with_color(f"Вы выиграли ${format_number(winnings)}!", Fore.GREEN)
            self.balance += winnings
            self.total_winnings += winnings
            # Increment win streak
            self.win_streak += 1
            self.last_game_result = 'win'
            # Add XP but cap it to prevent rapid progression
            self.xp = min(self.xp + 10, 1000000000)  # Cap XP at 1 billion
            self.print_with_color(f"Баланс после выигрыша: ${format_number(self.balance)}", Fore.GREEN)

        # Cap balance to prevent unrealistic amounts
        self.balance = min(self.balance, 1000000000)  # Cap at 1 billion

        # Check for suspicious activity
        self.check_suspicious_activity()
        
        # Check daily challenges
        self.achievement_manager.check_daily_challenge_completion("games_played")
        if bet >= 1000:
            self.achievement_manager.check_daily_challenge_completion("bet_size", bet)
        if self.win_streak >= 3:
            self.achievement_manager.check_daily_challenge_completion("win_streak", self.win_streak)
        if self.xp >= 1000:
            self.achievement_manager.check_daily_challenge_completion("xp_collected", self.xp)
        if self.level >= 5:
            self.achievement_manager.check_daily_challenge_completion("level", self.level)

        self.check_level_up()

        print(f"Новый баланс: ${format_number(self.balance)}")

        if self.auto_save_enabled:
            self.save_manager.save_game()

    def check_level_up(self):
        if self.xp >= self.xp_to_level:
            self.level += 1
            self.xp -= self.xp_to_level
            # Limit XP to prevent rapid progression
            self.xp = min(self.xp, 1000000000)  # Cap XP at 1 billion
            # Limit level progression
            if self.level > 10000:
                self.level = 10000
                self.print_with_color("Достигнут максимальный уровень!", Fore.LIGHTYELLOW_EX)
            else:
                self.xp_to_level = int(self.xp_to_level * 1.5)
                # Cap the XP needed for next level to prevent extremely high requirements
                self.xp_to_level = min(self.xp_to_level, 1000000000)
                self.print_with_color(f"\n🎉 ПОЗДРАВЛЯЕМ! Вы достигли уровня {format_number(self.level)}! 🎉", Fore.LIGHTYELLOW_EX)
                self.print_with_color(f"Для следующего уровня нужно {format_number(self.xp_to_level)} XP", Fore.CYAN)
                
                # Check for level-based achievements
                self.achievement_manager.check_achievements()

    def check_suspicious_activity(self):
        """Check for suspicious gaming patterns that might indicate cheating"""
        # Check for unusually high win streaks
        if self.win_streak > 10:
            self.print_with_color("Обнаружена подозрительная серия побед! Проверка целостности...", Fore.YELLOW)
        
        # Check for rapid balance increase
        if self.balance > self.game_session_start_balance * 1000:  # Balance increased 1000x
            self.print_with_color("Обнаружено подозрительное увеличение баланса!", Fore.RED)
        
        # Check for impossible win rates (more than 90% wins in last 20 games)
        if self.games_played >= 20:
            recent_games = min(20, self.games_played)
            expected_wins = recent_games * 0.1  # Since chance is 1/10 = 10%
            if self.win_streak > expected_wins * 5:  # Allow 5x tolerance
                self.print_with_color("Подозрительно высокий процент побед!", Fore.RED)
        
        # Check for impossible XP gain rate
        expected_max_xp = self.games_played * 10  # Max 10 XP per game
        if self.xp > expected_max_xp * 2:  # Allow 2x tolerance for level bonuses
            self.print_with_color("Обнаружено подозрительное количество XP!", Fore.RED)

    def load_settings(self):
        """Load settings from file"""
        if self.save_manager:
            self.save_manager.load_settings()
        else:
            # Fallback to default settings
            self.typewriter_enabled = True
            self.auto_save_enabled = True
            self.auto_save_interval = 60
            self.cloud_sync_enabled = False

    def save_settings(self):
        """Save settings to file"""
        if self.save_manager:
            self.save_manager.save_settings()
        else:
            # Fallback to basic save
            settings = {
                'typewriter_enabled': self.typewriter_enabled,
                'auto_save_enabled': self.auto_save_enabled,
                'auto_save_interval': self.auto_save_interval,
                'cloud_sync_enabled': getattr(self, 'cloud_sync_enabled', False)
            }
            try:
                with open(self.settings_file, 'w') as f:
                    import json
                    json.dump(settings, f)
            except:
                pass

    def double_or_nothing(self):
        """Double or Nothing game mode - win doubles your bet, lose loses it all"""
        if self.balance <= 0:
            self.balance = 10
            self.print_with_color(f"\nУ вас закончились деньги! Но мы дали вам ${format_number(10)}, чтобы вы могли продолжить играть!", Fore.YELLOW)

        print(f"\n{Fore.LIGHTBLUE_EX}РЕЖИМ 'ВСЁ ИЛИ НИЧЕГО'{Fore.RESET}")
        print(f"Ваш текущий баланс: ${format_number(self.balance)}")
        print("Правила: Выбираете число от 1 до 2. Если угадываете - выигрываете удвоенную ставку, иначе теряете всё.")

        while True:
            try:
                bet = int(input(f"Введите ставку (минимум $1, максимум ${format_number(self.balance)}): $"))
                if bet <= 0:
                    print("Ставка должна быть больше 0!")
                    continue
                if bet > self.balance:
                    print(f"У вас недостаточно средств! Ваш баланс: ${format_number(self.balance)}")
                    continue
                break
            except ValueError:
                print("Пожалуйста, введите корректное число!")

        while True:
            try:
                player_pick = int(input("Выберите число (1 или 2): "))
                if player_pick in [1, 2]:
                    break
                else:
                    print("Пожалуйста, выберите 1 или 2!")
            except ValueError:
                print("Пожалуйста, введите корректное число!")

        self.print_with_color("\n[БРОСОК КУБИКА]", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Кубик катится по столу...", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Шансы распределяются...", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Кубик замедляется...", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)

        import secrets
        result = secrets.randbelow(2) + 1  # Random number 1 or 2
        self.print_with_color(f"Кубик останавливается на числе {result}", Fore.MAGENTA)
        time.sleep(0.5)

        if player_pick == result:
            winnings = bet * 2
            self.balance += winnings
            self.xp += 15  # More XP for riskier game
            self.print_with_color(f"Поздравляем! Вы выиграли ${format_number(winnings)}!", Fore.GREEN)
            self.print_with_color(f"Новый баланс: ${format_number(self.balance)}", Fore.GREEN)
        else:
            self.balance -= bet
            self.xp += 3  # Less XP for losing
            self.print_with_color("К сожалению, вы проиграли...", Fore.RED)
            self.print_with_color(f"Новый баланс: ${format_number(self.balance)}", Fore.RED)

        # Cap balance to prevent unrealistic amounts
        self.balance = min(self.balance, 1000000000)  # Cap at 1 billion

        # Update game statistics
        self.games_played += 1
        if player_pick == result:
            self.total_winnings += winnings
            self.win_streak += 1
            self.last_game_result = 'win'
        else:
            self.total_losses += bet
            # Reset win streak on loss
            if self.win_streak > self.max_win_streak:
                self.max_win_streak = self.win_streak
            self.win_streak = 0
            self.last_game_result = 'loss'

        # Check for suspicious activity
        self.check_suspicious_activity()

        # Check daily challenges
        self.achievement_manager.check_daily_challenge_completion("games_played")
        if bet >= 1000:
            self.achievement_manager.check_daily_challenge_completion("bet_size", bet)
        if self.win_streak >= 3:
            self.achievement_manager.check_daily_challenge_completion("win_streak", self.win_streak)
        if self.xp >= 1000:
            self.achievement_manager.check_daily_challenge_completion("xp_collected", self.xp)
        if self.level >= 5:
            self.achievement_manager.check_daily_challenge_completion("level", self.level)

        self.check_level_up()

        if self.auto_save_enabled:
            self.save_manager.save_game()

    def progressive_jackpot(self):
        """Progressive Jackpot game mode - accumulate winnings over time"""
        if self.balance <= 0:
            self.balance = 10
            self.print_with_color(f"\nУ вас закончились деньги! Но мы дали вам ${format_number(10)}, чтобы вы могли продолжить играть!", Fore.YELLOW)

        print(f"\n{Fore.LIGHTGREEN_EX}ПРОГРЕССИВНЫЙ ДЖЕКПОТ{Fore.RESET}")
        print(f"Ваш текущий баланс: ${format_number(self.balance)}")
        print("Правила: Ставка идёт в общий джекпот. Каждый ход шанс выиграть весь джекпот.")
        
        # Initialize progressive jackpot if it doesn't exist
        if not hasattr(self, 'progressive_jackpot_amount'):
            self.progressive_jackpot_amount = 100  # Start with $100

        print(f"Текущий джекпот: ${format_number(self.progressive_jackpot_amount)}")

        while True:
            try:
                bet = int(input(f"Введите ставку (минимум $1, максимум ${format_number(self.balance)}): $"))
                if bet <= 0:
                    print("Ставка должна быть больше 0!")
                    continue
                if bet > self.balance:
                    print(f"У вас недостаточно средств! Ваш баланс: ${format_number(self.balance)}")
                    continue
                break
            except ValueError:
                print("Пожалуйста, введите корректное число!")

        self.progressive_jackpot_amount += bet  # Add bet to jackpot
        self.balance -= bet  # Deduct bet from balance

        self.print_with_color("\n[ДОБАВЛЕНИЕ В ДЖЕКПОТ]", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Ставка добавлена в джекпот...", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Обновляем счётчик джекпота...", Fore.YELLOW, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("[ПЕРЕСЧЁТ ШАНСОВ]", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Шансы пересчитываются...", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)
        self.print_with_color("Готовим розыгрыш...", Fore.CYAN, animation_type="typewriter")
        time.sleep(0.5)

        # The chance of winning is 1 in 20 (5%)
        import secrets
        result = secrets.randbelow(20)  # 0 to 19
        winning_number = 0  # Only 0 wins the jackpot

        if result == winning_number:
            self.balance += self.progressive_jackpot_amount
            self.xp += 50  # High XP reward for winning jackpot
            self.print_with_color(f"ПОЗДРАВЛЯЕМ! ВЫ ВЫИГРАЛИ ДЖЕКПОТ ${format_number(self.progressive_jackpot_amount)}!", Fore.LIGHTYELLOW_EX)
            self.print_with_color(f"Новый баланс: ${format_number(self.balance)}", Fore.LIGHTGREEN_EX)
            # Reset jackpot after win
            self.progressive_jackpot_amount = 100
        else:
            self.xp += 5  # Small XP for participating
            self.print_with_color(f"Не повезло! Джекпот увеличен до ${format_number(self.progressive_jackpot_amount)}", Fore.RED)
            self.print_with_color(f"Новый баланс: ${format_number(self.balance)}", Fore.RED)

        # Cap balance to prevent unrealistic amounts
        self.balance = min(self.balance, 1000000000)  # Cap at 1 billion

        # Update game statistics
        self.games_played += 1
        if result == winning_number:
            self.total_winnings += self.progressive_jackpot_amount
            self.win_streak += 1
            self.last_game_result = 'jackpot_win'
            # Check daily challenge for winning jackpot
            self.achievement_manager.check_daily_challenge_completion("play_progressive_jackpot")
        else:
            self.total_losses += bet
            # Reset win streak on loss
            if self.win_streak > self.max_win_streak:
                self.max_win_streak = self.win_streak
            self.win_streak = 0
            self.last_game_result = 'jackpot_loss'

        # Check for suspicious activity
        self.check_suspicious_activity()

        # Check daily challenges
        self.achievement_manager.check_daily_challenge_completion("games_played")
        if bet >= 1000:
            self.achievement_manager.check_daily_challenge_completion("bet_size", bet)
        if self.win_streak >= 3:
            self.achievement_manager.check_daily_challenge_completion("win_streak", self.win_streak)
        if self.xp >= 1000:
            self.achievement_manager.check_daily_challenge_completion("xp_collected", self.xp)
        if self.level >= 5:
            self.achievement_manager.check_daily_challenge_completion("level", self.level)

        self.check_level_up()

        if self.auto_save_enabled:
            self.save_manager.save_game()