import cv2
import mediapipe as mp
import numpy as np
import time

# ------------------ MEDIAPIPE ------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
# ------------------ CURSOR ------------------
CURSOR_RADIUS = 10
CURSOR_SMOOTHING = 0.25  # lower = smoother, slower

cursor_x, cursor_y = 0.5, 0.5

# ------------------ CALIBRATION ------------------
CALIBRATION_POINTS = [
    (0.025, 0.05), (0.50, 0.05), (0.95, 0.05),
    (0.025, 0.50), (0.50, 0.50), (0.95, 0.50),
    (0.025, 0.95), (0.50, 0.95), (0.95, 0.95)
]
DOT_RADIUS = 12
SETTLE_TIME = 0.3
CALIBRATION_TIME = 1.5

calibration_points = [
    "TOP_LEFT", "TOP_CENTER", "TOP_RIGHT",
    "MID_LEFT", "CENTER", "MID_RIGHT",
    "BOTTOM_LEFT", "BOTTOM_CENTER", "BOTTOM_RIGHT"
]
calib_index = 0
calib_data = {k: [] for k in calibration_points}
last_time = time.time()
calibrated = False

# ------------------ LANDMARKS ------------------
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]

# ------------------ GRID ------------------
grid_row, grid_col = 1, 1
GRID_COOLDOWN = 10
grid_cooldown = 0

# ------------------ BLINK ------------------
EAR_THRESHOLD = 0.23
MIN_BLINK_FRAMES = 3
frame_counter = 0
blink_text = ""
blink_detected = False

# ------------------ GAZE LIMITS ------------------
LEFT_T = RIGHT_T = UP_T = DOWN_T = 0.5
CENTER_RADIUS = 0.04
GAZE_HOLD_FRAMES = 3
gaze_counter = 0
last_gaze = "CENTER"
stable_gaze = "CENTER"

# ------------------ FUNCTIONS ------------------
def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def iris_gaze(eye, iris):
    ex = [p[0] for p in eye]
    ey = [p[1] for p in eye]
    ix = [p[0] for p in iris]
    iy = [p[1] for p in iris]

    min_x, max_x = min(ex), max(ex)
    min_y, max_y = min(ey), max(ey)

    gx = (np.mean(ix) - min_x) / max((max_x - min_x), 1)
    gy = (np.mean(iy) - min_y) / max((max_y - min_y), 1)

    return gx, gy

def draw_grid(frame, r, c):
    h, w, _ = frame.shape
    cw, ch = w // 3, h // 3
    for i in range(1, 3):
        cv2.line(frame, (i*cw, 0), (i*cw, h), (255,255,255), 1)
        cv2.line(frame, (0, i*ch), (w, i*ch), (255,255,255), 1)
    cv2.rectangle(frame, (c*cw, r*ch), ((c+1)*cw, (r+1)*ch), (0,255,0), 3)

# ------------------ CAMERA ------------------
cap = cv2.VideoCapture(0)

