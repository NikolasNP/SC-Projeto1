from string import ascii_uppercase

class CypherTable:
    def __init__(self):
        self.l = ascii_uppercase
        self.final_table = [self.l[i:] + self.l[:i] for i in range(len(self.l))]
