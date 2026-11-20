import pygame
import csv
import random
import time
from datetime import datetime

WIDTH, HEIGHT = 1000, 650
WHITE = (245, 245, 245)
BLACK = (25, 28, 35)
BLUE = (70, 160, 245)
GREEN = (70, 210, 130)
# Same length as: "The quick brown fox jumps over the lazy dog."
TYPING_TEXT_LEN = 44
TYPING_WORD_LENGTHS = (3, 5, 5, 3, 5, 4, 3, 4, 3)
WORDS_BY_LEN = {
    3: [
        'the', 'fox', 'dog', 'cat', 'sun', 'sky', 'red', 'big', 'run', 'map',
        'box', 'cup', 'hat', 'pen', 'key', 'log', 'mud', 'oak', 'pie', 'rat',
    ],
    4: [
        'over', 'lazy', 'blue', 'warm', 'cold', 'dark', 'soft', 'fast', 'bird',
        'lamp', 'desk', 'tree', 'rain', 'snow', 'wind', 'book', 'door', 'road',
    ],
    5: [
        'quick', 'brown', 'jumps', 'light', 'green', 'happy', 'water', 'table',
        'chair', 'cloud', 'stone', 'plant', 'music', 'paper', 'bread', 'flame',
    ],
}

def make_typing_text() -> str:
    words = [random.choice(WORDS_BY_LEN[n]) for n in TYPING_WORD_LENGTHS]
    words[0] = words[0].capitalize()
    text = ' '.join(words) + '.'
    assert len(text) == TYPING_TEXT_LEN
    return text

def results_filename() -> str:
    # Windows disallows / and : in filenames, so use dashes instead.
    stamp = datetime.now().strftime('%m-%d-%y_%H-%M-%S')
    return f'experiment_results({stamp}).csv'

# Set after create_window() so console prompts can run first.
screen = None
clock = None
font = None
small = None

def create_window():
    global screen, clock, font, small
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('CS464 Room Lighting Experiment')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 34)
    small = pygame.font.SysFont(None, 26)

def draw(lines):
    screen.fill(BLACK)
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, WHITE), (45, 45 + i * 45))

def wait_for_space(lines):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        draw(lines + ['Press SPACE to start.'])
        pygame.display.flip()
        clock.tick(60)

def mouse_task():
    wait_for_space(['Task A: Move the cursor into each blue ring.', 'There will be 10 rings.'])
    rng = random.Random(12345)
    positions = [(rng.randint(100, WIDTH - 100), rng.randint(190, HEIGHT - 90)) for _ in range(10)]
    index = 0
    start = time.perf_counter()
    # Require moving out before another target is accepted.
    ready = True
    while index < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        pos = pygame.mouse.get_pos()
        target = positions[index]
        inside = (pos[0] - target[0]) ** 2 + (pos[1] - target[1]) ** 2 <= 32 ** 2
        if not inside:
            ready = True
        if inside and ready:
            index += 1
            ready = False
            if index < 10:
                # Ensure next ring is not instantly counted.
                next_target = positions[index]
                if (pos[0] - next_target[0]) ** 2 + (pos[1] - next_target[1]) ** 2 <= 32 ** 2:
                    ready = False
        draw([f'Task A: Ring {min(index + 1, 10)} of 10'])
        if index < 10:
            pygame.draw.circle(screen, BLUE, positions[index], 32, 5)
        pygame.display.flip()
        clock.tick(60)
    return round(time.perf_counter() - start, 3)

def typing_task():
    wait_for_space(['Task B: Copy the sentence exactly.', 'Press ENTER when finished.'])
    prompt = make_typing_text()
    typed = ''
    start = time.perf_counter()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    duration = round(time.perf_counter() - start, 3)
                    errors = sum(a != b for a, b in zip(prompt, typed)) + abs(len(prompt) - len(typed))
                    return duration, errors
                if event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                elif event.unicode and event.unicode.isprintable():
                    typed += event.unicode
        draw(['Task B: Type the sentence below, then press ENTER:', prompt, '', 'Your text:', typed[-65:]])
        pygame.display.flip()
        clock.tick(60)

def ask_lux_level() -> float:
    while True:
        raw = input('What is the Lux light level from the mobile app? ').strip()
        try:
            return float(raw)
        except ValueError:
            print('Please enter a number only (for example 120 or 45.5).')

def ask_screen_brightness() -> int:
    choices = {'1': 10, '2': 50, '3': 100}
    print('Which percent screen brightness?')
    print('  1 = 10%')
    print('  2 = 50%')
    print('  3 = 100%')
    while True:
        choice = input('Choose 1, 2, or 3: ').strip()
        if choice in choices:
            return choices[choice]
        print('Please enter 1, 2, or 3 only.')

def main():
    print('CS464 Room Lighting Experiment')
    participant = input('Participant ID (no names): ').strip()
    while not participant:
        participant = input('Enter a participant ID: ').strip()
    condition = input('Room condition (dark/light): ').strip().lower()
    while condition not in ('dark', 'light'):
        condition = input('Please enter dark or light: ').strip().lower()
    order = random.choice(('AB', 'BA'))
    print(f'Task order randomly assigned: {order}')
    lux_level = ask_lux_level()
    screen_brightness = ask_screen_brightness()

    create_window()

    results = {}
    for task in order:
        if task == 'A':
            results['mouse_seconds'] = mouse_task()
        else:
            results['typing_seconds'], results['typing_errors'] = typing_task()
    columns = [
        'participant_id',
        'room_condition',
        'task_order',
        'lux_level',
        'screen_brightness_percent',
        'mouse_seconds',
        'typing_seconds',
        'typing_errors',
    ]
    row = {
        'participant_id': participant,
        'room_condition': condition,
        'task_order': order,
        'lux_level': lux_level,
        'screen_brightness_percent': screen_brightness,
        **results,
    }
    outfile = results_filename()
    with open(outfile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerow(row)
    draw([f'Finished! Results saved to {outfile}', 'You may close the window.'])
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()

if __name__ == '__main__':
    main()
