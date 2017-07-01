######second case is when you have an actual year and state of interest. That's what I'll be focusing on getting working first
# (the case when year != 0).
#
# To test run this function, use: gerrymander_tests_part1(2012,38,2012,0,0.75,0,'Pennsylvania','foo')
# p1 of the Matlab code is the probability, and it's the main thing that's being calculated

from datetime import datetime
from statistics import mean
import numpy as np
from scipy import stats
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt


######################################################################################################################

def gerrymander_read_results(year, states):
    # Let's read the csv file into a pandas dataframe
    df = pd.read_csv('House_1898_2014_voteshares_notext.csv', header=None)
    # Let's name the columns
    df.columns = ['Year', 'State', 'District', 'D_voteshare', 'Incumbent', 'Winner']
    # We'll only extract those with the correct year
    year_df = df[df['Year'] == year]
    # Now we'll just take the values with the correct states
    result = year_df[year_df['State'].isin(states)]
    # Drop the 'Year' column from the dataframe
    del result['Year']
    # Return the remaining dataframe
    return result


# This is a port of gerrymander_statename.m
#def gerrymander_statename(state_number_list):
#    '''This function accepts a list of ints as an input and returns the state
#    abbreviations corresponding to those numbers'''
#    statelist = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
#                 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NV', 'NH', 'NJ', 'NM',
#                 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA',
#                 'WA', 'WV', 'WI', 'WY']
#    print_list = [state_number for state_number in state_number_list if state_number > 0 and state_number < 51]
#    for i in range(len(print_list)):
#        print(statelist[print_list[i] - 1], end=' ')

# This is a port of gerrymander_statename.m
def gerrymander_statename(foo):
    statelist = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY '

    sfoo = ''
    foo = [round(float(i), 0) for i in foo]
    foo = [50 if i > 50 else i for i in foo]
    if len(foo) >= 1:
        for i in foo:
            if i >= 1 and i <= 50:
                ifoo = int(3 * (i - 1))
                sfoo = sfoo + str(statelist[ifoo:ifoo + 2]) + ' '
            else:
                sfoo = sfoo + 'XX '
    else:
        sfoo = 'Custom Data '

    return sfoo


def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]


def int_to_list(possible_int):
    '''This function converts an int to a list of ints with size = 1. If the input is already a list it returns it as is'''
    if type(possible_int) == int:
        possible_int = [possible_int]
    return possible_int

def vartest(data_c, var_c):
    '''This function calculates variance test like the similar function in Matlab in source code with left tail'''
    df = len(data_c) - 1
    var_d = np.var(data_c, ddof=1)
    x2 = df * var_d / var_c
    p2b = stats.chi2.cdf(x2, df)
    return p2b

######################################################################################################################


