# This is a port of gerrymander_statename.m
def gerrymander_statename(state_number_list):
    '''This function accepts a list of ints as an input and returns the state
    abbreviations corresponding to those numbers'''
    statelist = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NV', 'NH', 'NJ', 'NM',
                 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA',
                 'WA', 'WV', 'WI', 'WY']
    print_list = [state_number for state_number in state_number_list if state_number > 0 and state_number < 51]
    for i in range(len(print_list)):
        print(statelist[print_list[i] - 1], end=' ')