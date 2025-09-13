"""
World generation and chunk management
"""

import math
import random
from typing import Dict, Tuple, Set, Optional
from craft_config import *
from craft_math import Vector3, chunked

class Block:
    """Represents a single block in the world"""
    
    def __init__(self, block_type=EMPTY, x=0, y=0, z=0):
        self.type = block_type
        self.x = x
        self.y = y
        self.z = z
    
    def is_empty(self):
        return self.type == EMPTY
    
    def is_transparent(self):
        return self.type in TRANSPARENT_BLOCKS
    
    def is_plant(self):
        return self.type in PLANT_BLOCKS
    
    def is_solid(self):
        return not self.is_empty() and not self.is_transparent()

class Chunk:
    """Represents a 32x32 chunk of blocks"""
    
    def __init__(self, p, q):
        self.p = p  # Chunk X coordinate
        self.q = q  # Chunk Z coordinate
        self.blocks = {}  # Dict[(x,y,z)] = Block
        self.generated = False
        self.dirty = True  # Needs re-rendering
        self.faces = 0  # Number of visible faces
        
        # Bounding box for this chunk
        self.min_x = p * CHUNK_SIZE
        self.max_x = (p + 1) * CHUNK_SIZE - 1
        self.min_z = q * CHUNK_SIZE
        self.max_z = (q + 1) * CHUNK_SIZE - 1
        self.min_y = 0
        self.max_y = 255
    
    def get_block(self, x, y, z):
        """Get block at world coordinates"""
        return self.blocks.get((x, y, z), Block(EMPTY, x, y, z))
    
    def set_block(self, x, y, z, block_type):
        """Set block at world coordinates"""
        if block_type == EMPTY:
            if (x, y, z) in self.blocks:
                del self.blocks[(x, y, z)]
        else:
            self.blocks[(x, y, z)] = Block(block_type, x, y, z)
        self.dirty = True
    
    def contains_point(self, x, z):
        """Check if world coordinates are in this chunk"""
        return (self.min_x <= x <= self.max_x and 
                self.min_z <= z <= self.max_z)
    
    def get_local_coords(self, x, y, z):
        """Convert world coords to local chunk coords"""
        return x - self.min_x, y, z - self.min_z
    
    def get_world_coords(self, local_x, local_y, local_z):
        """Convert local chunk coords to world coords"""
        return self.min_x + local_x, local_y, self.min_z + local_z

