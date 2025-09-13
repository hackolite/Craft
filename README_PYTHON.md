# Craft - Python Edition

A Minecraft-like game implemented in Python using Pyglet, converted from the original C/OpenGL implementation.

## Features

- **3D Voxel World**: Infinite terrain generation with chunks
- **Block Building**: Place and destroy blocks
- **Player Movement**: Walking, flying, and physics
- **Multiplayer Support**: Compatible with original server
- **Modern Graphics**: OpenGL rendering with textures
- **Cross-Platform**: Runs on Windows, Mac, and Linux

## Requirements

- Python 3.7+
- Pyglet 2.0+
- NumPy
- Pillow (for texture loading)

## Installation

1. Install dependencies:
```bash
pip install pyglet numpy pillow
```

2. Clone or download the repository

3. Run the game:
```bash
python3 craft.py
```

Or test the modules without a display:
```bash
python3 launcher.py test
```

## Controls

- **WASD**: Move forward, left, backward, right
- **Space**: Jump (or fly up in fly mode)
- **Tab**: Toggle flying mode
- **Mouse**: Look around
- **ESC**: Toggle mouse capture
- **F**: Toggle orthographic view
- **F11**: Toggle fullscreen
- **Left Click**: Destroy block
- **Right Click**: Place block

## Game Modules

### Core Framework
- `craft.py` - Main game application and window management
- `craft_config.py` - Game configuration and constants
- `craft_math.py` - 3D math utilities (Vector3, Matrix4)

### Game Systems
- `craft_world.py` - World generation and chunk management
- `craft_player.py` - Player movement, camera, and physics
- `craft_renderer.py` - OpenGL rendering system
- `craft_input.py` - Input handling for keyboard and mouse

### Utilities
- `launcher.py` - Test launcher and module validation

## Architecture

The Python version maintains the same core architecture as the original C implementation:

1. **Chunk-based World**: 32x32 block chunks for infinite worlds
2. **OpenGL Rendering**: Modern OpenGL with vertex buffers
3. **Client-Server Model**: Compatible with original Python server
4. **Modular Design**: Separate systems for rendering, input, physics

## Conversion Status

✅ **Completed:**
- Core framework and window management
- 3D math utilities and transformations
- Player movement and camera system
- Basic world generation and chunks
- Block rendering with textures
- Input handling and controls

🚧 **In Progress:**
- Advanced texture system and shaders
- Block placement/destruction mechanics
- Multiplayer client integration
- UI and HUD elements

📋 **Todo:**
- Audio system
- Advanced graphics effects
- Optimization and performance tuning
- Complete feature parity with C version

## Compatibility

This Python version is designed to be compatible with:
- Original game assets (textures, shaders)
- Original multiplayer server
- Original save file format

## Development

To contribute or modify the game:

1. Test modules: `python3 launcher.py test`
2. Run game: `python3 craft.py`
3. Modify individual systems in their respective modules
4. The modular architecture allows easy extension and modification

## License

Same license as the original Craft project.

## Credits

Converted from the original Craft by Michael Fogleman.
Python/Pyglet implementation maintains the spirit and functionality of the original C version.