# 게임 사이트 주소 : https://www.gamesaien.com/game/fruit_box_a/
# 기본설정 : 화면 확대율 175%, 스크롤 최대한 위로 올린 상태

import pyautogui as pg
import time
import cv2
import numpy as np
from dataclasses import dataclass 
import pprint
from collections import deque

# 좌표의 구조체 선언
@dataclass
class Pos:
    x:int = None
    y:int = None

start = Pos(440, 275)           # 캡쳐할 시작 좌표
end   = Pos(1430, 855)          # 캡쳐할 끝 좌표


# time.sleep(1);
# pg.moveTo(start.x, start.y)     # 시작 위치로 이동
# time.sleep(1);
# pg.moveTo(end.x, end.y)         # 끝 위치로 이동


pg.click(700, 600)

# 게임 이미지 캡쳐
time.sleep(1);
captureWidth = end.x - start.x
captureHeight = end.y - start.y
pg.screenshot("D:\Programming\AppleGameAI-main\images\CaptureImage.png", region = (start.x, start.y, captureWidth, captureHeight))

# 게임 이미지를 2차원 데이터로 만들기 위해 미리 10개의 사과이미지를 가져오고 대조를 통해 숫자로 치환
# 미리 캡쳐해놓은 10개의 부분 이미지 파일 경로
appleImages = [
    "D:\Programming\AppleGameAI-main\\appleImages\\apple1.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple2.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple3.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple4.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple5.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple6.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple7.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple8.png",
    "D:\Programming\AppleGameAI-main\\appleImages\\apple9.png"
    ]

# 템플릿 이미지들을 읽어와서 리스트에 저장
templates = [cv2.imread(file, cv2.IMREAD_COLOR) for file in appleImages]

