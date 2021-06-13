# Assignment 3: Write a program to demonstrate the working of the Decision Tree based ID3 algorithm. Use an appropriate
# data set for building the decision tree and apply this knowledge to classify a new sample.


import ast
import csv
# import sys
import math
import os


def load_csv_to_header_data(filename):
    path = os.path.normpath(os.getcwd() + filename)
    ''' os.path.normpath(path)
Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B. This string manipulation may change the meaning of a path that contains symbolic links. On Windows, it converts forward slashes to backward slashes. To normalize case, use normcase().'''
    # print(path)
    fs = csv.reader(open(path))
    all_row = []
    for r in fs:
        all_row.append(r)
    headers = all_row[0]
    idx_to_name, name_to_idx = get_header_name_to_idx_maps(headers)
    data = {'header': headers, 'rows': all_row[1:], 'name_to_idx': name_to_idx, 'idx_to_name': idx_to_name}
    return data


def get_header_name_to_idx_maps(headers):
    name_to_idx = {}
    idx_to_name = {}
    for i in range(0, len(headers)):
        name_to_idx[headers[i]] = i
        idx_to_name[i] = headers[i]
        # print(name_to_idx)
        # print(idx_to_name)
    return idx_to_name, name_to_idx


def project_columns(data, columns_to_project):
    data_h = list(data['header'])
    data_r = list(data['rows'])
    all_cols = list(range(0, len(data_h)))
    columns_to_project_ix = [data['name_to_idx'][name] for name in columns_to_project]
    # print(columns_to_project_ix)
    columns_to_remove = [cidx for cidx in all_cols if cidx not in columns_to_project_ix]
    # print(columns_to_remove)
    for delc in sorted(columns_to_remove, reverse=True):
        del data_h[delc]
        for r in data_r:
            del r[delc]
    idx_to_name, name_to_idx = get_header_name_to_idx_maps(data_h)
    return {'header': data_h, 'rows': data_r, 'name_to_idx': name_to_idx, 'idx_to_name': idx_to_name}


def get_uniq_values(data):
    idx_to_name = data['idx_to_name']
    idxs = idx_to_name.keys()
    # print(idxs)
    val_map = {}
    for idx in iter(idxs):
        val_map[idx_to_name[idx]] = set()
    # print(val_map)
    for data_row in data['rows']:
        for idx in idx_to_name.keys():
            att_name = idx_to_name[idx]
            val = data_row[idx]
            if val not in val_map.values():
                val_map[att_name].add(val)
                # print(val_map)
    return val_map


def get_class_labels(data, target_attribute):
    rows = data['rows']
    # print(rows)
    col_idx = data['name_to_idx'][target_attribute]
    # print(col_idx)
    labels = {}
    for r in rows:
        val = r[col_idx]
        if val in labels:
            labels[val] = labels[val] + 1
        else:
            labels[val] = 1
    # print(labels)
    return labels


def entropy(n, labels):
    ent = 0
    for label in labels.keys():
        p_x = labels[label] / n
        ent += - p_x * math.log(p_x, 2)
    return ent


def partition_data(data, group_att):
    partitions = {}
    data_rows = data['rows']
    partition_att_idx = data['name_to_idx'][group_att]
    # print(partition_att_idx)
    for row in data_rows:
        row_val = row[partition_att_idx]
        # print(row_val)
        if row_val not in partitions.keys():
            partitions[row_val] = {'name_to_idx': data['name_to_idx'], 'idx_to_name': data['idx_to_name'],
                                   'rows': list()}
        partitions[row_val]['rows'].append(row)
    # print(partitions)
    return partitions


