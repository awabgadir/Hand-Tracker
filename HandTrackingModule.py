import cv2
import mediapipe as mp
import time

#3.11.5 ('base':conda)

class handDetector():
    def __init__(self, mode=False, maxHands=2):
        self.mode = mode
        self.maxHands = maxHands


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #can convert color to other forms!
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw: 
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img 
    
    def findPosition(self, img, handNo=0, draw=True): #change handNo to get position of multiple hands
        
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
 
            for id, lm in enumerate(myHand.landmark):

                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                # if id == 0:
                if draw: 
                    cv2.circle(img, (cx,cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList 

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        sucess, img = cap.read()
        img = detector.findHands(img) #write draw=False in param to not show drawing at all
        lmList = detector.findPosition(img) #write draw=False in param to not show custom drawing
        if len(lmList) != 0:
            print(lmList[4]) #change 4 to track certain locations

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

#^copy everything under main, import the libraries associated, and import HandTrackingModule.py as htm, put in front of red

if __name__ == "__main__":
    main()