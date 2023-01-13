import time
import tkinter
import tkinter.simpledialog
import tkinter.colorchooser
import tkinter.filedialog
from PIL import Image, ImageTk, ImageGrab


# 1 铅笔
# 2 直线
# 3 矩形
# 4 文本
# 5 橡皮擦
# 6 圆形


# 主窗口
def center_window(w, h):
    app.winfo_screenwidth()
    app.winfo_screenheight()
    app.geometry('%dx%d' % (w, h))


app = tkinter.Tk()
app.title('轩氏画图')
x = 1200
y = 800
center_window(x, y)

yesno = tkinter.IntVar(value=0)
what = tkinter.IntVar(value=1)
X = tkinter.IntVar(value=0)
Y = tkinter.IntVar(value=0)

foreColor = '#000000'
# 改背景色可以看到橡皮擦的实现
# backColor = '#000000'
backColor = '#FFFFFF'

image = tkinter.PhotoImage()
canvas = tkinter.Canvas(app, bg='white', width=x, height=y)
canvas.create_image(x, y, image=image)

lastDraw = 0
end = [0]
size = "20"


# 使用鼠标左键按下等动作探测，绘制曲线
def getter(widget):
    time.sleep(0.5)
    # 获取窗口x和画布widget的x，相加就是画布相对于屏幕的x
    x = app.winfo_x() + widget.winfo_x()
    y = app.winfo_y() + widget.winfo_y()
    if app.winfo_x() < 0:
        x = 0
    if app.winfo_y() < 0:
        y = 0
    # x1 = x + widget.winfo_width() + 200
    x1 = x + widget.winfo_width()
    # y1 = y + widget.winfo_height() + 200
    y1 = y + widget.winfo_height()
    filename = tkinter.filedialog.asksaveasfilename(filetypes=[('.jpg', 'JPG')],
                                                    initialdir='./1.jpg')
    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)


def onLeftButtonDown(event):
    yesno.set(1)
    X.set(event.x)
    Y.set(event.y)
    if what.get() == 4:
        canvas.create_text(event.x, event.y, font=("等线", int(size)), text=text, fill=foreColor)
        what.set(1)


def onLeftButtonMove(event):
    global lastDraw
    # 0表示没有按下鼠标左键
    if yesno.get() == 0:
        return
    # 铅笔
    if what.get() == 1:

        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill=foreColor)
        X.set(event.x)
        Y.set(event.y)
    # 直线
    elif what.get() == 2:
        try:
            canvas.delete(lastDraw)
        except Exception:
            pass

        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill=foreColor)
    # 矩形
    elif what.get() == 3:

        try:
            canvas.delete(lastDraw)
        except Exception:
            pass
        lastDraw = canvas.create_rectangle(X.get(), Y.get(), event.x, event.y,
                                           outline=foreColor)

    # 橡皮擦
    elif what.get() == 5:

        lastDraw = canvas.create_rectangle(event.x - 10, event.y - 10, event.x + 10, event.y + 10,
                                           outline=backColor)
    # 圆形
    elif what.get() == 6:

        try:
            canvas.delete(lastDraw)
        except Exception:
            pass
        lastDraw = canvas.create_oval(X.get(), Y.get(), event.x, event.y,
                                      fill=backColor, outline=foreColor)


def onLeftButtonUp(event):
    global lastDraw

    # 如果这里没有再次create，画直线后接着画矩形，直线会被删除，因为画矩形的时候在try语句中删除了lastDraw
    # 但是这样也有一个问题，画一次直线，其实画了两条一样的，因为create了两次
    # 如果画直线之后接着画铅笔，那么撤销这条直线需要撤销两次，因为画铅笔的代码中没有删除lastDraw

    # 直线
    if what.get() == 2:

        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y, fill=foreColor)
    # 矩形
    elif what.get() == 3:

        lastDraw = canvas.create_rectangle(X.get(), Y.get(), event.x, event.y, outline=foreColor)
    # 圆形
    elif what.get() == 6:

        lastDraw = canvas.create_oval(X.get(), Y.get(), event.x, event.y, outline=foreColor)
    yesno.set(0)
    end.append(lastDraw)


def onRightButtonUp(event):
    menu.post(event.x_root, event.y_root)


# 通过bind来移动画笔
canvas.bind('<Button-1>', onLeftButtonDown)
canvas.bind('<B1-Motion>', onLeftButtonMove)
canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
canvas.bind('<ButtonRelease-3>', onRightButtonUp)
canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

'''主菜单及其关联的函数'''
menu = tkinter.Menu(app, bg="red")
app.config(menu=menu)


def Open():
    filename = tkinter.filedialog.askopenfilename(title='导入图片',
                                                  filetypes=[('image', '*.jpg *.png *.gif')])
    if filename:
        global image

        image = Image.open(filename)
        image = image.resize((800, 600), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        canvas.create_image(400, 300, image=image)


menu.add_command(label='导入', command=Open)


def Save():
    getter(canvas)


menu.add_command(label='保存', command=Save)


def Clear():
    global lastDraw, end
    for item in canvas.find_all():
        canvas.delete(item)
    end = [0]
    lastDraw = 0


menu.add_command(label='清屏', command=Clear)


def Back():
    global end
    try:
        for i in range(end[-2], end[-1] + 1):
            canvas.delete(i)
        end.pop()
    except:
        end = [0]


menu.add_command(label='撤销', command=Back)

menu.add_separator()

'''子菜单及其关联的函数'''
menuType = tkinter.Menu(menu, tearoff=0)


def drawCurve():
    what.set(1)


menuType.add_command(label='铅笔', command=drawCurve)


def drawLine():
    what.set(2)


menuType.add_command(label='直线', command=drawLine)


def drawRectangle():
    what.set(3)


menuType.add_command(label='矩形', command=drawRectangle)


def drawCircle():
    what.set(6)


menuType.add_command(label='圆形', command=drawCircle)


def drawText():
    global text, size
    text = tkinter.simpledialog.askstring(title='输入文本', prompt='')
    if text is not None:
        size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=20)
        if size is None:
            size = "20"
    what.set(4)


menuType.add_command(label='文本', command=drawText)


def onErase():
    what.set(5)


menuType.add_command(label='橡皮擦', command=onErase)
menuType.add_separator()


def chooseForeColor():
    global foreColor
    foreColor = tkinter.colorchooser.askcolor()[1]


menuType.add_command(label='选择前景色', command=chooseForeColor)


def chooseBackColor():
    global backColor
    backColor = tkinter.colorchooser.askcolor()[1]


menuType.add_command(label='选择背景色', command=chooseBackColor)

menu.add_cascade(label='工具栏', menu=menuType)

app.mainloop()