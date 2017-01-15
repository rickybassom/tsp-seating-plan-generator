from tsp_solver.greedy import solve_tsp  # Install this with "pip install tsp_solver"
from numpy import fill_diagonal, zeros

# from scipy import spatial
# from scipy.spatial.distance import pdist


class Person:
    def __init__(self, ident, name=None, friend_name=None):
        self.ident = ident
        self.name = name
        self.friend = None
        self.friend_name = friend_name
        self.table_allocated = False
        self.friend_on_table = False

    def __str__(self):
        return str(self.ident)


class Table:
    SEATS = 10

    def __init__(self, ident, num_seats=SEATS):
        self.ident = ident
        self.seats = num_seats
        self.occupant_list = []
        self.happiness = 0

    def __str__(self):
        return str(self.ident)


def solve(person_list, table_types):
    # Create a distance matrix of persons
    num_people = len(person_list)
    a = zeros((num_people, num_people))
    a[:] = 1.0
    fill_diagonal(a, 0.0)

    # Set distance to friends very small (0.0)
    for person in person_list:
        if person.friend is None: continue
        a[person_list.index(person), person_list.index(person.friend)] = 0.0
        a[person_list.index(person.friend), person_list.index(person)] = 0.0

    # print a
    # print spatial.distance.squareform(a)

    # Solve the TSP for the distance matrix
    path = solve_tsp(a)
    # print path

    # Create the ordered seating list
    seating_list = []
    for segment in path:
        seating_list.append(person_list[segment])

    # Create a table list
    table_list = []

    for key, value in table_types.items():
        for i in range(0, value):
            table_list.append(Table(i, num_seats=key))

    # Assign people to tables
    person_iter = iter(seating_list)
    for table in table_list:
        while len(table.occupant_list) < table.seats:
            try:
                table.occupant_list.append(next(person_iter))
            except:
                break

    return table_list


def get_happiness(table_list):
    overall_happiness = 0
    for table in table_list:
        happiness = 0
        for person in table.occupant_list:
            # print person, person.friend
            happiness += table.occupant_list.count(person.friend)
            # if person.friend in table.occupant_list : happiness += 1
        # print "-------"
        # print happiness
        # print
        table.happiness = happiness
        overall_happiness += happiness

    return overall_happiness
