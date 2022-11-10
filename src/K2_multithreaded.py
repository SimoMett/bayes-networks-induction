import threading

import pandas

from gFunction import g_function
from node import Node


# nodes_set should be 'pred(node) - pi'
def get_node_that_maximises_g(node: Node, nodes_set, parents_set: set, cases_set: pandas.DataFrame):
    max_g_node = None
    max_g_value = 0

    for node_z in nodes_set:
        value = g_function(node, parents_set.union({node_z.var_name}), cases_set)
        if value > max_g_value:
            max_g_value = value
            max_g_node = node_z
    return max_g_node, max_g_value


def predecessors(node: Node, nodes_dict: dict, nodes_order) -> set:
    pred = set()
    for i in nodes_order:
        if i == node.var_name:
            break
        pred.add(nodes_dict[i])
    return pred


def k2_procedure(nodes_dict: dict, order_array, max_parents: int, cases_set: pandas.DataFrame) -> dict:
    k2_threads = []
    for node_name in order_array:
        thrd = threading.Thread(target=k2_on_node, args=(cases_set, max_parents, nodes_dict[node_name], nodes_dict, order_array))
        k2_threads.append(thrd)
        thrd.start()

    [thrd.join() for thrd in k2_threads]
    return nodes_dict


def k2_on_node(cases_set, max_parents, node, nodes_dict, order_array):
    pi = set()
    old_prob = g_function(node, pi, cases_set)
    ok_to_proceed = True
    while ok_to_proceed and len(pi) < max_parents:

        pred_minus_pi = predecessors(node, nodes_dict, order_array) - pi
        node_z, new_prob = get_node_that_maximises_g(node, pred_minus_pi, pi, cases_set)

        if new_prob > old_prob:
            old_prob = new_prob
            pi.add(node_z.var_name)
        else:
            ok_to_proceed = False
    node.parents = pi  # "write node and its parents"

    print("K2 on node", node.var_name, "done", flush=True)