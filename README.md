# seating-plan-generator
Generates a seating plan which maximises the number of people who sit with a friend over multiple tables.

The library generates tables of specified number and size similar to the Greedy Traveling Salesman algorithm. Instead, this library thinks of the cities as people and the distances between them as, if they’re a friend or not (0m/1m).

See [example/example.py](example/example.py) for an example.

Used in a real dinner (200 people over 20 tables) where 92% sat on the same table as a friend.
