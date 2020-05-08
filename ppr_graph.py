import networkx as nx
import sys, getopt
import pickle

DEFAULT_PATH = '/home/varun/Downloads/final_symptoms.csv'

def similar_symptoms(csv_file_path = DEFAULT_PATH):
    edge_list = dict()
    symptoms = set()
    with open(csv_file_path, "r") as fp:
        for line in fp:
            line = line.replace("\n", '').lower()
            nodes = sorted(line.split(','))
            count = len(nodes)
            for i in range(count-1):
                u = nodes[i]
                symptoms.add(u)
                if u not in edge_list:
                    edge_list[u] = dict()
                req_dict = edge_list[u]
                for j in range(i+1, count):
                    v = nodes[j]
                    symptoms.add(v)
                    if v not in req_dict:
                        req_dict[v] = 0
                    req_dict[v] += 1

    G = nx.Graph()
    for u, node_list in edge_list.items():
        edges = []
        if len(node_list) == 0:
            continue
        for v, w in node_list.items():
            edges.append((u, v, w))
        G.add_weighted_edges_from(edges)

    try:
        with open('/home/varun/Downloads/ppr_graph.pkl', 'wb') as f:
            pickle.dump(G, f)
        with open('/home/varun/Downloads/ppr_symptoms.pkl', 'wb') as f:
            symptoms.remove('symptoms')
            pickle.dump(symptoms, f)
        print('Pickles created')
    except Exception as e:
        print('Error while creating pickles')
        print('ERROR - ', e)

if __name__ == "__main__":

    inputFilePath = DEFAULT_PATH
    try:
        args = getopt.getopt(sys.argv[1:], "hi:", ["input_file="])
    except getopt.GetoptError:
      print('filename.py -i <inputfilepath>')
      sys.exit(2)

    for arg in args[0]:
        if '-i' in arg:
            inputFilePath = str(arg[1])

    rankings = similar_symptoms(inputFilePath)