# --------------------------- #
# Intro to CS Final Project   #
# Gaming Social Network       #
# --------------------------- #
#
#-------------------------------------------------------------------------------
# Author:        Christopher Martinez
# Course:        Udacity's CS 101
# Date:          5/4/16
# Background:
#
# You and your friend have decided to start a company that hosts a gaming
# social network site. Your friend will handle the website creation (they know
# what they are doing, having taken our web development class). However, it is
# up to you to create a data structure that manages the game-network information
# and to define several procedures that operate on the network.
#
# In a website, the data is stored in a database. In our case, however, all the
# information comes in a big string of text. Each pair of sentences in the text
# is formatted as follows:
#
# <user> is connected to <user1>, ..., <userM>.<user> likes to play <game1>, ..., <gameN>.
#
# For example:
#
# John is connected to Bryant, Debra, Walter.John likes to play The Movie: The Game,
# The Legend of Corgi, Dinosaur Diner.
#
# Note that each sentence will be separated from the next by only a period. There will
# not be whitespace or new lines between sentences.
#
# Your friend records the information in that string based on user activity on
# the website and gives it to you to manage. You can think of every pair of
# sentences as defining a user's profile.
#
# Consider the data structures that we have used in class - lists, dictionaries,
# and combinations of the two (e.g. lists of dictionaries). Pick one that
# will allow you to manage the data above and implement the procedures below.
#
# You may assume that <user> is a unique identifier for a user. For example, there
# can be at most one 'John' in the network. Furthermore, connections are not
# symmetric - if 'Bob' is connected to 'Alice', it does not mean that 'Alice' is
# connected to 'Bob'.
#
# Project Description
# ====================
# Your task is to complete the procedures according to the specifications below
# as well as to implement a Make-Your-Own procedure (MYOP). You are encouraged
# to define any additional helper procedures that can assist you in accomplishing
# a task. You are encouraged to test your code by using print statements and the
# Test Run button.
# -----------------------------------------------------------------------------

# Example string input to test code
example_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

# -----------------------------------------------------------------------------

def create_data_structure(string_input):
    """Parses a string to create a data structure for the Gaming Social Network.

    Arguments:
      string_input: a specifically structured block of text of the form:

      "Name_1 is connected to friend_1, friend_2, ..., friend_n.
       Name_1 likes to play game_1, game_2, ..., game_n.
       Name_2 is connected to friend_1, friend_2, ..., friend_n.
       Name_2 likes to play game_1, game_2, ..., game_n.
       ..."
       NOTE: no spaces after each '.'

    Return: a data structure of the form:

    {'con': {'name_1': [connections, ...], 'name_2': [connections, ...]},
     'gam': {'name_1': [games, .........], 'name_2': [games, .........]}}

    Conor Cases:
    If the string_input is an empty string, return a network with no users.
    """
    # Initialize the Gaming Social Network data structure
    network = {'con':{}, 'gam':{}}

    # Corner case: if string_input is an empty string, return an empty network
    if string_input == '':
        return {'con':{}, 'gam':{}}

    while string_input:
        # Extract and store the relevant "connections" data for the current
        # person
        start_con_phrase = string_input.find('is connected to')
        end_con_phrase = start_con_phrase + len('is connected to')
        next_period = string_input.find('.')
        name = string_input[:start_con_phrase - 1]
        connections_str = string_input[end_con_phrase + 1:next_period]
        connections_list = connections_str.split(', ')
        network['con'][name] = connections_list

        # Update string_input after extracting "connections" data for the
        # current person
        string_input = string_input[next_period + 1:]

        # Extract and store the relevant "games" data for the current person
        start_gam_phrase = string_input.find('likes to play')
        end_gam_phrase = start_gam_phrase + len('likes to play')
        next_period = string_input.find('.')
        name = string_input[:start_gam_phrase - 1]
        games_str = string_input[end_gam_phrase + 1:next_period]
        games_list = games_str.split(', ')
        network['gam'][name] = games_list

        # Update string_input after extracting "games" data for the current
        # person
        string_input = string_input[next_period + 1:]

    return network


def get_connections(network, user):
    """ Returns a list of all the connections that a user has.

    Arguments:
      network: a data structure for the Gaming Social Network
      user:    a string containing the name of the user

    Return:
      A list of all connections the user has.
      - If the user has no connections, return an empty list.
      - If the user is not in the network, return None.
    """
    # Check if the network has any users
    network_has_users = check_users(network)
    if network_has_users:
        # Check if the user is in the network
        user_in_network = check_user_in_network(network, user)
        if not user_in_network:
            return None
        # Check if the user has any connections
        user_has_connections = check_connections(network, user)
        if user_has_connections:
            return network['con'][user]
        # Else the user does not have any connections
        else:
            return []
    # Else the network does not have any users
    else:
        return None


