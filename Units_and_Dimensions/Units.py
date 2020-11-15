
class Unit:

    unit_symbol = {
        'M': 'kg',
        'L': 'm'
        
    }

    def __init__(self, M=0, L=0, T=0, O=0, I=0, N=0, J=0, name=None):
        self.dimensions = {
            'M' : M,
            'L' : L,
            'T' : T,
            'O' : O,
            'I' : I,
            'N' : N,
            'J' : J
        }
        self.name = name  #like newton, weber, kilogram etc

    def __mul__(self, other):
        result = Unit()
        for i in self.dimensions:
            result.dimensions[i] = self.dimensions[i] + other.dimensions[i]
        return result



unit1 = Unit(M=1)
unit2 = Unit(L=1)
print((unit1*unit2).dimensions)