def gerrymander_tests_part1(year, states, year_baseline, state_baseline, imputed_uncontested, symm, state_label,
                            output_filename):
    # Check to make sure states and state_baseline are lists of ints
    states = int_to_list(states)
    state_baseline = int_to_list(state_baseline)

    # electionmessage = 'U.S. House election of ' + str(year) + ' in ' + str(statename)
    electionmessage = 'Election to be analyzed: '
    baselinemessage = 'Districts to be sampled for fantasy delegations: '

    parameterlist0 = 'Parameters: year=%s ' % year
    if year == 0:
        parameterlist1 = 'states=%s ' % len(states)  # need to check!!!!
        parameterlist1 = parameterlist1 + ' year_baseline=%i state_baseline=' % year_baseline
    else:
        parameterlist1 = 'Parameters: year=%i states=%i year_baseline=%i state_baseline=' % (
            year, len(states), year_baseline)

    parameterlist2 = '%i ' % len(state_baseline)
    parameterlist3 = 'imputeduncontested=%.2f symm=%i statelabel=%s output_filename=%s' % (
        imputed_uncontested, symm, state_label, output_filename)
    parameterlisting = parameterlist0 + parameterlist1 + parameterlist2 + parameterlist3

    # reset_selective parameterlist0 parameterlist1 parameterlist2 parameterlist3

    if year == 0:
        #        stateraw=states(:,3); % use the variable "states" as the voting results data
        electionmessage = electionmessage + 'Custom data set, ' + state_label
    elif year in np.arange(1898, 2100, 2):
        statedata = gerrymander_read_results(year, states)
        stateraw = statedata['D_voteshare']  # I'm thinking he's looking for D_voteshare
        statename = [gerrymander_statename(states)]
        electionmessage = electionmessage + ' U.S. House election of ' + str(year) + ' in ' + str(statename)
    else:
        statedata = gerrymander_read_results(2012, 38)
        stateraw = statedata['D_voteshare']  # I'm thinking he's looking for D_voteshare
        statename = gerrymander_statename([38])
        print('Year parameter didn''t parse - defaulting to U.S. House Pennsylvania 2012')

    baselinemessage = 'Districts to be sampled for fantasy delegations: '

    ##############################################################################
    nationaldata = gerrymander_read_results(year_baseline, state_baseline)

    if year_baseline == 0:
        len(nationaldata)
        foo = np.random.normal(0.5, 0.15, 435)  # generate a generic random distribution
        foo[foo < 0] = 0
        foo[foo > 1] = 1
        nationaldata['D_voteshare'] = foo  # ????? really national data isn't loaded !!!
        nationalraw = foo
        baselinemessage = baselinemessage + ' Random, partisan-symmetric districts.';
    elif year_baseline in np.arange(1898, 2016, 2):
        baselinemessage = baselinemessage + ' U.S. House results of ' + str(year_baseline)
        if state_baseline[0] < 1:
            nationaldata = gerrymander_read_results(year_baseline, list(range(1, 51)))
            baselinemessage = baselinemessage + ' in all 50 states'
        else:
            nationaldata = gerrymander_read_results(year_baseline, state_baseline)
            if len(state_baseline) == 50:
                baselinemessage = baselinemessage + ' in all 50 states'
            elif len(state_baseline) >= 30:
                omitstates = np.setdiff1d(list(range(1, 51)), state_baseline)
                baselinemessage = baselinemessage + ' in all states, but omitting: ' + gerrymander_statename(
                    omitstates);
            else:
                baselinemessage = + baselinemessage + ' in: ' + str(gerrymander_statename(state_baseline))

        nationalraw = nationaldata['D_voteshare']
    else:  # just do Pennsylvania 2012 ???????? incorrect comment ????????
        nationaldata = gerrymander_read_results(2012, list(range(1, 51)))
        baselinemessage = baselinemessage + ' U.S. House 2012'
        print('Yearbaseline parameter didn''t parse - defaulting national data to 2012')

    N_delegates = len(stateraw)
    D_districts = indices(stateraw, lambda x: x >= 0.5)
    R_districts = indices(stateraw, lambda x: x < 0.5)
    N_D = len(D_districts)
    N_R = N_delegates - N_D

    # Let's round stateraw to 5 digits to for the 1.00000's to 1
    rounded_stateraw = [round(state, 5) for state in stateraw]
    anyimputed = 0 in rounded_stateraw or 1 in rounded_stateraw
    imputed_uncontested = min(imputed_uncontested, 1)
    imputed_uncontested = max(imputed_uncontested, 0)
    imputedfloor = min(imputed_uncontested, 1 - imputed_uncontested)

    stateresults = stateraw
    # Turn all the 0's in stateresults into whatever number the imputed floor is
    stateresults[stateresults == 0] = imputedfloor
    stateresults[stateresults == 1] = 1 - imputedfloor  # Setting value on a copy, gives a warning

    nationalresults = nationalraw
    nationalresults[nationalresults == 0] = imputedfloor
    nationalresults[nationalresults == 1] = 1 - imputedfloor

    D_mean_raw = mean(stateraw)
    R_mean_raw = 1 - D_mean_raw
    D_mean = mean(stateresults)
    R_mean = 1 - D_mean

    f1 = open(output_filename + '.html', 'w')

    site = 'http://gerrymander.princeton.edu';
    msg = '<b>Gerrymandering analyzer from Prof. Sam Wang, Princeton University</b>';
    print('<p><a href = "%s">%s</a></p>\n<p></p>\n<p>' % (site, msg), file=f1)

    print('%s</p>\n<p>' % (electionmessage), file=f1)
    print('%s</p>\n<p></p>\n<p>' % (baselinemessage), file=f1)
    state_name = gerrymander_statename(states)  # will give two-letter abbreviation of state

    if N_delegates <= 1:
        formatSpec = 'Analysis is not possible. %s only has one representative listed, and single-district states cannot be redistricted.</p>\n'
        print(formatSpec % state_name, file=f1);
    # results=0
    else:
        state_name = gerrymander_statename(states)  # will give two-letter abbreviation of state  ?????????
        formatSpec = 'The %s delegation has %i seats, %i Democratic/other and %i Republican.</p>\n<p>'
        print(formatSpec % (str(state_name), N_delegates, N_D, N_R), file=f1)
        if imputed_uncontested != 0:
            print('Uncontested races are assumed to have been won with %i%% of the vote.</p>\n<p>' % (
                imputed_uncontested * 100), file=f1)

        print('The average Democratic share of the two-party total vote was %2.1f%% (raw)' % (D_mean_raw * 100),
              file=f1)
        if D_mean_raw != D_mean:
            print(', %2.1f%% with imputation of uncontested races' % (D_mean * 100), file=f1)

        print('.</p>\n<p></p>\n<p>', file=f1)

        print('<b>Analysis of Intents</b></p>\n<p></p>\n<p>', file=f1);

        print(
            'If a political party wishes to create for itself an advantage, it will pack its opponents to win overwhelmingly in a small number of districts, while distributing its own votes more thinly, but still to produce reliable wins. ',
            file=f1)
        print('</p>\n<p></p>\n<p>', file=f1)
        print(
            'Partisan gerrymandering arises not from single districts, but from patterns of outcomes. Thus a single lopsided district may not be an offense - indeed, single-district gerrymandering is permitted by Supreme Court precedent, and may be required for the construction of individual districts that comply with the Voting Rights Act. Rather, it is combinations of outcomes that confer undue advantage to one party or the other.',
            file=f1)
        print('</p>\n<p></p>\n<p>', file=f1)
        print('The following two tests provide a way of quantifying any such advantage in a set of election results.',
              file=f1)
        print('</p>\n<p></p>\n<p>', file=f1)

        #########################################
        ##### Test for lopsided win margins #####
        #########################################

        print('%s Test 1\n' % str(datetime.now()))
        print('<b>First Test of Intents: Probing for lopsided win margins (the two-sample t-test):</b> ', file=f1)
        print(
            'To test for a lopsided advantage, one can compare each party''s winning margins and see if they are systematically different. ',
            file=f1)
        print('This is done using the <a href="http://vassarstats.net/textbook/ch11pt1.html">two-sample t-test</a>. ',
              file=f1)
        print(
            'In this test, the party with the <i>smaller</i> set of winning margins has the advantage.</p>\n<p></p>\n<p>',
            file=f1)

        if N_D >= 2 and N_R >= 2:
            # calculate 2-sied t-test:
            [t1, p1] = stats.ttest_ind(list(stateresults.tolist()[i] for i in D_districts), \
                                       list(1 - stateresults.tolist()[i] for i in R_districts), equal_var=True)
            # one side of the t test: there are two posibilities:
            # the mean sample 1 is > mean sample 2,  we want P/2 < Pcritical, t>0
            # mean sample 1 is < mean sample 2, we want P/2< Pcritical, t<0
            p1 = p1 / 2
            if mean(stateresults.tolist()[i] for i in D_districts) > mean(
                            1 - stateresults.tolist()[i] for i in R_districts):
                if t1 < 0:
                    # save the NULL hypothesis
                    p1 = p1 + 1
            else:
                if t1 > 0:
                    # save the NULL hypothesis
                    p1 = p1 + 1

            if p1 > 0.05:
                print(
                    'The difference between the two parties win margins does not meet established standards for statistical significance. ',
                    file=f1)
                print(
                    'The probability that this difference or larger could have arisen by partisan-unbiased mechanisms is %1.2f.' % p1,
                    file=f1)
            else:
                print(
                    'The difference between the two parties win margins meets established standards for statistical significance. ',
                    file=f1)
                if p1 >= 0.01:
                    print(
                        'The probability that this difference in win margins (or larger) would have arisen by partisan-unbiased mechanisms alone is %1.2f. ' % p1,
                        file=f1)
                else:
                    if p1 >= 0.001:
                        print(
                            'The probability that this difference in win margins (or larger) would have arisen by partisan-unbiased mechanisms alone is %1.3f. ' % p1,
                            file=f1)
                    else:
                        print(
                            'The probability that this difference in win margins (or larger) would have arisen by partisan-unbiased mechanisms alone is less than 0.001. ',
                            file=f1)

            print('</p>\n<p></p>\n<p>', file=f1)

            df_stateraw = stateraw.to_frame()
            df_stateraw['pol'] = np.where(df_stateraw['D_voteshare'] >= 0.5, 'Democratic', 'Republician')
            df_stateraw['D_voteshare'] = np.where(df_stateraw['D_voteshare'] >= 0.5, df_stateraw['D_voteshare'] * 100,
                                                  100 - df_stateraw['D_voteshare'] * 100)

            labels = ['Democratic', 'Republician']
            data_d = df_stateraw[df_stateraw.pol == 'Democratic']['D_voteshare']
            data_r = df_stateraw[df_stateraw.pol == 'Republician']['D_voteshare']
            data = [data_d, data_r]

            fig = plt.figure()
            fig.suptitle('Analysis of Intents: Lopsided wins by one side', fontsize=10, fontweight='bold')
            ax = fig.add_subplot(111)
            ax.boxplot(data, 0, 'ro', 0, labels=labels, showfliers=True, showmeans=True)
            ax.scatter(data_d, np.ones(len(data_d)))
            ax.scatter(data_r, 2 * np.ones(len(data_r)))
            ax.set_xlabel('Winning vote percentage')
            plt.savefig(output_filename + '_Test1.png')
 #           plt.show()
            print('<IMG SRC="%s_Test1.png" border="0" alt="Logo"></p>\n<p>' % output_filename, file=f1)
        else:
            print('Can''t compare win margins. For this test, both parties must have at least two seats.</p>\n<p></p>\n<p>',
                file=f1)

            #########################################
            ##### Test for asymmetric advantage #####
            #########################################
        print('%s Test 2\n' % str(datetime.now()))
        print('<b>Second Test of Intents: Probing for asymmetric advantage for one party (mean-median difference and/or chi-square test):</b> ',
            file=f1)
        print('The choice of test depends on whether the parties are closely matched (mean-median difference) or one party is dominant (chi-square test of variance).</p>\n<p></p>\n<p>',
            file=f1)

        partisan_balance = abs(mean(stateresults) - 0.5)
        if partisan_balance < 0.06:
            print(
                'When the parties are closely matched in overall strength, a partisan advantage will be evident in the form of a difference between the mean (a.k.a. average) vote share and the median vote share, calculated across all districts. </p>\n<p></p>\n<p>',
                file=f1)
            # mean minus median test
            mean_median_diff = mean(stateresults) - np.median(stateresults)
            SK_mmdiff = mean_median_diff / np.std(stateresults, ddof=1) * np.sqrt(
                len(stateresults) / 0.5708)  # the 0.5708 comes from p. 352 of Cabilio and Masaro 1996
            pvalue_mmdiff = min(norm.cdf(SK_mmdiff), 1 - norm.cdf(
                SK_mmdiff))  # One-tailed p-value, usually appropriate since most testers have a direction in mind
            mean_median_diff_p = abs(mean_median_diff) * 100
            if mean_median_diff < 0:
                print(
                    'The mean-median difference is %2.1f %% in a direction of advantage to the Democratic Party. ' % mean_median_diff_p,
                    file=f1)
            elif mean_median_diff > 0:
                print(
                    'The mean-median difference is %2.1f %% in a direction of advantage to the Republican Party. ' % mean_median_diff_p,
                    file=f1)
            else:
                print(
                    'The mean and median are identical, suggesting no identifiable advantage to either major party. This can occur in situations where all races are uncontested.',
                    file=f1)

            pvalue_mmdiff_p = pvalue_mmdiff * 100
            print(
                'The mean-median difference would reach this value in %2.1f %% of situations by a partisan-unbiased process. ' % pvalue_mmdiff_p,
                file=f1);
            if pvalue_mmdiff < 0.01:
                print(
                    'This difference is statistically significant (p<0.01), and in a case of suspected gerrymandering is extremely unlikely to have arisen by chance. ',
                    file=f1);
            elif pvalue_mmdiff < 0.05:
                print(
                    'This difference is statistically significant (p<0.05), and in a case of suspected gerrymandering is unlikely to have arisen by chance. ',
                    file=f1);
            else:
                print('This difference is not statistically significant (p>0.05). ', file=f1);
            print('</p>\n<p></p>\n<p>', file=f1)

            df_stateraw = stateraw.to_frame()
            df_stateraw['pol'] = np.where(df_stateraw['D_voteshare'] >= 0.5, 'Blue', 'Red')
            df_stateraw['D_voteshare'] = df_stateraw['D_voteshare'] * 100

            labels = statename
            data = [df_stateraw['D_voteshare']]
            color = list(df_stateraw['pol'])

            fig = plt.figure()
            fig.suptitle('Analysis of Intents: Mean-median difference in vote share', fontsize=10, fontweight='bold')
            ax = fig.add_subplot(111)
            ax.boxplot(data, 0, 'rs', 0, labels=labels, showmeans=True)
            ax.set_xlabel('Democratic Party vote share (%)')
            y = data[0]
            x = np.random.normal(1, 0.04, size=len(y))
            ax.plot(x, y)
            plt.savefig(output_filename + '_Test2a.png')
