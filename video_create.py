# -*- coding: utf-8 -*-

import cv2
import codecs
from PIL import Image
import os,sys,time
import subprocess as sp

class videoCut(object):

    def parse(self):
        source_filename='./video/为什么说防火防盗防闺蜜？？#街拍.mp4'
        #视频源
        videoCapture=cv2.VideoCapture(source_filename)
        #获取视频的帧率
        fps=videoCapture.get(cv2.CAP_PROP_FPS)
        #获取视频的分辨率
        img_size=(int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        output_filename='a.mp4'

        # 构建一个视频写入对象
        video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps, img_size)

        start_time=0
        peroid=5
        # 开始帧和结束帧
        start_frame = fps * start_time
        end_frame = start_frame + peroid * fps

        # 循环读取视频帧，只写入开始帧和结束帧之间的帧数据
        while True:
            success, frame = videoCapture.read()
            i=0
            if success:
                i += 1
                if start_frame <= i <= end_frame:
                    # 将截取到的画面写入“新视频”
                    video_writer.write(frame)
            else:
                break
        # 释放资源
        videoCapture.release()


    @staticmethod
    def adaptive_threshold():
        # Creating a VideoCapture object to read the video
        cap = cv2.VideoCapture('./video/为什么说防火防盗防闺蜜？？#街拍.mp4')

        # Loop untill the end of the video
        while (cap.isOpened()):

            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                               interpolation=cv2.INTER_CUBIC)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # conversion of BGR to grayscale is necessary to apply this operation
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # adaptive thresholding to use different threshold
            # values on different regions of the frame.
            Thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)

            cv2.imshow('Thresh', Thresh)
            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # release the video capture object
        cap.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    @staticmethod
    def smoothing():
        cap = cv2.VideoCapture('./video/为什么说防火防盗防闺蜜？？#街拍.mp4')
        # Loop untill the end of the video
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                               interpolation=cv2.INTER_CUBIC)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # using cv2.Gaussianblur() method to blur the video

            # (5, 5) is the kernel size for blurring.
            gaussianblur = cv2.GaussianBlur(frame, (5, 5), 0)
            cv2.imshow('gblur', gaussianblur)

            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # release the video capture object
        cap.release()

        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    @staticmethod
    def edge_detection():
        cap = cv2.VideoCapture('./video/为什么说防火防盗防闺蜜？？#街拍.mp4')
        # Loop untill the end of the video
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                               interpolation=cv2.INTER_CUBIC)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # conversion of BGR to grayscale is necessary to apply this operation
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # apply NOT operation on image and mask generated by thresholding
            BIT = cv2.bitwise_not(frame, frame, mask=mask)
            cv2.imshow('BIT', BIT)

            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # release the video capture object
        cap.release()

        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    @staticmethod
    def bitwise_operation():
        cap = cv2.VideoCapture('./video/为什么说防火防盗防闺蜜？？#街拍.mp4')
        # Loop untill the end of the video
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()

            frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                               interpolation=cv2.INTER_CUBIC)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # using cv2.Canny() for edge detection.
            edge_detect = cv2.Canny(frame, 100, 200)
            cv2.imshow('Edge detect', edge_detect)

            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # release the video capture object
        cap.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    @staticmethod
    def multiple_images_resize(path:str=None):
        # print(os.getcwd())
        os.chdir(path)
        mean_height=0
        mean_width=0

        num_of_images=len(os.listdir('.'))
        # print(num_of_images)
        for file in os.listdir('.'):
            im=Image.open(os.path.join(path,file))
            width,height=im.size
            mean_width+=width
            mean_height+=height


        mean_height=int(mean_height/num_of_images)
        mean_width=int(mean_width/num_of_images)

        for file in os.listdir('.'):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                    im=Image.open(os.path.join(path,file))

                    width,height=im.size
                    # print(width,height)

                    imResize=im.resize((mean_width,mean_height),Image.ANTIALIAS)
                    imResize.save(file,'JPEG',quality=95)
                    print(im.filename.split('\\')[-1],"is resized")

    @staticmethod
    def convert_chinese_pics_to_custom(path:str=None,saved_path:str=None):
        i=1
        for file in os.listdir(path):
            os.rename(os.path.join(path,file),os.path.join(saved_path,str(i).zfill(4)+".jpg"))
            i+=1

        return


    @staticmethod
    def generate_video(image_folder:str=None,video_name:str=None):
        video_name=video_name.split('\\')[-1]
        os.chdir(image_folder)

        images = [img for img in os.listdir(image_folder)
                  if img.endswith(".jpg") or
                  img.endswith(".jpeg") or
                  img.endswith("png")]


        # Array images should only consider
        # the image files ignoring others if any
        # print(images)

        frame = cv2.imread(os.path.join(image_folder, images[0]))


        # setting the frame width, height width
        # the width, height of first image
        height, width, layers = frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        #各参数含义（保存的文件名，对应文件名的内置格式指定，fps即帖数即一帧几秒，[数组形式中的宽，数组形式中的高]）
        # video = cv2.VideoWriter(video_name, fourcc, 20.0, (width, height))
        video = cv2.VideoWriter(video_name, fourcc, 1, (width, height))

        # Appending the images to the video one by one
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        # Deallocating memories taken for window creation
        cv2.destroyAllWindows()
        video.release()  # releasing the video generated

    @staticmethod
    def add_bgm(video_from:str=None,bgm_music_address:str=None,video_length:int=None,video_to:str=None):
        """
           :param video_from: 视频源路径（含文件）
           :param bgm_music_address: 背景音乐路径（含文件）
           :param video_length 视频的长度，准备的音频一定要长过视频或等于 视频多长秒数这里就填多少
           :param video_to: 导出文件路径（含文件）
           :return:
           """
        reconstruct='ffmpeg -i ' + video_from + ' -i '+ bgm_music_address + ' -t '+ str(video_length) +' -c copy ' + video_to
        return sp.call(reconstruct, shell=True)

    @staticmethod
    def add_watermark(video_path:str=None,wartermark_file_path: str=None,output_path:str=None):
        reconstruct = 'ffmpeg -i ' + video_path + ' -i '+ wartermark_file_path+ ' -filter_complex "[0]scale=1920:-2,setsar=1[bg];[bg][1]overlay=main_w-overlay_w-10:10"' + ' -c:v libx264 -c:a copy -max_muxing_queue_size 9999 ' +output_path
        return sp.call(reconstruct, shell=True)

    @staticmethod
    def main(origin_images_folder,resized_images_folder,video_name,bgm_music_address,video_length,video_to,watermark_file_path,output_path):
        """
        # ins.multiple_images_resize("C:\\Users\\guruYu\\Pictures\\22222")
        # ins.convert_chinese_pics_to_custom("C:\\Users\\guruYu\\Pictures\\22222","C:\\Users\\guruYu\\Pictures\\33333")
        # ins.generate_video("C:\\Users\\guruYu\\Pictures\\33333","test2.mp4")
        # ins.add_bgm(r"C:\Users\guruYu\Pictures\33333\test2.mp4",r"C:\Users\guruYu\Pictures\33333\anti.mp3",46,r"C:\Users\guruYu\Pictures\33333\output2.mp4")
        # ins.add_watermark(r"C:\Users\guruYu\Pictures\33333\output2.mp4",
        #                   r"C:\Users\guruYu\Pictures\33333\watermark1.jpg",
        #                   r"C:\Users\guruYu\Pictures\33333\output3.mp4")
        注释部分给参考，各参数各是什么含义
           :param origin_images_folder: 制作卡点视频图片所在路径
           :param resized_images_folder: 上述图片被改完尺寸后所在的路径
           :param video_name 导出视频的名称（只指定名称，不需要加路径）
           :param bgm_music_address: 背景音乐所在位置
           :param video_length: 生成视频的长度，点开看一下就知道，用于决定你制作多长的背景音乐，或者是准备到少多长的背景音乐
           :param video_to: 加完背景音乐后输出的文件名(含路径)
           :param watermark_file_path: 水印文件所在路径
           :param output_path: 最终生成的文件名
           以上各文件最好独立在各目录里，以便不发生混淆
           :return:
           """
        ins=videoCut()
        ins.multiple_images_resize(origin_images_folder)
        ins.convert_chinese_pics_to_custom(origin_images_folder,resized_images_folder)
        ins.generate_video(resized_images_folder,video_name)
        ins.add_bgm(video_name,bgm_music_address,video_length,video_to)
        ins.add_watermark(video_to,watermark_file_path,output_path)



if '__main__' == __name__:
    ins=videoCut()
    ins.main("#对应上方参数填写自己本地路径")
