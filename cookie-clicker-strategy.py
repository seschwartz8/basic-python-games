"""
Cookie Clicker Strategy Simulator by Sarah Schwartz 
(Skeleton and BuildInfo Class provided by Coursera)
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0 	
#SIM_TIME = 1000 #uncomment greater time when done testing

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0 #in seconds
        self._current_cps = 1.0
        #game history: tuples that track (time, item purchased, cost of item, cps of item)
        self._game_history = [(0.0, None, 0.0, 0.0)] 
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("Total cookies: " + str(self._total_cookies) + "\n"
                "Current cookies: " + str(self._current_cookies) + "\n"
                "Current time: " + str(self._current_time) + "\n"
                "Current cps: " + str(self._current_cps))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list in the form:
        (time, item, cost of item, total cookies)
        """
        return self._game_history

    def time_until(self, cookies):
        """
        Return seconds until you have the given number of cookies
        """
        #Calculate how many cookies you need until the given amount
        cookies_until = cookies - self._current_cookies
        #Calculate time it takes to get those cookies
        seconds_until = cookies_until / self._current_cps
        #Round up to next whole second
        seconds_until = math.ceil(seconds_until)
        if seconds_until > 0:
            return seconds_until
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            #Calculate cookies created during wait time
            cookies_created = time * self._current_cps
            #Update game state
            self._current_time = self._current_time + time
            self._current_cookies = self._current_cookies + cookies_created
            self._total_cookies = self._total_cookies + cookies_created
        else:
            return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies = self._current_cookies - cost
            self._current_cps = self._current_cps + additional_cps
            self._game_history.append((self._current_time, item_name, cost, self._total_cookies))
        else:
            return
    
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    #Clone BuildInfo object
    upgrades = build_info.clone()
    #Create ClickerState ojbect
    game = ClickerState()
    #Loop chosen strategy for the duration of the simulation
    while game.get_time() <= duration:
        item = strategy(game.get_cookies(), game.get_cps(), game.get_history(), (duration - game.get_time()), upgrades)
        if item == None:
            break
        elif item in upgrades.build_items():
            #Determine wait time until buying strategized item
            time = game.time_until(upgrades.get_cost(item))
            #Wait if within game duration
            if game.get_time() + time <= duration:
                game.wait(time)
            else:
                break
            #Buy item
            game.buy_item(item, upgrades.get_cost(item), upgrades.get_cps(item))
            #Update item price
            upgrades.update_item(item)
    #Collect final cookies with any leftover time and update game info
    if game.get_time() < duration:
        time_left = duration - game.get_time()
        game.wait(time_left)
    return game




def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    #Clone BuildInfo object
    upgrades = build_info.clone()
    #Initially store infinity
    item_cost = float("inf")
    cheapest_item = ""
    #Compare costs of items and store cheapest item name
    for item in upgrades.build_items():
        temp_cost = upgrades.get_cost(item)
        if temp_cost < item_cost and temp_cost <= (time_left * cps + cookies):
            cheapest_item = item
            item_cost = temp_cost
    if cheapest_item == "":
        return None
    else:
        return cheapest_item 

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    #Clone BuildInfo object
    upgrades = build_info.clone()
    #Initially store zero
    item_cost = 0.0
    expensive_item = ""
    #Compare costs of items and store expensive item name
    for item in upgrades.build_items():
        temp_cost = upgrades.get_cost(item)
        if temp_cost > item_cost and temp_cost <= (time_left * cps + cookies):
            expensive_item = item
            item_cost = temp_cost
    if expensive_item == "":
        return None
    else:
        return expensive_item 

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    Buy item with best value of cps to price
    """
    #Clone BuildInfo object
    upgrades = build_info.clone()
    #Calculate item's value
    chosen_item = ""
    chosen_value = 0.0
    #Compare item values and choose one with best value
    for item in upgrades.build_items():
        item_value = upgrades.get_cps(item) / upgrades.get_cost(item)
        if item_value > chosen_value and (upgrades.get_cost(item) <= 
                                        (time_left * cps + cookies)):
            chosen_item = item
            chosen_value = item_value
    if chosen_item == "":
        return None
    else:
        return chosen_item
        
    
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state


def run():
    """
    Run the simulator.
    """    
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    print
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    print
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()

