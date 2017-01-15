import seatingplangenerator
import signal
import os
import random


# Read the person list in from the CSV file
def get_persons():
    person_list = []
    with open('sample.csv', 'r') as infile:
        for index, line in enumerate(infile):
            temp_list = line.split(",")
            print(temp_list)
            person, friend = temp_list[0], temp_list[1].strip()
            if len(friend) == 0:
                friend = None
            # print person, friend
            person_list.append(seatingplangenerator.Person(index, name=person, friend_name=friend))

    # Allocate designated friends to each person
    for person1 in person_list:
        # print person1.name, "-", person1.friend_name
        for person2 in person_list:
            if person1.friend_name is None: continue
            if person2.name.lower() == person1.friend_name.lower():
                person1.friend = person2

    print("")
    for person in person_list:
        if person.friend is None:
            print(person.name + " - ")
        else:
            print(person.name + " - " + person.friend.name)

    return person_list

# Print results for best result
def print_results():
    print("no friends = " + str(NO_FRIENDS_NUM))
    for table in best_result:
        print("")
        print("Table: " + str(table.ident) + " - " + str(table.seats) + " seats")
        # for person in table.occupant_list : print person, person.friend
        for person in table.occupant_list:
            if person.friend is None:
                print(person.name)
            else:
                print(person.name)
        print("-----------")
        print("Happiness: " + str(table.happiness))
        print("-----------")
    print("Total Happiness: " + str(best_happiness) + "/" + str(NUM_PEOPLE - NO_FRIENDS_NUM))


# =====================================================================#
#  A signal handler so that if the process is killed it closes down
#  elegantly rather than crashing and burning.
# =====================================================================#

def signalHandler(signum, frame):
    print_results()
    if signum == signal.SIGINT: os._exit(0)


if __name__ == '__main__':
    # Add some signal handlers to trap SIGINT and SIGTSTP ctrl-z to monitor progress
    signal.signal(signal.SIGTSTP, signalHandler)
    signal.signal(signal.SIGINT, signalHandler)

    """
    # Create random people and friends
    NUM_PEOPLE = 198

    # Create person list
    for i in range(0,NUM_PEOPLE) : main_person_list.append(Person(i))

    # Assign friends to persons randomly
    for person in main_person_list :
        while True:
            friend = random.choice(main_person_list)
            if friend is not person :
                person.friend = friend
                break
    """

    table_types = {4: 5, 3: 2} # 5 "four-man" table, two "three-man" tables

    # Read the person list in from the CSV file
    main_person_list = get_persons()
    NUM_PEOPLE = len(main_person_list)

    global NO_FRIENDS_NUM
    NO_FRIENDS_NUM = 0
    for person in main_person_list:
        if person.friend == None:
            NO_FRIENDS_NUM += 1

    best_happiness = 0
    # Shuffle, solve and calculate happiness - get the best in many attempts
    for i in range(0, 100000):
        random.shuffle(main_person_list)
        tables_result = seatingplangenerator.solve(main_person_list, table_types)

        happiness = seatingplangenerator.get_happiness(tables_result)
        average_happiness = float(happiness) / len(main_person_list)
        print("Total happiness: " + str(happiness) + " Average table happiness: " + str(average_happiness))

        if happiness > best_happiness:
            best_happiness = happiness
            best_result = list(tables_result)

    # Print results for best result
    print_results()
