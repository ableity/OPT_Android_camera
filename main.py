from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import os


# from android.permissions import request_permissions, Permission


class CameraClick(FloatLayout):
    def __init__(self):
        super(CameraClick, self).__init__()
        self.flag = 0  # 相机是否可以进行拍照（例如：当在预览图片时不可以进行拍摄）
        self.zoom = 20  # 相机默认变焦值，注意与kv文件中的相同
        self.num = 0  # 相机拍摄的照片数量
        self.sum_of_nap = 0  # 相机拍摄之间的时间的总和
        self.num_of_pho = 360  # 默认拍摄的照片数量
        self.nap_moren = 0.999  # 默认拍照间隔
        self.nap = self.nap_moren  # 调整的拍照间隔

        self.label_change = True  # 通过改变label改变拍摄数量和时间间隔等参数，是否可以改变标志位

        # 通过改变label改变拍摄数量
        self.label_num_of_num = 0
        self.label_num_str = ['[ref="click"]NUM:360[/ref]', '[ref="click"]NUM:180[/ref]',
                              '[ref="click"]NUM:90[/ref]', '[ref="click"]NUM:60[/ref]',
                              '[ref="click"]NUM:10[/ref]']
        self.label_num = [360, 180, 90, 60, 10]

        # 通过改变label改变拍摄时间间隔
        self.label_num_of_nap = 0
        self.label_nap_str = ['[ref="click"]NAP:1.0[/ref]', '[ref="click"]NAP:1.5[/ref]',
                              '[ref="click"]NAP:2.0[/ref]', '[ref="click"]NAP:2.5[/ref]',
                              '[ref="click"]NAP:3.0[/ref]']
        self.label_nap = [1.0, 1.5, 2.0, 2.5, 3.0]

    def capture(self):
        '''
        拍摄一张照片
        '''
        if self.flag == 0:
            camera = self.ids['camera']
            camera.export_to_png("/storage/emulated/0/OPTcamera" + "/" + "IMG.png")

    def capture_1(self, nap):
        '''
        拍摄一张照片（循环拍照片函数的子函数）
        '''
        if self.flag == 0 and self.num < self.num_of_pho:
            camera = self.ids['camera']
            camera.export_to_png("/storage/emulated/0/OPTcamera" + "/" + str(self.num) + ".png")  # 拍摄一张照片
            self.num = self.num + 1  # 拍了多少照片了
            self.ids.num_of_pho.text = "NUM." + str("%.2f" % self.num)  # 照片拍摄数量
            # nap = self.adj_nap + nap
            self.ids.nap_of_pho.text = "NAP:" + str('%.2f' % nap)  # 上一个耗时
            self.sum_of_nap = self.sum_of_nap + nap
            self.ids.sum_nap_of_pho.text = "SUM:" + str('%.2f' % self.sum_of_nap)  # 共耗时
            if self.num >= self.num_of_pho:  # 停止
                self.ids.num_of_pho.text = self.label_num_str[self.label_num_of_num]
                self.ids.nap_of_pho.text = self.label_nap_str[self.label_num_of_nap]
                self.num = 0
                self.sum_of_nap = 0
                self.nap = self.nap_moren
                self.label_change = True
                return False

    def capture_begin(self):  # 开始连拍
        if self.flag == 0 and self.num == 0:
            self.label_change = False
            Clock.schedule_interval(self.capture_1, self.nap)

    def showpic(self):  # 展示capture拍摄的照片
        self.ids.led.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        if self.flag == 0:
            self.ids.led.source = "/storage/emulated/0/OPTcamera" + "/" + "IMG.png"
            self.ids.led.reload()
            self.ids.led.size_hint = (2, 2)
            self.flag = 1
            # self.ids.camera.play = False 停止取消相机预览，增加流畅度
        else:
            self.ids.led.size_hint = (0, 0)
            self.flag = 0
            # self.ids.camera.play = True

    def change_num(self):
        if self.label_change == True:
            if self.label_num_of_num < len(self.label_num) - 1:
                self.label_num_of_num = self.label_num_of_num + 1
            else:
                self.label_num_of_num = 0
            self.ids.num_of_pho.text = self.label_num_str[self.label_num_of_num]
            self.num_of_pho = self.label_num[self.label_num_of_num]

    def change_nap(self):
        if self.label_change == True:
            if self.label_num_of_nap < len(self.label_nap) - 1:
                self.label_num_of_nap = self.label_num_of_nap + 1
            else:
                self.label_num_of_nap = 0
            self.ids.nap_of_pho.text = self.label_nap_str[self.label_num_of_nap]
            self.nap_moren = self.label_nap[self.label_num_of_nap]
            self.nap = self.nap_moren

    def zoomadd(self):  # 变焦（拉近）
        if self.zoom < 90 and self.flag == 0:
            self.zoom = self.zoom + 10
            self.ids.camera.zoom = self.zoom
            # self.ids['camera'].play = True

    def zoomdev(self):  # 变焦（拉远）
        if self.zoom >= 10 and self.flag == 0:
            self.zoom = self.zoom - 10
            self.ids.camera.zoom = self.zoom


class TestCamera(App):

    def build(self):
        isExists = os.path.exists("/storage/emulated/0/OPTcamera")  # 检查文件夹是否存
        if not isExists:
            os.makedirs("/storage/emulated/0/OPTcamera")  # 不存在则创建
        return CameraClick()

    # def on_start(self):
    #     request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA])


if __name__ == "__main__":
    TestCamera().run()
