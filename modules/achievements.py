import datetime
from colorama import Fore
from modules.core import format_number


class AchievementManager:
    """Handles all achievements and daily challenges functionality for the game"""
    
    def __init__(self, game_instance):
        self.game = game_instance
        self.achievements_unlocked = []
        self.achievements_list = [
            {"id": 1, "name": "Первые шаги", "description": "Достичь 5 уровня", "unlocked": False, "reward": 100},
            {"id": 2, "name": "Счастливчик", "description": "Выиграть 5 раз подряд", "unlocked": False, "reward": 200},
            {"id": 3, "name": "Миллионер", "description": "Достичь баланса $1,000,000", "unlocked": False, "reward": 500},
            {"id": 4, "name": "Азартный игрок", "description": "Сыграть 100 игр", "unlocked": False, "reward": 300},
            {"id": 5, "name": "Джекпот", "description": "Выиграть прогрессивный джекпот", "unlocked": False, "reward": 1000},
            {"id": 6, "name": "Марафонец", "description": "Сыграть 10 часов подряд", "unlocked": False, "reward": 750},
            {"id": 7, "name": "Исследователь", "description": "Посетить все режимы игры", "unlocked": False, "reward": 400},
            {"id": 8, "name": "Магнат", "description": "Потратить $10,000 в магазине", "unlocked": False, "reward": 600}
        ]
        
        # Initialize daily challenges if they don't exist
        if not hasattr(self.game, 'last_daily_reset'):
            self.game.last_daily_reset = str(datetime.date.today())
        if not hasattr(self.game, 'daily_challenges_completed'):
            self.game.daily_challenges_completed = []
        if not hasattr(self.game, 'daily_challenges_list'):
            # Generate daily challenges
            self.generate_daily_challenges()

    def check_achievements(self):
        """Check if any achievements have been unlocked"""
        for achievement in self.achievements_list:
            if not achievement["unlocked"]:
                # Check if achievement conditions are met
                if achievement["id"] == 1 and self.game.level >= 5:  # First Steps - Reach level 5
                    self.unlock_achievement(achievement)
                elif achievement["id"] == 2 and self.game.win_streak >= 5:  # Lucky - Win 5 in a row
                    self.unlock_achievement(achievement)
                elif achievement["id"] == 3 and self.game.balance >= 1000000:  # Millionaire - Reach $1,000,000
                    self.unlock_achievement(achievement)
                elif achievement["id"] == 4 and self.game.games_played >= 100:  # Gambler - Play 100 games
                    self.unlock_achievement(achievement)
                elif achievement["id"] == 5 and self.game.last_game_result == 'jackpot_win':  # Jackpot - Win progressive jackpot
                    self.unlock_achievement(achievement)
                elif achievement["id"] == 7 and hasattr(self.game, 'visited_modes'):  # Explorer - Visit all game modes
                    # This would be triggered when visiting different game modes
                    pass

    def unlock_achievement(self, achievement):
        """Unlock an achievement and award the reward"""
        achievement["unlocked"] = True
        self.achievements_unlocked.append(achievement["id"])
        self.game.balance += achievement["reward"]
        self.game.print_with_color(f"🏆 НОВОЕ ДОСТИЖЕНИЕ: {achievement['name']}! 🏆", Fore.LIGHTYELLOW_EX)
        self.game.print_with_color(f"Награда: ${format_number(achievement['reward'])}", Fore.LIGHTGREEN_EX)
        self.game.print_with_color(f"Описание: {achievement['description']}", Fore.LIGHTCYAN_EX)
        self.game.print_with_color(f"Новый баланс: ${format_number(self.game.balance)}", Fore.LIGHTGREEN_EX)

    def show_achievements(self):
        """Display all achievements and their status"""
        print(f"\n{Fore.LIGHTYELLOW_EX}=== ДОСТИЖЕНИЯ ==={Fore.RESET}")
        for achievement in self.achievements_list:
            status = "✓" if achievement["unlocked"] else "○"
            color = Fore.LIGHTGREEN_EX if achievement["unlocked"] else Fore.LIGHTRED_EX
            print(f"{color}{status} {achievement['name']}{Fore.RESET}")
            print(f"   {achievement['description']} | Награда: ${format_number(achievement['reward'])}")
        print(f"\n{Fore.LIGHTCYAN_EX}Разблокировано: {len(self.achievements_unlocked)}/{len(self.achievements_list)} достижений{Fore.RESET}")

    def generate_daily_challenges(self):
        """Generate daily challenges"""
        import random
        
        possible_challenges = [
            {"name": "Выиграть 3 раза подряд", "reward": 500, "type": "win_streak", "target": 3},
            {"name": "Сделать ставку $1000", "reward": 300, "type": "bet_size", "target": 1000},
            {"name": "Достичь 5 уровня", "reward": 1000, "type": "level", "target": 5},
            {"name": "Сыграть 10 игр", "reward": 400, "type": "games_played", "target": 10},
            {"name": "Выиграть 5 игр", "reward": 600, "type": "games_won", "target": 5},
            {"name": "Собрать 1000 XP", "reward": 500, "type": "xp_collected", "target": 1000},
            {"name": "Сыграть в 'Всё или ничего'", "reward": 200, "type": "play_double_or_nothing", "target": 1},
            {"name": "Сыграть в 'Прогрессивный Джекпот'", "reward": 200, "type": "play_progressive_jackpot", "target": 1},
            {"name": "Посетить магазин", "reward": 100, "type": "visit_shop", "target": 1},
            {"name": "Сыграть в 'Монетку'", "reward": 150, "type": "play_coin_flip", "target": 1},
            {"name": "Сыграть в 'Бонусный раунд'", "reward": 150, "type": "play_bonus_round", "target": 1}
        ]
        
        # Select 3 random challenges
        self.game.daily_challenges_list = random.sample(possible_challenges, 3)
        for challenge in self.game.daily_challenges_list:
            challenge["completed"] = False
            challenge["claimed"] = False

    def reset_daily_challenges(self, today):
        """Reset daily challenges for a new day"""
        self.game.last_daily_reset = today
        self.game.daily_challenges_completed = []
        self.generate_daily_challenges()
        self.game.print_with_color("Ежедневные задания обновлены!", Fore.LIGHTYELLOW_EX)

    def check_daily_challenge_completion(self, challenge_type, value=None):
        """Check if a daily challenge has been completed"""
        for challenge in self.game.daily_challenges_list:
            if challenge["type"] == challenge_type and not challenge["completed"]:
                if challenge_type == "win_streak":
                    if value >= challenge["target"]:
                        challenge["completed"] = True
                        self.game.print_with_color(f"✅ Ежедневное задание выполнено: {challenge['name']}!", Fore.LIGHTGREEN_EX)
                elif challenge_type == "bet_size":
                    if value >= challenge["target"]:
                        challenge["completed"] = True
                        self.game.print_with_color(f"✅ Ежедневное задание выполнено: {challenge['name']}!", Fore.LIGHTGREEN_EX)
                elif challenge_type == "level":
                    if self.game.level >= challenge["target"]:
                        challenge["completed"] = True
                        self.game.print_with_color(f"✅ Ежедневное задание выполнено: {challenge['name']}!", Fore.LIGHTGREEN_EX)
                elif challenge_type == "games_played":
                    if self.game.games_played >= challenge["target"]:
                        challenge["completed"] = True
                        self.game.print_with_color(f"✅ Ежедневное задание выполнено: {challenge['name']}!", Fore.LIGHTGREEN_EX)
                elif challenge_type == "games_won":
                    # This would require tracking wins separately
                    pass
                elif challenge_type == "xp_collected":
                    if self.game.xp >= challenge["target"]:
                        challenge["completed"] = True
                        self.game.print_with_color(f"✅ Ежедневное задание выполнено: {challenge['name']}!", Fore.LIGHTGREEN_EX)
                elif challenge_type in ["play_double_or_nothing", "play_progressive_jackpot", 
                                       "visit_shop", "play_coin_flip", "play_bonus_round"]:
                    challenge["completed"] = True
                    self.game.print_with_color(f"✅ Ежедневное задание выполнено: {challenge['name']}!", Fore.LIGHTGREEN_EX)

    def daily_challenges(self):
        """Daily challenges with rewards"""
        import datetime
        
        print(f"\n{Fore.LIGHTRED_EX}=== ЕЖЕДНЕВНЫЕ ЗАДАНИЯ ==={Fore.RESET}")
        
        # Check if we need to reset daily challenges (new day)
        today = str(datetime.date.today())
        if self.game.last_daily_reset != str(today):
            self.reset_daily_challenges(str(today))
        
        # Display daily challenges
        print(f"{Fore.LIGHTYELLOW_EX}Задания на сегодня:{Fore.RESET}")
        for i, challenge in enumerate(self.game.daily_challenges_list):
            status = "✓" if challenge["completed"] else "○"
            color = Fore.LIGHTGREEN_EX if challenge["completed"] else Fore.LIGHTRED_EX
            print(f"{color}{status} {i+1}. {challenge['name']} - Награда: ${format_number(challenge['reward'])}{Fore.RESET}")
        
        print(f"\n{Fore.LIGHTCYAN_EX}Выполненные задания: {len([c for c in self.game.daily_challenges_list if c['completed']])}/{len(self.game.daily_challenges_list)}{Fore.RESET}")
        
        # Option to claim rewards for completed challenges
        incomplete_challenges = [c for c in self.game.daily_challenges_list if not c['completed']]
        completed_challenges = [c for c in self.game.daily_challenges_list if c['completed'] and not c.get('claimed', False)]
        
        if completed_challenges:
            print(f"\n{Fore.LIGHTGREEN_EX}Доступны награды за выполненные задания!{Fore.RESET}")
            for challenge in completed_challenges:
                print(f"- {challenge['name']}: ${format_number(challenge['reward'])}")
            
            claim_choice = input("\nЗабрать награды? (y/n): ").lower()
            if claim_choice == 'y':
                total_reward = sum(c['reward'] for c in completed_challenges)
                self.game.balance += total_reward
                for challenge in completed_challenges:
                    challenge['claimed'] = True
                self.game.print_with_color(f"Получено ${format_number(total_reward)} за выполнение заданий!", Fore.LIGHTYELLOW_EX)
                self.game.print_with_color(f"Новый баланс: ${format_number(self.game.balance)}", Fore.LIGHTGREEN_EX)
        
        if incomplete_challenges:
            print(f"\n{Fore.LIGHTYELLOW_EX}Продолжайте играть, чтобы выполнить задания!{Fore.RESET}")
        else:
            print(f"\n{Fore.LIGHTGREEN_EX}Поздравляем! Все задания на сегодня выполнены!{Fore.RESET}")
        
        input("\nНажмите Enter для возврата в меню...")

    def bonus_round(self):
        """Bonus round game - guess the number for extra rewards"""
        if self.game.balance <= 0:
            self.game.balance = 10
            self.game.print_with_color(f"\nУ вас закончились деньги! Но мы дали вам ${format_number(10)}, чтобы вы могли продолжить играть!", Fore.YELLOW)

        print(f"\n{Fore.LIGHTYELLOW_EX}=== БОНУСНЫЙ РАУНД ==={Fore.RESET}")
        print("Угадайте число от 1 до 5 чтобы выиграть бонус!")
        print(f"Ваш текущий баланс: ${format_number(self.game.balance)}")
        
        import secrets
        secret_number = secrets.randbelow(5) + 1  # Random number 1-5
        
        attempts = 3
        while attempts > 0:
            try:
                guess = int(input(f"У вас {attempts} попыток. Угадайте число (1-5): "))
                if guess < 1 or guess > 5:
                    print("Пожалуйста, введите число от 1 до 5!")
                    continue
                attempts -= 1
                
                if guess == secret_number:
                    bonus = 500 * (attempts + 1)  # Higher bonus for fewer attempts
                    self.game.balance += bonus
                    self.game.xp += 25
                    self.game.print_with_color(f"🎉 ПОЗДРАВЛЯЕМ! Вы угадали число {secret_number}!", Fore.LIGHTGREEN_EX)
                    self.game.print_with_color(f"Бонус: ${format_number(bonus)}", Fore.LIGHTYELLOW_EX)
                    self.game.print_with_color(f"Новый баланс: ${format_number(self.game.balance)}", Fore.LIGHTGREEN_EX)
                    break
                else:
                    if attempts > 0:
                        hint = "меньше" if guess > secret_number else "больше"
                        self.game.print_with_color(f"Неверно! Подсказка: правильное число {hint}", Fore.LIGHTRED_EX)
                    else:
                        self.game.print_with_color(f"К сожалению, вы не угадали. Загаданное число было {secret_number}", Fore.LIGHTRED_EX)
                        
            except ValueError:
                print("Пожалуйста, введите корректное число!")
        
        # Cap balance to prevent unrealistic amounts
        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion

        # Update game statistics
        self.game.games_played += 1
        self.game.check_level_up()
        self.check_achievements()
        
        # Check daily challenges
        self.check_daily_challenge_completion("games_played")
        if self.game.xp >= 1000:
            self.check_daily_challenge_completion("xp_collected", self.game.xp)
        if self.game.level >= 5:
            self.check_daily_challenge_completion("level", self.game.level)
        self.check_daily_challenge_completion("play_bonus_round")

        if self.game.auto_save_enabled:
            self.game.save_manager.save_game()

    def coin_flip_game(self):
        """Coin flip mini-game - double or nothing"""
        if self.game.balance <= 0:
            self.game.balance = 10
            self.game.print_with_color(f"\nУ вас закончились деньги! Но мы дали вам ${format_number(10)}, чтобы вы могли продолжить играть!", Fore.YELLOW)

        print(f"\n{Fore.LIGHTCYAN_EX}=== МОНЕТКА ==={Fore.RESET}")
        print("Орёл или решка? Удвойте свою ставку при победе!")
        print(f"Ваш текущий баланс: ${format_number(self.game.balance)}")

        while True:
            try:
                bet = int(input(f"Введите ставку (минимум $1, максимум ${format_number(self.game.balance)}): $"))
                if bet <= 0:
                    print("Ставка должна быть больше 0!")
                    continue
                if bet > self.game.balance:
                    print(f"У вас недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}")
                    continue
                break
            except ValueError:
                print("Пожалуйста, введите корректное число!")

        choice = ""
        while choice not in ["орёл", "решка"]:
            choice = input("Выберите 'орёл' или 'решка': ").lower().strip()
            if choice not in ["орёл", "решка"]:
                print("Пожалуйста, введите 'орёл' или 'решка'")

        self.game.print_with_color("Монетка подбрасывается...", Fore.YELLOW)
        time.sleep(1)
        self.game.print_with_color("Монетка вращается в воздухе...", Fore.CYAN)
        time.sleep(1)

        import secrets
        result = "орёл" if secrets.randbelow(2) == 0 else "решка"
        self.game.print_with_color(f"Монетка падает: {result}", Fore.MAGENTA)
        time.sleep(0.5)

        if choice == result:
            winnings = bet * 2
            self.game.balance += winnings
            self.game.xp += 12  # XP for mini-game
            self.game.print_with_color(f"Поздравляем! Вы выиграли ${format_number(winnings)}!", Fore.GREEN)
            self.game.print_with_color(f"Новый баланс: ${format_number(self.game.balance)}", Fore.GREEN)
        else:
            self.game.balance -= bet
            self.game.xp += 2  # Smaller XP for losing
            self.game.print_with_color("К сожалению, вы проиграли...", Fore.RED)
            self.game.print_with_color(f"Новый баланс: ${format_number(self.game.balance)}", Fore.RED)

        # Cap balance to prevent unrealistic amounts
        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion

        # Update game statistics
        self.game.games_played += 1
        self.game.check_level_up()
        self.check_achievements()
        
        # Check daily challenges
        self.check_daily_challenge_completion("games_played")
        self.check_daily_challenge_completion("play_coin_flip")
        if bet >= 1000:
            self.check_daily_challenge_completion("bet_size", bet)
        if self.game.xp >= 1000:
            self.check_daily_challenge_completion("xp_collected", self.game.xp)
        if self.game.level >= 5:
            self.check_daily_challenge_completion("level", self.game.level)

        if self.game.auto_save_enabled:
            self.game.save_manager.save_game()