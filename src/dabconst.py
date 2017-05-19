class tm1():
    def __init__(self, rate = 2048000):
        self.upsampling = rate / 2048000
        self.L = 76
        self.K = 1536

        self.S_F = 196608 * self.upsampling
        self.T_F = float(self.S_F) / rate

        self.S_NULL = 2656 * self.upsampling
        self.T_NULL = float(self.S_NULL) / rate

        self.S_S = 2552 * self.upsampling
        self.T_S = float(self.S_S) / rate

        self.S_U = 2048 * self.upsampling
        self.T_S = float(self.S_U) / rate

        self.S_GUARD = 504 * self.upsampling
        self.T_GUARD = float(self.S_GUARD) / rate
