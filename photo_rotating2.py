import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import copy


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

    def getv1(self):
        """
        获取第一个顶点
        """
        x0 = self.x0 if self.x0 < self.x1 else self.x1
        y0 = self.y0 if self.y0 < self.y1 else self.y1
        return x0, y0

    def getv4(self):
        """
        获取第四个顶点
        """
        x0 = self.x0 if self.x0 > self.x1 else self.x1
        y0 = self.y0 if self.y0 > self.y1 else self.y1
        return x0, y0

    def getcenter(self):
        """
        获得中心点
        """
        return int((self.x0 + self.x1) / 2), int((self.y0 + self.y1) / 2)


def cb_rotate():
    # # 按老师的要求，矩形裁剪框到图片的左边，一律不能旋转
    # global rec
    # global canvas_open
    # v1 = rec.getv1()
    # if v1[0] < canvas_open.winfo_reqwidth()/2:
    #     messagebox.showerror(message='请选择图片的右半部分')
    #     return

    global i_angle
    global angle
    try:
        # 获取角度
        angle = int(i_angle.get().strip())
    except:
        messagebox.showerror(message='请输入数字')

    global img_open
    global img_rotate
    # 裁剪图片
    img_corp = corp_img(img_open, *rec.getxy()[0], *rec.getxy()[1])
    # 旋转，改背景为透明
    img_corp = img_corp.convert('RGBA')
    img_rotate = img_corp.rotate(angle, expand=True)
    img_transparent = Image.new("RGBA", img_rotate.size, "white")
    newdata = []
    for i in img_transparent.getdata():
        if i[0] == 255 and i[1] == 255 and i[2] == 255:
            newdata.append((255, 255, 255, 0))
        else:
            newdata.append(i)
    img_transparent.putdata(newdata)
    img_transparent.paste(img_rotate, (0, 0), img_rotate)
    img_rotate = img_transparent
    # 等比例缩小
    # while img_rotate.size[0] > img_corp.size[0] or img_rotate.size[1] > img_corp.size[1]:
    #     # print(img_rotate.size)
    #     img_rotate = img_rotate.resize((int(img_rotate.size[0] * 0.9), int(img_rotate.size[1] * 0.9)), Image.LANCZOS)

    # 复制打开的图片
    # 深拷贝
    img_copy = copy.deepcopy(img_open)
    img_copy = img_copy.convert('RGBA')
    # print(img_copy, img_open)

    # 扩大图片
    # 原来的对角线长度作为边长
    diagonal = get_diagonal(*img_open.size)
    white_img = Image.new('RGBA', (diagonal, diagonal), 'white')
    # 在扩大的图片中，原图片的左上角起点
    # 函数参数分别为长、宽、中心点坐标
    # 中心点坐标由函数获取
    start_pos = get_vertex(img_copy.size[0], img_copy.size[1],
                           get_center((0, 0), white_img.size))[0]
    white_img.paste(img_copy, start_pos, img_copy)
    img_copy = white_img

    # 将图片裁剪的位置设置为白色
    white_img = Image.new('RGBA', img_corp.size, 'white')
    # img_open.paste(white_img, (0, 0), white_img)
    pos = (start_pos[0] + rec.getv1()[0], start_pos[1] + rec.getv1()[1])
    img_copy.paste(white_img, pos, white_img)
    # 把旋转结果贴到原图原来的位置
    # img_copy.paste(img_rotate, rec.get1v(), img_rotate)
    # 根据边长和中心点获得顶点
    pos = get_vertex(img_rotate.size[0], img_rotate.size[1], rec.getcenter())[0]

    # # 按老师的要求，要修改旋转后的图片贴在原图的中心，但是修改失败，改别的地方
    # global canvas_rotate
    # pos = get_vertex(canvas_rotate.winfo_reqwidth(), canvas_rotate.winfo_reqheight(),
    #                  get_center((0, 0), (canvas_rotate.winfo_reqwidth(), canvas_rotate.winfo_reqheight())))[0]
    # pos = int(canvas_rotate.winfo_reqwidth()/2)-int(img_rotate.size[0]/2),\
    #       int(canvas_rotate.winfo_reqheight())-int(img_rotate.size[1]/2)

    pos = (start_pos[0] + pos[0], start_pos[1] + pos[1])
    img_copy.paste(img_rotate, pos, img_rotate)
    img_rotate = img_copy

    # global canvas_rotate
    global img_rotate_tk
    global img_rotate_canvas
    # 将旋转结果显示在画布上
    img_rotate_tk = ImageTk.PhotoImage(img_rotate)
    if img_rotate_canvas is not None:
        canvas_rotate.delete(img_rotate_canvas)
    # 显示在画布上不需要获取顶点位置
    pos = get_vertex(img_rotate.size[0], img_rotate.size[1],
                     get_center((0, 0),
                                (canvas_rotate.winfo_reqwidth(), canvas_rotate.winfo_reqheight())))[0]
    pos = (start_pos[0] + pos[0], start_pos[1] + pos[1])
    # pos = (0, 0)
    # print(img_rotate.size)
    # print(get_center((0, 0), (canvas_rotate.winfo_reqwidth(), canvas_rotate.winfo_reqheight())))
    # print(pos)
    img_rotate_canvas = canvas_rotate.create_image((0, 0), image=img_rotate_tk, anchor='nw')


