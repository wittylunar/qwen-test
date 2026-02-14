from colorama import Fore
from modules.core import format_number


class ShopManager:
    """Handles all shop functionality for the game"""
    
    def __init__(self, game_instance):
        self.game = game_instance

    def shop(self):
        # Check if visiting shop completes a daily challenge
        self.game.achievement_manager.check_daily_challenge_completion("visit_shop")

        while True:
            try:
                print(f"\n{Fore.LIGHTBLUE_EX}=== МАГАЗИН ==={Fore.RESET}")
                print(f"{Fore.CYAN}Баланс: ${format_number(self.game.balance)}{Fore.RESET}")
                print(f"{Fore.LIGHTYELLOW_EX}1. Дополнительная жизнь - ${format_number(50)} (увеличивает шансы на выживание)")
                print(f"{Fore.LIGHTGREEN_EX}2. Удвоитель ставки - ${format_number(75)} (удваивает ваш следующий выигрыш)")
                print(f"{Fore.LIGHTCYAN_EX}3. Секретный патрон - ${format_number(100)} (уменьшает шанс проигрыша)")
                print(f"{Fore.LIGHTMAGENTA_EX}4. Щит безопасности - ${format_number(150)} (позволяет пережить один проигрыш)")
                print(f"{Fore.LIGHTWHITE_EX}5. Счастливое число - ${format_number(200)} (увеличивает шансы на выигрыш)")
                print(f"{Fore.LIGHTRED_EX}6. Бонусный раунд - ${format_number(300)} (дает дополнительную попытку)")
                print(f"{Fore.LIGHTYELLOW_EX}7. Золотой билет - ${format_number(500)} (гарантирует выигрыш в следующей игре)")
                print(f"{Fore.LIGHTBLUE_EX}8. Кристальный шар - ${format_number(750)} (предсказывает следующее число)")
                print(f"{Fore.LIGHTGREEN_EX}9. Увеличитель XP - ${format_number(1000)} (удваивает XP за победы)")
                print(f"{Fore.LIGHTCYAN_EX}10. Страховка - ${format_number(1200)} (возвращает 50% ставки при проигрыше)")
                print(f"{Fore.LIGHTMAGENTA_EX}11. VIP-подписка - ${format_number(2000)} (ежедневные бонусы +100$)")
                print(f"{Fore.LIGHTWHITE_EX}12. Секретная карта - ${format_number(5000)} (позволяет избежать поражение 1 раз)")
                print(f"{Fore.LIGHTRED_EX}13. Элитный статус - ${format_number(10000)} (повышает шансы на выигрыш)")
                print(f"{Fore.LIGHTYELLOW_EX}14. Личный ассистент - ${format_number(15000)} (советы по выигрышу)")
                print(f"{Fore.LIGHTBLUE_EX}15. Назад в меню")
                print(f"{Fore.LIGHTCYAN_EX}----------------")

                choice = input("Выберите опцию: ")

                if choice == "1":
                    if self.game.balance >= 50:
                        self.game.balance -= 50
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили дополнительную жизнь! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(50)}", Fore.RED)

                elif choice == "2":
                    if self.game.balance >= 75:
                        self.game.balance -= 75
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили удвоитель ставки! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(75)}", Fore.RED)

                elif choice == "3":
                    if self.game.balance >= 100:
                        self.game.balance -= 100
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили секретный патрон! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(100)}", Fore.RED)

                elif choice == "4":
                    if self.game.balance >= 150:
                        self.game.balance -= 150
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили щит безопасности! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(150)}", Fore.RED)

                elif choice == "5":
                    if self.game.balance >= 200:
                        self.game.balance -= 200
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили счастливое число! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(200)}", Fore.RED)

                elif choice == "6":
                    if self.game.balance >= 300:
                        self.game.balance -= 300
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили бонусный раунд! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(300)}", Fore.RED)

                elif choice == "7":
                    if self.game.balance >= 500:
                        self.game.balance -= 500
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили золотой билет! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(500)}", Fore.RED)

                elif choice == "8":
                    if self.game.balance >= 750:
                        self.game.balance -= 750
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили кристальный шар! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(750)}", Fore.RED)

                elif choice == "9":
                    if self.game.balance >= 1000:
                        self.game.balance -= 1000
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили увеличитель XP! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                        # Add XP boost functionality here
                        if not hasattr(self.game, 'xp_boost_active'):
                            self.game.xp_boost_active = True
                            self.game.xp_multiplier = 2
                        else:
                            self.game.xp_multiplier = 2
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(1000)}", Fore.RED)

                elif choice == "10":
                    if self.game.balance >= 1200:
                        self.game.balance -= 1200
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили страховку! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                        # Add insurance functionality here
                        if not hasattr(self.game, 'insurance_active'):
                            self.game.insurance_active = True
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(1200)}", Fore.RED)

                elif choice == "11":
                    if self.game.balance >= 2000:
                        self.game.balance -= 2000
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили VIP-подписку! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                        # Add VIP functionality here
                        if not hasattr(self.game, 'vip_status'):
                            self.game.vip_status = True
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(2000)}", Fore.RED)

                elif choice == "12":
                    if self.game.balance >= 5000:
                        self.game.balance -= 5000
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили секретную карту! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                        # Add secret card functionality here
                        if not hasattr(self.game, 'secret_card_available'):
                            self.game.secret_card_available = True
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(5000)}", Fore.RED)

                elif choice == "13":
                    if self.game.balance >= 10000:
                        self.game.balance -= 10000
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили элитный статус! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                        # Add elite status functionality here
                        if not hasattr(self.game, 'elite_status'):
                            self.game.elite_status = True
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(10000)}", Fore.RED)

                elif choice == "14":
                    if self.game.balance >= 15000:
                        self.game.balance -= 15000
                        # Cap balance to prevent unrealistic amounts
                        self.game.balance = min(self.game.balance, 1000000000)  # Cap at 1 billion
                        self.game.print_with_color(f"✅ Вы купили личного ассистента! Остаток: ${format_number(self.game.balance)}", Fore.GREEN)
                        # Add assistant functionality here
                        if not hasattr(self.game, 'assistant_available'):
                            self.game.assistant_available = True
                    else:
                        self.game.print_with_color(f"❌ Недостаточно средств! Ваш баланс: ${format_number(self.game.balance)}, цена: ${format_number(15000)}", Fore.RED)

                elif choice == "15":
                    break
                else:
                    self.game.print_with_color("❌ Неверный выбор!", Fore.RED)
            except (EOFError, KeyboardInterrupt):
                self.game.print_with_color("\nВыход из магазина...", Fore.LIGHTRED_EX)
                break