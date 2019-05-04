# Multiverse

Write a simulation engine
and use classes to encapsulate data and functionality.
Have (potentially) many universes
and many individuals. Each individual is initially in their own universe at a specified location.

Each condition is checked in the same order the individuals are
given from the input file:
1. If an individual passes near a location with treasure, she picks it up. As she carries more
items, her speed goes down under the weight. The speed change will impact either dx or dy
as they shift left to right.
If the magnitude (absolute value) of a person’s speed drops below 10 in either the x or y
directions, she stops moving. Stopped individuals will no longer move in later steps.
2. If an individual reaches the edge of the board, then she stops moving. Check for the center
of the individual being passed or at the border.
3. If two individuals hit each other while moving, they each drop the first reward they picked up
(if they have any). The reward returns to its original location. Note that dropping a reward
increases a person’s speed. After a collision, both individuals begin moving in the opposite
direction with their new speed.
4. If an individual comes near the location of a portal, then she moves to a different universe
that this portal points to. In the next simulation step, she will continue her journey in that
new universe.