def cb_save():
    global img_rotate
    img_rotate = crop_margin(img_rotate)
    file = filedialog.asksaveasfilename(filetypes=[('图片', '*.jpg *.jpeg *.png')])
    # img_rotate = img_rotate.convert('RGB')
    img_rotate.save(file)
    messagebox.showinfo(message='已保存至' + file, title='保存成功')


def get_diagonal(x, y):
    """
    获得对角线长度
    """
    return int(pow(x * x + y * y, 0.5))


def get_vertex(w, h, center):
    """
    根据中心点和长宽获得顶点
    """
    return (int(center[0] - w / 2), int(center[1] - h / 2)), (int(center[0] + w / 2), int(center[1] + h / 2))


def get_center(v1, v4):
    """
    获得中心点
    """
    return int((v1[0] + v4[0]) / 2), int((v1[1] + v4[1]) / 2)


def cb_open():
    """
    “打开图片”按钮的回调函数
    """
    global img_open
    # 选择对应格式的文件进行打开
    file = filedialog.askopenfilename(filetypes=[('图片', '*.png *.jpg *.jpeg')])
    if file is None or file == '':
        return
    # print(file)
    img_open = Image.open(file)

    global win
    # 获取图片尺寸
    img_openx, img_openy = img_open.size
    # print(img_openx, img_openy)
    # 获取屏幕大小，减100，取较小的值
    screenw = win.winfo_screenwidth() / 2
    screenh = win.winfo_screenheight() / 2
    # print(screenw, screenh)
    # 图片太大
    # 等比例缩小图片
    while img_openx > screenw or img_openy > screenh:
        img_openx = int(img_openx * 0.9)
        img_openy = int(img_openy * 0.9)
    img_open = img_open.resize((img_openx, img_openy), Image.LANCZOS)

    global win_open
    global f_open
    global e_angle
    global b_rotate
    # 打开图片的窗口
    win_open = tk.Toplevel(win)
    win_open.title('打开图片')
    # 将新窗口作为焦点，禁用与其他窗口的交互
    win_open.grab_set()
    # 创建框架，矩形区域
    f_open = tk.Frame(win_open)
    f_open.pack()
    # 旋转角度输入框
    e_angle = tk.Entry(f_open, textvariable=i_angle)
    e_angle.pack()
    # 旋转按钮
    b_rotate = tk.Button(f_open, text='旋转', command=cb_rotate)
    b_rotate.pack()

    global f_open2
    global canvas_open
    # 框架2
    f_open2 = tk.Frame(win_open)
    f_open2.pack()
    # 打开图片的画布
    canvas_open = tk.Canvas(f_open)
    # 设置左键按下和移动的回调函数
    canvas_open.bind('<Button-1>', mouse_left_down)
    canvas_open.bind('<B1-Motion>', mouse_left_move)
    canvas_open.bind('<ButtonRelease-1>', mouse_left_up)
    canvas_open.pack()

    global win_rotate
    global menu
    global f_rotate
    global canvas_rotate
    # 旋转结果的窗口
    win_rotate = tk.Toplevel(win_open)
    win_rotate.title('旋转结果')
    # 菜单
    menu = tk.Menu(win_rotate)
    win_rotate.config(menu=menu)
    # 保存
    menu.add_command(label='保存图片', command=cb_save)
    # 矩形区域框架
    f_rotate = tk.Frame(win_rotate)
    f_rotate.pack()
    # 画布
    canvas_rotate = tk.Canvas(f_rotate)
    canvas_rotate.pack()

    global img_open_tk
    global img_open_canvas
    # 设置大小
    f_open.configure(width=img_openx, height=img_openy)
    canvas_open.configure(width=img_openx, height=img_openy)
    # 设置旋转角度初始值
    i_angle.set('45')
    # 放置图片
    img_open_tk = ImageTk.PhotoImage(img_open)
    img_open_canvas = canvas_open.create_image(0, 0, image=img_open_tk, anchor='nw')

    # 设置矩形裁剪
    global rec
    global rec_canvas
    rec.setxy(4, 4, img_openx, img_openy)
    rec_canvas = canvas_open.create_rectangle(*rec.getxy(), outline='red', width=4)

    length = get_diagonal(img_openx, img_openy)
    # f_rotate.configure(width=img_openx, height=img_openy)
    # canvas_rotate.configure(width=img_openx, height=img_openy)
    f_rotate.configure(width=length, height=length)
    canvas_rotate.configure(width=length, height=length)

    # cb_rotate()

    win_open.mainloop()
    win_rotate.mainloop()


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


