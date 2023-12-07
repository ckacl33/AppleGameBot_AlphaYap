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
end   = Pos(1670, 750)          # 캡쳐할 끝 좌표

time.sleep(1);
pg.moveTo(start.x, start.y)     # 시작 위치로 이동
time.sleep(1);
pg.moveTo(end.x, end.y)         # 끝 위치로 이동


# 게임 이미지 캡쳐
time.sleep(2);
captureWidth = end.x - start.x
captureHeight = end.y - start.y
pg.screenshot("C:\\Users\\Lee\\appleGame\\CaptureImage.png", region = (start.x, start.y, captureWidth, captureHeight))
