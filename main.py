#!/usr/bin/env python3

import colorama
from colorama import Fore
from modules.core import RussianRouletteCore
from modules.ui import UIHandler
from modules.save import SaveManager
from modules.shop import ShopManager
from modules.achievements import AchievementManager
from modules.multiplayer import MultiplayerManager


class RussianRouletteGame(RussianRouletteCore):
    def __init__(self):
        # Initialize core functionality
        super().__init__()
        
        # Initialize other managers
        self.ui = UIHandler(self)
        self.save_manager = SaveManager(self)
        self.shop_manager = ShopManager(self)
        self.achievement_manager = AchievementManager(self)
        self.multiplayer_manager = MultiplayerManager(self)
        
        # Now that managers are initialized, we can load settings
        self.load_settings()

    def toggle_cloud_sync(self):
        """Toggle cloud synchronization on/off"""
        if not hasattr(self, 'cloud_sync_enabled'):
            self.cloud_sync_enabled = False
        
        self.cloud_sync_enabled = not self.cloud_sync_enabled
        
        status = "включена" if self.cloud_sync_enabled else "отключена"
        self.print_with_color(f"Облачная синхронизация {status}!", Fore.LIGHTCYAN_EX)
        
        # Save settings
        self.save_settings()

    def run(self):
        while True:
            try:
                self.ui.display_menu()
                choice = input("Выберите опцию: ")

                if choice == "1":
                    self.russian_roulette()
                elif choice == "2":
                    self.double_or_nothing()
                elif choice == "3":
                    self.progressive_jackpot()
                elif choice == "4":
                    self.achievement_manager.bonus_round()
                elif choice == "5":
                    self.achievement_manager.coin_flip_game()
                elif choice == "6":
                    self.multiplayer_manager.multiplayer_menu()
                elif choice == "7":
                    self.shop_manager.shop()
                elif choice == "8":
                    self.ui.show_stats()
                elif choice == "9":
                    self.achievement_manager.show_achievements()
                elif choice == "10":
                    self.ui.show_cheats()
                elif choice == "11":
                    self.achievement_manager.daily_challenges()
                elif choice == "12":
                    self.save_manager.save_game()
                elif choice == "13":
                    self.save_manager.load_game()
                elif choice == "14":
                    self.ui.display_settings_menu()
                elif choice == "15":
                    self.print_with_color("Спасибо за игру в Cuddly Chainsaw! До свидания!", Fore.LIGHTGREEN_EX)
                    break
                else:
                    self.print_with_color("Неверный выбор!", Fore.RED)
            except (EOFError, KeyboardInterrupt):
                # Handle cases where input is not available (like when running in certain environments)
                self.print_with_color("\nВыход из игры...", Fore.LIGHTRED_EX)
                break


def main():
    colorama.init(autoreset=True)

    game = RussianRouletteGame()
    game.run()


if __name__ == "__main__":
    main()