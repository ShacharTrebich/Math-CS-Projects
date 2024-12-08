from operator import truediv

import pygame
import random
import math
from pygame import mixer
pygame.init()


class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 247, 127, 0
	RED = 214, 40, 40
	BACKGROUND_COLOR = (237, 237, 233)

	#GRADIENTS = [(213, 189, 175),(227, 213, 202), (245, 235, 224)]
	GRADIENTS = [(237, 224, 212), (230, 203, 178), (221, 184, 146)]

	font_text = 'Merienda-VariableFont_wght.ttf'
	font_header = 'SofadiOne-Regular.ttf'
	FONT = pygame.font.Font(font_text, 20)
	LARGE_FONT = pygame.font.Font(font_header, 40)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 80))

	sorting = draw_info.FONT.render("K - Shaker Sort | H - Heap Sort | S - Selection Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 115))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False, rec_list=[]):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

		number_font = pygame.font.SysFont('comicsans', 10)  # פונט קטן יותר
		number_text = number_font.render(str(val), True, draw_info.BLACK)
		text_x = x + (draw_info.block_width // 4)  # ממקם במרכז
		text_y = (draw_info.height - (val - draw_info.min_val) * draw_info.block_height) - 13 # ממקם 10 פיקסלים מהחלק התחתון

		draw_info.window.blit(number_text, (text_x, text_y))

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst

##########################################################################
def draw_splash_screen(screen, width, height):
	# צבעים
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	ORANGE = (247, 127, 0)

	# יצירת פונטים
	title_font = pygame.font.Font('SofadiOne-Regular.ttf', 50)
	name_font = pygame.font.Font('Merienda-VariableFont_wght.ttf', 30)
	subtitle_font = pygame.font.Font('Merienda-VariableFont_wght.ttf', 25)

	# טקסטים
	title = title_font.render("Sorting Visualizer", True, ORANGE)
	name = name_font.render("Created by Shachar Trebich - 204735104", True, WHITE)
	subtitle = subtitle_font.render(" ", True, WHITE)

	# מיקומים
	title_pos = ((width - title.get_width()) // 2, height // 2 - 50)
	name_pos = ((width - name.get_width()) // 2, height // 2 + 20)
	subtitle_pos = ((width - subtitle.get_width()) // 2, height // 2 + 70)

	# אנימציה
	alpha = 0
	fade_in_speed = 3
	stay_time = 120  # כמה פריימים המסך יישאר
	fade_out_speed = 3

	# fade in
	while alpha < 255:
		screen.fill(BLACK)

		title.set_alpha(alpha)
		name.set_alpha(alpha)
		subtitle.set_alpha(alpha)

		screen.blit(title, title_pos)
		screen.blit(name, name_pos)
		screen.blit(subtitle, subtitle_pos)

		pygame.display.flip()
		alpha += fade_in_speed
		pygame.time.delay(10)

	# השהייה
	pygame.time.delay(stay_time * 10)

	# fade out
	while alpha > 0:
		screen.fill(BLACK)

		title.set_alpha(alpha)
		name.set_alpha(alpha)
		subtitle.set_alpha(alpha)

		screen.blit(title, title_pos)
		screen.blit(name, name_pos)
		screen.blit(subtitle, subtitle_pos)

		pygame.display.flip()
		alpha -= fade_out_speed
		pygame.time.delay(10)
##########################################################################

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


def merge_sort(draw_info, ascending = True):
	lst = draw_info.lst
	rec_list = []

	def merge(l, r):
		rec_list.append((l, r))
		if l < r:
			mid = (l + r)//2
			yield from merge (l, mid)
			yield from merge (mid + 1, r)
			new_list = []
			i = l
			j = mid + 1

			while (i <= mid) and (j <= r):
				draw_list(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True, rec_list)
				yield True
				if (lst[i] < lst[j] and ascending) or (lst[i] > lst[j] and not ascending):
					#lst[i],lst[j] = lst[j],lst[i]
					new_list.append(lst[i])
					i += 1
				else:
					new_list.append(lst[j])
					j += 1

			while i <= mid:
				draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True, rec_list)
				yield True
				new_list.append(lst[i])
				i += 1
			while j <= r:
				draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True, rec_list)
				yield True
				new_list.append(lst[j])
				j += 1
			lst[l:r + 1] = new_list
		rec_list.pop()

	yield from merge(0, len(lst) - 1)
	return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    l = 0
    r = len(lst) - 1

    def random_quicksort(draw_info, lst, l, r, ascending=True):
        if l < r:
            p = yield from random_partition(draw_info, lst, l, r, ascending)
            yield from random_quicksort(draw_info, lst, l, p - 1, ascending)
            yield from random_quicksort(draw_info, lst, p + 1, r, ascending)

    def random_partition(draw_info, lst, l, r, ascending):
        # בחירת פיבוט אקראי
        i = random.randint(l, r)
        lst[l], lst[i] = lst[i], lst[l]
        draw_list(draw_info, {l: draw_info.GREEN, i: draw_info.RED}, True)
        yield True
        return (yield from lomuto_partition(draw_info, lst, l, r, ascending))

    def lomuto_partition(draw_info, lst, l, r, ascending):
        red = l
        pivot = lst[l]
        for blue in range(l + 1, r + 1):
            if (lst[blue] < pivot and ascending) or (lst[blue] > pivot and not ascending):
                red += 1
                lst[red], lst[blue] = lst[blue], lst[red]
                draw_list(draw_info, {red: draw_info.GREEN, blue: draw_info.RED}, True)
                yield True

        lst[l], lst[red] = lst[red], lst[l]
        draw_list(draw_info, {l: draw_info.GREEN, red: draw_info.RED}, True)
        yield True
        return red

    return random_quicksort(draw_info, lst, l, r, ascending)

def heap_sort (draw_info, ascending = True):
	lst = draw_info.lst
	for n in range (1,len(lst)):
		while n > 0:
			parent = (n - 1) // 2
			num1 = lst[n]
			num2 = lst[parent]
			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[n],lst[parent] = lst[parent],lst[n]
				draw_list(draw_info, {n: draw_info.GREEN, parent: draw_info.RED}, True)
				yield True
				n = parent
			else:
				break

	for i in range (len(lst)-1, 0, -1):
		lst[0],lst[i] = lst[i],lst[0]
		draw_list(draw_info, {0: draw_info.GREEN, i: draw_info.RED}, True)
		yield True

		cur = 0
		while 2 * cur + 1 < i:
			left = 2 * cur + 1
			right = 2 * cur + 2
			largest = cur

			if left < i and ((lst[largest] < lst[left] and ascending) or (lst[largest] > lst[left] and not ascending)):
				largest = left
			if right < i and ((lst[largest] < lst[right] and ascending) or (lst[largest] > lst[right] and not ascending)):
				largest = right

			if largest != cur:
				lst[cur],lst[largest] = lst[largest],lst[cur]
				draw_list(draw_info, {cur: draw_info.GREEN, largest: draw_info.RED}, True)
				yield True
				cur = largest
			else:
				break
	return lst

def shaker_sort(draw_info, ascending = True):
	lst = draw_info.lst
	start = 0
	n = len(lst)
	end = n - 1
	swaped = True

	while swaped:
		swaped = False

		for i in range (start, end):
			if (lst[i] > lst[i+1] and ascending) or (lst[i] < lst[i+1] and not ascending):
				lst[i], lst[i+1] = lst[i+1], lst[i]
				draw_list(draw_info, {i: draw_info.GREEN, i + 1: draw_info.RED}, True)
				yield True
				swaped = True

		if swaped == False:
			break

		swaped = False
		end = end - 1
		for i in range (end - 1, start - 1, -1):
			if (lst[i] > lst[i+1] and ascending) or (lst[i] < lst[i+1] and not ascending):
				lst[i], lst[i+1] = lst[i+1], lst[i]
				draw_list(draw_info, {i: draw_info.GREEN, i + 1: draw_info.RED}, True)
				yield True
				swaped = True

		start = start + 1
	return lst

def selection_sort (draw_info, ascending = True):
	lst = draw_info.lst
	for i in range(len(lst)):
		min_index = i

		for j in range(i + 1, len(lst)):
			if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
				min_index = j

		if i != min_index:
			lst[i], lst[min_index] = lst[min_index], lst[i]
			draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
			yield True
	return lst

def main():
	#####################################################################
	pygame.init()
	width = 800
	height = 600
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Sorting Algorithm Visualization")

	# הצגת מסך הפתיחה
	draw_splash_screen(screen, width, height)
	#####################################################################

	mixer.init()
	mixer.music.load('Walking The Dog - Jeremy Korpas.mp3')
	tone = mixer.Sound('Walking The Dog - Jeremy Korpas.mp3')
	claps = mixer.Sound('claps-44774.mp3')

	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None


	while run:
		clock.tick(60)

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
				tone.stop()
				claps.play()

		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				tone.stop()
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				tone.play(-1)
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
				claps.stop()
			elif event.key == pygame.K_d and not sorting:
				ascending = False
				claps.stop()
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
				claps.stop()
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm = merge_sort
				sorting_algo_name = "Merge Sort"
				claps.stop()
			elif event.key == pygame.K_q and not sorting:
				sorting_algorithm = quick_sort
				sorting_algo_name = "Quick Sort"
				claps.stop()
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
				claps.stop()
			elif event.key == pygame.K_h and not sorting:
				sorting_algorithm = heap_sort
				sorting_algo_name = "Heap Sort"
				claps.stop()
			elif event.key == pygame.K_k and not sorting:
				sorting_algorithm = shaker_sort
				sorting_algo_name = "Shaker Sort"
				claps.stop()
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"
				claps.stop()


	pygame.quit()


if __name__ == "__main__":
	main()