# 주어진 이미지에서 가장 유사한 이미지의 번호를 찾는 함수
def findSimilarImageIndex(targetImage, templates):
    similarities = []

    for template in templates:
        result = cv2.matchTemplate(targetImage, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        similarities.append(maxVal)

    resultIndex = np.argmax(similarities)
    return resultIndex

# 이미지 불러오기
screenshot = cv2.imread("D:\Programming\AppleGameAI-main\images\CaptureImage.png")

# 부분 이미지의 크기 설정
print(captureWidth, captureHeight)
subImageWidth = captureWidth // 17
subImageHeight = captureHeight // 10

# 2차원 배열 초기화
grid = [[0 for i in range(17)] for j in range(10)]

# Initialize a dictionary of queues for numbers 1 through 9
queues = {i: deque() for i in range(1, 10)}

# 이미지에서 각 사과 부분을 잘라내어 2차원 배열에 저장
for i in range(10):
    for j in range(17):
        startX = i * subImageWidth
        endX = startX + subImageWidth
        startY = j * subImageHeight
        endY = startY + subImageHeight

        subImage = screenshot[startX:endX, startY:endY, :]

        # cv2.imwrite('D:\Programming\AppleGameAI-main\\appleImages\\capturedAppleImages\\{0}.png'.format(i * 17 + j), subImage)
        
        # 각 사과 부분을 1~9의 정수로 변환하여 저장
        grid[i][j] = round(findSimilarImageIndex(subImage, templates)) + 1

        queues[grid[i][j]].append((i, j))

# for number in range(1, 10):
#     print(f"Size of queue for number {number}: {len(queues[number])}")

# 2차원 배열 출력
pprint.pprint(grid)

# 드래그 할때, 합이 10이 되는지 판별
def check(sx, sy, ex, ey):
    sum = 0
    for x in range(sx, ex + 1):
        for y in range(sy, ey + 1):
            sum += grid[x][y]
    
    if sum == 10:
        # print(sx, sy, ex, ey, sum)
        return True
    else:
        return False

# 드래그하여 사과 지우기
def deletApple(sx, sy, ex, ey):
    # print( start.x + subImageWidth * sy, start.y + subImageHeight * sx, " -> " , start.x + subImageWidth * ey, start.y + subImageHeight * ex)
    pg.moveTo(start.x + subImageWidth * sy, start.y + subImageHeight * sx) 
    pg.dragTo(start.x + subImageWidth * (ey + 1) + 15, start.y + subImageHeight * (ex + 1) + 15, 1.4, button='left') # 시작 좌표, 끝 좌표, 드래그 시간 (1.3초가 정확도 괜찮은듯)

# 삭제된 부분 0으로 바꾸기
def makeZero(sx, sy, ex, ey):
    # print(sx, sy, ex, ey)
    for a in range(sx, ex + 1):
        for b in range(sy, ey + 1):
            grid[a][b] = 0

# 드래그 할때, 합이 10이 되는지 판별
def check2(inx, iny):
    (drx, dry) = checkDownRight(inx, iny)
    disDR = distance(inx, drx, iny, dry)
    (urx, ury) = checkUpRight(inx, iny)
    disUR = distance(inx, urx, iny, ury)
    (dlx, dly) = checkDownLeft(inx, iny)
    disDL = distance(inx, dlx, iny, dly)
    (ulx, uly) = checkUpLeft(inx, iny)
    disUL = distance(inx, ulx, iny, uly)

    # print(disDR, disUR, disDL, disUL)

    # Find the smallest value and its corresponding variable
    smallest_value = min(disDR, disUR, disDL, disUL)
    if smallest_value == 255:
        # print('not found')
        return False
    elif smallest_value == disDR:
        # print('disDR')
        deletApple(inx, iny, drx, dry)          # 사과 지우기
        makeZero(inx, iny, drx, dry)            # 0으로 바꾸기
        # pprint.pprint(grid)
        # print("==================================================")
    elif smallest_value == disUR:
        # print('disUR')
        deletApple(urx, iny, inx, ury)          # 사과 지우기
        makeZero(urx, iny, inx, ury)            # 0으로 바꾸기
        # pprint.pprint(grid)
        # print("==================================================")
    elif smallest_value == disDL:
        # print('disDL')
        deletApple(inx, dly, dlx, iny)          # 사과 지우기
        makeZero(inx, dly, dlx, iny)            # 0으로 바꾸기
        # pprint.pprint(grid)
        # print("==================================================")
    elif smallest_value == disUL:
        # print('disUL')
        deletApple(ulx, uly, inx, iny)          # 사과 지우기
        makeZero(ulx, uly, inx, iny)            # 0으로 바꾸기
        # pprint.pprint(grid)
        # print("==================================================")
    return True

def checkDownRight(inx, iny):
    for ex in range(inx, 10):
        for ey in range(iny, 17):
            if check(inx, iny, ex, ey):               # 합이 10이 된다면
                return (ex, ey)
    return (-1, -1)

def checkUpRight(inx, iny):
    for sx in range(inx, -1, -1):
        for ey in range(iny, 17):
            if check(sx, iny, inx, ey):               # 합이 10이 된다면
                return (sx, ey)
    return (-1, -1)

def checkDownLeft(inx, iny):
    for ex in range(inx, 10):
        for sy in range(iny, -1, -1):
            if check(inx, sy, ex, iny):               # 합이 10이 된다면
                return (ex, sy)
    return (-1, -1)

def checkUpLeft(inx, iny):
    for sx in range(inx, -1, -1):
        for sy in range(iny, -1, -1):
            if check(sx, sy, inx, iny):               # 합이 10이 된다면
                return (sx, sy)
    return (-1, -1)

def distance(x1, x2, y1, y2):
    if x1 == -1 or x2 == -1 or y1 == -1 or y2 == -1:
        return 255
    else:
        return abs(x1 - x2) + abs(y1 - y2)

# # 모든 경우의 수를 탐색
# while(True):
#     isFind = False
#     for sx in range(10):
#         for sy in range(17):
#             for ex in range(sx, 10):
#                 for ey in range(sy, 17):
#                     if check2(sx, sy, ex, ey):               # 합이 10이 된다면
#                         deletApple(sx, sy, ex, ey)          # 사과 지우기
#                         makeZero(sx, sy, ex, ey)            # 0으로 바꾸기
#                         isFind = True
                        
#                         # check
#                         pprint.pprint(grid)
#                         print("==================================================")

#     if isFind == False:
#         break

# beforelen = len(queues[9])

def checkNumQueue(qn):
    sumcnt = 0
    while True:
        cnt = 0
        for position in list(queues[qn]):
            x, y = position
            # print(position)
            if check2(x, y):
                cnt += 1
                queues[qn].remove(position)
                if(qn != 9):
                    sumcnt += cnt
                    return sumcnt
        if qn == 9 and cnt == 0:
            break
        elif qn != 9:
            sumcnt += cnt
            break
        else:
            sumcnt += cnt
    return sumcnt

qn = 9
while True:
    if(qn == 0):
        break
    remcnt = checkNumQueue(qn)
    print("qn " + str(qn) + " remcnt: " + str(remcnt))
    if(remcnt == 0):
        qn -= 1
    else:
        qn = 9

# print(9, 8)
# remcnt = 0
# for i in range(9, 7, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7)
# remcnt = 0
# for i in range(9, 6, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6)
# remcnt = 0
# for i in range(9, 5, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6, 5)
# remcnt = 0
# for i in range(9, 4, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6, 5, 4)
# remcnt = 0
# for i in range(9, 3, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6, 5, 4, 3)
# remcnt = 0
# for i in range(9, 2, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6, 5, 4, 3, 2)
# remcnt = 0
# for i in range(9, 1, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6, 5, 4, 3, 2, 1)
# remcnt = 0
# for i in range(9, 0, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))

# print(9, 8, 7, 6, 5, 4, 3, 2, 1)
# remcnt = 0
# for i in range(9, 0, -1):
#     remcnt += checkNumQueue(i)
# print("remcnt: " + str(remcnt))