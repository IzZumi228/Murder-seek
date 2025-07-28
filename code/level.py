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
from ai import *
from game_over_trigger import FinishingTrigger

mock_dialogue = { 
	'Sylvia': {
		'statement': 'I was helping Elsie in the greenhouses most of the day, checking on some of her new plants. We stayed inside away from the cold and didn’t step outside much.', 
		'observation': 'The wind was picking up later in the afternoon, but I didn’t notice anything out of the ordinary near the main house.'
		}, 
	'Jasper': {
		'statement': 'I spent the day with Elsie, went over some of the water samples she collected from the nearby stream. We were mostly outside, chatting and moving around the property together.', 
		'observation': 'Sylvia’s workshop was strange oddly quiet the entire day, which is not like her at all. Usually, you’d hear the hammer and saw from there without fail.'
		}, 
	'Elsie': {
		'statement': 'I was with Jasper, helping him go through some plants by the riverbank and talking about what’s growing nearby this season. We didn’t really go near the house much until evening.', 
		'observation': 'Marlowe didn’t show up at the Farm Shop like he usually does; I found that a bit strange since he’s normally there every day.'
		}, 
	'Marlowe': {
		'statement': "I wasn’t at the Farm Shop because I had to deal with some unexpected paperwork in town; it kept me away longer than I thought. I made sure to take care of the business early, so I wouldn't miss much here.", 
		'observation': 'Nothing out of the ordinary caught my eye around the farm today. It seemed like a regular day from where I was.'
		}
}




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
		self.current_dialogues = mock_dialogue

		#final decision variables
		self.actual_murderer = "Sylvia"  # or whatever the correct answer is
		self.game_over = False
		self.final_guess = None
		self.game_over_time = None




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
		self.npcs.append(NPC((864, 1200), (864, 1200, 348, 336), self.all_sprites, "Elsie", self.current_dialogues['Elsie']))
		self.npcs.append(NPC((2784, 960), (2784, 960, 768, 576), self.all_sprites, "Jasper", self.current_dialogues['Jasper']))
		self.npcs.append(NPC((2208, 1632), (2208, 1632, 480, 384), self.all_sprites, "Marlowe", self.current_dialogues["Marlowe"]))
		self.npcs.append(NPC((1152, 3120), (1152, 3120, 912, 96), self.all_sprites, "Sylvia", self.current_dialogues['Sylvia']))


		self.finishing_trigger = FinishingTrigger((3550, 1708), self.all_sprites)
		

	def run(self, dt):

		if self.game_over:
			self.dialogue_manager.draw(self.display_surface)
			# after 3 seconds, restart
			if pygame.time.get_ticks() - self.game_over_time >= 3000:
				self.restart_level()

			return
		
		

		self.all_sprites.custom_draw(self.player)
		self.all_sprites.update(dt)

		in_proximity_npc = None
		in_proximity_finish_trigger = False

		for npc in self.npcs:
			if self.player.rect.colliderect(npc.rect.inflate(40, 40)):
				in_proximity_npc = npc
				break

		if self.player.rect.colliderect(self.finishing_trigger.rect.inflate(40, 40)):
			in_proximity_finish_trigger = True

		# show npc dialogue UI
		if in_proximity_npc:
			self.dialogue_manager.draw(self.display_surface)
			self.dialogue_manager.set_options([
				("Who are you?", in_proximity_npc.intoduction),
				("What have you been doing on the day of the murder?", in_proximity_npc.dialogues["statement"]),
				("Have you noticed anything unusual?", in_proximity_npc.dialogues["observation"]),
			])
		elif in_proximity_finish_trigger:
			self.dialogue_manager.draw(self.display_surface)
			self.dialogue_manager.set_options([
				("The Murderer is Sylvia", "Are you sure?"),
				("The Murderer is Marlowe", "Are you sure?"),
				("The Murderer is Jasper", "Are you sure?"),
				("The Murderer is Elsie", "Are you sure?"),
			])
		else:
			self.dialogue_manager.close()
			self.dialogue_manager.clear_options()

		# Handle clicks
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()[0]
		clicked, chosen_label = self.dialogue_manager.handle_click(mouse_pos, mouse_pressed, self.dialogue_manager.option_rects)

		if in_proximity_finish_trigger and clicked and chosen_label:
			if "The Murderer is" in chosen_label:
				self.final_guess = chosen_label.replace("The Murderer is ", "")
				if self.final_guess == self.actual_murderer:
					self.end_game(victory=True)
				else:
					self.end_game(victory=False)

		# ESC to close
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			self.dialogue_manager.close()
				



	def end_game(self, victory):
		self.dialogue_manager.clear_options()
		if victory:
			self.dialogue_manager.open("You were right! Justice has been served. Launching new round...")
		else:
			self.dialogue_manager.open(f"That was incorrect. The real murderer was {self.actual_murderer}. Launching new round...")

		self.game_over = True
		self.game_over_time = pygame.time.get_ticks()

	def restart_level(self):
		print("restarting...")
		self.__init__()



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


