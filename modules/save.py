import json
import os
import base64
import hashlib
import time
from datetime import datetime
from colorama import Fore


class SaveManager:
    """Handles all save and load functionality for the game"""
    
    def __init__(self, game_instance):
        self.game = game_instance
        self.save_file = self.game.save_file
        self.settings_file = self.game.settings_file

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.game.typewriter_enabled = settings.get('typewriter_enabled', True)
                    self.game.auto_save_enabled = settings.get('auto_save_enabled', True)
                    self.game.auto_save_interval = settings.get('auto_save_interval', 60)
                    self.game.cloud_sync_enabled = settings.get('cloud_sync_enabled', False)
            except:
                pass

    def save_settings(self):
        settings = {
            'typewriter_enabled': self.game.typewriter_enabled,
            'auto_save_enabled': self.game.auto_save_enabled,
            'auto_save_interval': self.game.auto_save_interval,
            'cloud_sync_enabled': getattr(self.game, 'cloud_sync_enabled', False)
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except:
            pass

    def compute_checksum(self, data):
        """Compute a checksum for the game data to verify integrity"""
        # Convert data to string and hash it
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def encrypt_data_with_checksum(self, data):
        """Encrypt data along with its checksum"""
        # Add checksum to the data
        data_with_checksum = data.copy()
        data_with_checksum['checksum'] = self.compute_checksum(data)
        json_str = json.dumps(data_with_checksum)
        encoded_bytes = base64.b64encode(json_str.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def decrypt_data_with_checksum(self, encrypted_data):
        """Decrypt data and verify its checksum"""
        try:
            decoded_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            json_str = decoded_bytes.decode('utf-8')
            data = json.loads(json_str)
            
            # Extract and remove checksum
            if 'checksum' in data:
                stored_checksum = data.pop('checksum')
                # Recompute checksum from the remaining data
                computed_checksum = self.compute_checksum(data)
                
                # Verify checksum
                if stored_checksum != computed_checksum:
                    self.game.print_with_color("Обнаружено повреждение или изменение файла сохранения!", Fore.RED)
                    return None
            
            return data
        except:
            return None

    def decrypt_data(self, encrypted_data):
        """Legacy method for backward compatibility"""
        try:
            decoded_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            json_str = decoded_bytes.decode('utf-8')
            return json.loads(json_str)
        except:
            return None

    def save_game(self):
        data = {
            'balance': self.game.balance,
            'xp': self.game.xp,
            'level': self.game.level,
            'xp_to_level': self.game.xp_to_level,
            'achievements_unlocked': self.game.achievement_manager.achievements_unlocked,
            'games_played': self.game.games_played,
            'total_winnings': self.game.total_winnings,
            'total_losses': self.game.total_losses,
            'win_streak': self.game.win_streak,
            'max_win_streak': self.game.max_win_streak,
            'progressive_jackpot_amount': getattr(self.game, 'progressive_jackpot_amount', 100),
            'last_save_time': time.time(),
            'cloud_sync_enabled': getattr(self.game, 'cloud_sync_enabled', False)
        }

        encrypted_data = self.encrypt_data_with_checksum(data)

        try:
            with open(self.save_file, 'w') as f:
                f.write(encrypted_data)
            self.game.print_with_color("Игра сохранена!", Fore.GREEN)
            
            # Optionally sync to cloud if enabled
            if getattr(self.game, 'cloud_sync_enabled', False):
                self.cloud_sync_save(data)
            
            return True
        except:
            self.game.print_with_color("Ошибка при сохранении игры.", Fore.RED)
            return False

    def cloud_sync_save(self, data):
        """Save game data to cloud storage (simulated)"""
        try:
            # Simulate cloud sync by saving to a separate file
            import json
            import base64
            from datetime import datetime
            
            # Add timestamp to data
            data['cloud_sync_timestamp'] = datetime.now().isoformat()
            
            # Encode data for cloud storage
            json_str = json.dumps(data)
            encoded_bytes = base64.b64encode(json_str.encode('utf-8'))
            encoded_data = encoded_bytes.decode('utf-8')
            
            # Write to cloud sync file
            cloud_file = "cloud_save.dat"
            with open(cloud_file, 'w') as f:
                f.write(encoded_data)
            
            self.game.print_with_color("Игра синхронизирована с облаком!", Fore.LIGHTBLUE_EX)
        except Exception as e:
            self.game.print_with_color(f"Ошибка синхронизации с облаком: {str(e)}", Fore.RED)

    def cloud_sync_load(self):
        """Load game data from cloud storage (simulated)"""
        try:
            cloud_file = "cloud_save.dat"
            if not os.path.exists(cloud_file):
                self.game.print_with_color("Нет данных в облачном хранилище.", Fore.YELLOW)
                return False
                
            with open(cloud_file, 'r') as f:
                encoded_data = f.read()
            
            # Decode cloud data
            decoded_bytes = base64.b64decode(encoded_data.encode('utf-8'))
            json_str = decoded_bytes.decode('utf-8')
            data = json.loads(json_str)
            
            # Load the data into the game
            self.game.balance = data.get('balance', 100)
            self.game.xp = data.get('xp', 0)
            self.game.level = data.get('level', 1)
            self.game.xp_to_level = data.get('xp_to_level', 100)
            
            # Load achievements and statistics
            self.game.achievement_manager.achievements_unlocked = data.get('achievements_unlocked', [])
            # Mark achievements as unlocked in the achievements list
            for achievement_id in self.game.achievement_manager.achievements_unlocked:
                for achievement in self.game.achievement_manager.achievements_list:
                    if achievement['id'] == achievement_id:
                        achievement['unlocked'] = True
            self.game.games_played = data.get('games_played', 0)
            self.game.total_winnings = data.get('total_winnings', 0)
            self.game.total_losses = data.get('total_losses', 0)
            self.game.win_streak = data.get('win_streak', 0)
            self.game.max_win_streak = data.get('max_win_streak', 0)
            self.game.progressive_jackpot_amount = data.get('progressive_jackpot_amount', 100)
            
            # Reset session statistics when loading game
            self.game.game_session_start_balance = self.game.balance
            self.game.last_game_result = None
            
            # Set cloud sync as enabled
            self.game.cloud_sync_enabled = data.get('cloud_sync_enabled', False)
            
            self.game.print_with_color("Игра загружена из облака!", Fore.LIGHTGREEN_EX)
            return True
        except Exception as e:
            self.game.print_with_color(f"Ошибка загрузки из облака: {str(e)}", Fore.RED)
            return False

    def load_game(self):
        # Ask user if they want to load from cloud or local
        if os.path.exists("cloud_save.dat") or (hasattr(self.game, 'cloud_sync_enabled') and self.game.cloud_sync_enabled):
            choice = input("Найдено облачное сохранение. Загрузить из облака? (y/n): ").lower()
            if choice == 'y':
                return self.cloud_sync_load()
        
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    encrypted_data = f.read()

                data = self.decrypt_data_with_checksum(encrypted_data)
                if data is not None:
                    # Validate loaded data to prevent cheating
                    balance = data.get('balance', 100)
                    xp = data.get('xp', 0)
                    level = data.get('level', 1)
                    xp_to_level = data.get('xp_to_level', 100)
                    
                    # Apply validation checks
                    if not isinstance(balance, (int, float)) or balance < 0 or balance > 1000000000:  # Max 1 billion
                        self.game.print_with_color("Обнаружено подозрительное значение баланса в файле сохранения!", Fore.RED)
                        return False
                    
                    if not isinstance(xp, (int, float)) or xp < 0 or xp > 1000000000:
                        self.game.print_with_color("Обнаружено подозрительное значение XP в файле сохранения!", Fore.RED)
                        return False
                        
                    if not isinstance(level, int) or level < 1 or level > 10000:
                        self.game.print_with_color("Обнаружено подозрительное значение уровня в файле сохранения!", Fore.RED)
                        return False
                        
                    if not isinstance(xp_to_level, (int, float)) or xp_to_level < 100 or xp_to_level > 1000000000:
                        self.game.print_with_color("Обнаружено подозрительное значение XP для следующего уровня в файле сохранения!", Fore.RED)
                        return False
                    
                    self.game.balance = balance
                    self.game.xp = xp
                    self.game.level = level
                    self.game.xp_to_level = xp_to_level
                    # Load achievements and statistics
                    self.game.achievement_manager.achievements_unlocked = data.get('achievements_unlocked', [])
                    # Mark achievements as unlocked in the achievements list
                    for achievement_id in self.game.achievement_manager.achievements_unlocked:
                        for achievement in self.game.achievement_manager.achievements_list:
                            if achievement['id'] == achievement_id:
                                achievement['unlocked'] = True
                    self.game.games_played = data.get('games_played', 0)
                    self.game.total_winnings = data.get('total_winnings', 0)
                    self.game.total_losses = data.get('total_losses', 0)
                    self.game.win_streak = data.get('win_streak', 0)
                    self.game.max_win_streak = data.get('max_win_streak', 0)
                    self.game.progressive_jackpot_amount = data.get('progressive_jackpot_amount', 100)
                    # Load cloud sync setting
                    self.game.cloud_sync_enabled = data.get('cloud_sync_enabled', False)
                    # Reset session statistics when loading game
                    self.game.game_session_start_balance = balance
                    self.game.last_game_result = None
                    self.game.print_with_color("Игра загружена!", Fore.GREEN)
                    return True
                else:
                    self.game.print_with_color("Ошибка при загрузке игры (неверный формат данных).", Fore.RED)
                    return False
            except Exception as e:
                self.game.print_with_color(f"Ошибка при загрузке игры: {str(e)}", Fore.RED)
                return False
        else:
            self.game.print_with_color("Сохранений не найдено.", Fore.YELLOW)
            return False