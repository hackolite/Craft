#!/usr/bin/env python3
"""
Test launcher for Craft - can run without display for testing
"""

import os
import sys

def test_modules():
    """Test that all modules can be imported"""
    print("Testing Craft modules...")
    
    try:
        print("  Testing config module...")
        from craft_config import WINDOW_WIDTH, WINDOW_HEIGHT
        print(f"    Window size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        print("  Testing math module...")
        from craft_math import Vector3, Matrix4
        v = Vector3(1, 2, 3)
        print(f"    Vector test: {v}")
        
        print("  Testing world module...")
        from craft_world import World, Chunk, Block
        world = World(seed=12345)
        print(f"    World created with seed: {world.seed}")
        
        print("All modules loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading modules: {e}")
        return False

def launch_game():
    """Launch the full game with display"""
    print("Launching Craft game...")
    
    try:
        # Set up display (if available)
        os.environ['DISPLAY'] = os.environ.get('DISPLAY', ':0')
        
        # Import and run the game
        from craft import main
        main()
        
    except Exception as e:
        print(f"Error launching game: {e}")
        print("This might be because no display is available.")
        print("Try running on a system with a graphical display.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test mode - just check modules
        success = test_modules()
        sys.exit(0 if success else 1)
    else:
        # Full game mode
        if test_modules():
            launch_game()
        else:
            print("Module tests failed. Cannot launch game.")
            sys.exit(1)

if __name__ == "__main__":
    main()