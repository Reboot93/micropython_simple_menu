import _thread, time, sys
from machine import Pin

## 1. listSet(list)
## 2. start()   # loop
## 3. if checked, loop exit, Menu.res_flag = self.clecked
##    if bt_quit, loop exit, Menu.res_falg = -1

class Menu():
    # self.count = 菜单项目数，1 开始
    # menu_print 中 count = 当前显示内容所选中项，0 开始
    # self.checked = 当前选中项数， 0开始
    # self.res_flag # -1 (exit)
                    # -2 (run)
                    # other (self.checked)

    def __init__(self, display, w, h, up=2, down=27, L=4, R=35):
        self.res_flag = -2
        self.flash_flag = 0
        self.list = []
        self.up = Pin(2, Pin.IN)
        self.down = Pin(27, Pin.IN)
        self.checked = 0
        self.L = Pin(4, Pin.IN)
        self.R = Pin(35, Pin.IN)
        self.w = w
        self.h = h
        self.display = display


    def start(self):
        try:
            self.menu_flag = 1
            self.res_flag = -2
            _thread.start_new_thread(self.bt_check_thread, ())
            self.flash_flag = 1
            while self.menu_flag == 1:
                if self.flash_flag == 1:
                    self.flash_flag = 0
                    self.menu_print()
                time.sleep_ms(10)
        except:
            self.menu_flag = 0
            sys.exit(0)

    def stop(self):
        self.menu_flag = 0

    def bt_check_thread(self):
        smooth = 25
        out_smooth = 150
        time.sleep_ms(200)
        while self.menu_flag == 1:
            if self.up.value() == 1:
                time.sleep_ms(smooth)
                if self.up.value() == 1:
                    if self.checked > 0:
                        self.checked = self.checked - 1
                    elif self.checked == 0:
                        self.checked = self.count - 1
                    self.flash_flag = 1
                    time.sleep_ms(out_smooth)
            if self.down.value() == 1:
                time.sleep_ms(smooth)
                if self.down.value() == 1:
                    if self.checked < self.count - 1:
                        self.checked = self.checked + 1
                    elif self.checked < self.count:
                        self.checked = 0
                    self.flash_flag = 1
                    time.sleep_ms(out_smooth)
            if self.L.value() == 1:
                time.sleep_ms(smooth)
                if self.L.value() == 1:
                    self.menu_flag = 0
                    #self.stop()
                    self.res_flag = -1
                    break
            if self.R.value() == 1:
                time.sleep_ms(smooth)
                if self.R.value() == 1:
                    self.menu_flag = 0
                    #self.stop()
                    self.res_flag = self.checked
                    break
            time.sleep_ms(10)

    def menu_print(self):
        self.display.fill(0)
        count = 0   # 已打印项数
        out_count = 0   # 位于屏幕上方需要跳过的项数，随着 title.text() 而 减少
        ex_count = 0    # 位于屏幕上方需要跳过的项数
        if self.checked >= (self.h / 16):   # 判断当前选中项是否超出屏幕能显示的范围
            out_count = self.checked + 1 - (self.h / 16)
        for title in self.list:
            if out_count < 1 and count < (self.h / 16): # 绘制不超过屏幕显示数量的title
                self.display.text(title, 4, 4 + (16 * count))
                if count + out_count + ex_count == self.checked:   # 当前 title 为被选中项时，打印边框
                    self.display.rect(0, 16 * count, (len(title) * 8) + 8, 16, 1)
                count = count + 1
            else:
                out_count = out_count - 1
                ex_count = ex_count + 1
        self.display.show()

    def listSet(self, list):
        self.list = list
        self.count = len(list)