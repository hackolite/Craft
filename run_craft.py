#!/usr/bin/env python3
"""
Craft Game Launcher
Simplified launcher to start the game with proper error handling
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    try:
        import pyglet
    except ImportError:
        missing.append("pyglet")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import PIL
    except ImportError:
        missing.append("pillow")
    
    return missing

def main():
    print("🎮 Craft Game Launcher")
    print("======================")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print(f"📦 Install with: pip install {' '.join(missing)}")
        return 1
    
    print("✅ All dependencies found")
    
    # Check if we're in the right directory
    if not os.path.exists("craft.py"):
        print("❌ craft.py not found. Please run this from the Craft directory.")
        return 1
    
    print("🚀 Starting Craft game...")
    print()
    print("Controls:")
    print("  WASD: Move")
    print("  Mouse: Look around") 
    print("  Space: Jump")
    print("  Tab: Toggle flying")
    print("  ESC: Toggle mouse capture")
    print("  F11: Toggle fullscreen")
    print()
    
    try:
        # Import and run the game
        from craft import main as craft_main
        craft_main()
    except ImportError as e:
        print(f"❌ Failed to import game modules: {e}")
        return 1
    except Exception as e:
        print(f"❌ Game error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())