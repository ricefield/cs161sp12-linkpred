import math
import redis

"""
Terminology: 
    Interests(IN) - people who you've added in your circles
    Fans(FA) - people who've added you in their circles
    Friends(FR) - people who you've added and have added you in circles

    I use common neighbors and mutual neighbors interchangeably.
"""


"""
Enum for all the mutual neighbor types
"""
class Mutual_Neighbor:
    FR_OF_FR, FA_OF_FA, IN_OF_IN, FR_OF_IN, FR_OF_FA, FA_OF_IN, FA_OF_FR, IN_OF_FA, IN_OF_FR = range(9) 


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
    def __init__(self, snapshot, DEBUG = False):
        self.snapshot = snapshot
        self.r_server=redis.Redis("localhost")
        self.DEBUG = DEBUG


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
    Returns set of all_mutual_neighbors of the specified type
    Params: uid as string, neighbor_type(use one of the Neighbor_Type enums)
    """
    def get_mutual_neighbors(self, uid1, uid2, mutual_neighbor_type):
       
        mutual_neighbors = {Mutual_Neighbor.FR_OF_FR : self.get_common_friends(uid1, uid2),
                       
                       Mutual_Neighbor.FA_OF_FA : 
                       self.get_user_fans(uid1).intersection(self.get_user_interests(uid2)),
                       
                       Mutual_Neighbor.IN_OF_IN : 
                       self.get_user_interests(uid1).intersection(self.get_user_fans(uid2)),
                       
                       Mutual_Neighbor.FR_OF_FA : 
                       self.get_user_fans(uid1).intersection(self.get_user_friends(uid2)),
                       
                       Mutual_Neighbor.FR_OF_IN : 
                       self.get_user_interests(uid1).intersection(self.get_user_friends(uid2)),

                       Mutual_Neighbor.FA_OF_FR :
                       self.get_user_friends(uid1).intersection(self.get_user_interests(uid2)),

                       Mutual_Neighbor.FA_OF_IN :
                       self.get_common_interests(uid1, uid2),

                       Mutual_Neighbor.FR_OF_FA : 
                       self.get_user_fans(uid1).intersection(self.get_user_friends(uid2)),

                       Mutual_Neighbor.FR_OF_IN :
                       self.get_user_interests(uid1).intersection(self.get_user_friends(uid2)),

                       Mutual_Neighbor.IN_OF_FA :
                       self.get_common_fans(uid1,uid2),

                       Mutual_Neighbor.IN_OF_FR :
                       self.get_user_friends(uid1).intersection(self.get_user_fans(uid2)),
                       }

        return mutual_neighbors[mutual_neighbor_type]


    """
    Returns set of all neighbors of the specified type
    Params: uid as string, neighbor_type(use one of the Neighbor_Type enums)
    """
    def get_neighbors(self, uid, neighbor_type):
        neighbors = {Neighbor_Type.FR : self.get_user_friends(uid),
                     Neighbor_Type.FA : self.get_user_fans(uid),
                     Neighbor_Type.IN : self.get_user_interests(uid)}

        return neighbors[neighbor_type]


    """ 
    Returns jaccard's coefficient as a float for two users.
    Params: uid1 and uid2 as strings and use enums (Neighbor_Type and
            Mutual_Neighbor) defined above for neighbor types and mutual
            neighbor type. For mutual neighbor type it is what uid2 is to uid1
    """
    def get_jaccard(self, uid1, uid2, neighbor_type, mutual_neighbor_type):
        #jaccard is intersectin of neighbors(common neighbors) over all neighbors
        #9 different types of mutual neighbors 3 different types of neighbors
        neighbors_intersection = len(self.get_mutual_neighbors(uid1, uid2, mutual_neighbor_type))
        all_neighbors = len(self.get_neighbors(uid1, neighbor_type)) + len(self.get_neighbors(uid2, neighbor_type))
        
        return float(neighbors_intersection)/all_neighbors


    """ 
    Returns adamic/adar as a float for two users.
    Params: uid1 and uid2 as strings and use enums (Neighbor_Type and
            Mutual_Neighbor) defined above for neighbor types and mutual
            neighbor type. For mutual neighbor type it is what uid2 is to uid1
    """
    def get_adamic(self, uid1, uid2, neighbor_type, mutual_neighbor_type):
        #sum over all common neighbor(9 types) and for each common neighbor 1/log(# neighbors each common
        #neighbor has(3 types)
        result = 0.0
        mutual_neighbors = self.get_mutual_neighbors(uid1, uid2, mutual_neighbor_type) 
        
        for n in mutual_neighbors:
            neighbor_count = len(self.get_neighbors(n, neighbor_type))
            if neighbor_count != 0:
                result +=  ( 1 / float(math.log(neighbor_count)) )
        
        return result

    """ 
    Returns Preferential attachment as an integer for two users.
    Params: uid1 and uid2 as strings and use enums (Neighbor_Type)
            defined above for neighbor_type param    
    """
    def get_pref_attachment(self, uid1, uid2, neighbor_type):
        uid1_neighbors = self.get_neighbors(uid1, neighbor_type)
        uid2_neighbors = self.get_neighbors(uid2, neighbor_type)
        return len(uid1_neighbors) * len(uid2_neighbors)


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
            if DEBUG:
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
        i = 0
        for (p1, p2) in edges:
            i += 1
            if DEBUG:
                print i
            if p1 in all_users and p2 in all_users and p2 in list(self.get_user_fans(p1)):
                result.append(True)
            else:
                result.append(False)
        return result
            
