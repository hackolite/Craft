"""
Network client for multiplayer support
Compatible with the existing server.py
"""

import socket
import threading
import time
from craft_config import *

class NetworkClient:
    """Handles network communication with the server"""
    
    def __init__(self, game):
        self.game = game
        self.socket = None
        self.connected = False
        self.receive_thread = None
        self.last_position_send = 0
        
        # Server info
        self.host = None
        self.port = None
        self.player_id = None
    
    def connect(self, host='127.0.0.1', port=4080):
        """Connect to the server"""
        try:
            self.host = host
            self.port = port
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            # Send version
            self.send_command('V', '1')
            
            print(f"Connected to server at {host}:{port}")
            return True
            
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            self.connected = False
            if self.socket:
                self.socket.close()
            print("Disconnected from server")
    
    def send_command(self, command, *args):
        """Send a command to the server"""
        if not self.connected:
            return
        
        message = f"{command},{','.join(map(str, args))}\n"
        try:
            self.socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")
            self.disconnect()
    
    def send_position(self):
        """Send player position to server"""
        if not self.connected:
            return
        
        now = time.time()
        if now - self.last_position_send < 0.1:  # Rate limit
            return
        
        player = self.game.player
        self.send_command(
            'P',
            player.position.x,
            player.position.y,
            player.position.z,
            player.rotation_x,
            player.rotation_y
        )
        self.last_position_send = now
    
    def send_block_update(self, x, y, z, block_type):
        """Send block update to server"""
        self.send_command('B', x, y, z, block_type)
    
    def request_chunk(self, p, q):
        """Request a chunk from the server"""
        self.send_command('C', p, q, 0)  # 0 = no cache key
    
    def _receive_loop(self):
        """Receive messages from server"""
        buffer = ""
        
        while self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                
                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line:
                        self._handle_message(line)
                        
            except Exception as e:
                if self.connected:  # Only print if we didn't intentionally disconnect
                    print(f"Error receiving data: {e}")
                break
        
        self.connected = False
    
    def _handle_message(self, message):
        """Handle a message from the server"""
        try:
            parts = message.split(',')
            command = parts[0]
            args = parts[1:]
            
            if command == 'U':  # YOU (your player ID and position)
                self.player_id = int(args[0])
                x, y, z, rx, ry = map(float, args[1:6])
                # Update player position if needed
                
            elif command == 'B':  # BLOCK
                p, q, x, y, z, w = map(int, args)
                # Update block in world
                self.game.world.set_block(x, y, z, w)
                
            elif command == 'P':  # POSITION (other player)
                player_id = int(args[0])
                x, y, z, rx, ry = map(float, args[1:6])
                # Update other player position
                
            elif command == 'T':  # TALK (chat message)
                text = ','.join(args)
                print(f"Chat: {text}")
                
            elif command == 'E':  # TIME (day/night cycle)
                timestamp, day_length = map(float, args)
                # Update time of day
                
            # Add more message handlers as needed
            
        except Exception as e:
            print(f"Error handling message '{message}': {e}")

class MultiplayerGame:
    """Integration class for multiplayer features"""
    
    def __init__(self, game):
        self.game = game
        self.client = NetworkClient(game)
        self.server_mode = False
    
    def connect_to_server(self, host='127.0.0.1', port=4080):
        """Connect to multiplayer server"""
        return self.client.connect(host, port)
    
    def disconnect_from_server(self):
        """Disconnect from server"""
        self.client.disconnect()
    
    def update(self):
        """Update multiplayer state"""
        if self.client.connected:
            # Send position updates
            self.client.send_position()
    
    def on_block_changed(self, x, y, z, block_type):
        """Called when a block is changed locally"""
        if self.client.connected:
            self.client.send_block_update(x, y, z, block_type)
    
    def on_chunk_loaded(self, p, q):
        """Called when a chunk needs to be loaded"""
        if self.client.connected:
            self.client.request_chunk(p, q)