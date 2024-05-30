class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, matrixFilePath=None):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}

        if matrixFilePath:
            self.load_matrix(matrixFilePath)

    def load_matrix(self, matrixFilePath):
        with open(matrixFilePath, 'r') as file:
            lines = file.readlines()
            self.numRows = int(lines[0].split('=')[1])
            self.numCols = int(lines[1].split('=')[1])

            for line in lines[2:]:
                if line.strip():
                    row, col, value = self.parse_entry(line.strip())
                    self.elements[(row, col)] = value

    def parse_entry(self, entry):
        if not (entry.startswith('(') and entry.endswith(')')):
            raise ValueError("Input file has wrong format")
        row, col, value = map(int, entry[1:-1].split(','))
        return row, col, value

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def __str__(self):
        return f"SparseMatrix({self.numRows}x{self.numCols}) with elements: {self.elements}"

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition")
        
        result = SparseMatrix(self.numRows, self.numCols)
        for (i, j), value in self.elements.items():
            result.set_element(i, j, value + other.get_element(i, j))
        
        for (i, j), value in other.elements.items():
            if (i, j) not in self.elements:
                result.set_element(i, j, value)
        
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        
        result = SparseMatrix(self.numRows, self.numCols)
        for (i, j), value in self.elements.items():
            result.set_element(i, j, value - other.get_element(i, j))
        
        for (i, j), value in other.elements.items():
            if (i, j) not in self.elements:
                result.set_element(i, j, -value)
        
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        
        result = SparseMatrix(self.numRows, other.numCols)
        for (i, k), value in self.elements.items():
            for j in range(other.numCols):
                result.set_element(i, j, result.get_element(i, j) + value * other.get_element(k, j))
        
        return result
def main():
    import os

    def load_sparse_matrix(file_path):
        return SparseMatrix(matrixFilePath=file_path)

    def perform_operation(matrix1, matrix2, operation):
        if operation == 'add':
            return matrix1.add(matrix2)
        elif operation == 'subtract':
            return matrix1.subtract(matrix2)
        elif operation == 'multiply':
            return matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation")

    matrix1_path = input("Enter path for first sparse matrix file: ")
    matrix2_path = input("Enter path for second sparse matrix file: ")
    operation = input("Enter the operation to perform (add, subtract, multiply): ")

    matrix1 = load_sparse_matrix(matrix1_path)
    matrix2 = load_sparse_matrix(matrix2_path)

    result = perform_operation(matrix1, matrix2, operation)
    print(result)

if __name__ == "__main__":
    main()
