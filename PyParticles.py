import math, random
from collections import Counter

def collide(p1, p2):
    """ Tests whether two particles overlap
    If they do, make them bounce and spread disease if one is infected but the other is not
    Bouncing means update their angle and position, BUT NOT SPEED
    
    In our simulation, people do not slow down or speed up after colliding with someone
    """
    
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < (p1.size + p2.size):
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        tangent = math.atan2(dy, dx)
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap
        
        if p1.infection_status == 'Infected' and p2.infection_status == 'Healthy':
            p2.disease.days_infected = 1
        elif p2.infection_status == 'Infected' and p1.infection_status == 'Healthy':
            p1.disease.days_infected = 1       

class Disease:
    
    def __init__(self, days_infected=0, duration=500, incubation_time=0, chance_of_spreading=1):
        self.days_infected = days_infected
        self.duration = duration
        self.incubation_time = incubation_time
    
    def update(self):
        if self.days_infected > 0:
            self.days_infected += 1

class Particle:
    """ A circular object with a velocity, size and mass """
    
    def __init__(self, pos, size=4, mass=1, drag=1, speed=1, angle=0, elasticity=1, disease=Disease(), thickness=0):
        self.x, self.y = pos
        self.size = size
        self.thickness = thickness
        self.speed = speed
        self.angle = angle
        self.mass = mass
        self.drag = drag
        self.elasticity = elasticity
        self.disease = disease
        
        self.get_infection_status()
        self.update_color()

    def get_infection_status(self):
        
        if self.disease.days_infected == 0:
            self.infection_status = 'Healthy'
        elif self.disease.days_infected < self.disease.incubation_time:
            self.infection_status = 'Incubation'
        elif self.disease.days_infected < self.disease.duration + self.disease.incubation_time:
            self.infection_status = 'Infected'
        else:
            self.infection_status = 'Recovered'

    def update_color(self):
        colour_map = {'Healthy': (0, 0, 255), 'Incubation': (255, 0, 255), 'Infected': (255, 0, 0), 'Recovered': (0, 255, 0)}
        self.colour = colour_map[self.infection_status]
        
    def move(self):
        """ Update position based on speed, angle
            Update speed based on drag """

        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag
        
class Environment:
    """ Defines the boundary of a simulation and its properties """
    
    def __init__(self, size, mass_of_air=0, elasticity=1, when_measure_starts=1, pct_population_measure=0.75, measure_speed_decrease=0.5):
        self.width, self.height = size
        self.particles = []
        
        self.colour = (255,255,255)
        self.mass_of_air = mass_of_air
        self.elasticity = elasticity
        self.acceleration = None
        self.particle_status = []
        
        self.measure_enacted = False
        self.when_measure_starts = when_measure_starts
        self.pct_population_measure = pct_population_measure
        self.measure_speed_decrease = measure_speed_decrease
        
    def addParticles(self, n=1, **kargs):
        """ Add n particles with properties given by keyword arguments """
        
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size)) # size = particle size, so particle is not across walls
            y = kargs.get('y', random.uniform(size, self.height - size)) # size = particle size, so particle is not across walls
            elasticity = kargs.get('elasticity', 1)
            speed = kargs.get('speed', random.random())
            angle = kargs.get('angle', random.uniform(0, math.pi*2))
            
            days_infected = kargs.get('days_infected', 0)
            duration = kargs.get('duration', 500)
            incubation_time = kargs.get('incubation_time', 0)
            disease = Disease(days_infected=days_infected, duration=duration, incubation_time=incubation_time)
            particle = Particle((x, y), size=size, mass=mass, speed=speed, elasticity=elasticity, angle=angle, disease=disease)
            self.particles.append(particle)

    def update(self):
        """  Moves particles and tests for collisions with the walls and each other """
        
        for i, particle in enumerate(self.particles):
            particle.move()
            if self.acceleration:
                particle.accelerate(self.acceleration)
            self.bounce(particle)
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)
            
            particle.disease.update()
            particle.get_infection_status()
            particle.update_color()
            
        c = Counter([particle.infection_status for particle in self.particles])
        if c['Infected'] >= sum(c.values()) * self.when_measure_starts and not self.measure_enacted:
            for particle in self.particles:
                if random.random() <= self.pct_population_measure:
                    particle.speed *= self.measure_speed_decrease
                    particle.in_measure = True
                else:
                    particle.in_measure = False
            self.measure_enacted = True
        
        elif c['Infected'] < sum(c.values()) * self.when_measure_starts and self.measure_enacted:
            for particle in self.particles:
                if particle.in_measure:
                    particle.speed /= self.measure_speed_decrease
                    particle.in_measure = False
                    
            self.measure_enacted = False
            
        self.particle_status.append(c)        

    def bounce(self, particle):
        """ Tests whether a particle has hit the boundary of the environment """
        
        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity
    
    def get_infection_state(self):
        return Counter([p.infection_status for p in self.particles])