prev_gx, prev_gy = 0.5, 0.5  # for head movement filter

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = face_mesh.process(rgb)

    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0]
        left_eye, right_eye, left_iris, right_iris = [], [], [], []

        for i in LEFT_EYE:
            x, y = int(lm.landmark[i].x*w), int(lm.landmark[i].y*h)
            left_eye.append((x,y))
        for i in RIGHT_EYE:
            x, y = int(lm.landmark[i].x*w), int(lm.landmark[i].y*h)
            right_eye.append((x,y))
        for i in LEFT_IRIS:
            x, y = int(lm.landmark[i].x*w), int(lm.landmark[i].y*h)
            left_iris.append((x,y))
        for i in RIGHT_IRIS:
            x, y = int(lm.landmark[i].x*w), int(lm.landmark[i].y*h)
            right_iris.append((x,y))

        gx_l, gy_l = iris_gaze(left_eye, left_iris)
        gx_r, gy_r = iris_gaze(right_eye, right_iris)

        gaze_x = (gx_l + gx_r) / 2
        gaze_y = (gy_l + gy_r) / 2

        # ------------- HEAD MOVEMENT FILTER ----------------
        if abs(gaze_x - prev_gx) > 0.3 or abs(gaze_y - prev_gy) > 0.3:
            gaze_x, gaze_y = prev_gx, prev_gy
        else:
            prev_gx, prev_gy = gaze_x, gaze_y

        # ---------------- CALIBRATION MODE ----------------
        if not calibrated:
            px = int(CALIBRATION_POINTS[calib_index][0] * w)
            py = int(CALIBRATION_POINTS[calib_index][1] * h)

            cv2.circle(frame, (px, py), DOT_RADIUS, (0, 0, 255), -1)
            cv2.putText(frame, "LOOK AT THE DOT", (px - 120, py - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            cv2.putText(frame, f"Calibration {calib_index+1}/9",
                        (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            elapsed = time.time() - last_time
            if elapsed > SETTLE_TIME:
                calib_data[calibration_points[calib_index]].append((gaze_x, gaze_y))

            if elapsed > CALIBRATION_TIME:
                calib_index += 1
                last_time = time.time()
                if calib_index == len(calibration_points):
                    calibrated = True
                    center_x = np.mean([v[0] for v in calib_data["CENTER"]])
                    center_y = np.mean([v[1] for v in calib_data["CENTER"]])
                    left_x = np.mean([v[0] for v in calib_data["MID_LEFT"]])
                    right_x = np.mean([v[0] for v in calib_data["MID_RIGHT"]])
                    up_y = np.mean([v[1] for v in calib_data["TOP_CENTER"]])
                    down_y = np.mean([v[1] for v in calib_data["BOTTOM_CENTER"]])

                    LEFT_T = (left_x + center_x)/2
                    RIGHT_T = (right_x + center_x)/2
                    UP_T = (up_y + center_y)/2
                    DOWN_T = (down_y + center_y)/2

                    print("Calibration complete")
                    print("LEFT_T, RIGHT_T, UP_T, DOWN_T:", LEFT_T, RIGHT_T, UP_T, DOWN_T)

        # ---------------- LIVE MODE ----------------
        else:
            # Center dead-zone
            if abs(gaze_x - center_x) < CENTER_RADIUS and abs(gaze_y - center_y) < CENTER_RADIUS:
                gaze = "CENTER"
            else:
                if gaze_x < LEFT_T:
                    gaze = "LEFT"
                elif gaze_x > RIGHT_T:
                    gaze = "RIGHT"
                elif gaze_y < UP_T:
                    gaze = "UP"
                elif gaze_y > DOWN_T:
                    gaze = "DOWN"

            # Gaze hold logic
            if gaze == last_gaze:
                gaze_counter += 1
            else:
                gaze_counter = 0
                last_gaze = gaze

            if gaze_counter >= GAZE_HOLD_FRAMES:
                if grid_cooldown == 0:
                    if gaze == "LEFT" and grid_col > 0:
                        grid_col -= 1
                    elif gaze == "RIGHT" and grid_col < 2:
                        grid_col += 1
                    elif gaze == "UP" and grid_row > 0:
                        grid_row -= 1
                    elif gaze == "DOWN" and grid_row < 2:
                        grid_row += 1
                    grid_cooldown = GRID_COOLDOWN
                gaze_counter = 0
            else:
                grid_cooldown = max(grid_cooldown-1,0)

            # ---------------- BLINK SELECTION ----------------
            ear_left = eye_aspect_ratio(left_eye)
            ear_right = eye_aspect_ratio(right_eye)
            ear = (ear_left + ear_right)/2

            if ear < EAR_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= MIN_BLINK_FRAMES:
                    blink_detected = True
                    print(f"BLINK SELECT: Grid cell {grid_row*3 + grid_col +1}")
                    blink_text = "BLINK!"
                frame_counter = 0

            draw_grid(frame, grid_row, grid_col)
            cv2.putText(frame, f"Gaze: {gaze}", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255),2)
            cv2.putText(frame, blink_text, (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)
            if blink_detected:
                blink_detected = False

    cv2.imshow("9-Point Calibrated Gaze + Blink System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
