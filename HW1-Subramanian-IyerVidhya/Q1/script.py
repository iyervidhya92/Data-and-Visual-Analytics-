import csv
import json
import time
import tweepy


# You must use Python 2.7.x

# 1 point
def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    with open('keys.json') as keys_file:
        keys = json.load(keys_file)
    return keys['api_key'], keys['api_secret'], keys['token'], keys['token_secret']


# 4 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    # Add code here to populate primary_friends
    for friend in tweepy.Cursor(api.friends, screen_name=root_user).items(no_of_friends):
        primary_friends.append((str(root_user), str(friend.screen_name)))
    return primary_friends


# 4 points
def getNextLevelFriends(api, users_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each user in users_list
    # rtype: list containing entries in the form of a tuple (user, friend)
    next_level_friends = []
    # Add code here to populate next_level_friends
    for user in users_list:
        next_level_friends.extend(getPrimaryFriends(api,user, no_of_friends))
    return next_level_friends

def getPrimaryFollowers(api, root_user, no_of_followers):
    primary_followers = []
    for follower in tweepy.Cursor(api.followers, screen_name=root_user).items(no_of_followers):
        primary_followers.append((str(follower.screen_name), str(root_user)))
    return primary_followers

# 4 points
def getNextLevelFollowers(api, users_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each user in users_list
    # rtype: list containing entries in the form of a tuple (follower, user)
    next_level_followers = []
    # Add code here to populate next_level_followers
    for users in users_list:
        next_level_followers.extend(getPrimaryFollowers(api, users, no_of_followers))
    return next_level_followers


# 3 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.
    all_edges = []
    # Add code here to populate all_edges
    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    all_edges.extend(primary_friends)
    friends_list = [x[1] for x in primary_friends]
    next_level_friends = getNextLevelFriends(api, friends_list, no_of_neighbours)
    all_edges.extend(next_level_friends)
    next_level_followers = getNextLevelFollowers(api, friends_list, no_of_neighbours)
    all_edges.extend(next_level_followers)
    print all_edges
    return all_edges


# 2 points
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    #data = list(set(data))
    with open(output_file, 'w') as out:
            writer = csv.writer(out)
            writer.writerow(['Source','Target'])
            writer.writerows(data)


"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""


def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth, timeout = 50, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)


if __name__ == '__main__':
    testSubmission()

