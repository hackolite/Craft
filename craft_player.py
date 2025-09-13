"""
Player class for movement and camera control
"""

import math
from pyglet.gl import *
from craft_math import Vector3, Matrix4, radians, clamp
from craft_config import *

class Player:
    """Player class handling movement, camera, and physics"""
    
    def __init__(self):
        # Position and orientation
        self.position = Vector3(0, 32, 0)  # Start above ground
        self.velocity = Vector3(0, 0, 0)
        self.rotation_x = 0.0  # Pitch (up/down)
        self.rotation_y = 0.0  # Yaw (left/right)
        
        # Player state
        self.flying = False
        self.on_ground = False
        self.in_water = False
        
        # Movement flags
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        
        # Camera settings
        self.fov = FOV
        self.ortho = False
        self.zoom = False
        
        # Physics constants
        self.gravity = GRAVITY
        self.jump_velocity = JUMP_VELOCITY
        self.walking_speed = WALKING_SPEED
        self.flying_speed = FLYING_SPEED
        self.terminal_velocity = TERMINAL_VELOCITY
        
        # Collision box (half-extents)
        self.width = 0.4
        self.height = 1.8
    
    def update(self, dt, input_handler, world):
        """Update player physics and movement"""
        # Handle input
        self._handle_input(input_handler)
        
        # Calculate movement vector
        movement = Vector3(0, 0, 0)
        
        if self.moving_forward:
            movement.x -= math.sin(radians(self.rotation_y))
            movement.z -= math.cos(radians(self.rotation_y))
        
        if self.moving_backward:
            movement.x += math.sin(radians(self.rotation_y))
            movement.z += math.cos(radians(self.rotation_y))
        
        if self.moving_left:
            movement.x -= math.cos(radians(self.rotation_y))
            movement.z += math.sin(radians(self.rotation_y))
        
        if self.moving_right:
            movement.x += math.cos(radians(self.rotation_y))
            movement.z -= math.sin(radians(self.rotation_y))
        
        # Normalize movement
        if movement.length() > 0:
            movement = movement.normalize()
        
        # Apply movement speed
        speed = self.flying_speed if self.flying else self.walking_speed
        movement = movement * speed * dt
        
        if self.flying:
            # Flying movement
            if self.jumping:
                movement.y += self.flying_speed * dt
            
            # Apply movement directly
            self.position = self.position + movement
        else:
            # Ground-based movement with physics
            self.velocity.x = movement.x / dt if dt > 0 else 0
            self.velocity.z = movement.z / dt if dt > 0 else 0
            
            # Apply gravity
            if not self.on_ground:
                self.velocity.y -= self.gravity * dt
                if self.velocity.y < -self.terminal_velocity:
                    self.velocity.y = -self.terminal_velocity
            
            # Jumping
            if self.jumping and self.on_ground:
                self.velocity.y = self.jump_velocity
                self.on_ground = False
            
            # Apply velocity
            new_pos = self.position + self.velocity * dt
            
            # Collision detection (simplified)
            self.position = self._handle_collision(new_pos, world)
            
            # Check if on ground
            ground_y = self._get_ground_level(world)
            if self.position.y <= ground_y + 0.1:
                self.position.y = ground_y
                self.velocity.y = 0
                self.on_ground = True
            else:
                self.on_ground = False
    
    def _handle_input(self, input_handler):
        """Process input for movement"""
        keys = input_handler.keys_pressed
        
        self.moving_forward = keys.get(CRAFT_KEY_FORWARD, False)
        self.moving_backward = keys.get(CRAFT_KEY_BACKWARD, False)
        self.moving_left = keys.get(CRAFT_KEY_LEFT, False)
        self.moving_right = keys.get(CRAFT_KEY_RIGHT, False)
        self.jumping = keys.get(CRAFT_KEY_JUMP, False)
        self.zoom = keys.get(CRAFT_KEY_ZOOM, False)
    
    def _handle_collision(self, new_pos, world):
        """Handle collision with world (simplified)"""
        # For now, just prevent going below a certain level
        if new_pos.y < 0:
            new_pos.y = 0
            self.velocity.y = 0
        
        return new_pos
    
    def _get_ground_level(self, world):
        """Get ground level at player position (simplified)"""
        # For now, return a basic ground level
        # TODO: Implement proper world collision detection
        return 1.0
    
    def apply_camera_transform(self):
        """Apply camera transformation to OpenGL matrix stack"""
        # Apply rotation (pitch and yaw)
        glRotatef(-self.rotation_x, 1, 0, 0)  # Pitch
        glRotatef(-self.rotation_y, 0, 1, 0)  # Yaw
        
        # Apply translation (move world opposite to player)
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)
    
    def get_view_matrix(self):
        """Get view matrix for camera"""
        matrix = Matrix4.identity()
        
        # Apply rotation
        matrix.rotate_x(radians(-self.rotation_x))
        matrix.rotate_y(radians(-self.rotation_y))
        
        # Apply translation
        matrix.translate(-self.position.x, -self.position.y, -self.position.z)
        
        return matrix
    
    def get_forward_vector(self):
        """Get forward direction vector"""
        rx = radians(self.rotation_x)
        ry = radians(self.rotation_y)
        
        return Vector3(
            -math.sin(ry) * math.cos(rx),
            -math.sin(rx),
            -math.cos(ry) * math.cos(rx)
        )
    
    def get_right_vector(self):
        """Get right direction vector"""
        ry = radians(self.rotation_y)
        return Vector3(math.cos(ry), 0, -math.sin(ry))
    
    def get_up_vector(self):
        """Get up direction vector"""
        forward = self.get_forward_vector()
        right = self.get_right_vector()
        return right.cross(forward).normalize()
    
    def handle_mouse_motion(self, dx, dy):
        """Handle mouse movement for camera control"""
        sensitivity = 0.1
        
        if INVERT_MOUSE:
            dy = -dy
        
        self.rotation_y += dx * sensitivity
        self.rotation_x += dy * sensitivity
        
        # Clamp pitch to prevent camera flipping
        self.rotation_x = clamp(self.rotation_x, -90, 90)
        
        # Normalize yaw
        while self.rotation_y > 180:
            self.rotation_y -= 360
        while self.rotation_y < -180:
            self.rotation_y += 360
    
    def toggle_flying(self):
        """Toggle flying mode"""
        self.flying = not self.flying
        if self.flying:
            self.velocity.y = 0  # Stop falling when entering fly mode
    
    def toggle_ortho(self):
        """Toggle orthographic projection"""
        self.ortho = not self.ortho