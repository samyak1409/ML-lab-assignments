# Assignment 1: Implement and demonstrate the FIND-S algorithm for finding the most specific hypothesis based on a given
# set of training data samples. Read the training data from a .CSV file.


from csv import reader


with open('dataset.csv') as csv_file:
    data = reader(csv_file)

    attrs = next(data)
    print('\nAttributes:', attrs, '\n')
    h = ['Φ' for _ in attrs[:-1]]
    print('h initialized to most specific hypothesis:', h, '\n')

    for values in data:  # assigning first positive record to h (find-s considers +ve records only)
        print('Record:', values)
        if values[-1] == 'Yes':
            h = values[:-1]
            print('h:', h, '\n')
            break

    for values in data:  # generalizing
        print('Record:', values)
        if values[-1] == 'Yes':
            for i, value in enumerate(values[:-1]):
                if h[i] != value:
                    h[i] = '?'
        print('h:', h, '\n')

print('Generalised hypothesis:', h)
