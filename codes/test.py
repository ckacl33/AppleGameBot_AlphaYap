# 드래그 되는지 확인할려고 파일하나 만듦

import pyautogui as pg
import time
import cv2
import numpy as np
from dataclasses import dataclass 
import pprint

# 좌표의 구조체 선언
@dataclass
class Pos:
    x:int = None
    y:int = None

start = Pos(830, 250)           # 캡쳐할 시작 좌표
end   = Pos(1680, 750)          # 캡쳐할 끝 좌표

# 캡쳐한 이미지 크기
captureWidth = end.x - start.x
captureHeight = end.y - start.y

# 부분 이미지의 크기 설정
print(captureWidth, captureHeight)
subImageWidth = captureWidth // 17
subImageHeight = captureHeight // 10

print(subImageWidth, subImageHeight)

# 드래그하여 사과 지우기
def deletApple(sx, sy, ex, ey):
    print( start.x + subImageWidth * sx, start.y + subImageHeight * sy, " -> " , start.x + subImageWidth * ex, start.y + subImageHeight * ey)
    pg.moveTo(start.x + subImageWidth * sx, start.y + subImageHeight * sy) 
    pg.dragTo(start.x + subImageWidth * (ex + 1), start.y + subImageHeight * (ey + 1), 1, button='left')

time.sleep(1)
deletApple(1, 2, 2, 5)