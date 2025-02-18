# Zane Baker
# Python implementation of stable matching problem
def gs(men, women, pref):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man,woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """
    # preprocessing
    ## build the rank dictionary
    rank={}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m]=i
            i+=1
    ## create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)    #initially all men and women are free
    numpartners = len(men) 
    S = {}           #build dictionary to store engagements 

    #run the algorithm
    while freemen:
        m = freemen.pop()
        #get the highest ranked woman that has not yet been proposed to
        w = pref[m][prefptr[m]]
        prefptr[m]+=1
        if w not in S: S[w] = m
        else:
            mprime = S[w]
            if rank[w][m] < rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
    return S

def gs_block(men, women, pref, blocked):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man, woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """
    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m] = i
            i += 1
    
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)
    numpartners = len(men)
    unblocked_pairs = {}

    # run the algorithm
    while freemen:
        m = freemen.pop()
        w = pref[m][prefptr[m]]
        if (m, w) in blocked:
            prefptr[m] += 1
            if  prefptr[m] >= len(men):
                break  
            w = pref[m][prefptr[m]]
        if len(men) > prefptr[m]:
            prefptr[m] += 1 
            if (m,w) not in unblocked_pairs:
                unblocked_pairs[w] = m
            else:
                mprime = unblocked_pairs[w]
                if rank[w][m] < rank[w][mprime]:
                    unblocked_pairs[w] = m
                    freemen.add(mprime)
                else:
                    freemen.add(m)
    return unblocked_pairs

  

   
    
def gs_tie(men, women, preftie):
 # preprocessing
    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in preftie[w]:
            for m in men:
                rank[w][m] = i
                i += 1

    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)
    freewomen=set(women)
    matched = {} #store matched pairs

    while freemen:
        m = freemen.pop()
        best_female_pairings = preftie[m][prefptr[m]]
        prefptr[m] += 1
        # Form the best pairings using the max function with lambda
        for w in women:
         w=max(best_female_pairings, key=lambda women: rank[women][m])
         if len(preftie[m]) > prefptr[m]:
          prefptr[m]+1
        if w not in matched:
            matched[w] = m #pair the ideal female pairs with available males
        else:
            mprime = matched[w]
            if rank[w][m] < rank[w][mprime]:
                matched[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
    else:
        pass
    return matched
    


if __name__=="__main__":
    #input data
    themen = ['xavier','yancey','zeus']
    thewomen = ['amy','bertha','clare']

    thepref = {'xavier': ['amy','bertha','clare'],
           'yancey': ['bertha','amy','clare'],
           'zeus': ['amy','bertha','clare'],
           'amy': ['yancey','xavier','zeus'],
           'bertha': ['xavier','yancey','zeus'],
           'clare': ['xavier','yancey','zeus']
           }
    thepreftie = {'xavier': [{'bertha'},{'amy'},{'clare'}],
           'yancey': [{'amy','bertha'},{'clare'}],
           'zeus': [{'amy'},{'bertha','clare'}],
           'amy': [{'zeus','xavier','yancey'}],
           'bertha': [{'zeus'},{'xavier'},{'yancey'},],
           'clare': [{'xavier','yancey'},{'zeus'}]
           }
    
    blocked = {('xavier','clare'),('zeus','clare'),('zeus','amy')}

    
    match = gs(themen,thewomen,thepref)
    print(match)
    
    match_block = gs_block(themen,thewomen,thepref,blocked)
    print(match_block)

    match_tie = gs_tie(themen,thewomen,thepreftie)
    print(match_tie)