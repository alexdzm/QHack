#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def error_wire(circuit_output):
    """Function that returns an error readout.

    Args:
        - circuit_output (?): the output of the `circuit` function.

    Returns:
        - (np.ndarray): a length-4 array that reveals the statistics of the
        error channel. It should display your algorithm's statistical prediction for
        whether an error occurred on wire `k` (k in {1,2,3}). The zeroth element represents
        the probability that a bitflip error does not occur.

        e.g., [0.28, 0.0, 0.72, 0.0] means a 28% chance no bitflip error occurs, but if one
        does occur it occurs on qubit #2 with a 72% chance.
    """
    
    # QHACK #
    out=circuit_output
    p0=np.trace(np.matmul(np.outer([alpha,0,0,0,0,0,0,np.sqrt(1-alpha**2)],[alpha,0,0,0,0,0,0,np.sqrt(1-alpha**2)]),out))
    p1=np.trace(np.matmul(np.outer([0,0,0,np.sqrt(1-alpha**2),alpha,0,0,0],[0,0,0,np.sqrt(1-alpha**2),alpha,0,0,0]),out))
    p2=np.trace(np.matmul(np.outer([0,0,alpha,0,0,np.sqrt(1-alpha**2),0,0],[0,0,alpha,0,0,np.sqrt(1-alpha**2),0,0]),out))
    p3=np.trace(np.matmul(np.outer([0,alpha,0,0,0,0,np.sqrt(1-alpha**2),0],[0,alpha,0,0,0,0,np.sqrt(1-alpha**2),0]),out))
    '''
    p0=np.dot([alpha,0,0,0,0,0,0,np.sqrt(1-alpha**2)],np.sqrt(circuit_output))
    p1=np.dot([0,0,0,np.sqrt(1-alpha**2),alpha,0,0,0],np.sqrt(circuit_output))
    p2=np.dot([0,0,alpha,0,0,np.sqrt(1-alpha**2),0,0],np.sqrt(circuit_output))
    p3=np.dot([0,alpha,0,0,0,0,np.sqrt(1-alpha**2),0],np.sqrt(circuit_output))'''
    
    return np.real([p0,p1,p2,p3])
    # process the circuit output here and return which qubit was the victim of a bitflip error!

    # QHACK #


dev = qml.device("default.mixed", wires=3)


@qml.qnode(dev)
def circuit(p, alpha, tampered_wire):
    """A quantum circuit that will be able to identify bitflip errors.

    DO NOT MODIFY any already-written lines in this function.

    Args:
        p (float): The bit flip probability
        alpha (float): The parameter used to calculate `density_matrix(alpha)`
        tampered_wire (int): The wire that may or may not be flipped (zero-index)

    Returns:
        Some expectation value, state, probs, ... you decide!
    """

    qml.QubitDensityMatrix(density_matrix(alpha), wires=[0, 1, 2])

    # QHACK #

    # put any input processing gates here
    qml.CNOT(wires=[0,1])
    qml.CNOT(wires=[0,2])

    qml.BitFlip(p, wires=int(tampered_wire))

    # put any gates here after the bitflip error has occurred

    # return something!
    # QHACK #
    return qml.state()

    #return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2))


def density_matrix(alpha):
    """Creates a density matrix from a pure state."""
    # DO NOT MODIFY anything in this code block
    psi = alpha * np.array([1, 0], dtype=float) + np.sqrt(1 - alpha**2) * np.array(
        [0, 1], dtype=float
    )
    psi = np.kron(psi, np.array([1, 0, 0, 0], dtype=float))
    return np.outer(psi, np.conj(psi))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = np.array(sys.stdin.read().split(","), dtype=float)
    p, alpha, tampered_wire = inputs[0], inputs[1], int(inputs[2])

    error_readout = np.zeros(4, dtype=float)
    circuit_output = circuit(p, alpha, tampered_wire)
    error_readout = error_wire(circuit_output)

    print(*error_readout, sep=",")
