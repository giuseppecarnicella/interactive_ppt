import cv2
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector


########## Presentation folder path ##########
folderPath = "Presentation"

########## Camera Setup ##########
width, height = 1280, 720                                              # 1280, 720 ; 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
gestureThreshold = int(height * 0.7)                                   # Line height, height above which hand gestures are recognized on the camera

########## Hand Detector ##########
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

########## Variables ##########
pathImages = sorted(os.listdir(folderPath), key=lambda x: x.lower())    # Get list of presentation images
imgNumber = 0                                                           # Index of current slide, starts at value 0

buttonPressed = False                                                   # Signal indicating whether to wait before a new gesture
delay = 15                                                              # Time delay threshold for gesture recognition (in frames)
counter = 0                                                             # Counter for tracking time elapsed since last gesture

annotations = [[]]                                                      # Stores the lists of coordinates of the index finger to draw
annotationNumber = -1                                                   # Stores the number of lists of coordinates of the index finger to draw
annotationStart = False                                                 # Signals not to draw a connection line between the previous and next lines to be drawn

prev_hand_pos = None                                                    # Stores hand wrist coordinates in the previous frame
movement_threshold = 15                                                 # Distance threshold for wrist movement detection
len_last_movements = 4                                                  # Length for the list of movements
last_movements = ['nothing'] * len_last_movements                       # Store the last detected wrist movements

while True:
    # Get the current frame from the camera capture
    success, img = cap.read()
    img = cv2.flip(img, 1)                  # Current image-frame
    
    # Get the current image-slide
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgSlide = cv2.imread(pathFullImage)  # Current image-slide

    # Find the hand, its landmarks, and draw them
    hands, img = detectorHand.findHands(img)
    #hands, img = detectorHand.findHands(img, flipType=False)
    
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    # ---------- If hand is detected ---------- #
    if hands and buttonPressed is False:

        hand    = hands[0]                          # Get the first hand found
        fingers = detectorHand.fingersUp(hand)      # List of which fingers are up
        lmList  = hand["lmList"]                    # List of 21 Landmark points

        # To facilitate drawing the cursor (lmList[8] represents the index of the hand)
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))    # Restricts the vertical movement of the index finger of the hand within the slide
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))     # Restricts the horizontal movement of the index finger of the hand within the slide
        indexFinger = xVal, yVal                                                # Store the coordinates of the index finger

        # ---------- If the y-coordinate of the center of the hand is at the height of the line and the hand is open ---------- #
        if hand["center"][1] <= gestureThreshold and fingers == [1, 1, 1, 1, 1]:
            
            hand_pos = lmList[0][0], lmList[0][1]       # Stores the current coordinates of the hand's wrist
                
            # Compares the current position of the hand's wrist with the previous one to determine if the hand is moving
            if prev_hand_pos is not None:
                if hand_pos[0] - prev_hand_pos[0] > movement_threshold:     # From left to right
                    last_movements.append('sx')
                elif hand_pos[0] - prev_hand_pos[0] < -movement_threshold:  # From right to left
                    last_movements.append('dx')
                else:
                    last_movements.append('nothing')
                    
            if len(last_movements) > len_last_movements:
                last_movements.pop(0)
                        
            prev_hand_pos = hand_pos                    # Update the variable prev_hand_pos
                
            # GESTURE 1 : Left
            if all(movement == 'sx' for movement in last_movements):
                prev_hand_pos = None
                last_movements = ['nothing'] * len_last_movements
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1                      # Move to the previous slide
                    annotations = [[]]                  
                    annotationNumber = -1
                    annotationStart = False   
            # GESTURE 2 : Right
            elif all(movement == 'dx' for movement in last_movements):
                prev_hand_pos = None
                last_movements = ['nothing'] * len_last_movements
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1                      # Move to the next slide
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False               
        else:
            prev_hand_pos = None
            last_movements.append('nothing')
            if len(last_movements) > len_last_movements:
                last_movements.pop(0)

        # GESTURE 3 : Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgSlide, indexFinger, 12, (0, 0, 255), cv2.FILLED) # Draw a circle positioned at the coordinates of the index finger

        # GESTURE 4.1 : Draw Pointer (Memorize the coordinates of the index finger to draw them in code section 4.2)
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgSlide, indexFinger, 12, (0, 0, 255), cv2.FILLED) # Draw a circle positioned at the coordinates of the index finger
        else:
            annotationStart = False

        # GESTURE 5 : Erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

    # ---------- Control if a certain time interval "delay" has passed before being able to make a new gesture ---------- #
    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    # GESTURE 4.2 : Draw Pointer (Draw the coordinates of the index finger that were stored in code section 4.1)
    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgSlide, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    # Display windows
    cv2.imshow("Presentation", imgSlide)        # Display current slide image
    cv2.imshow("Camera", img)                   # Display current camera-captured image

    # Stop the program if the ESC key is pressed
    key = cv2.waitKey(1)
    if key == 27:
        break