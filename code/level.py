import pygame 
from settings import *
from player import Player
from sprites import Generic, Water
from pytmx.util_pygame import load_pygame
from support import *
from cow import Cow
from rabbit import Rabbit
from npc import NPC
from dialgue_manager import DialogueManager

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()

		#dialogues
		self.dialogue_manager = DialogueManager()
		self.npcs = []


		self.setup()

	def setup(self):
		tmx_data = load_pygame('data/map.tmx')

		

		

		# fence
		for x, y, surface in tmx_data.get_layer_by_name('Fenses').tiles():
			Generic((x*TILE_SIZE, y*TILE_SIZE), surface, [self.all_sprites, self.collision_sprites], LAYERS['fenses'])

		for x, y, surface in tmx_data.get_layer_by_name('Buildings').tiles():
			Generic((x*TILE_SIZE, y*TILE_SIZE), surface, [self.all_sprites, self.collision_sprites], LAYERS['buildings'])
			
		for x, y, surface in tmx_data.get_layer_by_name('Props').tiles():
			Generic((x*TILE_SIZE, y*TILE_SIZE), surface, [self.all_sprites, self.collision_sprites], LAYERS['props'])

		for x, y, surface in tmx_data.get_layer_by_name('Overlays').tiles():
			Generic(
    		    pos=(x * TILE_SIZE, y * TILE_SIZE),
    		    surf=surface,
    		    groups=[self.all_sprites],
    		    z=LAYERS['overlays'],
    		    use_hitbox=False  
    		)
		

		self.player = Player((3360, 1520), self.all_sprites, self.collision_sprites)
		Generic(
			pos = (0,0),
			surf = pygame.image.load("graphics/world/ground.png").convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])
		
		self.cow = Cow((912, 2496), (912, 2496, 250, 200), self.all_sprites, LAYERS['overlays'])
		self.rabbit =Rabbit((2700, 3408), (2700, 3408, 800, 200), self.all_sprites, LAYERS['rabbit'])


		self.npcs = []
		self.npcs.append(NPC((864, 1200), (864, 1200, 348, 336), self.all_sprites, "elsie"))
		self.npcs.append(NPC((2784, 960), (2784, 960, 768, 576), self.all_sprites, "finn"))
		self.npcs.append(NPC((2208, 1632), (2208, 1632, 480, 384), self.all_sprites, "reed"))
		self.npcs.append(NPC((1152, 3120), (1152, 3120, 912, 96), self.all_sprites, "sylvia"))

	def run(self, dt):
		self.all_sprites.custom_draw(self.player)
		self.all_sprites.update(dt)

		# Check if player is near any NPC
		in_proximity = None
		for npc in self.npcs:
			if self.player.rect.colliderect(npc.rect.inflate(40, 40)):
				in_proximity = npc
				break

		# If no NPC is near, close dialogue
		if not in_proximity:
			self.dialogue_manager.close()

		# Dialogue input
		keys = pygame.key.get_pressed()
		if in_proximity and keys[pygame.K_e]:  # E to ask about unusual things
			self.dialogue_manager.open(in_proximity.dialogues['seen'])

		elif in_proximity and keys[pygame.K_q]:  # Q to ask who they are
			self.dialogue_manager.open(in_proximity.dialogues['who'])

		elif keys[pygame.K_ESCAPE]:
			self.dialogue_manager.close()

		# Draw dialogue
		self.dialogue_manager.draw(self.display_surface)



class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()


	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)


