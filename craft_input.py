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
        # TODO: Implement block destruction logic
        pass
    
    def _handle_block_place(self):
        """Handle block placement"""
        # TODO: Implement block placement logic
        pass
    
    def toggle_mouse_capture(self):
        """Toggle mouse capture state"""
        self.mouse_captured = not self.mouse_captured
        self.game.set_exclusive_mouse(self.mouse_captured)
    
    def is_key_pressed(self, key_symbol):
        """Check if a key is currently pressed"""
        return self.keys_pressed.get(key_symbol, False)