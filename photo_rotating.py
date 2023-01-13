import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class RecTangle:
    """
    矩形裁剪
    """
    x0 = 10
    y0 = 10
    x1 = 100
    y1 = 100

    def setxy(self, x_0, y_0, x_1, y_1):
        """
        设置矩形顶点
        """
        self.x0 = x_0
        self.y0 = y_0
        self.x1 = x_1
        self.y1 = y_1

    def getxy(self):
        """
        返回矩形顶点
        """
        return (self.x0, self.y0), (self.x1, self.y1)

    def get4v(self):
        """
        获得矩形四个顶点
        """
        return (self.x0, self.y0), \
               (self.x1, self.y0), \
               (self.x0, self.y1), \
               (self.x1, self.y1)

    def getv(self, v):
        """
        获取对角的顶点
        """
        if v == 1:
            return self.x1, self.y1
        elif v == 2:
            return self.x0, self.y1
        elif v == 3:
            return self.x1, self.y0
        else:
            return self.x0, self.y0


def cb_rotate():
    global i_angle
    global angle
    try:
        angle = int(i_angle.get().strip())
    except:
        messagebox.showerror(message='请输入数字')

    global img
    # 裁剪图片
    img_corp = corp_img(img, rec.x0, rec.y0, rec.x1, rec.y1)
    # 旋转，改背景为白色
    im = img_corp.convert('RGBA')
    rot = im.rotate(angle, expand=True)
    img_r = Image.new("RGBA", rot.size, "white")
    img_r.paste(rot, (0, 0), rot)

    # 将图片裁剪的位置设置为白色
    white_im = Image.new('RGBA', img_corp.size, 'white')
    img.paste(white_im, (0, 0), white_im)

    global canvas2
    global image_r_c
    global image_r
    image_r = ImageTk.PhotoImage(img_r)
    if image_r_c is not None and canvas2 is not None:
        canvas2.delete(image_r_c)
    image_r_c = canvas2.create_image(0, 0, image=image_r, anchor='nw')


def cb_save():
    pass


# IMG_EXTS = [
#     ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".jp2", ".j2k", ".jpf",
#     ".jpx", ".jpm", ".mj2", ".jxr", ".hdp", ".wdp", ".gif", ".raw", ".webp",
#     ".png", ".apng", ".mng", ".tiff", ".tif", ".svg", ".svgz", ".pdf", ".xbm",
#     ".bmp", ".dib", ".ico", ".3dm", ".max"
# ]
def cb_open():
    """
    “打开图片”按钮的回调函数
    """
    global img
    # 选择对应格式的文件进行打开
    file = filedialog.askopenfilename(filetypes=[('图片', '*.png *.jpg *.jpeg')])
    if file is None or file == '':
        return
    # print(file)
    img = Image.open(file)

    # 获取图片尺寸
    imgx, imgy = img.size
    # print(imgx, imgy)
    # 获取屏幕大小，减100，取较小的值
    screenw = win.winfo_screenwidth() - 100
    screenh = win.winfo_screenheight() - 100 - 100
    # print(screenw, screenh)
    # 图片太大
    # 等比例缩小图片
    while imgx > screenw or imgy > screenh:
        imgx = int(imgx * 0.9)
        imgy = int(imgy * 0.9)
    img = img.resize((imgx, imgy), Image.LANCZOS)

    # 打开图片的窗口
    win2 = tk.Toplevel(win)
    win2.title('旋转操作')
    # 将新窗口作为焦点，禁用与其他窗口的交互
    win2.grab_set()

    # 创建框架矩形区域
    f1 = tk.Frame(win2)
    f1.pack()
    # 旋转角度输入框
    global i_angle
    e_angle = tk.Entry(f1, textvariable=i_angle)
    i_angle.set('0')
    e_angle.pack()
    # 旋转按钮
    b_rotate = tk.Button(f1, text='旋转', command=cb_rotate)
    b_rotate.pack()

    # 图片的框架矩形区域
    f2 = tk.Frame(win2, width=imgx, height=imgy)
    f2.pack()
    # 创建画布
    global canvas
    canvas = tk.Canvas(f2, width=imgx, height=imgy)
    # 放置图片
    image = ImageTk.PhotoImage(img)
    i = canvas.create_image(0, 0, image=image, anchor='nw')

    # 设置矩形裁剪
    global rec
    global rec_canvas
    rec.setxy(4, 4, imgx, imgy)
    rec_canvas = canvas.create_rectangle(*rec.getxy(), outline='red', width=4)
    # 设置左键按下和移动的回调函数
    canvas.bind('<Button-1>', mouse_left_down)
    canvas.bind('<B1-Motion>', mouse_left_move)
    canvas.bind('<ButtonRelease-1>', mouse_left_up)
    # canvas.bind('<ButtonRelease-3>', onRightButtonUp)
    canvas.pack()

    # 旋转后图片的新窗口
    win3 = tk.Toplevel(win2)
    win3.title('旋转结果')

    # 创建菜单
    menu = tk.Menu(win3)
    win3.config(menu=menu)
    # 保存
    # menu.add_command(label='保存图片', command=cb_save)

    global canvas2
    # 旋转后的图片显示在第三个窗口
    f3 = tk.Frame(win3, width=imgx, height=imgy)
    f3.pack()
    canvas2 = tk.Canvas(f3, width=imgx, height=imgy)
    canvas2.pack()

    cb_rotate()

    win2.mainloop()
    win3.mainloop()


