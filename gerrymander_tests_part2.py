import numpy as np

#Fake data to test it out
number_of_simulations=1000000
fid = 'test'
num_matching = 13
symm_ = 0
stateresults = [1,2,3,4]
actual_Dseats = 7
meanseats = 9
SDseats = .5
p3 = .023


print('<p><b>Test of Effects: How many extra seats did either party gain relative to party-neutral sampling? (fantasy delegations)</b>: ')
print('It is possible to estimate how the state''s delegation would be composed if votes were distributed according to natural variations in districting. ')
print('This is done by drawing districts at random from a large national sample, and then examining combinations whose vote totals are similar to the actual outcome. ')
print('</p>\n<p></p>\n<p>')

#Actual logic
if num_matching > 0:
    if symm_ == 0:
        print('In the following simulations, the "fantasy delegations" give a sense of what would happen on average, based on national standards for districting. The sampled districts come from real elections, and therefore the simulations include the Republican advantage arising from population clustering.')
    else:
        print('In the following simulations, individual districts used to build "fantasy delegations" were flipped at random, thus generating a partisan-symmetric distribution. Consequently, these simulations ignore population clustering and show what would occur in a fully partisan-symmetric situation.')
    print('</p>\n<p></p>\n<p>')
    print('<IMG SRC="%s_Test3.jpg" border="0" alt="Logo"></p>\n<p>')

    print('In this election, the average Democratic vote share across all districts was %2.1f%%, and Democrats won %i seats. ',np.mean(stateresults)*100, actual_Dseats)
    print('%i fantasy delegations with the same vote share had an average of %.1f Democratic seats (green symbol), with a standard deviation of %.1f seats (see error bar). ',num_matching,meanseats,SDseats)
    print('The actual outcome (red symbol) was therefore advantageous to')
    if meanseats-actual_Dseats<0:
        print(' Democrats. ')
    elif meanseats-actual_Dseats>0:
        print(' Republicans. ')
    
    if p3>0.05:
        print('However, this advantage was not statistically significant. ')
    elif p3<=0.05:
        print('This advantage meets established standards for statistical significance, and ')
        if p3>=0.01:
            print('the probability that it would have arisen by partisan-unbiased mechanisms alone is %1.2f. ',p3)
        else:
            if p3>=0.001:
                print('the probability that it would have arisen by partisan-unbiased mechanisms alone is %1.3f. ')
            else:
                print('the probability that it would have arisen by partisan-unbiased mechanisms alone is less than 0.001. ')
else:
    print('None of the %i simulations had a similar vote share as the actual election results. Change input parameters and try again?',number_of_simulations)