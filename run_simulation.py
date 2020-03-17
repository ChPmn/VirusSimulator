# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 10:05:48 2020

@author: Gebruiker
"""
import pygame
import random
# import PyParticles

pygame.display.set_caption('Tutorial 10')
(width, height) = (100, 100)
(width, height) = (600, 300)
screen = pygame.display.set_mode((width, height))
env = Environment((width, height), mass_of_air=0, elasticity=1)

# env.addParticles(498, **{'size': 4, 'mass': 15}, speed=2.5, drag=1)
SPEED = 0.5
NR_DAYS_RECOVERY = 200
env.addParticles(199, size=4, mass=15, infected_days=0, speed=0.00001, drag=1)
env.addParticles(5, size=4, mass=15, infected_days=1, speed=0.00001, drag=1)

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_particle = env.findParticle(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        selected_particle.mouseMove(pygame.mouse.get_pos())

    env.update()
    screen.fill(env.colour)
    for p in env.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)
      
    pygame.display.flip()
    if env.particle_status[-1]['Infected'] == 0:
        running = False

pygame.quit()
#%%
nr_infected = [c['Infected'] for c in env.particle_status]
nr_healthy = [c['Healthy'] for c in env.particle_status]
nr_recovered = [c['Recovered'] for c in env.particle_status]
import matplotlib.pyplot as plt
plt.plot(nr_infected, color='r')
plt.plot(nr_healthy, color='b')
plt.plot(nr_recovered, color='g')