#            plt.show()
            print('<IMG SRC="%s_Test2a.png" border="0" alt="Logo"></p>\n<p></p>\n<p>' % output_filename, file=f1)

        else:
            print('Can''t compare win margins. For this test, both parties must have at least two seats.</p>\n<p></p>\n<p>', file=f1)

    if partisan_balance < 0.05:
        print('When one party is dominant statewide, it gains an overall advantage by spreading its strength as uniformly as possible across districts. The statistical test to detect an abnormally uniform pattern is the <a href="http://www.itl.nist.gov/div898/handbook/eda/section3/eda358.htm">chi-square test</a>, in which the vote share of the majority party-controlled seats are compared with nationwide patterns.</p>\n<p></p>\n<p>', file=f1);
        # chi square test on majority of delegation
        if len(D_districts) > len(R_districts):
            varcompare = np.var(nationalresults[nationalresults > 0.5])
            p2b = vartest(list(stateresults.tolist()[i] for i in D_districts), varcompare)
            std_value = np.std(list(stateresults.tolist()[i] for i in D_districts)*100, ddof=1)
            var_value = np.sqrt(varcompare)*100
            print('The standard deviation of the Democratic majority''s winning vote share is %2.1f %%. ' % std_value, file=f1)
            print('At a national level, the standard deviation is %2.1f %%. ' % var_value, file=f1)
        else:
            data_1 = nationalresults[nationalresults < 0.5]
            varcompare = np.var(data_1, ddof=1)
            p2b = vartest(list(stateresults.tolist()[i] for i in R_districts), varcompare)
            std_value = np.std(list(stateresults.tolist()[i] for i in R_districts), ddof=1) * 100
            var_value = np.sqrt(varcompare) * 100
            print('The standard deviation of the Republican majority''s winning vote share is %2.1f %%. ' % std_value,
                  file=f1)
            print('At a national level, the standard deviation is %2.1f %%. ' % var_value, file=f1)

        if p2b<0.01:
            print('This difference is statistically significant (p<0.01), and in a case of suspected gerrymandering is extremely unlikely to have arisen by chance. ', file=f1)
        elif p2b<0.05:
            print('This difference is statistically significant (p<0.05), and in a case of suspected gerrymandering is unlikely to have arisen by chance. ', file=f1)
        else:
            print('This difference is not statistically significant (p>0.05). ', file=f1)

        print('</p>\n<p>', file=f1)

