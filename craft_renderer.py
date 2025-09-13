"""
Rendering system using Pyglet and OpenGL
"""

import pyglet
from pyglet.gl import *
import numpy as np
from craft_config import *
from craft_math import Vector3, Matrix4

class Renderer:
    """Handles all rendering operations"""
    
    def __init__(self):
        # Load textures
        self.textures = {}
        self._load_textures()
        
        # Vertex buffer for chunks
        self.chunk_buffers = {}
        
        # UI elements
        self.crosshair_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        
        # Create crosshair
        self._create_crosshair()
        
        print("Renderer initialized")
    
    def _load_textures(self):
        """Load game textures"""
        try:
            # Load main texture atlas
            self.textures['blocks'] = pyglet.image.load('textures/texture.png').get_texture()
            self.textures['sky'] = pyglet.image.load('textures/sky.png').get_texture()
            self.textures['font'] = pyglet.image.load('textures/font.png').get_texture()
            print("Textures loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load textures: {e}")
            # Create placeholder textures
            self._create_placeholder_textures()
    
    def _create_placeholder_textures(self):
        """Create simple placeholder textures"""
        # Create a simple colored texture atlas
        import pyglet.image
        
        # Create a 256x256 texture with a grid pattern
        width, height = 256, 256
        data = []
        
        for y in range(height):
            for x in range(width):
                # Create a checkerboard pattern with different colors for different blocks
                block_x = x // 16
                block_y = y // 16
                block_id = block_y * 16 + block_x
                
                # Generate color based on block ID
                r = (block_id * 37) % 256
                g = (block_id * 73) % 256
                b = (block_id * 131) % 256
                
                # Add checkerboard pattern within each block
                if ((x % 16) < 8) ^ ((y % 16) < 8):
                    r = min(255, r + 40)
                    g = min(255, g + 40)
                    b = min(255, b + 40)
                
                data.extend([r, g, b, 255])
        
        # Convert to Pyglet texture
        image_data = pyglet.image.ImageData(
            width, height, 'RGBA', bytes(data)
        )
        self.textures['blocks'] = image_data.get_texture()
        
        # Sky texture (simple blue gradient)
        sky_data = []
        for y in range(256):
            for x in range(256):
                # Gradient from light blue to dark blue
                blue_intensity = int(135 + (256 - y) * 120 / 256)
                blue_intensity = min(255, max(0, blue_intensity))
                sky_data.extend([135, 206, blue_intensity, 255])
        
        sky_image = pyglet.image.ImageData(
            256, 256, 'RGBA', bytes(sky_data)
        )
        self.textures['sky'] = sky_image.get_texture()
        
        print("Created placeholder textures with block atlas and sky gradient")
    
    def _create_crosshair(self):
        """Create crosshair for UI"""
        if SHOW_CROSSHAIRS:
            # Simple crosshair lines
            self.crosshair_lines = self.crosshair_batch.add(
                4, GL_LINES, None,
                ('v2f', [0, -10, 0, 10, -10, 0, 10, 0]),  # Vertical and horizontal lines
                ('c3B', [255, 255, 255] * 4)  # White color
            )
    
    def render_world(self, world, player, timer):
        """Render the 3D world"""
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        
        # Bind block texture
        if 'blocks' in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['blocks'].id)
        
        # Get visible chunks
        visible_chunks = world.get_visible_chunks(player.position)
        
        # Render each chunk
        for chunk in visible_chunks:
            self._render_chunk(chunk)
        
        glDisable(GL_TEXTURE_2D)
    
    def _render_chunk(self, chunk):
        """Render a single chunk"""
        if not chunk.generated:
            return
        
        # Check if we need to rebuild the chunk mesh
        if chunk.dirty:
            self._build_chunk_mesh(chunk)
            chunk.dirty = False
        
        # Render the chunk's vertex buffer
        chunk_id = (chunk.p, chunk.q)
        if chunk_id in self.chunk_buffers:
            buffer_data = self.chunk_buffers[chunk_id]
            if buffer_data:
                self._render_vertex_buffer(buffer_data)
    
    def _build_chunk_mesh(self, chunk):
        """Build vertex buffer for a chunk"""
        vertices = []
        
        # Iterate through all blocks in chunk
        for (x, y, z), block in chunk.blocks.items():
            if block.is_empty():
                continue
            
            # Generate faces for this block
            faces = self._get_visible_faces(chunk, x, y, z, block)
            
            for face in faces:
                vertices.extend(self._get_face_vertices(x, y, z, face, block.type))
        
        # Store vertex buffer
        chunk_id = (chunk.p, chunk.q)
        if vertices:
            self.chunk_buffers[chunk_id] = vertices
        else:
            self.chunk_buffers[chunk_id] = None
    
    def _get_visible_faces(self, chunk, x, y, z, block):
        """Determine which faces of a block should be rendered"""
        faces = []
        
        # Check each face direction
        directions = [
            ('front',  0,  0,  1),
            ('back',   0,  0, -1),
            ('right',  1,  0,  0),
            ('left',  -1,  0,  0),
            ('top',    0,  1,  0),
            ('bottom', 0, -1,  0),
        ]
        
        for face_name, dx, dy, dz in directions:
            neighbor_x, neighbor_y, neighbor_z = x + dx, y + dy, z + dz
            neighbor = chunk.get_block(neighbor_x, neighbor_y, neighbor_z)
            
            # Render face if neighbor is empty or transparent
            if neighbor.is_empty() or (neighbor.is_transparent() and neighbor.type != block.type):
                faces.append(face_name)
        
        return faces
    
    def _get_face_vertices(self, x, y, z, face, block_type):
        """Get vertices for a specific face of a block"""
        # Block texture coordinates (simplified - assuming 16x16 texture atlas)
        tex_size = 1.0 / 16.0  # 16x16 grid
        tex_x = (block_type % 16) * tex_size
        tex_y = (block_type // 16) * tex_size
        
        # Define face vertices (position + texture coordinates)
        if face == 'front':  # +Z face
            return [
                x, y, z+1,     tex_x, tex_y,
                x+1, y, z+1,   tex_x + tex_size, tex_y,
                x+1, y+1, z+1, tex_x + tex_size, tex_y + tex_size,
                x, y, z+1,     tex_x, tex_y,
                x+1, y+1, z+1, tex_x + tex_size, tex_y + tex_size,
                x, y+1, z+1,   tex_x, tex_y + tex_size,
            ]
        elif face == 'back':  # -Z face
            return [
                x+1, y, z,     tex_x, tex_y,
                x, y, z,       tex_x + tex_size, tex_y,
                x, y+1, z,     tex_x + tex_size, tex_y + tex_size,
                x+1, y, z,     tex_x, tex_y,
                x, y+1, z,     tex_x + tex_size, tex_y + tex_size,
                x+1, y+1, z,   tex_x, tex_y + tex_size,
            ]
        elif face == 'right':  # +X face
            return [
                x+1, y, z+1,   tex_x, tex_y,
                x+1, y, z,     tex_x + tex_size, tex_y,
                x+1, y+1, z,   tex_x + tex_size, tex_y + tex_size,
                x+1, y, z+1,   tex_x, tex_y,
                x+1, y+1, z,   tex_x + tex_size, tex_y + tex_size,
                x+1, y+1, z+1, tex_x, tex_y + tex_size,
            ]
        elif face == 'left':  # -X face
            return [
                x, y, z,       tex_x, tex_y,
                x, y, z+1,     tex_x + tex_size, tex_y,
                x, y+1, z+1,   tex_x + tex_size, tex_y + tex_size,
                x, y, z,       tex_x, tex_y,
                x, y+1, z+1,   tex_x + tex_size, tex_y + tex_size,
                x, y+1, z,     tex_x, tex_y + tex_size,
            ]
        elif face == 'top':  # +Y face
            return [
                x, y+1, z+1,   tex_x, tex_y,
                x+1, y+1, z+1, tex_x + tex_size, tex_y,
                x+1, y+1, z,   tex_x + tex_size, tex_y + tex_size,
                x, y+1, z+1,   tex_x, tex_y,
                x+1, y+1, z,   tex_x + tex_size, tex_y + tex_size,
                x, y+1, z,     tex_x, tex_y + tex_size,
            ]
        elif face == 'bottom':  # -Y face
            return [
                x, y, z,       tex_x, tex_y,
                x+1, y, z,     tex_x + tex_size, tex_y,
                x+1, y, z+1,   tex_x + tex_size, tex_y + tex_size,
                x, y, z,       tex_x, tex_y,
                x+1, y, z+1,   tex_x + tex_size, tex_y + tex_size,
                x, y, z+1,     tex_x, tex_y + tex_size,
            ]
        
        return []
    
    def _render_vertex_buffer(self, vertices):
        """Render a vertex buffer"""
        if not vertices:
            return
        
        # Convert vertices to proper format for OpenGL
        # Each vertex: [x, y, z, u, v]
        vertex_count = len(vertices) // 5
        
        # Draw vertices as triangles
        glBegin(GL_TRIANGLES)
        for i in range(0, len(vertices), 5):
            # Texture coordinate
            glTexCoord2f(vertices[i+3], vertices[i+4])
            # Vertex position
            glVertex3f(vertices[i], vertices[i+1], vertices[i+2])
        glEnd()
    
    def render_ui(self, game):
        """Render 2D UI elements"""
        # Switch to 2D rendering
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, game.width, 0, game.height, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable depth testing for UI
        glDisable(GL_DEPTH_TEST)
        
        # Render crosshair at screen center
        if SHOW_CROSSHAIRS:
            glPushMatrix()
            glTranslatef(game.width // 2, game.height // 2, 0)
            self.crosshair_batch.draw()
            glPopMatrix()
        
        # Render text info
        if SHOW_INFO_TEXT:
            self._render_info_text(game)
        
        # Restore 3D rendering
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def _render_info_text(self, game):
        """Render information text"""
        player = game.player
        info_text = [
            f"Position: {player.position.x:.1f}, {player.position.y:.1f}, {player.position.z:.1f}",
            f"Rotation: {player.rotation_x:.1f}, {player.rotation_y:.1f}",
            f"Flying: {'Yes' if player.flying else 'No'}",
            f"Chunks: {len(game.world.chunks)}",
        ]
        
        # Create text labels
        y_offset = game.height - 30
        for i, text in enumerate(info_text):
            label = pyglet.text.Label(
                text,
                font_name='Arial',
                font_size=12,
                x=10,
                y=y_offset - i * 20,
                color=(255, 255, 255, 255)
            )
            label.draw()