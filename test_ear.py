import cv2
import mediapipe as mp
import numpy as np

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

grid_row = 1  # 0,1,2
grid_col = 1
GRID_COOLDOWN = 10
grid_cooldown_counter = 0

# Blink parameters
EAR_THRESHOLD = 0.23
MIN_BLINK_FRAMES = 3
LONG_BLINK_FRAMES = 10
COOLDOWN_FRAMES = 6       # prevents double detection
EAR_WINDOW = 3            # smoothing window

frame_counter = 0
cooldown_counter = 0
blink_text = ""
ear_history = []
# ---------------- GAZE PARAMETERS ----------------
GAZE_WINDOW = 5
LEFT_T, RIGHT_T = 0.35, 0.65
UP_T, DOWN_T = 0.35, 0.65
STABLE_FRAMES = 5

gaze_x_hist, gaze_y_hist = [], []
gaze_counter = 0
prev_gaze = "CENTER"
stable_gaze = "CENTER"
# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)
def get_gaze_ratio(eye_points):
    xs = [p[0] for p in eye_points]
    ys = [p[1] for p in eye_points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    eye_width = max_x - min_x
    eye_height = max_y - min_y

    if eye_width == 0 or eye_height == 0:
        return 0.5, 0.5

    center_x = sum(xs) / len(xs)
    center_y = sum(ys) / len(ys)

    gaze_x = (center_x - min_x) / eye_width
    gaze_y = (center_y - min_y) / eye_height

    return gaze_x, gaze_y
def draw_grid(frame, row, col):
    h, w, _ = frame.shape
    cw, ch = w // 3, h // 3

    for i in range(1, 3):
        cv2.line(frame, (i*cw, 0), (i*cw, h), (255,255,255), 1)
        cv2.line(frame, (0, i*ch), (w, i*ch), (255,255,255), 1)

    x1, y1 = col * cw, row * ch
    x2, y2 = x1 + cw, y1 + ch
    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 3)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        left_eye, right_eye = [], []

        for idx in LEFT_EYE:
            lm = face_landmarks.landmark[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            left_eye.append((x, y))
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        for idx in RIGHT_EYE:
            lm = face_landmarks.landmark[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            right_eye.append((x, y))
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # ---- EAR SMOOTHING ----
        ear_history.append(ear)
        if len(ear_history) > EAR_WINDOW:
            ear_history.pop(0)
        ear_avg = sum(ear_history) / len(ear_history)

        cv2.putText(frame, f"EAR: {ear_avg:.3f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # ---- BLINK STABILITY LOGIC ----
        if cooldown_counter > 0:
            cooldown_counter -= 1
            blink_text = ""
        else:
            if ear_avg < EAR_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= LONG_BLINK_FRAMES:
                    blink_text = "LONG BLINK"
                    print("LONG BLINK detected")
                    cooldown_counter = COOLDOWN_FRAMES
                elif frame_counter >= MIN_BLINK_FRAMES:
                    blink_text = "BLINK"
                    print("BLINK detected")
                    cooldown_counter = COOLDOWN_FRAMES
                frame_counter = 0
        # ---------------- GAZE ----------------
        gx_l, gy_l = get_gaze_ratio(left_eye)
        gx_r, gy_r = get_gaze_ratio(right_eye)
        gaze_x = (gx_l + gx_r) / 2
        gaze_y = (gy_l + gy_r) / 2

        gaze_x_hist.append(gaze_x)
        gaze_y_hist.append(gaze_y)
        if len(gaze_x_hist) > GAZE_WINDOW:
            gaze_x_hist.pop(0)
            gaze_y_hist.pop(0)

        gaze_x_s = sum(gaze_x_hist) / len(gaze_x_hist)
        gaze_y_s = sum(gaze_y_hist) / len(gaze_y_hist)

        gaze_dir = "CENTER"
        if gaze_x_s < LEFT_T:
            gaze_dir = "LEFT"
        elif gaze_x_s > RIGHT_T:
            gaze_dir = "RIGHT"
        elif gaze_y_s < UP_T:
            gaze_dir = "UP"
        elif gaze_y_s > DOWN_T:
            gaze_dir = "DOWN"

        if gaze_dir == prev_gaze:
            gaze_counter += 1
        else:
            gaze_counter = 0
            prev_gaze = gaze_dir

        if gaze_counter >= STABLE_FRAMES:
            stable_gaze = gaze_dir
        if grid_cooldown_counter > 0:
            grid_cooldown_counter -= 1
        else:
            if stable_gaze == "LEFT" and grid_col > 0:
                grid_col -= 1
                grid_cooldown_counter = GRID_COOLDOWN
            elif stable_gaze == "RIGHT" and grid_col < 2:
                grid_col += 1
                grid_cooldown_counter = GRID_COOLDOWN
            elif stable_gaze == "UP" and grid_row > 0:
                grid_row -= 1
                grid_cooldown_counter = GRID_COOLDOWN
            elif stable_gaze == "DOWN" and grid_row < 2:
                grid_row += 1
                grid_cooldown_counter = GRID_COOLDOWN
                # Blink select
        if blink_text == "BLINK":
            selected = grid_row*3 + grid_col + 1
            print(f"Selected cell: {selected}")

        # UI
        draw_grid(frame, grid_row, grid_col)
        cv2.putText(frame, f"Gaze: {stable_gaze}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(frame, blink_text, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Stable Blink Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