#        labels = statename
#        data = [df_stateraw['D_voteshare']]
#        color = list(df_stateraw['pol'])

#        fig = plt.figure()
#        fig.suptitle('Analysis of Intents: Chi-square test for unusually uniform outcomes', fontsize=10, fontweight='bold')
#        ax = fig.add_subplot(111)
#        ax.boxplot(data, 0, 'ro', 0, labels=labels, showfliers=True, showmeans=True)
#        ax.set_xlabel('Districts (sorted by vote share)')
#        ax.set_ylabel('Democratic vote share (%)')
#        plt.savefig(output_filename + '_Test2b.png')
#        plt.show()
#        print('<IMG SRC="%s_Test2b.png" border="0" alt="Logo"></p>\n<p>' % output_filename, file=f1)

    f1.close()

    #    % JPEG: show barplot of all districts
    #    % inset message, SD of majority district vote share, compare with national SD
    #        Fig2b = figure(3);
    #        set(Fig2b, 'Position', [600 100 600 300])
    #        title('Analysis of Intents: Chi-square test for unusually uniform outcomes')
    #        hold on
    #    % plot zone of chance for majority?
    #        plot([0 length(D_districts)+length(R_districts)+0.5],[50 50],'-k');
    #        if length(D_districts)>0
    #            bar([1:length(D_districts)],100*stateraw(D_districts),'b')
    #        end
    #        if length(R_districts)>0
    #            bar([length(D_districts)+1:length(D_districts)+length(R_districts)],100*stateraw(R_districts),'r')
    #        end
    #        axis([0 length(D_districts)+length(R_districts)+0.5 -3 100]);
    #        xlabel('Districts (sorted by vote share)')
    #        ylabel('Democratic vote share (%)')
    #        set(gca,'XTick',[]);
    #        set(gca,'YTick',[0 10 20 30 40 50 60 70 80 90 100]);
    #
    #        set(gcf,'PaperPositionMode','auto')
    #        print([output_filename '_Test2b_hires.jpg'],'-djpeg','-r300')
    #        screen2jpeg([output_filename '_Test2b.jpg'])#
    #
    #        fprintf(fid,'<IMG SRC="%s_Test2b.jpg" border="0" alt="Logo"></p>\n<p></p>\n',output_filename);
    #    end
    #    results=1;
    # end


# import pylab as P
# import numpy as np
# P.figure()
# P.xlim([0,2])
# y = data[0]
# x = np.ones(len(y))
# P.plot(x, y, 'r.', color = 'red')
# y = data[1]
# x = np.ones(len(y))
# P.plot(x, y, 'r.', color = 'blue')
# P.show()

gerrymander_tests_part1(2016,3,2016,0,0.75,0,'Arizona','foo')