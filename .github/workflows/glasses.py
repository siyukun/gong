import sensor, image,time,math
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
left_roi = [0,0,320,140]#需要根据镜头的位置来设定

while(True):
    index1=0#眨眼频率
    n=100
    x1=0
    y1=0
    while(n>0):
        clock.tick()
        img=sensor.snapshot()
        statistics=img.get_statistics()
        img.binary([(statistics[6]-15, 255)])#这块需要再改进一下
        blobs = img.find_blobs([(245, 255)],roi=left_roi,invert=True,area_threshold=20,merge_cb=15)
        if blobs:
            max_blob = max(blobs, key=lambda b: b.pixels())
            x, y, w, h = max_blob.rect()
            img.draw_rectangle((x, y, w, h), color=0)

            if (math.fabs(x-x1)+math.fabs(y-y1))>10:
                index1=index1+1
            x1,y1=x,y
        n=n-1
    print(index1)
    #if index<50:




