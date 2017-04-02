import numpy as np
import cv2
import os

from multiprocessing import Process, Queue
import time

#from common import clock, draw_str, StatValue
#import video

class FLANN(Process):

    def __init__(self,frame_queue, output_queue, descriptor, height, width):
        Process.__init__(self)
        self.frame_queue = frame_queue
        self.output_queue = output_queue
        self.height = height
        self.width = width
        self.stop = False
        self.descriptor = descriptor


    def get_frame(self):
        if not self.frame_queue.empty():
            return True, self.frame_queue.get()
        else:
            return False, None

    def stopProcess(self):
        self.stop = True

    def search(self, gray):
        queryKP,queryDesc=detector.detectAndCompute(gray,None)
        bf = cv2.BFMatcher()
        matches=bf.knnMatch(queryDesc, self.descriptor, k=2)
        goodMatch=[]
        for m,n in matches:
            if(m.distance<0.75*n.distance):
                goodMatch.append(m)
        MIN_MATCH_COUNT=50
        if(len(goodMatch)>=MIN_MATCH_COUNT):
            tp=[]
            qp=[]
            for m in goodMatch:
                tp.append(trainKP[m.trainIdx].pt)
                qp.append(queryKP[m.queryIdx].pt)
            tp,qp=np.float32((tp,qp))
            #os.system("say wow look a stopsign")
            H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)

            trainBorder=np.float32([[[0,0],[0,self.height-1],[self.width-1,self.height-1],[self.width-1,0]]])
            queryBorder=cv2.perspectiveTransform(trainBorder,H)
            os.system("say found")

            if self.output_queue.full():
                self.output_queue.get_nowait()
            self.output_queue.put(queryBorder)
        return True

    def run(self):
        while not self.stop:
            ret, frame = self.get_frame()
            if ret:
                self.search(frame)


if __name__ == '__main__':

    frame_sum = 0
    init_time = time.time()

    def put_frame(frame):
        if Input_Queue.full():
            Input_Queue.get_nowait()
        Input_Queue.put(frame)


    cap = cv2.VideoCapture(0)

    #training section
    detector=cv2.xfeatures2d.SIFT_create()
    FLANN_INDEX_KDITREE=0
    flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
    flann=cv2.FlannBasedMatcher(flannParam,{})
    trainImg=cv2.imread("stop_sign.jpg")
    h,w,c = trainImg.shape
    trainImgGray = cv2.cvtColor(trainImg,cv2.COLOR_BGR2GRAY)
    trainKP,trainDesc=detector.detectAndCompute(trainImgGray,None)



    threadn = cv2.getNumberOfCPUs()
    if(threadn > 4):
        threadn = 2
    threaded_mode = True

    process_list = []
    Input_Queue = Queue(maxsize = 5)
    Output_Queue = Queue(maxsize = 5)

    for x in range((threadn -1)):
        ft = FLANN(frame_queue = Input_Queue, output_queue = Output_Queue, descriptor = trainDesc, height = h, width = w)
        ft.daemon = True
        ft.start()
        process_list.append(ft)

    ch = cv2.waitKey(1)
    cv2.namedWindow('Threaded Video', cv2.WINDOW_NORMAL)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        put_frame(gray)
        #resize
        h,w = gray.shape
        if(h > 720):
            gray = cv2.resize(gray, (0,0), fx=720/h, fy=720/h)
            h,w = gray.shape
        l = int((w-h)/2)
        r = h+l
        #print(w, h, l, r)
        gray = gray[0:h, l:r] #crop

        contour = cv2.Canny(gray, 80, 200, apertureSize = 3)
        combined = cv2.addWeighted(contour, 0.8, gray, 0.2, 0)
        combined = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)
        if not Output_Queue.empty():
            result = Output_Queue.get()
            cv2.polylines(combined,[np.int32(result)],True,(0,0,255),5)
            ch = cv2.waitKey(5)


        stream = np.concatenate((combined, combined), axis=1)
        target = 400
        # if(h > target):
        #     stream = cv2.resize(stream, (0,0), fx=target/h, fy=target/h)
        cv2.imshow('frame',stream)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
