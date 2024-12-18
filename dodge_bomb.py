import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_RIGHT: (5, 0),
    pg.K_LEFT: (-5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横、縦）/画面内：True,画面買い：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示させ、5秒止める
    引数：画面Surface
    戻り値：なし
    """
    black_out = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_out, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    black_out.set_alpha(50)

    font_go = pg.font.Font(None, 80)
    txt_go = font_go.render("Game Over", True, (255, 255, 255))
    txt_go_rct = txt_go.get_rect()
    txt_go_rct.center = WIDTH/2, HEIGHT/2

    cry_ktn_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_ktn_img_rct = cry_ktn_img.get_rect()
    cry_ktn_img_rct.center = WIDTH/2-40*len("Game Over")/2, HEIGHT/2

    screen.blit(black_out, [0, 0])
    screen.blit(txt_go, txt_go_rct)
    screen.blit(cry_ktn_img, cry_ktn_img_rct)
    cry_ktn_img_rct.move_ip(40*len("Game Over"), 0)
    screen.blit(cry_ktn_img, cry_ktn_img_rct)
    pg.display.update()
    time.sleep(5)
    return
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0
    vx = 5
    vy = 5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)
        #爆弾を画面内にとどめる
        if check_bound(bb_rct) == (True, False):
            vy *= -1
        if check_bound(bb_rct) == (False, True):
            vx *= -1
        if bb_rct.colliderect(kk_rct):
            gameover(screen)
            return
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
