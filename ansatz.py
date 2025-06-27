from ruquant import QuantumCircuit

class UCCSDAnsatz:
    def __init__(self, num_qubits: int, num_electrons: int):
        self.num_qubits = num_qubits
        self.num_electrons = num_electrons
        
    def build_circuit(self, params: List[float]) -> QuantumCircuit:
        """Построение UCCSD анзатца"""
        qc = QuantumCircuit(self.num_qubits)
        
        # Добавление начального состояния Хартри-Фока
        for i in range(self.num_electrons):
            qc.x(i)
        
        # Добавление кластерных операторов
        param_idx = 0
        for i in range(self.num_electrons):
            for a in range(self.num_electrons, self.num_qubits):
                # Одиночные возбуждения
                qc.ry(params[param_idx], i)
                qc.cnot(i, a)
                qc.ry(params[param_idx+1], a)
                qc.cnot(i, a)
                param_idx += 2
                
                # Двойные возбуждения
                for j in range(i+1, self.num_electrons):
                    for b in range(a+1, self.num_qubits):
                        qc.cnot(i, j)
                        qc.cnot(a, b)
                        qc.ry(params[param_idx], j)
                        qc.cnot(j, b)
                        qc.ry(params[param_idx+1], b)
                        qc.cnot(j, b)
                        qc.cnot(i, j)
                        qc.cnot(a, b)
                        param_idx += 2
        return qc
