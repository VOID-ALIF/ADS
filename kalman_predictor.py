from filterpy.kalman import KalmanFilter
import numpy as np

class TrajectoryPredictor:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=4, dim_z=2)
        dt = 1.0
        self.kf.F = np.array([[1, 0, dt, 0],
                              [0, 1, 0, dt],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        self.kf.H = np.array([[1, 0, 0, 0],
                              [0, 1, 0, 0]])
        self.kf.P *= 1000
        self.kf.R *= 5
        self.kf.Q *= 0.01
        self.initialized = False

    def update(self, x, y):
        if not self.initialized:
            self.kf.x[:2, 0] = [x, y]
            self.kf.x[2:, 0] = [0, 0]
            self.initialized = True
        self.kf.predict()
        self.kf.update([x, y])
        return self.kf.x[:2]

    def predict_future(self, steps=10):
        preds = []
        state = self.kf.x.copy()
        for _ in range(steps):
            state = self.kf.F @ state
            preds.append(state[:2].copy())
        return preds
