from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = results[0].boxes
        if detections is None or detections.xyxy is None:
            return [], [], []
        return (
            detections.xyxy.cpu().numpy(),
            detections.conf.cpu().numpy(),
            detections.cls.cpu().numpy()
        )
