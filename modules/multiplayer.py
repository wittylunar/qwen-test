import socket
import threading
import pickle
import time
import random
from colorama import Fore


class MultiplayerManager:
    """Handles multiplayer functionality for the game"""
    
    def __init__(self, game_instance):
        self.game = game_instance
        self.is_server = False
        self.is_client = False
        self.server_socket = None
        self.client_socket = None
        self.players = []  # List of connected players
        self.player_id = None  # ID of this player
        self.room_id = None  # ID of the room this player is in
        self.max_players = 7  # Maximum players in a room
        self.port = 3074  # Port for multiplayer
        self.host_ip = None  # IP address of the host
        self.game_in_progress = False  # Whether a multiplayer game is running

    def start_server(self):
        """Start a multiplayer server to host games"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Get local IP address
            hostname = socket.gethostname()
            self.host_ip = socket.gethostbyname(hostname)
            
            # If the IP is localhost, try to get actual IP
            if self.host_ip == "127.0.0.1" or self.host_ip.startswith("127."):
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(("8.8.8.8", 80))
                    self.host_ip = s.getsockname()[0]
            
            self.server_socket.bind((self.host_ip, self.port))
            self.server_socket.listen(self.max_players)
            
            self.is_server = True
            self.player_id = 0  # Host is always player 0
            self.room_id = f"ROOM_{random.randint(1000, 9999)}"
            
            self.game.print_with_color(f"Сервер запущен на {self.host_ip}:{self.port}", Fore.LIGHTGREEN_EX)
            self.game.print_with_color(f"ID комнаты: {self.room_id}", Fore.LIGHTCYAN_EX)
            self.game.print_with_color(f"Ожидание подключения игроков... (максимум {self.max_players})", Fore.LIGHTYELLOW_EX)
            
            # Start accepting connections in a separate thread
            server_thread = threading.Thread(target=self.accept_connections)
            server_thread.daemon = True
            server_thread.start()
            
            return True
        except Exception as e:
            self.game.print_with_color(f"Ошибка при запуске сервера: {str(e)}", Fore.RED)
            return False

    def accept_connections(self):
        """Accept incoming player connections"""
        while len(self.players) < self.max_players:
            try:
                client_socket, addr = self.server_socket.accept()
                player_id = len(self.players)
                
                # Send player info to the new client
                player_info = {
                    'player_id': player_id,
                    'room_id': self.room_id,
                    'max_players': self.max_players
                }
                
                client_socket.send(pickle.dumps(player_info))
                
                # Add player to the list
                player_data = {
                    'socket': client_socket,
                    'address': addr,
                    'player_id': player_id,
                    'connected': True
                }
                
                self.players.append(player_data)
                
                self.game.print_with_color(f"Игрок {player_id} подключился с {addr[0]}:{addr[1]}", Fore.LIGHTGREEN_EX)
                self.game.print_with_color(f"Всего игроков: {len(self.players)}/{self.max_players}", Fore.LIGHTCYAN_EX)
                
                # Start listening for messages from this client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, player_id))
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                self.game.print_with_color(f"Ошибка при подключении игрока: {str(e)}", Fore.RED)
                break

    def handle_client(self, client_socket, player_id):
        """Handle messages from a connected client"""
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                self.process_message(message, player_id)
        except Exception as e:
            self.game.print_with_color(f"Ошибка при обработке сообщения от игрока {player_id}: {str(e)}", Fore.RED)
        finally:
            # Remove player from the list
            for player in self.players:
                if player['player_id'] == player_id:
                    player['connected'] = False
                    self.game.print_with_color(f"Игрок {player_id} отключился", Fore.LIGHTRED_EX)
                    break

    def connect_to_server(self, host_ip):
        """Connect to a multiplayer server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host_ip, self.port))
            
            # Receive player info from server
            data = self.client_socket.recv(4096)
            player_info = pickle.loads(data)
            
            self.player_id = player_info['player_id']
            self.room_id = player_info['room_id']
            self.max_players = player_info['max_players']
            self.is_client = True
            
            self.game.print_with_color(f"Подключено к серверу {host_ip}:{self.port}", Fore.LIGHTGREEN_EX)
            self.game.print_with_color(f"Ваш ID: {self.player_id}, Комната: {self.room_id}", Fore.LIGHTCYAN_EX)
            
            # Start listening for messages from server
            client_thread = threading.Thread(target=self.receive_messages)
            client_thread.daemon = True
            client_thread.start()
            
            return True
        except Exception as e:
            self.game.print_with_color(f"Ошибка при подключении к серверу: {str(e)}", Fore.RED)
            return False

    def receive_messages(self):
        """Receive messages from the server"""
        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                self.process_message(message, self.player_id)
        except Exception as e:
            self.game.print_with_color(f"Ошибка при получении сообщений: {str(e)}", Fore.RED)
            self.disconnect_from_server()

    def disconnect_from_server(self):
        """Disconnect from the multiplayer server"""
        try:
            if self.client_socket:
                self.client_socket.close()
            self.is_client = False
            self.player_id = None
            self.room_id = None
            self.game.print_with_color("Отключено от сервера", Fore.YELLOW)
        except Exception as e:
            self.game.print_with_color(f"Ошибка при отключении: {str(e)}", Fore.RED)

    def send_message(self, message):
        """Send a message to the server or clients"""
        try:
            serialized_msg = pickle.dumps(message)
            if self.is_server:
                # Send to all connected clients
                for player in self.players:
                    if player['connected']:
                        player['socket'].send(serialized_msg)
            elif self.is_client:
                # Send to server
                self.client_socket.send(serialized_msg)
        except Exception as e:
            self.game.print_with_color(f"Ошибка при отправке сообщения: {str(e)}", Fore.RED)

    def process_message(self, message, sender_id):
        """Process incoming messages"""
        msg_type = message.get('type', '')
        
        if msg_type == 'chat':
            self.game.print_with_color(f"[Игрок {sender_id}]: {message['content']}", Fore.LIGHTBLUE_EX)
        elif msg_type == 'game_action':
            # Process game actions
            action = message.get('action', '')
            if action == 'start_game':
                self.game_in_progress = True
                self.game.print_with_color("Многопользовательская игра началась!", Fore.LIGHTGREEN_EX)
            elif action == 'player_move':
                self.game.print_with_color(f"Игрок {sender_id} сделал ход", Fore.LIGHTYELLOW_EX)
        elif msg_type == 'player_ready':
            self.game.print_with_color(f"Игрок {sender_id} готов", Fore.LIGHTGREEN_EX)

    def create_room(self):
        """Create a new multiplayer room"""
        if self.is_server:
            self.game.print_with_color("Вы уже являетесь хостом комнаты!", Fore.YELLOW)
            return False
        
        success = self.start_server()
        if success:
            self.game.print_with_color(f"Комната создана! ID: {self.room_id}", Fore.LIGHTGREEN_EX)
            self.game.print_with_color(f"IP-адрес: {self.host_ip}:{self.port}", Fore.LIGHTCYAN_EX)
            self.game.print_with_color(f"Пригласите других игроков присоединиться к этой комнате", Fore.LIGHTYELLOW_EX)
            return True
        else:
            self.game.print_with_color("Не удалось создать комнату", Fore.RED)
            return False

    def join_room(self, host_ip):
        """Join an existing multiplayer room"""
        if self.is_client:
            self.game.print_with_color("Вы уже подключены к комнате!", Fore.YELLOW)
            return False
        
        success = self.connect_to_server(host_ip)
        if success:
            self.game.print_with_color(f"Присоединились к комнате {self.room_id}", Fore.LIGHTGREEN_EX)
            # Send ready signal to server
            ready_msg = {'type': 'player_ready', 'player_id': self.player_id}
            self.send_message(ready_msg)
            return True
        else:
            self.game.print_with_color("Не удалось присоединиться к комнате", Fore.RED)
            return False

    def list_rooms(self):
        """List available multiplayer rooms (simulated)"""
        self.game.print_with_color("=== ДОСТУПНЫЕ КОМНАТЫ ===", Fore.LIGHTYELLOW_EX)
        # In a real implementation, this would scan the network for available rooms
        # For now, we'll simulate some rooms
        simulated_rooms = [
            {"id": "ROOM_1001", "host": "192.168.1.100", "players": 3, "max": 7},
            {"id": "ROOM_2056", "host": "192.168.1.105", "players": 5, "max": 7},
            {"id": "ROOM_3021", "host": "192.168.1.110", "players": 1, "max": 7}
        ]
        
        for room in simulated_rooms:
            status = "ПОЛНАЯ" if room['players'] >= room['max'] else f"{room['players']}/{room['max']}"
            color = Fore.LIGHTRED_EX if room['players'] >= room['max'] else Fore.LIGHTGREEN_EX
            print(f"{color}ID: {room['id']} | Хост: {room['host']} | Игроки: {status}{Fore.RESET}")
        
        print(f"\n{Fore.LIGHTCYAN_EX}Чтобы присоединиться к комнате, используйте команду 'join <IP-адрес>'{Fore.RESET}")

    def leave_room(self):
        """Leave the current multiplayer room"""
        if self.is_server:
            # Close the server
            if self.server_socket:
                self.server_socket.close()
            self.is_server = False
            self.room_id = None
            self.player_id = None
            # Reset player list
            self.players = []
            self.game.print_with_color("Сервер остановлен и комната закрыта", Fore.LIGHTYELLOW_EX)
        elif self.is_client:
            # Disconnect from server
            self.disconnect_from_server()
            self.game.print_with_color("Покинули комнату", Fore.LIGHTYELLOW_EX)
        else:
            self.game.print_with_color("Вы не подключены ни к одной комнате", Fore.YELLOW)

    def sync_game_state(self):
        """Synchronize game state with other players"""
        if not (self.is_server or self.is_client):
            return  # Not in multiplayer mode
        
        game_state = {
            'type': 'game_state',
            'player_id': self.player_id,
            'balance': self.game.balance,
            'xp': self.game.xp,
            'level': self.game.level,
            'timestamp': time.time()
        }
        
        self.send_message(game_state)

    def broadcast_game_action(self, action, data=None):
        """Broadcast a game action to all players in the room"""
        if not (self.is_server or self.is_client):
            return  # Not in multiplayer mode
        
        message = {
            'type': 'game_action',
            'action': action,
            'data': data,
            'player_id': self.player_id,
            'timestamp': time.time()
        }
        
        self.send_message(message)

    def start_multiplayer_game(self):
        """Start a multiplayer game session"""
        if not self.is_server:
            self.game.print_with_color("Только хост может начать игру!", Fore.RED)
            return False
        
        if len(self.players) < 2:
            self.game.print_with_color("Нужно как минимум 2 игрока для начала игры!", Fore.RED)
            return False
        
        # Check if all players are ready
        ready_players = [p for p in self.players if p.get('ready', False)]
        if len(ready_players) < 2:
            self.game.print_with_color(f"Не все игроки готовы! Готовы: {len(ready_players)}/{len(self.players)}", Fore.RED)
            return False
        
        self.game_in_progress = True
        self.broadcast_game_action('start_game')
        
        self.game.print_with_color("Многопользовательская игра началась!", Fore.LIGHTGREEN_EX)
        
        # Start the multiplayer game loop
        self.multiplayer_game_loop()
        
        return True

    def multiplayer_game_loop(self):
        """Main game loop for multiplayer mode"""
        self.game.print_with_color("=== МНОГОПОЛЬЗОВАТЕЛЬСКАЯ ИГРА АКТИВНА ===", Fore.LIGHTYELLOW_EX)
        
        # For now, just run for a limited time or until game ends
        # In a real implementation, this would handle the actual multiplayer game logic
        game_duration = 30  # seconds
        start_time = time.time()
        
        while self.game_in_progress and (time.time() - start_time) < game_duration:
            time.sleep(1)  # Check periodically
            
            # Synchronize state periodically
            self.sync_game_state()
        
        self.end_multiplayer_game()

    def end_multiplayer_game(self):
        """End the multiplayer game session"""
        self.game_in_progress = False
        if self.is_server:
            self.broadcast_game_action('end_game')
        
        self.game.print_with_color("Многопользовательская игра завершена!", Fore.LIGHTYELLOW_EX)

    def multiplayer_russian_roulette(self):
        """Multiplayer version of Russian Roulette"""
        if not self.is_server and not self.is_client:
            self.game.print_with_color("Сначала присоединитесь к комнате!", Fore.RED)
            return
        
        if not self.game_in_progress:
            self.game.print_with_color("Игра еще не началась!", Fore.RED)
            return
        
        self.game.print_with_color("=== МНОГОПОЛЬЗОВАТЕЛЬСКАЯ РУССКАЯ РУЛЕТКА ===", Fore.LIGHTYELLOW_EX)
        
        if self.is_server:
            # Host manages the game
            self.game.print_with_color("Вы хост игры. Управляйте ходами игроков.", Fore.LIGHTCYAN_EX)
            
            # Wait for players to make their bets
            self.game.print_with_color("Ожидание ставок игроков...", Fore.LIGHTYELLOW_EX)
            
            # In a real implementation, this would wait for all players to submit their bets
            # For now, we'll simulate
            time.sleep(5)  # Simulate waiting for players
            
            # Generate random result
            import secrets
            result = secrets.randbelow(10) + 1  # Random number 1-10
            self.game.print_with_color(f"Результат рулетки: {result}", Fore.LIGHTGREEN_EX)
            
            # Broadcast result to all players
            game_result = {
                'type': 'game_result',
                'game': 'multiplayer_russian_roulette',
                'result': result,
                'timestamp': time.time()
            }
            self.send_message(game_result)
            
            # Process results for each player
            for player in self.players:
                if player['connected']:
                    # In a real game, we'd check if this player won or lost
                    # For now, we'll just simulate
                    player_won = secrets.randbelow(2) == 0  # 50% chance
                    if player_won:
                        self.game.print_with_color(f"Игрок {player['player_id']} выиграл!", Fore.LIGHTGREEN_EX)
                    else:
                        self.game.print_with_color(f"Игрок {player['player_id']} проиграл!", Fore.LIGHTRED_EX)
        else:
            # Client waits for host to manage the game
            self.game.print_with_color("Ожидание начала игры от хоста...", Fore.LIGHTYELLOW_EX)
            
            # Place your bet when prompted by the host
            while True:
                try:
                    bet = int(input(f"Введите вашу ставку (баланс: {self.game.format_number(self.game.balance)}): $"))
                    if bet <= 0:
                        print("Ставка должна быть больше 0!")
                        continue
                    if bet > self.game.balance:
                        print(f"У вас недостаточно средств! Ваш баланс: {self.game.format_number(self.game.balance)}")
                        continue
                    break
                except ValueError:
                    print("Пожалуйста, введите корректное число!")
            
            # Send bet to host
            bet_message = {
                'type': 'player_bet',
                'player_id': self.player_id,
                'bet': bet,
                'choice': int(input("Выберите число от 1 до 10: "))
            }
            self.send_message(bet_message)
            
            # Wait for game result
            self.game.print_with_color("Ваша ставка отправлена. Ожидание результата...", Fore.LIGHTCYAN_EX)

    def multiplayer_tournament(self):
        """Multiplayer tournament mode"""
        if not self.is_server and not self.is_client:
            self.game.print_with_color("Сначала присоединитесь к комнате!", Fore.RED)
            return
        
        self.game.print_with_color("=== МНОГОПОЛЬЗОВАТЕЛЬСКИЙ ТУРНИР ===", Fore.LIGHTYELLOW_EX)
        self.game.print_with_color("Турнир будет начат хостом", Fore.LIGHTCYAN_EX)
        
        # In a real implementation, this would manage a tournament with multiple rounds
        # For now, we'll just notify players
        if self.is_server:
            self.broadcast_game_action('tournament_start')
            self.game.print_with_color("Турнир начат! Игроки будут соревноваться друг с другом.", Fore.LIGHTGREEN_EX)

    def multiplayer_menu(self):
        """Multiplayer submenu"""
        while True:
            try:
                print(f"\n{Fore.LIGHTCYAN_EX}=== МНОГОПОЛЬЗОВАТЕЛЬСКОЕ МЕНЮ ==={Fore.RESET}")
                print(f"{Fore.LIGHTYELLOW_EX}1. Создать комнату")
                print(f"{Fore.LIGHTGREEN_EX}2. Присоединиться к комнате")
                print(f"{Fore.LIGHTBLUE_EX}3. Показать доступные комнаты")
                print(f"{Fore.LIGHTMAGENTA_EX}4. Покинуть комнату")
                print(f"{Fore.LIGHTWHITE_EX}5. Начать многопользовательскую игру")
                print(f"{Fore.LIGHTRED_EX}6. Многопользовательская рулетка")
                print(f"{Fore.LIGHTCYAN_EX}7. Турнир")
                print(f"{Fore.LIGHTYELLOW_EX}8. Назад в главное меню")
                print(f"{Fore.LIGHTCYAN_EX}---------------------------")

                choice = input("Выберите опцию: ")

                if choice == "1":
                    self.create_room()
                elif choice == "2":
                    ip = input("Введите IP-адрес хоста: ")
                    self.join_room(ip)
                elif choice == "3":
                    self.list_rooms()
                elif choice == "4":
                    self.leave_room()
                elif choice == "5":
                    self.start_multiplayer_game()
                elif choice == "6":
                    self.multiplayer_russian_roulette()
                elif choice == "7":
                    self.multiplayer_tournament()
                elif choice == "8":
                    break
                else:
                    self.game.print_with_color("Неверный выбор!", Fore.RED)
            except (EOFError, KeyboardInterrupt):
                self.game.print_with_color("\nВыход из многопользовательского меню...", Fore.LIGHTRED_EX)
                break