# VirusSimulator - Simulating spread of viruses

Inspired by the [Washtington Post][1] and borrowing a lot of code from [Peter Collingridge][2], simulating how a virus spread under many different scenarios.


<img src="virology_expert.jpg">

## Blue, Purple, Red and Green persons show stages of the disease
Every sphere in the simulation is a person. The color of the person shows the stage of the disease in this person.


| Color  	| Status     	| Meaning                                                                                                                                                                                                                                                                  	|
|--------	|------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Blue   	| Healthy    	| A person has doesn't have the disease and hasn't had it either, and is therefore susceptible to the disease                                                                                                                                                              	|
| Purple 	| Incubation 	| A person that is infected, but does not show symptoms yet. This person cannot spread the disease. After a defined time, this person will turn infected. In the standard scenario, the disease does not have an incubation period, so purple persons do not exist 	|
| Red    	| Infected   	| A person that is infected by the disease and will spread it around when s/he collides with a Healthy person                                                                                                                                                              	|
| Green  	| Recovered  	| A person that has recovered from the disease, and is not susceptible to the virus anymore                                                                                                                                                                                	|


## Results show effects of every scenario
When no one is infected anymore, the simulation stops. When running multiple scenarios, the difference between te scenarios will be plotted: how many were infected at the same time (stretch on the health care system) and the total number of people that were infected (providing herd immunity).

## Options
* People characteristics
  * Population_size: how many people are in the simulation (default = 200)
  * speed: determines how quickly people move around (default = 1)
  * size: how wide one person can spread a virus (default = 4)
  * nr_infected: the number of people that are infected at the beginning (default = 2)
  * pct_quarantined: the percentage of (uninfected) people that do not move - ever (default = 0)
* Environment characteristics
  * height_pixels_per_person: to determine the concentration of people -> lower is more dense surrounding (default = 3)
  * Allow for distributions of speeds among the population (TO BE DONE)
* Disease
  * Incubation time (default = 0)
  * Chance of spreading (default = 1)
  * Time of disease (TO BE DONE, default = 500)
  * Mortality rate (TO BE DONE)
* Measures
  * when_measure_starts: Slowing people down while a percentage of the population is infected (default: 100%)
  * measure_speed_decrease: factor by which the people are slowed down (default=50%)
  * pct_population_meausre: percentage of the population that is slowed down by the measure (TO BE DONE) (default: 75%)

### Other to-do's
* Figure out why speed is so different for different size. Is this because larger scenarios require heavier calculations, therefore slowing the simulation down (as if the speed is slower), or is something else going on?
* Make one simulation easily runnable, e.g. by adding widgets to set the parameters

[1]:https://www.washingtonpost.com/graphics/2020/world/corona-simulator/
[2]:http://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/
 