def avg_entropy_w_partitions(data, splitting_att, target_attribute):  # find uniq values of splitting att
    data_rows = data['rows']
    n = len(data_rows)
    partitions = partition_data(data, splitting_att)
    avg_ent = 0
    # p=partitions.keys()
    # print(p)
    for partition_key in partitions.keys():
        partitioned_data = partitions[partition_key]
        partition_n = len(partitioned_data['rows'])
        partition_labels = get_class_labels(partitioned_data, target_attribute)
        partition_entropy = entropy(partition_n, partition_labels)
        avg_ent += partition_n / n * partition_entropy
    return avg_ent, partitions


def most_common_label(labels):
    mcl = max(labels, key=lambda k: labels[k])
    return mcl


def id3(data, uniqs, remaining_atts, target_attribute):
    labels = get_class_labels(data, target_attribute)
    # print(labels)
    node = {}
    # a=len(labels.keys())
    # print(a)
    if len(labels.values()) == 1:
        node['label'] = next(iter(labels.keys()))
        # print(node)
        return node
        # print(labels)
    if len(remaining_atts) == 0:
        node['label'] = most_common_label(labels)
        return node

    n = len(data['rows'])
    ent = entropy(n, labels)
    max_info_gain = None
    max_info_gain_att = None
    max_info_gain_partitions = None
    for remaining_att in remaining_atts:
        avg_ent, partitions = avg_entropy_w_partitions(data, remaining_att, target_attribute)
        info_gain = ent - avg_ent
        if max_info_gain is None or info_gain > max_info_gain:
            max_info_gain = info_gain
            max_info_gain_att = remaining_att
            max_info_gain_partitions = partitions
    if max_info_gain is None:
        node['label'] = most_common_label(labels)
        return node
    node['attribute'] = max_info_gain_att
    node['nodes'] = {}
    remaining_atts_for_subtrees = set(remaining_atts)
    remaining_atts_for_subtrees.discard(max_info_gain_att)
    uniq_att_values = uniqs[max_info_gain_att]

    for att_value in uniq_att_values:
        if att_value not in max_info_gain_partitions.keys():
            node['nodes'][att_value] = {'label': most_common_label(labels)}
            continue
        partition = max_info_gain_partitions[att_value]
        node['nodes'][att_value] = id3(partition, uniqs, remaining_atts_for_subtrees, target_attribute)
    return node


def load_config(config_file):
    with open(config_file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
        print(data)
    return ast.literal_eval(data)


'''ast.literal_eval(node_or_string)
Safely evaluate an expression node or a string containing a Python literal or container display. The string or node provided may only consist of the following Python literal structures: strings, bytes, numbers, tuples, lists, dicts, sets, booleans, and None.

This can be used for safely evaluating strings containing Python values from untrusted sources without the need to parse the values oneself. It is not capable of evaluating arbitrarily complex expressions, for example involving operators or indexing.'''


def pretty_print_tree(root):
    stack = []
    rules = set()

    def traverse(node, stack, rules):
        if 'label' in node:
            stack.append(' THEN ' + node['label'])
            rules.add(''.join(stack))
            stack.pop()
        elif 'attribute' in node:
            ifnd = 'IF ' if not stack else ' AND '
            stack.append(ifnd + node['attribute'] + ' EQUALS ')
            for subnode_key in node['nodes']:
                stack.append(subnode_key)
                traverse(node['nodes'][subnode_key], stack, rules)
                stack.pop()
            stack.pop()

    traverse(root, stack, rules)
    print(os.linesep.join(rules))


def main():
    data = load_csv_to_header_data('//dataset.csv')
    data = project_columns(data, ['Outlook', 'Temperature', 'Humidity', 'Windy', 'PlayTennis'])
    target_attribute = 'PlayTennis'
    remaining_attributes = set(data['header'])
    remaining_attributes.remove(target_attribute)
    print(remaining_attributes)
    uniqs = get_uniq_values(data)
    root = id3(data, uniqs, remaining_attributes, target_attribute)
    pretty_print_tree(root)


if __name__ == "__main__": main()

# NOTE: this code is taken from https://github.com/rajathv/Machine-Learning-Lab/blob/master/labprog3/ID3%20algorithm%20with%20python.py
