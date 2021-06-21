# Assignment 5: Write a program to implement the naive Bayesian classifier for a sample training data set stored as a
# .CSV file. Compute the accuracy of the classifier, considering few test data sets.


from csv import reader


with open('dataset.csv') as csv_file:
    data = list(reader(csv_file))
rec_count = len(data)
print('\nTotal records:', rec_count)


# Fetching Classes:
cls1 = data[0][-1]
for rec in data:
    if rec[-1] != cls1:
        cls2 = rec[-1]
        break
else:
    cls2 = None
    exit('All the data belong to a single class: ' + cls1)

print(f'Classes: "{cls1}" and "{cls2}"')


split_ratio = 0.9  # b/w 0 and 1 (both not included)
print('Split ratio (training data:testing data):', split_ratio)
split_index = int(rec_count*split_ratio)


# Training:
cls1_data, cls2_data = [], []
cls1_wrd_cnt, cls2_wrd_cnt = 0, 0
for rec in data[:split_index]:
    cls = rec[-1]
    if cls == cls1:
        for word in rec:
            cls1_data.append(word)
            cls1_wrd_cnt += 1
    else:  # if cls = cls2
        for word in rec:
            cls2_data.append(word)
            cls2_wrd_cnt += 1
unq_wrd_cnt = len(set(cls1_data+cls2_data))
print(f'Words in class "{cls1}": {cls1_wrd_cnt}')
print(f'Words in class "{cls2}": {cls2_wrd_cnt}')
print(f'Total unique words: {unq_wrd_cnt} \n')


# Testing:
correct, total = 0, rec_count-split_index
for rec in data[split_index:]:
    cls1_prob, cls2_prob = 1, 1
    for word in rec[:-1]:
        # Using Laplace Smoothing:
        cls1_prob = (cls1_data.count(word)+1) / (cls1_wrd_cnt + unq_wrd_cnt)
        cls2_prob = (cls2_data.count(word)+1) / (cls2_wrd_cnt + unq_wrd_cnt)
    # print('Record:', rec)  # debugging
    # print(f'Probabilities of classes => "{cls1}": {cls1_prob}, "{cls2}": {cls2_prob}')  # debugging
    if cls1_prob > cls2_prob:
        pred_cls = cls1
    elif cls2_prob > cls1_prob:
        pred_cls = cls2
    else:  # if cls1_prob = cls2_prob
        # print('Equal probability, skipping \n')  # debugging
        total -= 1  # removing this rec's count
        continue
    act_cls = rec[-1]
    # print(f'Predicted Class: "{pred_cls}", Actual Class: "{act_cls}" \n')  # debugging
    if pred_cls == act_cls:
        correct += 1
print('Accuracy in %:', correct*100/total)
