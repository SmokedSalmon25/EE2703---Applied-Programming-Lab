import numpy as np

def evalSpice(filename):
    circuit, nodes, source_vars, v_sources = clean_circuit(filename)
    req_size = len(nodes) + len(source_vars)        #number of variables
    nodes.remove("GND")
    nodes.insert(0, "GND")      #ensuring that GND is the first variable
    nodes.extend(source_vars)       #nodes now contains all the variables
    mapping = {node: index for index, node in enumerate(nodes)}     #creating a mapping
    cond_matrix, out = build_matrix(circuit, mapping, req_size)     #making the matrices
    try:
        X = np.linalg.solve(cond_matrix, out)       #solving the matrices
    except np.linalg.LinAlgError as e:
        if 'Singular matrix' in str(e):     #error caused due to improper circuit
            raise ValueError('Circuit error: no solution')
    volt_dict, current_dict = build_dict(nodes, v_sources, X)       #building the dictionaries
    return volt_dict, current_dict

def clean_circuit(file_path):       #takes in a file path and outputs various useful lists and dictionaries, including a cleaned circuit
    circuit = []        #will contain a list of lists of split lines
    nodes = []
    flag = 0        #used to check the existence of header and footer of the circuit
    v_sources = []
    elements = []
    try:
        with open(file_path, "r") as file:
            file_contents = file.read()
    except FileNotFoundError:       #raising an error if the file does not exist
            raise FileNotFoundError('Please give the name of a valid SPICE file as input')
    lines = file_contents.split('\n')       #splitting the file into lines
    for line in lines:      #reading through the lines
        if line == ".end" and flag == 1:        #ignoring lines after this marker
            flag = -1
            break
        if flag == 1:       #the header has been encountered, and the circuit begins
            extract_elements(line, circuit, nodes, v_sources, elements)
        if line == ".circuit":        #ignoring the lines before this marker
            flag = 1
    if (flag != -1):        #occurs if circuit header and footer are not properly encountered
        raise ValueError('Malformed circuit file')
    unique_elements = set(elements)     
    if (len(circuit) != len(unique_elements)):      #occurs if any element repeats
        raise ValueError('Repeated Element')
    source_vars = ["i_"+ source for source in v_sources]        #renaming the voltage source variables for clarity
    return circuit, nodes, source_vars, v_sources

def extract_elements(line, circuit, nodes, v_sources, elements):        #takes in a line and appends necessary quiantities to the lists passed
    words = line.split("#")     #ignoring comments
    words1 = words[0].split()       #splitting at blanks to get words
    elements.append(words1[0])      #storing elements
    if (words1[0][0].upper() == 'V' or words1[0][0].upper() == 'R' or words1[0][0].upper() == 'I'):     #valid elements
        if (words1[0][0].upper() == 'V'):
            v_sources.append(words1[0])     #storing all voltage sources
            if (len(words1) != 5 or words1[3] != "dc"):     #checking SPICE syntex
                raise TypeError ("Voltage Source input line has error")
        if (words1[0][0].upper() == "I"):
            if (len(words1) != 5 or words1[3] != "dc"):
                raise TypeError ("Current Source input line has error")
        if (words1[0][0].upper() == "R"):
            if (len(words1) != 4):
                raise TypeError ("Resisitance input line has error")                
        circuit.append(words1)      #if everything is correct, append the list of words to circuit
        if not words1[1] in nodes:
            nodes.append(words1[1])     #building list of unique nodes
        if not words1[2] in nodes:
            nodes.append(words1[2]) 
    else:
        raise ValueError('Only V, I, R elements are permitted')
    return circuit, nodes, v_sources

def build_matrix(circuit, mapping, req_size):       #builds the conduction and output matrix given the circuit, mapping and number of variables
    cond_matrix  = np.array([np.zeros(req_size) for _ in range (req_size)])     #initialization
    out = np.zeros(req_size)
    for line in circuit:
        num_1 = mapping[line[1]]        #nodes connected to element
        num_2 = mapping[line[2]]
        if line[0][0] == 'R':       #resistance    
            try:        #checking for string values       
                res = float(line[3])
            except ValueError:
                raise ValueError('Malformed circuit file')
            if res >= float(0):     #handling 0 and negative values of R
                pass
            elif res == float(0):
                res = float(1e-10)
            else:
                raise ValueError('Negative Resistance')
            cond_matrix[num_1][num_1] += 1 / res        #making necessary changes to the matrix
            cond_matrix[num_2][num_2] += 1 / res        
            cond_matrix[num_1][num_2] -= 1 / res
            cond_matrix[num_2][num_1] -= 1 / res
        if line[0][0] == 'V':       #voltage source
            num_3 = mapping["i_"+ line[0]]      #line corresponding to current through voltage source
            cond_matrix[num_1][num_3] -= 1
            cond_matrix[num_2][num_3] += 1
            cond_matrix[num_3][num_1] += 1
            cond_matrix[num_3][num_2] -= 1
            try:        #checking for invalid voltage
                voltage = float(line[4])
            except ValueError:
                raise ValueError('Malformed circuit file')
            out[num_3] += float(voltage)
        if line[0][0] == "I":       #current source
            try:        #checking for invalid current
                voltage = float(line[4])
            except ValueError:
                raise ValueError('Malformed circuit file')
            out[num_1] -= float(line[4])
            out[num_2] += float(line[4])
    out[0] = 0      #rewriting first row of input and output to satisfy the constraint that GND has 0 voltage
    cond_matrix[0] = np.zeros(req_size)
    cond_matrix[0][0] += 1
    return cond_matrix, out

def build_dict(nodes, v_sources, X):        #builds the required dictionaries
    volt_dict = {}      #here, the variable "nodes" contains all the variables, nodes as well as source currents
    current_dict = {}
    for i in range (len(nodes) - len(v_sources)):       #writing down values for node voltages
        volt_dict[nodes[i]] = X[i]
    for i in range (len(nodes) - len(v_sources), len(nodes)):       #writing down currents through voltage sources
        current_dict[v_sources[i - (len(nodes) - len(v_sources))]] = -X[i]
    return volt_dict, current_dict  