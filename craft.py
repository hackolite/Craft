#!/usr/bin/env python3
"""
Craft - Minecraft clone in Python using Pyglet
Converted from original C/OpenGL implementation
"""

import pyglet
from pyglet.gl import *
from pyglet import clock
import math
import numpy as np
from typing import Tuple, List, Dict, Optional

# Import game modules
try:
    from craft_config import *
    from craft_math import Matrix4, Vector3
    from craft_world import World, Chunk, Block
    from craft_renderer import Renderer
    from craft_player import Player
    from craft_input import InputHandler
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all craft_*.py files are in the same directory")
    exit(1)

class CraftGame(pyglet.window.Window):
    def __init__(self):
        # Initialize key bindings first
        init_key_bindings()
        
        super().__init__(
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            caption="Craft - Python Edition",
            resizable=True,
            vsync=VSYNC
        )
        
        # Initialize OpenGL settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glDepthFunc(GL_LESS)
        
        # Game state
        self.running = True
        self.dt = 0.0
        self.timer = 0.0
        
        # Initialize game components
        self.world = World()
        self.player = Player()
        self.renderer = Renderer()
        self.input_handler = InputHandler(self)
        
        # Schedule update loop
        clock.schedule_interval(self.update, 1.0/60.0)  # 60 FPS
        
        print("Craft game initialized")
    
    def update(self, dt):
        """Update game state"""
        self.dt = dt
        self.timer += dt
        
        # Update player
        self.player.update(dt, self.input_handler, self.world)
        
        # Update world
        self.world.update(self.player.position)
    
    def on_draw(self):
        """Render the game"""
        self.clear()
        
        # Set up 3D projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspect = self.width / self.height
        fov = 65.0
        gluPerspective(fov, aspect, 0.1, 500.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Apply camera transformation
        self.player.apply_camera_transform()
        
        # Render world
        self.renderer.render_world(self.world, self.player, self.timer)
        
        # Render UI (2D overlay)
        self.renderer.render_ui(self)
    
    def on_resize(self, width, height):
        """Handle window resize"""
        glViewport(0, 0, width, height)
        return True
    
    def on_key_press(self, symbol, modifiers):
        """Handle key press events"""
        self.input_handler.on_key_press(symbol, modifiers)
    
    def on_key_release(self, symbol, modifiers):
        """Handle key release events"""
        self.input_handler.on_key_release(symbol, modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse movement"""
        self.input_handler.on_mouse_motion(x, y, dx, dy)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button press"""
        self.input_handler.on_mouse_press(x, y, button, modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse button release"""
        self.input_handler.on_mouse_release(x, y, button, modifiers)
    
    def on_close(self):
        """Handle window close"""
        self.running = False
        self.close()

def main():
    """Main entry point"""
    print("Starting Craft game...")
    
    # Create and run the game
    game = CraftGame()
    pyglet.app.run()

if __name__ == "__main__":
    main()