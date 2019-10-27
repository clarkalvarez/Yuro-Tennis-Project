import cv2
import numpy as np
def nothing(x):
    
    pass
cap=cv2.VideoCapture(1)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H","Trackbars",0,180,nothing)
cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
cv2.createTrackbar("L-V","Trackbars",118,255,nothing)
cv2.createTrackbar("U-H","Trackbars",180,180,nothing)
cv2.createTrackbar("U-S","Trackbars",255,255,nothing)
cv2.createTrackbar("U-V","Trackbars",255,255,nothing)
ret,frame1 = cap.read()
ret,frame2 = cap.read()
font = cv2.FONT_HERSHEY_COMPLEX
while True:
 
    _, frame = cap.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L-H","Trackbars")
    l_s = cv2.getTrackbarPos("L-S","Trackbars")
    l_v = cv2.getTrackbarPos("L-V","Trackbars")
    u_h = cv2.getTrackbarPos("U-H","Trackbars")
    u_s = cv2.getTrackbarPos("U-S","Trackbars")
    u_v = cv2.getTrackbarPos("U-V","Trackbars")
    lower_red=np.array([l_h,l_s,l_v])
    upper_red=np.array([u_h,u_s,u_v])
    mask=cv2.inRange(hsv,lower_red,upper_red)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel)
    
    
    
    contours, hierarchy= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        if area>400:
            cv2.drawContours(frame,[approx],0,(0,0,0),3)
            if len(approx) ==3:
                cv2.putText(frame,"Triangle", (x,y),font, 1, (0,0,0))
            elif len(approx) ==4:
                cv2.putText(frame,"Rectangle", (x,y),font, 1, (0,0,0))
            elif 10< len(approx) <20:
                cv2.putText(frame,"Circle", (x,y),font, 1, (0,0,0))
             
                
    diff = cv2.absdiff(frame1,frame2)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    _, thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated=cv2.dilate(thresh,None,iterations=3)
    contours, _=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x,y,w,h)=cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 700:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1, "Status: {}".format('Movement'),(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
   # cv2.drawContours(frame1,contours,-1,(0,255,0),2)
    cv2.imshow("feed",frame1)
    frame1=frame2
    ret,frame2=cap.read()
    cv2.imshow("FRAME",frame)
    cv2.imshow("MASK",mask)
   
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()