def corp_img(img, x_begin, y_begin, x_end, y_end):
    if x_begin < x_end:
        min_x = x_begin
        max_x = x_end
    else:
        min_x = x_end
        max_x = x_begin
    if y_begin < y_end:
        min_y = y_begin
        max_y = y_end
    else:
        min_y = y_end
        max_y = y_begin
    return img.crop((min_x, min_y, max_x, max_y))


def in_rec(p1, p2, error=10):
    """
    判断p1是否在以p2为中心的小矩形区域中
    矩形返回±error误差
    """
    if p1[0] in range(p2[0] - error, p2[0] + error) and p1[1] in range(p2[1] - error, p2[1] + error):
        return True
    else:
        return False


def mouse_left_down(event):
    global rec
    global vertex_focus
    global v_opposite
    v4 = rec.get4v()
    # 判断当前左键按下的位置处于矩形裁剪的哪个顶点
    # 或者不处于
    for i in range(len(v4)):
        # print(event.x, event.y)
        # print(v4[i])
        if in_rec((event.x, event.y), v4[i]):
            # print('OK')
            vertex_focus = i + 1
            v_opposite = rec.getv(vertex_focus)
            # print(vertex_focus, v_opposite, sep='\n')
            break


def mouse_left_move(event):
    global v_opposite
    global rec_canvas
    global canvas

    # 左键按下的位置不处于矩形裁剪的四个顶点
    if vertex_focus == 0:
        return

    if rec_canvas is not None and canvas is not None:
        canvas.delete(rec_canvas)
    rec_canvas = canvas.create_rectangle(v_opposite[0], v_opposite[1], event.x,
                                         event.y, outline='red', width=4)


def mouse_left_up(event):
    global vertex_focus
    global v_opposite
    global rec
    vertex_focus = 0
    rec.setxy(*v_opposite, event.x, event.y)


# 鼠标焦点处于矩形裁剪的哪个顶点上
vertex_focus = 0
# 旋转角度
angle = 0
# 裁剪的矩形
rec = RecTangle()
rec_canvas = None
# 焦点顶点的对角
v_opposite = rec.getv(0)
# 旋转编辑的画布
canvas = None
# 打开的图片
img = None
# 旋转结果的画布
canvas2 = None
# 旋转后画布上的图片
image_r_c = None
image_r = None

win = tk.Tk()
# 旋转角度输入值
i_angle = tkinter.StringVar()
# 设置窗口标题
win.title('图片旋转')
# 设置窗口大小
win.geometry('500x300')
# 设置窗口参数，bg背景颜色
win.configure(bg='grey')
# 创建按钮
b_open = tk.Button(win, text='打开图片', height=2, width=10, command=cb_open)
b_open.place(x=100, y=100)
# b_open.pack(padx=10, pady=10)
# tk.Label(win, text='标签1').pack()
win.mainloop()
