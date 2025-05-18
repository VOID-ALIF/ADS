import cv2
from yolov8_detector import YoloDetector
from tracker import MultiObjectTracker
from annotation import annotate_frame

video_path = "assets/Drone&Eagle.mp4"
cap = cv2.VideoCapture(video_path)

detector = YoloDetector("yolov8n.pt")
tracker = MultiObjectTracker()
frame_id = 0

# Define defense zone (top-left, bottom-right)
zone = ((100, 100), (400, 400))

def is_violation(predicted_path, zone):
    (x1, y1), (x2, y2) = zone
    for pt in predicted_path:
        x, y = pt
        if x1 < x < x2 and y1 < y < y2:
            return True
    return False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    boxes, confs, classes = detector.detect(frame)

    if len(boxes) > 0:
        # Get center points of all detections
        centers = [((x1+x2)/2, (y1+y2)/2) for (x1, y1, x2, y2) in boxes]

        # Update tracker
        tracked = tracker.update(centers)

        # Annotate all tracked objects
        for obj_id, x, y in tracked:
            preds = tracker.trackers[obj_id]['tracker'].predict_future(steps=20)
            violation = is_violation(preds, zone)

            # Draw red ID if it's a threat
            color = (0, 0, 255) if violation else (0, 255, 0)
            frame = annotate_frame(
                frame,
                center=(int(x), int(y)),
                future_preds=preds,
                obj_id=obj_id,
                color=color
            )

        # Draw defense zone
        (zx1, zy1), (zx2, zy2) = zone
        cv2.rectangle(frame, (zx1, zy1), (zx2, zy2), (255, 0, 0), 2)

        # Show frame
        cv2.imshow("Defense View", frame)

        # Save snapshot
        key = cv2.waitKey(1)
        if key == ord('s'):
            snapshot_path = f"snapshots/frame_{frame_id}.jpg"
            cv2.imwrite(snapshot_path, frame)
            print(f"Saved snapshot: {snapshot_path}")
        elif key == ord('q'):
            break

    frame_id += 1

cap.release()
cv2.destroyAllWindows()