# Helper function for get_connections and get_games_liked
def check_users(network):
    """Returns True if the network has at least one user, False otherwise.

    Arguments:
      network: a data structure for the Gaming Social Network
    """
    if network['con'] == {}:
        return False
    else:
        return True


# Helper function for get_connections
def check_connections(network, user):
    """Returns True if the user has at least one connection in the network,
       False otherwise."""
    if network['con'][user] == []:
        return False
    else:
        return True


# Helper function for get_connections and get_games_liked
def check_user_in_network(network, user):
    """Returns True if the user is in the network, False otherwise."""
    if user in network['con']:
        return True
    else:
        return False


def get_games_liked(network, user):
    """Returns a list of all the games a user likes.

    Arguments:
      network: a data structure for the Gaming Social Network
      user:    a string containing the name of the user

    Return:
      A list of all games the user likes.
      - If the user likes no games, return an empty list.
      - If the user is not in network, return None.
    """
    # Check if the network has any users
    network_has_users = check_users(network)
    if network_has_users:
        # Check if the user is in the network
        user_in_network = check_user_in_network(network, user)
        if not user_in_network:
            return None
        # Check if the user has any liked games
        user_has_games = check_games(network, user)
        if user_has_games:
            return network['gam'][user]
        # Else the user does not have any games
        else:
            return []
    # Else the network does not have any users
    else:
        return None


# Helper function for get_games_liked
def check_games(network, user):
    """Returns True if the user has at least one liked game in the network,
       False otherwise."""
    if network['gam'][user] == []:
        return False
    else:
        return True


def add_connection(network, user_A, user_B):
    """Adds a connection from user_A to user_B if both users exist in the network.

    Arguments:
      network: a data structure for the Gaming Social network
      user_A:  a string with the name of the user the connection is from
      user_B:  a string with the name of the user the connection is to

    Return:
      The updated network with the new connection added.
      - If a connection already exists from user_A to user_B, return the
        network unchanged.
      - If user_A or user_Ab is not in the network, return False.
    """
    # Check that both users are in the network
    user_A_in_network = check_user_in_network(network, user_A)
    user_B_in_network = check_user_in_network(network, user_B)
    if not user_A_in_network or not user_B_in_network:
        return False
    # Check that a connection doesn't already exist from user_A to user_B
    connections_for_user_A = get_connections(network, user_A)
    if user_B not in connections_for_user_A:
        network['con'][user_A].append(user_B)
        return network
    # Else a connection from user_A to user_B already exists, so return the
    # network unchanged
    else:
        return network


def add_new_user(network, user, games):
    """ Creates a new user profile and adds that user to the network, along with
    any game preferences specified in games. Assumes that the user has no
    connections to begin with.

    Arguments:
      network: a data structure for the Gaming Social Network
      user:    a string containing the name of the user to be added to the network
      games:   a list of strings containing the user's favorite games, e.g.:
               ['Ninja Hamsters', 'Super Mushroom Man', 'Dinosaur Dinner']

    Return:
      the updated network with the new user and game preferences added. The
      new user should have no connections.
      - If the user already exists in network, return network *UNCHANGED*
        (do not change the user's game preferences)
    """
    # If the user is already in the network, return the network unchanged
    user_in_network = check_user_in_network(network, user)
    if user_in_network:
        return network
    # Else add the user: without any connections and with the given games list
    else:
        network['con'][user] = []
        network['gam'][user] = games
        return network


def get_secondary_connections(network, user):
    """Finds all the secondary connections (i.e. connections of connections) of
    a given user.

    Arguments:
      network: a data structure for the Gaming Social Network
      user:    a string containing the name of the user

    Return:
      A list containing the secondary connections (connections of connections).
      - If the user is not in the network, return None.
      - If a user has no primary connections to begin with, return an empty list.

    NOTE:
      It is OK if a user's list of seconday connections includes the user
      himself/herself. It is also OK if the list containing a user's primary
      connection that is a secondary connection as well.
    """
    # Check if the user is in the network
    user_in_network = check_user_in_network(network, user)
    if user_in_network:
        # If the user has no primary connections, return an empty list
        if network['con'][user] == []:
            return []
        # Else the user does have primary connections, so find and return a
        # list of secondary connections
        else:
            L = []
            for connection in network['con'][user]:
                for secondary_connection in network['con'][connection]:
                    if secondary_connection not in L:
                        L.append(secondary_connection)
            return L
    # Else the user is not in the network
    else:
        return None


