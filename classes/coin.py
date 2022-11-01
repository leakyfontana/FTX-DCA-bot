class Coin(): 
    def __init__(self, dict):
        self.coin: str
        self.free: int
        self.spotBorrow: int
        self.total: int
        self.usdValue: int
        self.availableWithoutBorrow: int

        for key in dict:
            setattr(self, key, dict[key])

    def __str__(self):
        return f'Coin({self.coin})'