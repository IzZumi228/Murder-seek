from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 48

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'ground': 1,
    'path': 2,
	'soil': 3,
    'main': 5,
    'rabbit': 6,
    'fenses': 7,
    'props': 8,
    'buildings': 9,
    'overlays': 10
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}

CHARACTER_LOCATIONS = {
    'Sylvia': 'Workshop',
    'Marlowe': 'Farm Shop',
    'Elsie': 'Garden',
    'Jasper': 'Lake'
}

CHARACTER_INTRODUCTIONS = {
    'Sylvia': "I'm Sylvia. I keep the buildings standing around here—barns, fences, sheds, you name it. I prefer the sound of hammering to talking, but I’ll help if I can.",
    'Marlowe': "Name’s Marlowe. I drift from place to place, selling rare seeds and oddities. This farm’s quiet… good soil, strange energy. Thought I’d stay a while.",
    'Elsie': "Oh! I'm Elsie. I care for the greenhouse and all the plants around the farm. If it’s green and growing, chances are I’ve had a hand in it.",
    'Jasper': "Jas Holt. I fish, I chat, I keep an ear to the ground. If you’re looking for gossip or catfish, I’m your guy."
}

