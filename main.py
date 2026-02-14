import cv2
from hand_tracking import hands, get_hand_gesture, draw_hand_landmarks
from face_tracking import detect_smile
from game_logic import Character

cap = cv2.VideoCapture(0)
player = Character()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hand_landmarks(frame, hand_landmarks)
            open_fingers = get_hand_gesture(hand_landmarks)

            # Movement
            if "Index" in open_fingers:
                player.move_up()
            if "Middle" in open_fingers:
                player.move_down()
            if "Ring" in open_fingers:
                player.move_left()
            if "Pinky" in open_fingers and "Thumb" not in open_fingers:
                player.move_right()

            # Shooting
            player.shoot(open_fingers)

    # Power from smile
    if detect_smile(frame):
        player.activate_power()
    else:
        player.deactivate_power()

    # Update bullets
    player.update_bullets()

    # Draw character
    color = (0, 255, 0) if not player.power else (0, 0, 255)
    cv2.circle(frame, (player.x, player.y), 30, color, -1)

    # Draw bullets
    for b in player.bullets:
        cv2.circle(frame, (b.x, b.y), 5, (255, 255, 0), -1)

    # HUD
    cv2.putText(frame, f"Power: {'ON' if player.power else 'OFF'}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Bullets: {len(player.bullets)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("AI Vision Game", frame)

    if cv2.waitKey(5) & 0xFF in [ord('e'), ord('E')]:
        break

cap.release()
cv2.destroyAllWindows()