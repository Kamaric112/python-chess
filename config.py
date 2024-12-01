class Config:
    def __init__(self):
        # Các tham số mặc định
        self.playerA = "Default Player A"
        self.playerB = "Default Player B"
        self.time = 10  # Thời gian mặc định là 10 phút

    def update(self, playerA=None, playerB=None, time=None):
        if playerA is not None:
            self.playerA = playerA
        if playerB is not None:
            self.playerB = playerB
        if time is not None:
            self.time = time
