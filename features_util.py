import redis

"""
Terminology:
    Interests - people who you've added in your circles
    Fans - people who've added you in their circles
    Friends - people who you've added and have added you in circles
"""
            
class Feature_Extractor:

    """
    Params: snapshot is filename of snapshot as string
    i.e for test-graph-2011-07-04.txt it will be 'test-graph-2011-07-04'
    """
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.r_server=redis.Redis("localhost")

    """
    Returns number of users in the snapshot
    Params: None
    """
    def num_users(self):
        return self.r_server.scard("%s:users" % (self.snapshot))

    """
    Returns a set of all uid's in the snapshot
    Params: None
    """
    def get_users(self):
        return self.r_server.smembers("%s:users" % (self.snapshot))

    """
    Returns a set of all uid's interests in the snapshot
    Params: uid as a string
    """
    def get_user_interests(self, uid):
        return self.r_server.smembers("%s:%s:interests" % (self.snapshot, uid))


    """
    Returns a set of all uid's fans in the snapshot
    Params: uid as a string
    """
    def get_user_fans(self, uid):
        return self.r_server.smembers("%s:%s:fans" % (self.snapshot, uid))


    """
    Returns a set of all uid's friends in the snapshot
    Params: uid as a string
    """
    def get_user_friends(self, uid):
        return self.r_server.sinter("%s:%s:interests" % (self.snapshot, uid), 
                                    "%s:%s:fans" % (self.snapshot, uid))

                                    
    """
    Returns a set of the two users' common friends
    Params: uid1 and uid2 as strings
    """
    def get_common_friends(self, uid1, uid2):
        uid1_friends = self.get_user_friends(uid1)
        uid2_friends = self.get_user_friends(uid2)
        return uid1_friends.intersection(uid2_friends)

        
    """
    Returns a list of tuples of test edges
    """
    def get_follow_only_edges(self):
        out = []
        all_users = toList(self.get_users())
        for user in all_users:
            interests = self.get_user_interests(user)
            fans = self.get_user_fans(user)
            people = toList(interests.difference(fans))
            for person in people:
                if person in all_users:
                    out.append((user, person))
        return out


"""
Extracts the values of a set into a list
"""
def toList(set):
    output = []
    while True:
        try:
            val = set.pop()
            output.append(val)
        except KeyError:
            break
    return output