"""
Input handler for keyboard and mouse events
"""

from pyglet.window import mouse, key
from craft_config import *

class InputHandler:
    """Handles input events and maintains input state"""
    
    def __init__(self, game):
        self.game = game
        self.keys_pressed = {}
        self.mouse_captured = True
        self.mouse_sensitivity = 0.1
        
        # Capture mouse cursor
        if self.mouse_captured:
            self.game.set_exclusive_mouse(True)
    
    def on_key_press(self, symbol, modifiers):
        """Handle key press events"""
        self.keys_pressed[symbol] = True
        
        # Handle special keys
        if symbol == CRAFT_KEY_FLY:
            self.game.player.toggle_flying()
        elif symbol == CRAFT_KEY_ORTHO:
            self.game.player.toggle_ortho()
        elif symbol == key.ESCAPE:
            # Toggle mouse capture
            self.toggle_mouse_capture()
        elif symbol == key.F11:
            # Toggle fullscreen
            self.game.set_fullscreen(not self.game.fullscreen)
        elif symbol == key.M and (modifiers & key.MOD_CTRL):
            # Ctrl+M: Toggle multiplayer
            if self.game.offline_mode:
                self.game.connect_to_server()
            else:
                self.game.go_offline()
    
    def on_key_release(self, symbol, modifiers):
        """Handle key release events"""
        if symbol in self.keys_pressed:
            self.keys_pressed[symbol] = False
    
    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse movement"""
        if self.mouse_captured:
            self.game.player.handle_mouse_motion(dx, dy)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button press"""
        if not self.mouse_captured:
            self.toggle_mouse_capture()
            return
        
        if button == mouse.LEFT:
            # Destroy block
            self._handle_block_destroy()
        elif button == mouse.RIGHT:
            # Place block
            self._handle_block_place()
    
    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse button release"""
        pass
    
    def _handle_block_destroy(self):
        """Handle block destruction"""
        # Cast ray from player position to find target block
        hit_result = self._cast_ray()
        if hit_result:
            x, y, z = hit_result
            self.game.world.set_block(x, y, z, EMPTY)
            print(f"Destroyed block at {x}, {y}, {z}")
    
    def _handle_block_place(self):
        """Handle block placement"""
        # Cast ray to find placement position
        hit_result = self._cast_ray(for_placement=True)
        if hit_result:
            x, y, z = hit_result
            # Place grass block by default
            self.game.world.set_block(x, y, z, GRASS)
            print(f"Placed block at {x}, {y}, {z}")
    
    def _cast_ray(self, for_placement=False):
        """Cast ray from player to find block intersection"""
        player = self.game.player
        forward = player.get_forward_vector()
        
        # Ray casting parameters
        max_distance = 10.0
        step_size = 0.1
        
        # Cast ray
        for i in range(int(max_distance / step_size)):
            distance = i * step_size
            pos = player.position + forward * distance
            
            x, y, z = int(pos.x), int(pos.y), int(pos.z)
            block = self.game.world.get_block(x, y, z)
            
            if not block.is_empty():
                if for_placement:
                    # Return the position just before the hit block
                    prev_distance = max(0, distance - step_size)
                    prev_pos = player.position + forward * prev_distance
                    return int(prev_pos.x), int(prev_pos.y), int(prev_pos.z)
                else:
                    # Return the hit block position
                    return x, y, z
        
        return None
    
    def toggle_mouse_capture(self):
        """Toggle mouse capture state"""
        self.mouse_captured = not self.mouse_captured
        self.game.set_exclusive_mouse(self.mouse_captured)
    
    def is_key_pressed(self, key_symbol):
        """Check if a key is currently pressed"""
        return self.keys_pressed.get(key_symbol, False)