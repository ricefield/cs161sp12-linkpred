import redis

"""
Terminology: 
    Interests(IN) - people who you've added in your circles
    Fans(FA) - people who've added you in their circles
    Friends(FR) - people who you've added and have added you in circles
"""


"""
Enum for all the mutual neighbor types
"""
class Mutual_Neighbor:
    FR_OF_FR, FA_OF_FA, IN_OF_IN, FR_OF_IN, FR_OF_FAN, FA_OF_IN, FA_OF_FR, IN_OF_FA, IN_OF_FR = range(9) 


"""
Enum for all neighbor types
"""
class Neighbor_Type:
    FR, FA, IN = range(3)

    
class Feature_Extractor:

    TEST_SIZE = 1000

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
    Returns a set of the two users' common interests 
    Params: uid1 and uid2 as strings 
    """
    def get_common_interests(self, uid1, uid2):
        uid1_interests = self.get_user_interests(uid1)
        uid2_interests = self.get_user_interests(uid2)
        return uid1_interests.intersection(uid2_interests)


    """ 
    Returns a set of the two users' common fans
    Params: uid1 and uid2 as strings 
    """
    def get_common_fans(self, uid1, uid2):
        uid1_fans = self.get_user_fans(uid1)
        uid2_fans = self.get_user_fans(uid2)
        return uid1_fans.intersection(uid2_fans)


    """ 
    Returns jaccard's coefficient as a float for two users.
    Params: uid1 and uid2 as strings and use enums (Neighbor_Type and
            Mutual_Neighbor) defined above for neighbor types and mutual
            neighbor type. For mutual neighbor type it is what uid2 is to uid1
    """
    def get_jaccard(self, uid1, uid2, neighbor_type, mutual_neighbor_type):
        #jaccard is intersectin of neighbors(common neighbors) over all neighbors
        #9 different types of mutual neighbors 3 different types of neighbors
        neighbor_num = {Neighbor_Type.FR : len(self.get_user_friends(uid1)) + len(self.get_user_friends(uid2)),
                        Neighbor_Type.FA : len(self.get_user_fans(uid1)) + len(self.get_user_fans(uid2)),
                        Neighbor_Type.IN : len(self.get_user_interests(uid1)) + len(self.get_user_interests(uid2))}

        mutual_n_num = {Mutual_Neighbor.FR_OF_FR : len(self.get_common_friends(uid1, uid2)),
                       
                       Mutual_Neighbor.FA_OF_FA : 
                       len(self.get_user_fans(uid1).intersection(self.get_user_interests(uid2))),
                       
                       Mutual_Neighbor.IN_OF_IN : 
                       len(self.get_user_interests(uid1).intersection(self.get_user_fans(uid2))),
                       
                       Mutual_Neighbor.FR_OF_FA : 
                       len(self.get_user_fans(uid1).intersection(self.get_user_friends(uid2))),
                       
                       Mutual_Neighbor.FR_OF_IN : 
                       len(self.get_user_interests(uid1).intersection(self.get_user_friends(uid2))),

                       Mutual_Neighbor.FA_OF_FR :
                       len(self.get_user_friends(uid1).intersection(self.get_user_interests(uid2))),

                       Mutual_Neighbor.FA_OF_IN :
                       len(self.get_common_interests(uid1, uid2)),

                       Mutual_Neighbor.FR_OF_FA : 
                       len(self.get_user_fans(uid1).intersection(self.get_user_friends(uid2))),

                       Mutual_Neighbor.FR_OF_IN :
                       len(self.get_user_interests(uid1).intersection(self.get_user_friends(uid2))),

                       Mutual_Neighbor.IN_OF_FA :
                       len(self.get_common_fans(uid1,uid2)),

                       Mutual_Neighbor.IN_OF_FR :
                       len(self.get_user_friends(uid1).intersection(self.get_user_fans(uid2))),
                       }
        
        return float(mutual_n_num[mutual_neighbor_type]) / neighbor_num[neighbor_type]


    """
    Returns a list of tuples (a,b) containing only follows
    (so a->b but not b->a)
    """
    def get_follow_only_edges(self):
        out = []
        all_users = list(self.get_users())
        i = 0
        for user in all_users:
            i += 1
            print i
            if i > Feature_Extractor.TEST_SIZE:
                break
            interests = self.get_user_interests(user)
            fans = self.get_user_fans(user)
            people = list(interests.difference(fans))
            for person in people:
                if person in all_users:
                    out.append((user, person))
        return out
   

    """
    Returns a list of results (True/False) for the list of tuples (a,b) indicating
    whether b followed back a
    """
    def get_results(self, edges):
        result = []
        all_users = list(self.get_users())
        for (p1, p2) in edges:
            if p1 in all_users and p2 in all_users and p2 in list(self.get_user_fans(p1)):
                result.append(True)
            else:
                result.append(False)
        return result
            
