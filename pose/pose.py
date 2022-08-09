#intention is to make a program for detecting humans in video and then estimating the poses

##for detecting humans in video
from time import time
import numpy as np
import cv2
from google.colab.patches import cv2_imshow
import mediapipe as mp
import matplotlib.pyplot as plt
import math
mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils

pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity = 2)
vid = cv2.VideoCapture('test.mp4')

while vid.isOpened():
    success, frame = vid.read()
    try:
        # convert the frame to RGB format
        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # processing RGB frame for results
        results = pose.process(RGB)
        print(results.pose_landmarks)
        # draw detected pose on the frame
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # show the final output
        cv2.imshow('Output', frame)
    except:
        break
    if cv2.waitKey(1) == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()




#now we create a pose detction function
def detectPose(image, pose, display=True):
    
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,connections=mpPose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height),(landmark.z * width)))

    if display:
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output");plt.axis('off');
        
        mpDraw.plot_landmarks(results.pose_world_landmarks, mpPose.POSE_CONNECTIONS)
    else:
        return output_image, landmarks

pose_video = mpPose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
video = cv2.VideoCapture('warrior.mp4')
time1 = 0
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    frame, _ = detectPose(frame, pose_video, display=False)
    time2 = time()
    if (time2 - time1)>0 :
        frames_per_second = 1.0 / (time2 - time1) 
        cv2.putText(frame, 'FPS: {}'.format(int(frames_per_second)), (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    
    # Update the previous frame time to this frame time.
    # As this frame will become previous frame in next iteration.
    time1 = time2
    
    # Display the frame.
    cv2_imshow(frame)
    
    k = cv2.waitKey(1) == 0xFF
    
    # Check if 'ESC' is pressed.
    if(k == 27):
        
        # Break the loop.
        break

# Release the VideoCapture object.
video.release()

# Close the windows.
cv2.destroyAllWindows()



#now that all frames and videos are working correctly,
#lets classify poses based in angles
def poseAngles(landmark1, landmark2, landmark3):
    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle
#testing
angle = poseAngles((120, 356, 65), (262, 233, 0), (178, 241, 0)) 
# Display the calculated angle.
print(f'The calculated angle is {angle}')

##now that we can accurately calculate the angles, lets define poses
def poseClassify(landmarks, output_image, display=False):
    # Initialize the label of the pose which is not known at this stage.
    label = 'Unknown pose'
    color = (0, 0, 255)
    #required angles.
    #angle between the left shoulder, elbow and wrist points. 
    left_elbow_angle = poseAngles(landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value],landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value],landmarks[mpPose.PoseLandmark.LEFT_WRIST.value])
    
    #angle between the right shoulder, elbow and wrist points. 
    right_elbow_angle = poseAngles(landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value],landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value],landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value])   
    
    #angle between the left elbow, shoulder and hip points. 
    left_shoulder_angle = poseAngles(landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value],landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value],landmarks[mpPose.PoseLandmark.LEFT_HIP.value])

    #angle between the right hip, shoulder and elbow points. 
    right_shoulder_angle = poseAngles(landmarks[mpPose.PoseLandmark.RIGHT_HIP.value],landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value],landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value])

    #angle between the left hip, knee and ankle points. 
    left_knee_angle = poseAngles(landmarks[mpPose.PoseLandmark.LEFT_HIP.value],landmarks[mpPose.PoseLandmark.LEFT_KNEE.value],landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value])

    #angle between the right hip, knee and ankle points 
    right_knee_angle = poseAngles(landmarks[mpPose.PoseLandmark.RIGHT_HIP.value],landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value],landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value])

    #for warrior pose
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
        if left_shoulder_angle < 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:
                    label = 'Warrior II Pose' 
    #for tree pose
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
            label = 'Tree Pose'
    #checking if the pose is classified successfully
    if label != 'Unknown pose':
        color = (0, 255, 0)  
     
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    
    #the resultant image
    if display:
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    else:
        return output_image, label

video = cv2.VideoCapture('tree.mp4')
while video.isOpened():
    success, frame = video.read()
    if not success:
        continue
    frame, landmarks = detectPose(frame, pose_video, display=False)
    if landmarks:
        # Perform the pose classification.
        frame, _ = poseClassify(landmarks, frame, display=False)
    # Display the frame.
    cv2.imshow('Pose Detection', frame)
    k = cv2.waitKey(1) == 0xFF
    if(k == 27):
        break
video.release()
cv2.destroyAllWindows()