# Assignment 2: For a given set of training data examples stored in a .CSV file, implement and demonstrate the Candidate
# Elimination algorithm to output a description of the set of all hypothesis consistent with the training examples.


from csv import reader


with open('dataset.csv') as csv_file:
    data = reader(csv_file)

    attrs = next(data)[:-1]
    print('\nAttributes:', attrs, '\n')
    attr_range = range(len(attrs))
    s = ['Φ' for _ in attr_range]
    g = [['?' for _ in attr_range] for _ in attr_range]
    print('Specific hypothesis:', s)
    print('General hypothesis:', g, '\n')

    # Finding and saving opposites of values (application- when first record is -ve)
    data = list(data)  # typecasting iterator to iterable

set_list, dict_list = [set() for _ in attr_range], [{} for _ in attr_range]
for i in attr_range:
    set_, dict_ = set_list[i], dict_list[i]
    for record in data:
        set_.add(record[i])
        if len(set_) == 2:  # coz any attr can have 2 values at max
            e1, e2 = set_
            dict_[e1], dict_[e2] = e2, e1
            break
    else:  # if opposite state of a value doesn't exist in (whole column of) dataset
        dict_[set_.pop()] = '?'
print('Opposites:', dict_list, '\n')

# Assigning first record:
for values in data:  # Candidate Elimination considers both +ve as well as -ve records
    print('Values:', values)
    if values[-1] == 'Yes':  # +ve
        s = values[:-1]
        print('s:', s, '\n')
        break
    else:  # -ve
        for i, value in enumerate(values[:-1]):
            g[i][i] = dict_list[i][value]
        print('g:', g, '\n')

for values in data:
    print('Values:', values)
    if values[-1] == 'Yes':  # generalize
        for i, value in enumerate(values[:-1]):
            if s[i] != value:
                s[i] = '?'
        print('s:', s)
    else:  # specify
        for i, value in enumerate(values[:-1]):
            if s[i] != value:
                g[i][i] = s[i]
        print('g:', g)
    print()


# Syncing s and g:
for i, g_list in enumerate(g[:]):  # https://stackoverflow.com/a/1207427/3064538
    if s[i] == '?' or g_list == ['?' for _ in attr_range]:
        g.remove(g_list)

print('Generalised hypothesis:', s)
print('Specified hypothesis:', g, '\n')

# Making version space: (note- following logic needs to be reviewed)
version_space = set()
for g_list in g:
    for i, g_value in enumerate(g_list):
        if s[i] == g_value:
            for j, s_value in enumerate(s):
                if g_value != '?' and s_value != '?' and g_value != s_value:
                    temp = ['?' for _ in attr_range]
                    temp[i], temp[j] = g_value, s_value
                    version_space.add(tuple(temp))  # coz list is not hashable

print('Version space:', version_space)
