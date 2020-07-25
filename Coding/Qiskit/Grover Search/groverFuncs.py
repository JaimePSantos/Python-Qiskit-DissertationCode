#Grover
def markedList(markedList,N):
    oracleList = np.ones(2**N)
    for element in markedList:
        oracleList[element] = -1
    return oracleList.tolist()


def oracleGrover(markedList,N):
    qreg = QuantumRegister(N)
    qc = QuantumCircuit(qreg,name='Oracle')
    qc.diagonal(markedList,qreg)
    return qc


def diffusionGrover(N):
    qreg = QuantumRegister(N)
    difCirc = QuantumCircuit(qreg,name='Diffusion')
    difCirc.h(qreg)
    
    aux = markedList([0],N)
    qcAux = oracleGrover(aux,N)
    difCirc.append(qcAux,range(N))
    
    difCirc.h(qreg)
    return difCirc

def grover(marked,N,backend,steps):
    qc = QuantumCircuit(N,N)
    qcOracle = oracleGrover(markedList(marked,N),N)
    qcDiffusion = diffusionGrover(N)
    qc.h(range(N))
    for i in range(steps):
        qc.append(qcOracle,range(N))
        qc.barrier()
        qc.append(qcDiffusion,range(N))
        qc.barrier()
    qc = transpile(qc,basis_gates=['cx','u3'],backend=backend,optimization_level=2)
    qc.barrier()
    qc.measure(range(N),range(N))
    return qc

def grover2(marked,N,steps):
    qc = QuantumCircuit(N,N)
    qcOracle = oracleGrover(markedList(marked,N),N)
    qcDiffusion = diffusionGrover(N)
    qc.h(range(N))
    for i in range(steps):
        qc.append(qcOracle,range(N))
        qc.barrier()
        qc.append(qcDiffusion,range(N))
        qc.barrier()
    qc = transpile(qc,basis_gates=['cx','u3'],optimization_level=3)
    qc.barrier()
    qc.measure(range(N),range(N))
    return qc

def simul(qc):
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc,backend,shots=3000).result().get_counts()
    return result