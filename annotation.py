import cv2

def annotate_frame(frame, center, future_preds, obj_id=None, color=(0, 255, 0)):
    if center:
        cv2.circle(frame, center, 5, color, -1)
        if obj_id is not None:
            cv2.putText(frame, f'ID {obj_id}', (center[0]+5, center[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    for pt in future_preds:
        cv2.circle(frame, (int(pt[0]), int(pt[1])), 3, (0, 0, 255), -1)

    return frame