class World:
    """Manages the game world and chunks"""
    
    def __init__(self, seed=None):
        self.seed = seed or random.randint(0, 2**31)
        random.seed(self.seed)
        
        self.chunks = {}  # Dict[(p,q)] = Chunk
        self.loaded_chunks = set()  # Set of (p,q) coordinates
        
        # Noise for terrain generation (simplified)
        self.terrain_scale = 0.02
        self.terrain_height = 16
        self.terrain_base = 8
        
        print(f"World initialized with seed: {self.seed}")
    
    def update(self, player_position):
        """Update world based on player position"""
        player_chunk_p = chunked(player_position.x)
        player_chunk_q = chunked(player_position.z)
        
        # Load chunks around player
        self._load_chunks_around(player_chunk_p, player_chunk_q)
        
        # Unload distant chunks
        self._unload_distant_chunks(player_chunk_p, player_chunk_q)
    
    def _load_chunks_around(self, center_p, center_q):
        """Load chunks around the center position"""
        for dp in range(-CREATE_CHUNK_RADIUS, CREATE_CHUNK_RADIUS + 1):
            for dq in range(-CREATE_CHUNK_RADIUS, CREATE_CHUNK_RADIUS + 1):
                p = center_p + dp
                q = center_q + dq
                
                if (p, q) not in self.chunks:
                    self._generate_chunk(p, q)
    
    def _unload_distant_chunks(self, center_p, center_q):
        """Unload chunks that are too far from player"""
        to_remove = []
        
        for (p, q) in self.chunks:
            distance = max(abs(p - center_p), abs(q - center_q))
            if distance > DELETE_CHUNK_RADIUS:
                to_remove.append((p, q))
        
        for chunk_key in to_remove:
            del self.chunks[chunk_key]
            self.loaded_chunks.discard(chunk_key)
    
    def _generate_chunk(self, p, q):
        """Generate a new chunk with terrain"""
        chunk = Chunk(p, q)
        
        # Generate terrain for this chunk
        for x in range(chunk.min_x, chunk.max_x + 1):
            for z in range(chunk.min_z, chunk.max_z + 1):
                height = self._get_terrain_height(x, z)
                
                # Place blocks based on height
                for y in range(0, min(height + 1, 256)):
                    if y == 0:
                        # Bedrock layer
                        block_type = STONE
                    elif y < height - 3:
                        # Deep underground
                        block_type = STONE
                    elif y < height:
                        # Underground
                        block_type = DIRT
                    else:
                        # Surface
                        block_type = GRASS
                    
                    chunk.set_block(x, y, z, block_type)
                
                # Add plants on grass
                if height > 0 and random.random() < 0.1:
                    plant_type = random.choice([TALL_GRASS, YELLOW_FLOWER, RED_FLOWER])
                    chunk.set_block(x, height + 1, z, plant_type)
                
                # Add trees occasionally
                if height > 5 and random.random() < 0.02:
                    self._generate_tree(chunk, x, height + 1, z)
        
        chunk.generated = True
        self.chunks[(p, q)] = chunk
        self.loaded_chunks.add((p, q))
    
    def _get_terrain_height(self, x, z):
        """Get terrain height at world coordinates using noise"""
        # Simple noise-based terrain generation
        noise_value = (
            math.sin(x * self.terrain_scale) * 
            math.cos(z * self.terrain_scale) +
            math.sin(x * self.terrain_scale * 2) * 
            math.cos(z * self.terrain_scale * 2) * 0.5
        )
        
        height = int(self.terrain_base + noise_value * self.terrain_height)
        return max(1, min(height, 64))  # Clamp height
    
    def _generate_tree(self, chunk, x, y, z):
        """Generate a simple tree at the given coordinates"""
        tree_height = random.randint(4, 7)
        
        # Tree trunk
        for i in range(tree_height):
            chunk.set_block(x, y + i, z, WOOD)
        
        # Tree leaves (simple sphere)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                for dz in range(-2, 3):
                    if dx*dx + dy*dy + dz*dz <= 4:  # Sphere radius
                        leaf_x = x + dx
                        leaf_y = y + tree_height + dy
                        leaf_z = z + dz
                        
                        if leaf_y > y + tree_height - 2:  # Only upper part
                            chunk.set_block(leaf_x, leaf_y, leaf_z, LEAVES)
    
    def get_chunk(self, p, q):
        """Get chunk at chunk coordinates"""
        return self.chunks.get((p, q))
    
    def get_chunk_for_position(self, x, z):
        """Get chunk containing the given world coordinates"""
        p = chunked(x)
        q = chunked(z)
        return self.get_chunk(p, q)
    
    def get_block(self, x, y, z):
        """Get block at world coordinates"""
        chunk = self.get_chunk_for_position(x, z)
        if chunk:
            return chunk.get_block(x, y, z)
        return Block(EMPTY, x, y, z)
    
    def set_block(self, x, y, z, block_type):
        """Set block at world coordinates"""
        chunk = self.get_chunk_for_position(x, z)
        if chunk:
            chunk.set_block(x, y, z, block_type)
    
    def get_visible_chunks(self, player_position):
        """Get chunks that should be rendered"""
        player_p = chunked(player_position.x)
        player_q = chunked(player_position.z)
        
        visible = []
        for (p, q), chunk in self.chunks.items():
            distance = max(abs(p - player_p), abs(q - player_q))
            if distance <= RENDER_CHUNK_RADIUS:
                visible.append(chunk)
        
        return visible