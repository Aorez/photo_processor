from PIL import Image

src_im = Image.open("1.jpg")
angle = 45
size = 100, 100

# dst_im = Image.new("RGBA", (196, 283), "blue")
# im = src_im.convert('RGBA')
# rot = im.rotate(angle, expand=True).resize(size)
# dst_im.paste(rot, (50, 50), rot)
# dst_im.save("test.png")

im = src_im.convert('RGBA')
rot = im.rotate(angle, expand=True)
dst_im = Image.new("RGBA", rot.size, "white")
newdata = []
for i in dst_im.getdata():
    if i[0] == 255 and i[1] == 255 and i[2] == 255:
        newdata.append((255, 255, 255, 0))
    else:
        newdata.append(i)
dst_im.putdata(newdata)
dst_im.paste(rot, (0, 0), rot)
dst_im.save("test.png")
