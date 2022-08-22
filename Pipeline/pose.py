import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils # 포즈 위 추정 표시 그리기 위함
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose # 포즈 처리

# 웹캡 열기
cap = cv2.VideoCapture(0)

with mp_pose.Pose( # 포즈 추적, 감지 최소 신뢰성
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose: 
  
  while cap.isOpened(): # 카메라 켜있는동안 루프
    success, image = cap.read() # 사진 한장 얻기
    if not success: # 사진 못얻어왔으면
      print("Ignoring empty camera frame.") # 에러 출력
      continue # 카메라 로딩 중일수도 있으니 cont, 루프 처음으로 돌아감

        
    # 성능 향상 위해 이미지 쓰기불가로 전환후 RGB 전환
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image) # 포즈 검출

    # 이미지 쓰기가능으로 전환 후 다시 BGR 전환
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # 임의로 넣은 양 손목 좌표와 사이 거리
    if results.pose_landmarks:
                wrist1 = int(results.pose_landmarks.landmark[15].x * 100 )
                wrist2 = int(results.pose_landmarks.landmark[16].x * 100 )
                dist = abs(wrist1 - wrist2)
                cv2.putText(
                    image, text='f1=%d f2=%d dist=%d ' % (wrist1,wrist2,dist), org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=255, thickness=3)  
                
    
    # 이미지에 랜드마크 위치 표시
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    # 그 이미지 화면에 flip 해서 출력
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    
    if cv2.waitKey(5) & 0xFF == 27:
      break
    
cap.release()