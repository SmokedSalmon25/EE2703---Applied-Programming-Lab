# Assignment 2 - SPICE simulation

In this assignment, we are required to read in the SPICE simulator representation of a circuit and output the voltages of the nodes and currents through the voltage sources, thus essentially solving the circuit. We do this by applying the modified nodal analysis method. The code can be broken down into three major steps:

- Reading in the circuit
- Building the matrix
- Solving the matrix

## Step 1: Reading in the circuit

- The SPICE simulator representation of a ciruit involves the header *.circuit* and the footer *.end* clearly flanking the circuit. Thus, one must ignore lines above the header and below the footer, while simultaneously checking for the existence of the same to ensure that the given circuit is valid.
- One also needs to ensure that in the circuit, everything after the *#* symbol is ignored as a comment.
- All this is done using the *clean_circuit* function in the code, where the existence of the given file is checked and, if it exists, the file is opened and read.
- The file is iterated through line by line, and appropriate flags are raised upon reaching the header and the footer.
- Between the header and the footer, the function *extract_elements* is called to check the validity of each element line, and store the element, the nodes that it connects and its value.
- A few error cases considered here are the passing of valid elements, expected syntax of particular elements (5 parts of a voltage or current source, 4 for a resistance) and passing of anything else apart from dc sources.
- Converting the value associated with each element to a float raises an error in case of improper imput, and further checking raises error in case of a negative value of resistance.
- Repetition of element names is also checked for.
- Further, a list of nodes is also returned.

## Step 2: Building the matrix

- Once the necessary information has been extracted, a matrix is constructed using the *build_matrix* function.
- The variables of the circuit are each of the node voltages, as well as the currents through the nodes.
- A mapping is created between the variables and whole numbers to help keep track of rows corresponding to variables in the circuit.
- For the resistances, the conductance is appropriately added and subtracted to elements of the conductance matrix, considering the rows and the nodes it is connected to.
- For a resistance of 0 ohms, an approximation of converting it to a very small value is carried out (1e-10 ohms)
- For current sources, current is taken into consideration in the output matrix keeping sign conventions in mind.
- For voltage sources, current through it is taken into consideration, and the constraint of potential difference between the two nodes is added.
- Finally, as the matric now consists of dependent equations, one equation is replaced with the constraint that the voltage of *GND* is 0.

## Step 3: Solving the Matrix

- Gaussian Elimination is used to solve the above matrix, which is of the form *AX = B*
- This is done using the predefined function from the *numpy* library, *np.linalg.solve*

In this manner, any circuit containing resistances and independent current and voltage sources can be solved.

I would like to acknowledge the contributions made by Nitin G. (EE22B041), discussions with whom have helped me make significant progress with my code.
