def str_to_posting(txt: str):
    content = txt.split('-')
    for i in range(2, len(content)):
        content[i] = content[i].split(',')
    return Posting(*content)

class Posting: # This is the posting class that stores indexes information

    def __init__(self, docId: int, weight:int, head_index: list, bold_index: list, reg_index: list):
        self._docId = docId
        self._weight = weight
        self._head_index = head_index
        self._bold_index = bold_index
        self._reg_index = reg_index
        # probably need more attributes

    def docId(self):
        return self._docId
    
    def weight(self):
        return self._weight
    
    def head_index(self):
        return self._head_index
    
    def bold_index(self):
        return self._bold_index
    
    def reg_index(self):
        return self._reg_index
    
    def __repr__(self):
        return (f"{self.docId()}-{self.weight()}-{','.join(str(i) for i in self.head_index())}-{','.join(str(i) for i in self.bold_index())}-{','.join(str(i) for i in self.reg_index())}")
