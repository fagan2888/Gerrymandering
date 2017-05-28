import random
import numpy as np

''' To run this: 
Dvotes = [1, 0, 0, 1, 0]
stateDvotes = [1, 0, 0, 1]
number_of_simulated_delegations = [2,2]
symmet = 0
filename = "filename"

gerry_fantasy_delegations(stateDvotes, Dvotes, symmet, number_of_simulated_delegations, filename)
'''

'''
 paste into code that calls this code:
 [meanseats,SDseats,sigma,actual_Dseats,total_state_seats,num_matching,alpha]=gerry_fantasy_delegations(stateresults,nationalresults,1000000,outputfilename);
 or cut starting with line below, then paste into command window
 stateDvotes=stateresults;Dvotes=nationalresults;number_of_simulated_delegations=1000000';outputfilename='foo';


 gerry_fantasy_delegations.m - Stripped-down gerrymandering simulation. 
 Copyright Sam Wang under GNU License, 2016. 
 OK to copy, distribute, and modify, but retain this header
 
 Princeton Election Consortium
 http://election.princeton.edu
 http://gerrymander.princeton.edu

 inputs:
   stateDvotes

 outputs:
   meanseats - average number of D seats in simulations
   SDseats - standard deviation of D seats in simulations
   sigma - binomial SD
   actual_Dseats - number of actual D seats in delegation
   total_state_seats - total number of seats in delegation
   num_matching - number of simulations matching % vote criterion
   alpha - one-tailed likelihood of actual outcome arising in simulations

 units are in fraction of two-party vote - multiply by 100 to get percentages

 alldistricts is the set of districts from which to build simulated delegations
 '''

def gerry_fantasy_delegations(stateDvotes,Dvotes,symmet,number_of_simulated_delegations,outputfilename):
    # alldistricts is the set of districts from which to build simulated
    # delegations
    alldist = len(Dvotes)
    alldistricts = list(range(alldist))  # Gives you [0,1,2,..,alldist]
    total_state_seats = len(stateDvotes)
    # I'm not sure what you want here
    sdist = total_state_seats
    # Dvotes=normrnd(0.5,0.15,size(alldistricts)); % create a symmetric
    # distribution to sample from # This is commented out in Sam's work. Do you
    # want it?

    # true delegation
    # statewide average D vote share
    s_dvote = sum([stateDvotes[sdist-1]]) / total_state_seats # The minus 1 is to go from matlab to python indexing
    actual_Dseats = sum([stateDvotes[sdist-1] > 0.5])  # number of actual D seats won

    # simulate some delegations
    # clear p dseats # Unclear on this
    p = np.zeros(number_of_simulated_delegations)
    dseats = np.zeros(number_of_simulated_delegations)
    if symmet == 0:
        for i in range(len(number_of_simulated_delegations)):
            # pick a random set of districts
            print("total_state_seats is {}".format(total_state_seats))
            valu = np.floor([alldist * random.random() for i in range(total_state_seats)]) + 1
            print(random.randint(1,total_state_seats) * alldist)
            fantasydel = []
            for x in range(len(valu)):
                fantasydel.append(alldistricts[int(valu[x])-1])
            Dvotes_of_fant = [Dvotes[fantasydel[x]-1] for x in range(len(fantasydel))]
            p[i] = sum(Dvotes_of_fant) / total_state_seats
            # average two - party vote share in the simulated delegation
            #dseats[i] = sum(Dvotes[fantasydel] > 0.5)
            # the simulated delegation has this many D seats
    else:
        for i in range(len(number_of_simulated_delegations)):
            fantasydel = alldistricts[0]#[np.floor(random.randint(1,total_state_seats) * alldist) + 1]
            # pick a random set of districts
            flips = np.sign(random.randint(1,total_state_seats)) - 0.5
            #p[i] = (sum(np.multiply(Dvotes[fantasydel-1],flips)) + len(flips[flips == -1])) / total_state_seats
            # average two - party vote share in the simulated delegation
            #dseats[i] = sum(Dvotes(fantasydel(flips[flips == 1])) > 0.5) + sum(Dvotes(fantasydel(flips[flips == -1])) < 0.5)
            # the simulated delegation has this many D seats