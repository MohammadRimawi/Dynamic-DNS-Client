class InvalidIPv4(Exception):
    """Exception raised when providing an invalid IPv4"""
    def __init__(self, ip):
        self.message = f'The IP: "{ip}" is not a valid IPv4'
    def __str__(self):
        return str(self.message)
