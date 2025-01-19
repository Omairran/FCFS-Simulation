import pygame
import sys
import random

pygame.init()

pygame.mixer.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("FCFS Scheduling Simulation")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 223, 0)


def get_font(size):
    return pygame.font.SysFont("Comic Sans MS", size, True)

def draw_gradient(screen):
    for i in range(720):
        red = (i // 3) % 256
        green = (i // 2) % 256
        blue = (i // 4) % 256
        color = (red, green, blue) 
        pygame.draw.line(screen, color, (0, i), (1280, i))

class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.x = 150
        self.y = 100 + pid * 70
        self.color = random.choice([BLUE, RED, YELLOW, GREEN])
        self.moving_to_cpu = False
        self.executed = False
        self.sound_played = False  

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 30)
        text = get_font(20).render(f"P{self.pid} ({self.remaining_time}s)", True, WHITE)
        screen.blit(text, (self.x - 25, self.y - 10))

    def move_to_cpu(self, target_x, target_y):
        if not self.executed:
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            speed = 5  # Pixels per frame
            if distance > speed:
                self.x += speed * (dx / distance)
                self.y += speed * (dy / distance)
            else:
                self.x = target_x
                self.y = target_y
                self.moving_to_cpu = False

move_to_cpu_sound = pygame.mixer.Sound("move_to_cpu.mp3")  
cpu_execution_sound = pygame.mixer.Sound("cpu_execution.mp3")  
process_completion_sound = pygame.mixer.Sound("process_completion.mp3")  

def FCFS():
    running = True
    processes = [Process(i + 1, random.randint(2, 8)) for i in range(5)]
    gantt_chart = []
    cpu_x, cpu_y = 640, 360
    current_process = None
    process_index = 0
    execution_timer = 0
    process_queue = []  
    termination_timer = None  

    while running:
        draw_gradient(SCREEN)  

        title_text = get_font(40).render("FCFS Scheduling Simulation", True, WHITE)
        SCREEN.blit(title_text, (400, 20))

        queue_text = get_font(30).render("Ready Queue", True, WHITE)
        SCREEN.blit(queue_text, (50, 50))
        for process in processes:
            if not process.executed:
                # Add shadow effect behind the process circle
                pygame.draw.circle(SCREEN, GRAY, (process.x + 5, process.y + 5), 30)
                process.draw(SCREEN)

        pygame.draw.rect(SCREEN, LIGHT_BLUE, (cpu_x - 40, cpu_y - 40, 80, 80), border_radius=10)
        pygame.draw.circle(SCREEN, BLUE, (cpu_x, cpu_y), 50, 5)  # Glowing effect around the CPU
        cpu_text = get_font(30).render("CPU", True, WHITE)
        SCREEN.blit(cpu_text, (cpu_x - 30, cpu_y - 70))

        gantt_text = get_font(30).render("Gantt Chart", True, WHITE)
        SCREEN.blit(gantt_text, (50, 500))
        gantt_start_x = 200
        time_marker = 0
        for i, process in enumerate(gantt_chart):
            pygame.draw.rect(SCREEN, process.color, (gantt_start_x + i * 120, 550, 100, 40), border_radius=15)
            text = get_font(20).render(f"P{process.pid}", True, WHITE)
            SCREEN.blit(text, (gantt_start_x + i * 120 + 35, 560))

            time_text = get_font(20).render(str(time_marker), True, WHITE)
            SCREEN.blit(time_text, (gantt_start_x + i * 120, 600))
            time_marker += process.burst_time

        if gantt_chart:
            time_text = get_font(20).render(str(time_marker), True, WHITE)
            SCREEN.blit(time_text, (gantt_start_x + len(gantt_chart) * 120, 600))

        if current_process is None and process_index < len(processes):
            current_process = processes[process_index]
            current_process.moving_to_cpu = True
            current_process.sound_played = False 
            process_queue.append(current_process) 
            process_index += 1
            execution_timer = current_process.burst_time * 60  
            if not current_process.sound_played:  
                move_to_cpu_sound.play() 
                current_process.sound_played = True

        if current_process:
            if current_process.moving_to_cpu:
                current_process.move_to_cpu(cpu_x, cpu_y)
            else:
                current_process.draw(SCREEN)
                if execution_timer > 0:
                    execution_timer -= 1
                    if execution_timer % 60 == 0: 
                        current_process.remaining_time -= 1
                        cpu_execution_sound.play()  
                else:
                    current_process.executed = True
                    gantt_chart.append(current_process)  
                    process_completion_sound.play()  
                    current_process = None
                    if process_index == len(processes): 
                        print("All processes have been executed!")
                        termination_timer = 180  


        if termination_timer is not None:
            termination_timer -= 1
            if termination_timer <= 0:
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


FCFS()