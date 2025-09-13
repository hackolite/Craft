# Craft

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#installation)
[![Language](https://img.shields.io/badge/language-C%20%7C%20Python-green)](#implementations)

A Minecraft-like voxel game with both **C/OpenGL** and **Python/Pyglet** implementations. Features infinite terrain generation, multiplayer support, and modern graphics rendering.

🌐 **Website**: http://www.michaelfogleman.com/craft/

![Screenshot](https://i.imgur.com/SH7wcas.png)

## 🚀 Quick Start

**Choose your implementation:**

| **C/OpenGL Version** (Original) | **Python Version** (Modern Port) |
|---|---|
| ✅ Full-featured and optimized | ✅ Easy to modify and extend |
| ✅ High performance | ✅ Cross-platform Python |
| ✅ Production ready | 🚧 In active development |
| [📖 Full C Documentation](#c-implementation) | [📖 Python Documentation](README_PYTHON.md) |

### 🐍 Python Version (Recommended for Development)

```bash
# Install dependencies
pip install pyglet numpy pillow

# Run the game
python3 craft.py
```

### ⚡ C Version (Recommended for Performance)

```bash
# Install dependencies (see detailed instructions below)
# Then build and run:
git clone https://github.com/hackolite/Craft.git
cd Craft
cmake .
make
./craft
```

## 📋 Table of Contents

- [Features](#-features)
- [Implementations](#-implementations)
- [Installation](#-installation)
  - [C Implementation](#c-implementation)
  - [Python Implementation](#python-implementation)
- [Multiplayer](#-multiplayer)
- [Controls](#-controls)
- [Chat Commands](#-chat-commands)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🌍 World Generation
- **Infinite terrain** using Perlin/Simplex noise algorithms
- **Chunk-based loading** (32x32 blocks) for optimal performance
- **10+ block types** with easy extensibility
- **Natural structures**: grass, flowers, trees, and landscapes

### 🎮 Gameplay
- **Building & destruction** with left/right click mechanics
- **Flying and walking modes** with realistic physics
- **Day/night cycles** with dynamic lighting
- **Transparent blocks** (glass) and natural plants
- **World persistence** via SQLite3 database

### 🌐 Multiplayer
- **Client-server architecture** with Python server
- **Real-time synchronization** of player actions
- **Chat system** with commands
- **Player observation** modes (main view + picture-in-picture)

### 🎨 Graphics
- **Modern OpenGL** with vertex/fragment shaders
- **Ambient occlusion** for realistic lighting
- **Textured sky dome** with time-based transitions
- **Frustum culling** and optimization for smooth performance

## 🛠️ Implementations

This repository contains **two complete implementations** of the Craft game:

### C Implementation (Original)
- **Language**: C99 with OpenGL
- **Performance**: Highly optimized, production-ready
- **Features**: Complete feature set, mature codebase
- **Best for**: Playing the game, high-performance needs
- **Location**: `src/` directory, built with CMake

### Python Implementation (Modern Port)
- **Language**: Python 3.7+ with Pyglet
- **Performance**: Good performance, easier to modify
- **Features**: Core features implemented, actively developed
- **Best for**: Learning, modding, experimentation
- **Location**: `craft*.py` files
- **Documentation**: [README_PYTHON.md](README_PYTHON.md)

Both implementations are compatible with the same:
- 🗺️ World save format
- 🌐 Multiplayer server
- 🎨 Texture assets
- 🎮 Game mechanics

## 💻 Installation

### C Implementation

**Dependencies needed:**
- CMake 2.8+
- OpenGL development libraries
- CURL development libraries

#### 🍎 macOS

```bash
# Using Homebrew (recommended)
brew install cmake

# Or download from: http://www.cmake.org/cmake/resources/software.html
```

#### 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install cmake libglew-dev xorg-dev libcurl4-openssl-dev
sudo apt-get build-dep glfw
```

#### 🪟 Windows

1. **Install dependencies:**
   - Download and install [CMake](http://www.cmake.org/cmake/resources/software.html)
   - Download and install [MinGW](http://www.mingw.org/)
   - Add `C:\MinGW\bin` to your `PATH`
   - Download [cURL](http://curl.haxx.se/download.html) so that CURL/lib and CURL/include are in your Program Files

2. **Build with MinGW:**
   ```bash
   cmake -G "MinGW Makefiles"
   mingw32-make
   ```

#### 🔨 Build and Run (All Platforms)

```bash
git clone https://github.com/hackolite/Craft.git
cd Craft
cmake .
make
./craft
```

### Python Implementation

**Requirements:**
- Python 3.7+
- Pyglet 2.0+
- NumPy
- Pillow

#### 📦 Installation

```bash
# Install Python dependencies
pip install pyglet numpy pillow

# Clone repository (if not already done)
git clone https://github.com/hackolite/Craft.git
cd Craft

# Run Python version
python3 craft.py

# Or test modules
python3 launcher.py test
```

> 📚 **Detailed Python Documentation**: See [README_PYTHON.md](README_PYTHON.md) for complete Python implementation details.

## 🌐 Multiplayer

> **Note**: The original craft.michaelfogleman.com server has been taken down. You'll need to run your own server for multiplayer.

### 🖥️ Server Setup

**Compile the world generation library:**
```bash
gcc -std=c99 -O3 -fPIC -shared -o world -I src -I deps/noise deps/noise/noise.c src/world.c
```

**Run the Python server:**
```bash
python server.py [HOST [PORT]]
```

### 🎮 Client Connection

**Command line:**
```bash
./craft [HOST [PORT]]
```

**In-game command:**
```
/online [HOST [PORT]]
```

## 🎮 Controls

### 🚶 Movement
| Key | Action |
|-----|--------|
| **WASD** | Move forward, left, backward, right |
| **Space** | Jump |
| **Tab** | Toggle between walking and flying |
| **ZXCVBN** | Move in exact XYZ directions |

### 🔨 Building
| Key | Action |
|-----|--------|
| **Left Click** | Destroy block |
| **Right Click** | Create block (or **Cmd + Left Click** on Mac) |
| **Ctrl + Right Click** | Toggle block as light source |
| **1-9** | Select block type to create |
| **E** | Cycle through block types |

### 📷 Camera & View
| Key | Action |
|-----|--------|
| **Mouse** | Look around |
| **Left Shift** | Zoom |
| **F** | Orthographic mode |
| **O** | Observe players in main view |
| **P** | Observe players in picture-in-picture |
| **Arrow Keys** | Emulate mouse movement |
| **Enter** | Emulate mouse click |

### 💬 Communication
| Key | Action |
|-----|--------|
| **T** | Type into chat |
| **/** | Enter command |
| **`** | Write text on blocks (signs) |

## 💬 Chat Commands

| Command | Description |
|---------|-------------|
| `/goto [NAME]` | Teleport to another user (random if NAME unspecified) |
| `/list` | Display connected users |
| `/login NAME` | Switch to registered username (case-sensitive) |
| `/logout` | Become guest user |
| `/offline [FILE]` | Switch to offline mode (default save: "craft") |
| `/online HOST [PORT]` | Connect to specified server |
| `/pq P Q` | Teleport to specified chunk coordinates |
| `/spawn` | Return to spawn point |

## 📸 Screenshots

![Main Screenshot](https://i.imgur.com/foYz3aN.png)

## 🔧 Technical Implementation

### 🌍 World Generation
- **Algorithm**: Simplex noise for deterministic, position-based terrain
- **Architecture**: 32x32 block chunks with XZ plane organization  
- **Persistence**: SQLite3 database stores only player modifications (delta)
- **Optimization**: Only exposed block faces are rendered

### 🎨 Rendering Engine
- **API**: Modern OpenGL with vertex/fragment shaders
- **Performance**: Frustum culling, VBO optimization
- **Effects**: Ambient occlusion, transparency, sky dome texturing
- **Text**: Bitmap atlas rendering on 2D rectangles

### 🌐 Networking Protocol
- **Transport**: Plain TCP sockets with ASCII line-based protocol
- **Synchronization**: Real-time player positions, block updates, chat
- **Caching**: Client-side chunk caching with delta updates
- **Performance**: Background SQLite writes, transaction batching

### 🗃️ Dependencies

**C Implementation:**
- **GLEW** - OpenGL extension management
- **GLFW** - Cross-platform window management  
- **CURL** - HTTPS/SSL for authentication
- **lodepng** - PNG texture loading
- **sqlite3** - World persistence
- **tinycthread** - Cross-platform threading

**Python Implementation:**
- **Pyglet** - OpenGL graphics and windowing
- **NumPy** - Mathematical operations
- **Pillow** - Image processing

## 🤝 Contributing

### 🔧 Development Setup

1. **Fork the repository**
2. **Clone your fork**
3. **Test both implementations:**
   ```bash
   # Test C build
   cmake . && make
   
   # Test Python modules  
   python3 launcher.py test
   ```

### 📝 Guidelines

- 🎯 **Focus on minimal changes** for maximum compatibility
- 🧪 **Test both C and Python** implementations when possible
- 📚 **Update documentation** for any new features
- 🔄 **Maintain compatibility** between implementations

### 🐛 Issues & Features

- 🐛 **Bug reports**: Please include OS, implementation (C/Python), and steps to reproduce
- ✨ **Feature requests**: Consider implementation in both C and Python versions
- 🤝 **Pull requests**: Test thoroughly and update relevant documentation

## 📄 License

Licensed under the **MIT License** - see [LICENSE.md](LICENSE.md) for details.

```
Copyright (C) 2013 Michael Fogleman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 🙏 Credits

**Original Author**: [Michael Fogleman](http://www.michaelfogleman.com)  
**Python Port**: Community contributions  
**Inspiration**: Minecraft by Mojang Studios

---

### 📚 Additional Resources

- 🌐 **Project Website**: http://www.michaelfogleman.com/craft/
- 🐍 **Python Documentation**: [README_PYTHON.md](README_PYTHON.md)
- 🔧 **Technical Blog Post**: [Original implementation details](http://0fps.wordpress.com/2013/07/03/ambient-occlusion-for-minecraft-like-worlds/)

**⭐ Star this repository if you found it useful!**
