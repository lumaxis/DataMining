import recommendations
import operator

# Use Pearson correlation to balance missing ratings
for person in recommendations.critics:
    print "\nTop matches for " + person + " are:"
    print (sorted(recommendations.topMatches(recommendations.critics,person,'sim_pearson').iteritems(), key=operator.itemgetter(1), reverse=True)[:3])


print recommendations.getRecommendations(recommendations.critics,'Toby','sim_pearson')