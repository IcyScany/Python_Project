import ddddocr
import numpy as np
import cv2


def interference_line(img):
    h, w = img.shape[:2]
    # opencv矩阵点是反的
    # img[1,2] 1:图片的高度，2：图片的宽度
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                img[x, y] = 255  # 判断一圈有多少白的，超过2，就转成白的。
    return img


# 由于背景的一些噪声时相对独立的，所以进行8领域点过滤
# k是过滤条件
def remove_noise(img, k=4):
    img2 = img
    w, h = img2.shape

    def get_neighbors(img3, r, c):
        count = 0
        for i in [r - 1, r, r + 1]:
            for j in [c - 1, c, c + 1]:
                if img3[i, j] > 220:  # 纯白色
                    count += 1
        return count

    for x in range(w):
        for y in range(h):
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                img2[x, y] = 255
            else:
                n = get_neighbors(img2, x, y)  # 得到邻居的数量，纯白色的邻居
                if n > k:
                    img2[x, y] = 255
    return img2


def get_result(img):
    # 二值化处理
    t, img = cv2.threshold(img, 200, 230, cv2.THRESH_BINARY)
    # 去噪声
    # img = remove_noise(img)
    # 去线
    # img = interference_line(img)
    # 滤波
    # 定义卷积核
    kernel = np.random.randn(2, 2)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # img = cv2.erode(img, kernel)
    # img = cv2.dilate(img, kernel)

    cv2.imwrite('final_captcha.png', img)

    with open('final_captcha.png', 'rb') as f:
        img = f.read()
    # 识别+计算
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(img) + '='
    print(res)
    ans = 0

    if 'o' in res:
        res = res.replace('o', '0')
    if 'O' in res:
        res = res.replace('O', '0')
    if 'J' in res:
        res = res.replace('J', '1')
    if 'j' in res:
        res = res.replace('j', '1')
    if 'F' in res:
        res = res.replace('F', '+')
    if 'f' in res:
        res = res.replace('f', '+')
    if 'S' in res:
        res = res.replace('S', '5')
    if 's' in res:
        res = res.replace('s', '5')
    if 'b' in res:
        res = res.replace('b', '6')
    if 'B' in res:
        res = res.replace('B', '8')
    if 'r' in res:
        res = res.replace('r', '+')
    if 'g' in res:
        res = res.replace('g', '9')
    if 't' in res:
        res = res.replace('t', '+')
    if '一' in res:
        res = res.replace('一', '-')
    if 'x' in res:
        res = res.replace('x', '+')
    if '+' in res:
        ans = int(res.split('+')[0]) + int(res.split('+')[1][:-1])
        print(ans)
    if '-' in res:
        ans = int(res.split('-')[0]) - int(res.split('-')[1][:-1])
        print(ans)

    return ans


if __name__ == '__main__':
    image = cv2.imread('get_captcha.png', cv2.IMREAD_GRAYSCALE)
    answer = get_result(image)
    print(answer)