def count_common_connections(network, user_A, user_B):
    """Finds the number of people that user_A and user_B have in common.

    Arguments:
      network: a data structure for the Gaming Social Network
      user_A:  a string containing the name of user_A
      user_B:  a string containing the name of user_B

    Return:
      The number of connections in common (as an integer).
      - If user_A or user_B is not in network, return False.
    """
    count = 0
    # Check if both users are in the network. If either user_A or user_B are
    # not in the network, return False.
    user_A_in_network = check_user_in_network(network, user_A)
    user_B_in_network = check_user_in_network(network, user_B)
    if not user_A_in_network or not user_B_in_network:
        return False
    # Else both user_A and user_B are in the network, so count their common
    # connections
    else:
        for connection_A in network['con'][user_A]:
            if connection_A in network['con'][user_B]:
                count += 1
        return count


def find_path_to_friend(network, user_A, user_B, checked=None, in_network=None):
    """Find a connections path from user_A to user_B. It has to be an existing
    path, but it DOES NOT have to be the shortest path.

    Arguments:
      network: a data structure for the Gaming Social network
      user_A:  a string containing the name of user_A
      user_B:  a string containing the name of user_B

    Return:
      A list showing the path from user_A to user_B.
      - If such a path does not exist, return None.
      - If user_A or user_B is not in the network, return None.

    Sample output:
      >>> print(find_path_to_friend(network, 'Abe', 'Zed'))
      >>> ['Abe', 'Gel', 'Sam, 'Zed']
      This implies that Abe is connected with Gel, who is connected with Sam,
      who is connected with Zed.
    """
    # For this project, Udacity's auto-grader restricts the use of default
    # parameters that are lists. The below if-statement is a workaround.
    if checked == None:
        checked = []

    # On the initial call to find_path_to_friend, check if both users are in the
    # network. If they are not in the network, return None.
    if in_network == None:
        user_A_in_network = check_user_in_network(network, user_A)
        user_B_in_network = check_user_in_network(network, user_B)
        if user_A_in_network and user_B_in_network:
            in_network = True
        else:
            return None

    # If both users are in the network, find the path to friend.
    if in_network:
        # Initialize the path to include the seed user.
        path = [user_A]
        # Add the seed user to the list of users already checked.
        checked.append(user_A)
        # Get the list of connections for the current user.
        connections = get_connections(network, user_A)
        # If the target user is in the connections of the current user, return
        # the result of appending the target user to the end of the current path.
        if user_B in connections:
            return path + [user_B]
        # Else the target user is not in connections of the current user, so loop
        # through the connections of the current user to see if the target user
        # is in the connections of the connections of the target user. Keep doing
        # this until a valid path to the target user is found (recursively).
        else:
            for person in connections:
                if person not in checked:
                    new_path = find_path_to_friend(network, person, user_B, checked, in_network)
                    if new_path:
                        return path + new_path
        return None

# Make-Your-Own-Procedure (MYOP)
# -----------------------------------------------------------------------------
# Your MYOP should either perform some manipulation of your network data
# structure (like add_new_user) or it should perform some valuable analysis of
# your network (like path_to_friend). Don't forget to comment your MYOP. You
# may give this procedure any name you want.

# Replace this with your own procedure! You can also uncomment the lines below
# to see how your code behaves. Have fun!
# TODO: Finish the MYOP portion when you have time

net = create_data_structure(example_input)
#print(get_connections(net, 'Alice'))
#print get_connections(net, "Debra")
#print get_games_liked(net, "John")
#print(add_connection(net, "John", "Freda"))
#print(add_new_user(net, "Debra", []))
#print(add_new_user(net, "Nick", ["Seven Schemers", "The Movie: The Game"])) # True
# print(get_secondary_connections(net, "Freda"))
# print(get_secondary_connections(net, "Mercedes"))
#print count_common_connections(net, "Mercedes", "John")
#print(find_path_to_friend(net, "John", "Freda"))

# network = create_data_structure('')
# print(network)
# network = add_new_user(network, 'Alice', [])
# print(network)
# network = add_new_user(network, 'Bob', [])
# print(network)
# network = add_new_user(network, 'Carol', [])
# print(network)
# network = add_connection(network, 'Alice', 'Bob')
# print(network)
#print(find_path_to_friend(net, 'John', 'Jennie'))