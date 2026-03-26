import cv2
from ultralytics import YOLO
from color_classifier import is_blue_car


class TrafficAnalyzer:
    def __init__(self, model_path="yolov8n.pt"):
        """
        Load YOLO model.
        """
        self.model = YOLO(model_path)

        # ONLY detect cars (not bus, truck, motorcycle)
        self.vehicle_classes = {"car"}
        self.person_class = "person"

    def process_frame(self, frame):
        """
        Process a single frame:
        - detect cars
        - detect people
        - detect blue cars
        - draw rectangles
        - count cars, blue cars, people
        """
        output = frame.copy()

        car_count = 0
        blue_car_count = 0
        people_count = 0

        results = self.model(frame, verbose=False)

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                class_name = self.model.names[cls_id]

                # Skip low confidence detections
                if conf < 0.35:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # Clamp coordinates
                h, w = frame.shape[:2]
                x1 = max(0, min(x1, w - 1))
                y1 = max(0, min(y1, h - 1))
                x2 = max(0, min(x2, w - 1))
                y2 = max(0, min(y2, h - 1))

                if x2 <= x1 or y2 <= y1:
                    continue

                # ONLY CARS
                if class_name in self.vehicle_classes:
                    car_count += 1

                    car_crop = frame[y1:y2, x1:x2]
                    blue_flag, blue_ratio = is_blue_car(car_crop)

                    if blue_flag:
                        # RED rectangle for BLUE cars
                        color = (0, 0, 255)  # Red in BGR
                        blue_car_count += 1
                        label = f"Blue Car {conf:.2f}"
                    else:
                        # BLUE rectangle for OTHER CARS
                        color = (255, 0, 0)  # Blue in BGR
                        label = f"Car {conf:.2f}"

                    cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        output,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )

                # PERSONS
                elif class_name == self.person_class:
                    people_count += 1

                    color = (0, 255, 0)  # Green
                    label = f"Person {conf:.2f}"

                    cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        output,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )

        # Stats panel
        cv2.rectangle(output, (10, 10), (340, 120), (40, 40, 40), -1)

        cv2.putText(output, f"Total Cars: {car_count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(output, f"Blue Cars: {blue_car_count}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(output, f"People Count: {people_count}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        stats = {
            "total_cars": car_count,
            "blue_cars": blue_car_count,
            "other_cars": car_count - blue_car_count,
            "people": people_count
        }

        return output, stats