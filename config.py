class Config:
    def __init__(self):
        self.playerA = "BLACK"
        self.playerB = "WHITE"
        self.time = 10
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "123456789"
        self.db_name = "chess_matches"

    def update(self, player_a=None, player_b=None, time_limit=None):
        if player_a is not None:
            self.playerA = player_a
        if player_b is not None:
            self.playerB = player_b
        if time_limit is not None:
            self.time = time_limit