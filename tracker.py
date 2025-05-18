import numpy as np
from kalman_predictor import TrajectoryPredictor
from scipy.spatial.distance import cdist

class MultiObjectTracker:
    def __init__(self, max_distance=50):
        self.trackers = {}
        self.next_id = 0
        self.max_distance = max_distance

    def update(self, detections):
        """
        detections: list of (x, y) tuples (center of each detection)
        Returns: list of (id, x, y) for current tracked objects
        """
        new_centroids = np.array(detections)
        ids = list(self.trackers.keys())
        old_centroids = np.array([self.trackers[_id]['last_pos'] for _id in ids])

        assignments = {}
        if len(old_centroids) > 0 and len(new_centroids) > 0:
            dist_matrix = cdist(old_centroids, new_centroids)
            for i, row in enumerate(dist_matrix):
                min_j = np.argmin(row)
                if row[min_j] < self.max_distance:
                    assignments[ids[i]] = new_centroids[min_j]

        # Update assigned trackers
        updated = []
        used = set()
        for _id, pos in assignments.items():
            tracker = self.trackers[_id]['tracker']
            tracker.update(*pos)
            self.trackers[_id]['last_pos'] = pos
            updated.append((_id, *tracker.kf.x[:2]))
            used.add(tuple(pos))

        # Add new trackers for unmatched detections
        for det in detections:
            if tuple(det) not in used:
                tracker = TrajectoryPredictor()
                tracker.update(*det)
                self.trackers[self.next_id] = {
                    'tracker': tracker,
                    'last_pos': det
                }
                updated.append((self.next_id, *det))
                self.next_id += 1

        return updated
