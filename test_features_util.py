import features_util

f = features_util.Feature_Extractor('test-graph-2011-07-04')

users = list(f.get_users())

print ""
print ""
print "neighbors type FA of %s: " % users[0], f.get_neighbors(users[0], features_util.Neighbor_Type.FA)
print "neighbors type IN of %s: " % users[0], f.get_neighbors(users[0], features_util.Neighbor_Type.IN)
print "neighbors type FR of %s: " % users[0], f.get_neighbors(users[0], features_util.Neighbor_Type.FR)
print "neighbors type FR of %s: " % users[1], f.get_neighbors(users[1], features_util.Neighbor_Type.FR)
print ""
print ""
print "mutual neighbors type FR_OF_FR of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.FR_OF_FR)
print "mutual neighbors type IN_OF_IN of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.IN_OF_IN)
print "mutual neighbors type FA_OF_FA of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.FA_OF_FA)
print "mutual neighbors type FR_OF_FA of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.FR_OF_FA)
print "mutual neighbors type FR_OF_IN of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.FR_OF_IN)
print "mutual neighbors type IN_OF_FR of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.IN_OF_FR)
print "mutual neighbors type IN_OF_FA of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.IN_OF_FA)
print "mutual neighbors type FA_OF_FR of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.FA_OF_FR)
print "mutual neighbors type FA_OF_IN of %s, %s :" % (users[0], users[1]), f.get_mutual_neighbors(users[0], users[1], features_util.Mutual_Neighbor.FA_OF_IN)
print ""
print ""
print "pref attachment of %s, %s :" %(users[0], users[1]), f.get_pref_attachment(users[0], users[1], features_util.Neighbor_Type.FR)
print "adamic/adar FR, FR of FR of %s, %s: " %(users[0], users[1]), f.get_adamic(users[0], users[1], features_util.Neighbor_Type.FR, features_util.Mutual_Neighbor.FR_OF_FR)
print "jaccard FR, FR of FR of %s, %s: " %(users[0], users[1]), f.get_jaccard(users[0], users[1], features_util.Neighbor_Type.FR, features_util.Mutual_Neighbor.FR_OF_FR)
