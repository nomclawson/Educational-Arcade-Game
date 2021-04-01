from globals import Sprite 
from globals import arcade 


def  createExplosionTextureList():
    """
	Creates a list of textures used by the Explossion class
    The frames need to be preloaded before an instance of this class
    Then the list will be passed to the constructor
	"""
    columns = 16
    count = 60
    sprite_width = 256
    sprite_height = 256
    file_name = ":resources:images/spritesheets/explosion.png"
    list_textures  =  arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)
    return list_textures

class Explosion(Sprite):
    """ This class creates an explosion animation """
    def __init__(self, texture_list, x, y):
        super().__init__()

        # Start at the first frameS
        self.current_texture = 0
        self.textures = texture_list
        self.center_x = x
        self.center_y = y

    def update(self):
        """
		Updates to the next frame of the animation. If the sprite is at the end of the frames
        then delete the sprite.
		"""
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()
