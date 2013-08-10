from math import sqrt
from items.models import Item
from accounts.models import Persona

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
        'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
        'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
        'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
        'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
        'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
        'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
        }
        

diccionario = {}

def getMatrix():
    personas = Persona.objects.all()
    #construir el diccionario (matriz) de usuarios-items valorados/fanme
    #teniendo en cuenta los fanme, comentarios y recomendaciones realizados por cada item
    #diccionario = {}
    for persona in personas:
        dic = {}
        for item in persona.items.all():
            com = Item.objects.filter(users_are_comment=persona.user).count()
            recom_cant = item.recomendacion_set.filter(user_origen=persona.user).count()
            dic[item.nombre] = float(1 + recom_cant + com)
        diccionario[persona.user.username] = dic
    return diccionario
    
    
def updateMatrix(item, persona, diccionario):
    com = Item.objects.filter(users_are_comment=persona.user).count()
    recom_cant = item.recomendacion_set.filter(user_origen=persona.user).count()
    diccionario[persona.user.username][item.nombre] = float(1 + recom_cant + com)
    


# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
    """
    >>> reload(recommendations)
    >>> recommendations.sim_distance(recommendations.critics, 'Lisa Rose','Gene Seymour')
    0.148148148148
    """
    # Get the list of shared_items
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    # if they have no ratings in common, return 0
    if len(si)==0: return 0
    # Add up the squares of all the differences
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sum_of_squares)


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
    """ 
    >>> reload(recommendations)
    >>> print recommendations.sim_pearson(recommendations.critics,
    ... 'Lisa Rose','Gene Seymour')
    0.396059017191

    """
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    # Find the number of elements
    n=len(si)
    # if they are no ratings in common, return 0
    if n==0: return 0
    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_distance):
    """
    >> reload(recommendations)
    >> recommendations.topMatches(recommendations.critics,'Toby',n=3)
    [(0.99124070716192991, 'Lisa Rose'), (0.92447345164190486, 'Mick LaSalle'),
    (0.89340514744156474, 'Claudia Puig')]
    """
    scores=[(similarity(prefs,person,other), other) for other in prefs if other!=person]
    # Sort the list so the highest scores appear at the top
    scores.sort( )
    scores.reverse( )
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_distance):
    """
    >>> reload(recommendations)
    >>> recommendations.getRecommendations(recommendations.critics,'Toby')
    [(3.3477895267131013, 'The Night Listener'), (2.8325499182641614, 'Lady in the
    Water'), (2.5309807037655645, 'Just My Luck')]

    """
    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort( )
    rankings.reverse( )
    return rankings
    
    
def transformPrefs(prefs):
    """
    >> reload(recommendations)
    >> movies=recommendations.transformPrefs(recommendations.critics)
    >> recommendations.topMatches(movies,'Superman Returns')
    [(0.657, 'You, Me and Dupree'), (0.487, 'Lady in the Water'), (0.111, 'Snakes on a
    Plane'), (-0.179, 'The Night Listener'), (-0.422, 'Just My Luck')]

    """
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result


