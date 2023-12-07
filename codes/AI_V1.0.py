# 게임 사이트 주소 : https://www.gamesaien.com/game/fruit_box_a/
# 기본설정 : 화면 확대율 100%, 스크롤 최대한 위로 올린 상태

import pyautogui as pg
import time
import cv2
import numpy as np
from dataclasses import dataclass 

# 좌표의 구조체 선언
@dataclass
class Pos:
    x:int = None
    y:int = None

start = Pos(830, 250)           # 캡쳐할 시작 좌표
end   = Pos(1680, 750)          # 캡쳐할 끝 좌표

time.sleep(1);
pg.moveTo(start.x, start.y)     # 시작 위치로 이동
time.sleep(1);
pg.moveTo(end.x, end.y)         # 끝 위치로 이동


# 게임 이미지 캡쳐
time.sleep(2);
captureWidth = end.x - start.x
captureHeight = end.y - start.y
pg.screenshot("C:\\Users\\Lee\\appleGame\\images\\CaptureImage.png", region = (start.x, start.y, captureWidth, captureHeight))

# 게임 이미지를 2차원 데이터로 만들기 위해 미리 10개의 사과이미지를 가져오고 대조를 통해 숫자로 치환
# 미리 캡쳐해놓은 10개의 부분 이미지 파일 경로
appleImages = [
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple1.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple2.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple3.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple4.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple5.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple6.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple7.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple8.png",
    "C:\\Users\\Lee\\appleGame\\appleImages\\apple9.png"
    ]

# 템플릿 이미지들을 읽어와서 리스트에 저장
templates = [cv2.imread(file, cv2.IMREAD_COLOR) for file in appleImages]

# 주어진 이미지에서 가장 유사한 이미지의 번호를 찾는 함수 (수정필요)
def findSimilarImageIndex(targetImage, templates):
    similarities = []

    for template in templates:
        targetImageHeight, targetImageWidth, _ = targetImage.shape
        templateResized = cv2.resize(template, (targetImageHeight, targetImageWidth))

        result = cv2.matchTemplate(targetImage, templateResized, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        similarities.append(maxVal)

    resultIndex = np.argmax(similarities)
    return resultIndex

# 이미지 불러오기
screenshot = cv2.imread("C:\\Users\\Lee\\appleGame\\images\\CaptureImage.png")

# 부분 이미지의 크기 설정
print(captureWidth, captureHeight)
subImageWidth = captureWidth // 17
subImageHeight = captureHeight // 10

# 2차원 배열 초기화
grid = np.zeros((10, 17), dtype=int)

# 이미지에서 각 사과 부분을 잘라내어 2차원 배열에 저장
for i in range(10):
    for j in range(17):
        startX = i * subImageWidth
        endX = startX + subImageWidth
        startY = j * subImageHeight
        endY = startY + subImageHeight

        subImage = screenshot[startX:endX, startY:endY, :]

        cv2.imwrite('C:\\Users\\Lee\\appleGame\\capturedAppleImages\\{0}.png'.format(i * 17 + j), subImage)
        
        # 각 사과 부분을 1~9의 정수로 변환하여 저장
        # grid[i, j] = round(findSimilarImageIndex(subImage, templates))

# 2차원 배열 출력
print(*grid)