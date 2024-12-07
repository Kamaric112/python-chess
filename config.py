class Config:
    def __init__(self):
        # Các tham số mặc định
        self.playerA = "BLACK"
        self.playerB = "WHITE"
        self.time = 10  # Thời gian mặc định là 10 phút

    def update(self, player_a=None, player_b=None, time_limit=None):
        if player_a is not None:
            self.playerA = player_a
        if player_b is not None:
            self.playerB = player_b
        if time_limit is not None:
            self.time = time_limit