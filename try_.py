import cv2 as cv
import numpy as np


# 输入cv.imread后的图片，通过点击四个点选择要裁剪的部分
def get_window_size(src, bound=600):
    h, w = src.shape[0], src.shape[1]
    if h > w:
        h, w = bound, int(w * bound / h)
    else:
        h, w = int(h * bound / w), bound
    return (h, w)


class Indexer:
    def __init__(self):
        self.id = 0

    def get_id(self):
        self.id = (self.id + 1)
        return (self.id)


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        img = param['src']
        win_name = param['window']
        indexer = param['indexer']
        points = param['points']

        curr_id = indexer.get_id()
        points.append((x, y))
        print('第{}个顶点: ({},{})'.format(curr_id, x, y))

        cv.circle(img, (x, y), 10, (0, 0, 255), thickness=2)
        cv.putText(
            img,
            str(curr_id),  # 文字
            (x, y),  # 坐标
            cv.FONT_HERSHEY_PLAIN,
            5,  # 字号
            (0, 0, 255),  # 字体颜色
            thickness=2  # 粗细
        )

        cv.imshow(win_name, img)


# 输入cv.imread后的图片，通过点击四个点选择要裁剪的部分
def get_points(src):
    points = []
    indexer = Indexer()
    h, w = get_window_size(src)
    win_name = 'get_points'
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(win_name, width=w, height=h)
    cv.imshow(win_name, src)
    cv.setMouseCallback(win_name, on_EVENT_LBUTTONDOWN,
                        param={'src': src, 'window': win_name, 'indexer': indexer, 'points': points})
    cv.waitKey(0)
    cv.destroyAllWindows()
    if len(points) > 4:
        return points[0:4]
    # print(points)
    # points=[(2, 14), (90, 50), (87, 194), (1, 204)]
    return points


# 输入cv.imread后的图片，展示图片长什么样
def show_img(src):
    win_name = 'show_img'
    h, w = get_window_size(src)
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(win_name, width=w, height=h)
    cv.imshow(win_name, src)
    cv.waitKey(0)
    cv.destroyAllWindows()


def photo_cut_restore(src, points, H, W):
    target_points = [(0, 0), (W, 0), (W, H), (0, H)]
    points, target_points = np.array(points, dtype=np.float32), np.array(target_points, dtype=np.float32)
    M = cv.getPerspectiveTransform(points, target_points)
    # print('透视变换矩阵:', M)

    result = cv.warpPerspective(src_copy, M, (0, 0))
    result = result[:H, :W]
    win_name = 'Result'
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(win_name, width=W, height=H)
    cv.imshow(win_name, result)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return result


if __name__ == '__main__':
    path = './3.jpg'
    src = cv.imread(path)
    src_copy = src.copy()

    # show_img(src)

    W = 20
    H = 20
    # points=[(124, 182), (181, 177), (180, 243), (125, 266)]
    points = get_points(src)
    print(points)
    n = 20
    W = int(W * n)
    H = int(H * n)

    result = photo_cut_restore(src_copy, points, H, W)

    output_file = '1.jpg'
    cv.imwrite(output_file, result)
