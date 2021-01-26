# Lab Hack
> A Roguelike Venture in Super-Science!

# Phase 1: Easy Revisions:
* todo: Change (E) to Equipped (change window size?)

* todo: Sorted inventory 

* todo: Remove "that way is blocked for walls."

* todo: Add player level to status bar.
* todo: Add power, defense, to status bar.
* todo: Add turns to status bar.
* todo: Change player XP points to standard, instead of just the amount needed to level up.

### Refactoring:
* todo: Move main functionality to engine
* todo: Add tests for map generation, procgen
* todo: Add skeleton tests for other things that are testable...
* todo: Replace deprecated tcod.fov functions with updated versions.
* todo: Rendering constants to make it easier to manipulate and read.
	RENDERING = { HP_BAR }
* test game_map and procgen
* Test components and actions?

### Monsters and Items
* todo: Raise the orc damage so it goes through leather armor.
* todo: Track monsters kills.
* todo: Add better msg to drinking healing potion.
* todo: Add random monster placement generator
* todo: Add python typing???
* todo: When monsters die, converted them to Items so we can pick them up!
* todo: Made the radius of FOV a smaller.
* todo: Infravision?
* todo: Remember where items were

# Phase 2: Making the project FUN!
* todo: Robots
* todo: Classic nethack monsters
* todo: Genetic Experiments
* todo: Monster Variations
* todo: Aliens
* todo: Operatives
* todo: Normal/Real monsters
* todo: Items
* todo: New potions/vials
* todo: Melee weapons
* todo: Ranged weapons
* todo: Explosives
* todo: Firearms
* todo: Map features, traps, rooms

# Phase 3: Major Updates
* todo: Add monster info to each monster
* todo: Monsters get random items, weapons, armor
* todo: Death drops
* todo: Dnotation style damage
* todo: logging
* todo: up-stairs tile and ability to backtrack
* todo: Graceful exit for going up first level stair.
* todo: Speed system
* todo: Randomized descriptions for items
* todo: multi layered FOV, you have 2 radius - immediate and far. We cannot make out far away monsters, but they can follow us.
* todo: A basic stationary shopkeeper

### Other possible additions/revisions:
* Scene Management
* Event Management/Messaging
* Data-Driven Design (over ECS)

* Make the Engine a class and pass the engine to the renderer
* Each state has a separate render/draw function, and is passed the current game engine as an argument. That way you can segregate code for each screen and keep your render functions small, easy to read, and fast to compile.

* http://gamedevgeek.com/tutorials/managing-game-states-in-c/




# Resources and tutorials
* [DONE]: http://rogueliketutorials.com/tutorials/tcod/v2/
* todo: https://www.reddit.com/r/roguelikedev/comments/dsv9lq/roguelike_tutorial_hypothetical_extended_version/
* todo: http://rogueliketutorials.com/tutorials/tcod/
* todo: http://bfnightly.bracketproductions.com/rustbook/
* todo: https://users.freebasic-portal.de/rdc/tutorials.html#mozTocId58846

https://github.com/aBrydson/fun-with-python-tcod.git

https://www.reddit.com/r/roguelikedev/comments/al06ab/exercise_ideas_for_libtcod/
* convert field-of-view to use the Map class in python-tcod. It introduced the numpy ndarray and it took me ages to get it working properly.
* Use rexpaint to draw a map of a region, with different background_colours for each country. Then using tcod load a console from the .xp file. Use mouse coordinates (cx,cy) to check the background colour of the cell against a dict of 'origins' which have the RGB of the background as the value - then print the key (the country's name) to a separate offscreen console. Then blit that console to the root, slightly offset from the mouse point. You don't need to use rexpaint (though it is super-handy) - the aim here is to understand how to index the console.bg array , so any console with two different background colours would work.

* Fade from one offscreen console to another (a loading image and the aforementioned map in my case) using the console's bg_alpha and fg_alpha values. Thinking about it this might be the easiest of the three, but maybe because that's because I did it recently...



### Features
* Component System
* Event Handling System
* Potions, Scrolls
* Basic Monster AI

### Tutorials Completed
* [DONE] http://rogueliketutorials.com/tutorials/tcod/v2/
* https://www.reddit.com/r/roguelikedev/comments/dsv9lq/roguelike_tutorial_hypothetical_extended_version/
* http://rogueliketutorials.com/tutorials/tcod/
* http://bfnightly.bracketproductions.com/rustbook/


# DONE:

* DONE: , to pickup
* DONE: Ctrl-X for character info
* DONE: Make sure title and messages reflect the LabHack theme.
* SKIPPED: Add more science lab look to colors, gray/white
* DONE: Removed HP from attack msg, instead say "hits"
* DONE: Remove msg for gaining xp.
* DONE: Say "the xxx dies", instead
* DONE: Add ability to view messages after death
* DONE: Remove level-up menu, make random instead.
* SKIPPED: Remove color from message console
* DONE: Extend the length of the message box
* DONE: Move message rendering from the MessageLog to rendering_functions.
* DONE: Move game_map rendering to rendering_functions
* DONE: Go through and extract out obvious magic numbers, constants.
* DONE: Convert src and tests files to package import format.
* SKIPPED: Break out actions to separate files in directory. messy...
* DONE: Refactor keys and inputs
* DONE: Move Actor to own file
* DONE: Move Item to own file
* DONE: Move GameWorld to own file
* DONE: Move Rect.. to own file
* SKIPPED: Rename Impossible to ImpossibleException
* DONE: Make sure confusion can't make monsters hit themselves.
* SKIPPED: Break input handlers apart to separate files.
* DONE: Move MainMenu class to input_handlers.
* DONE: Move message box to top of screen
* DONE: Separate root console
* DONE: Separate map panel
* DONE: Separate msg panel
* DONE: Separate stat panel