def crop_margin(img, padding=(0, 0, 0, 0)):
    """
    去除图片的白边
    """
    # 转换成RGB格式，然后运用getbbox方法
    img = img.convert('RGB')
    # getbbox实际上检测的是黑边，所以要先将image对象反色
    img_ivt = ImageOps.invert(img)
    # 如果担心检测出来的bbox过小，可以加点padding
    bbox = img_ivt.getbbox()
    left = bbox[0] - padding[0]
    top = bbox[1] - padding[1]
    right = bbox[2] + padding[2]
    bottom = bbox[3] + padding[3]
    img_crop = img.crop([left, top, right, bottom])
    return img_crop


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
    global canvas_open

    # 左键按下的位置不处于矩形裁剪的四个顶点
    if vertex_focus == 0:
        return

    if rec_canvas is not None:
        canvas_open.delete(rec_canvas)
    rec_canvas = canvas_open.create_rectangle(v_opposite[0], v_opposite[1], event.x,
                                              event.y, outline='red', width=4)


def mouse_left_up(event):
    global vertex_focus
    global v_opposite
    global rec
    vertex_focus = 0
    rec.setxy(*v_opposite, event.x, event.y)


# 主窗口
win = tk.Tk()
# 窗口标题
win.title('图片旋转')
# 窗口大小
win.geometry('500x300')
# 设置窗口参数，bg背景颜色
win.configure(bg='grey')
# 打开图片的按钮
b_open = tk.Button(win, text='打开图片', height=2, width=10, command=cb_open)
b_open.place(x=100, y=100)
# b_open.pack(padx=10, pady=10)
# tk.Label(win, text='标签1').pack()

# 打开图片的窗口
win_open = None
# 创建框架，矩形区域
f_open = None
# 旋转角度输入框
e_angle = None
# 旋转按钮
b_rotate = None

# 框架2
f_open2 = None
# 打开图片的画布
canvas_open = None

# 旋转结果的窗口
win_rotate = None
# 菜单
menu = None
# 矩形区域框架
f_rotate = None
# 画布
canvas_rotate = None

# 打开的图片
img_open = None
img_open_tk = None
img_open_canvas = None
# 旋转结果图片
img_rotate = None
img_rotate_tk = None
img_rotate_canvas = None
# 裁剪的矩形
rec = RecTangle()
rec_canvas = None
# 焦点顶点的对角
v_opposite = rec.getv(0)
# 鼠标焦点处于矩形裁剪的哪个顶点上
vertex_focus = 0
# 旋转角度
angle = 0
# 旋转角度输入值
i_angle = tk.StringVar()

win.mainloop()
