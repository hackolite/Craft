"""
Compatibility layer for existing server.py
Uses our new craft_world module instead of the C library
"""

from craft_world import World as CraftWorld
from collections import OrderedDict

# Compatibility wrapper to make our World work with the existing server
class World(object):
    def __init__(self, seed=None, cache_size=64):
        self.craft_world = CraftWorld(seed)
        self.cache = OrderedDict()
        self.cache_size = cache_size
    
    def create_chunk(self, p, q):
        """Create chunk compatible with server expectations"""
        # Use our world generation
        chunk = self.craft_world.get_chunk(p, q)
        if not chunk:
            # Force generation if not exists
            self.craft_world._generate_chunk(p, q)
            chunk = self.craft_world.get_chunk(p, q)
        
        # Convert to format expected by server
        result = {}
        if chunk and chunk.blocks:
            for (x, y, z), block in chunk.blocks.items():
                result[(x, y, z)] = block.type
        
        return result
    
    def get_chunk(self, p, q):
        """Get chunk with caching"""
        try:
            chunk = self.cache.pop((p, q))
        except KeyError:
            chunk = self.create_chunk(p, q)
        self.cache[(p, q)] = chunk
        if len(self.cache) > self.cache_size:
            self.cache.popitem(False)
        return chunk

# Dummy noise functions for compatibility
def dll_seed(x):
    pass

def dll_simplex2(x, y, octaves=1, persistence=0.5, lacunarity=2.0):
    import math
    return math.sin(x * 0.1) * math.cos(y * 0.1)

def dll_simplex3(x, y, z, octaves=1, persistence=0.5, lacunarity=2.0):
    import math
    return math.sin(x * 0.1) * math.cos(y * 0.1) * math.sin(z * 0.1)