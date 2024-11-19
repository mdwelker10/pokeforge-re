class APIException(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
      
    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message
        }
    
    def __str__(self):   
        return f"{self.code}: {self.message}"

    def __repr__(self):
        return f"APIException(code={self.code}, message={self.message!r})"
    
    # Needed because Exception takes *args, and doesnt have an implicity message attribute
    @property
    def message(self):
        return self.args[0]