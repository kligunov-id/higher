# Higher

A Rogue-like game where you climb a tower to the beats of the music

### Game rules

Your goal as a player is to stay on the falling tower for as long as possible.
Each beat you should move your player or use your abilities to climb the tower, while it will simultaneously fall down

### Controls

Basic player movement is controlled by **WASD** (*and not arrows*) keys. When the key is pressed *to the beat of music* the player will move one tile to the top, left, bottom or right correspondingly

Navigation through menues can be operated through both keyboard and mouse, with **WS** keys to browse through buttons, **AD** to choose entries from the list and **Escape** key to 

### Ablities

Abilities are additional actions that the player can perform *instead* of moving. They are actvated by **HJKL** keys, and you can freely bind any abilitiy set you want to theese keys via ability selection menu
Abilities, just like regular movement, must be activated *to the beat of music*

### Obstacles 

There are two main type of obstacles presented in the game - **walls** and **holes**. For the sake of "teleporting" abilities (only **Hop** for now) they are quite the same - when tried to teleport to them player will stay in place - but for the continous actions they differ. Player can freely move through **holes**, but can't stay on them and will roll back to the last free tile when trying to end movement on the **holes**. When trying to move into the wall, the player will stop the actions immediately, thus **Knight** abilities can be used to jump over **holes**, but not over **walls**

### Chunks

The map is generated by stitching together randomly chosen chunks from the prepared pool. As the game progressess, the more and more difficult chunks are loaded, resulting in difficulty increasing throughout the game

### Customization

Game allows to choose from a set of music tracks to play throughout the game. Keep in mind that those tracks regulate when the beats will appear, thus th e bpm of the track is affecting the game difficulty

Also you can customize the ability set used in game through special menu. You can swap default abilities for a new ones, or change their order to activate them by different keys
