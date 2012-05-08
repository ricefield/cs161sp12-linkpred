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

def extract_values(set):
    output = []
    while True:
        try:
            val = set.pop()
            output.append(val)
        except IndexError:
            break
    return output