# python3 
# Bounce game
 
import pygame
from pygame.locals import *
import sys,random,time,math
 
class GameWindow(object):
    '''window'''
    def __init__(self,*args,**kw):      
        self.window_length = 540
        self.window_wide = 500
        #draw the window of the game 
        self.game_window = pygame.display.set_mode((self.window_length,self.window_wide))
        #title
        pygame.display.set_caption("CatchBallGame")
        #background colour
        self.window_color = (144,112,152)
 
    def backgroud(self):
        #draw the background colour
        self.game_window.fill(self.window_color)

class Rect(object):
    '''rackt'''
    def __init__(self,*args,**kw):
        #racket's size and cokour 
        self.rect_color = (96,138,157)
        self.rect_length = 100
        self.rect_wide = 15
 
    def rectmove(self):
        
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
                           
        if self.mouse_x >= self.window_length-self.rect_length//2:
            self.mouse_x = self.window_length-self.rect_length//2
        if self.mouse_x <= self.rect_length//2:
            self.mouse_x = self.rect_length//2
        pygame.draw.rect(self.game_window,self.rect_color,((self.mouse_x-self.rect_length//2),(self.window_wide-self.rect_wide),self.rect_length,self.rect_wide))
 
class Ball(object):
    '''ball'''
    def __init__(self,*args,**kw):
        #ball's size colour and speed
        self.ball_color = (255,195,0)       
        self.move_x = 5
        self.move_y = 5
        self.radius = 10
 
    def ballready(self):
        #ball's initial position
        self.ball_x = self.mouse_x
        self.ball_y = self.window_wide-self.rect_wide-self.radius
                  
        pygame.draw.circle(self.game_window,self.ball_color,(self.ball_x,self.ball_y),self.radius)
 
    def ballmove(self):
                   
        pygame.draw.circle(self.game_window,self.ball_color,(self.ball_x,self.ball_y),self.radius)      
        self.ball_x += self.move_x
        self.ball_y -= self.move_y
        
        self.ball_window()
        self.ball_rect()
        
        #how to lose
        if self.ball_y > 520:
            self.gameover = self.over_font.render("Game Over",False,(0,0,0))
            self.game_window.blit(self.gameover,(100,130))
            self.over_sign = 1
 
 
class Brick(object):
    def __init__(self,*args,**kw):
        #blocks' size and colour
        self.brick_color = (181,243,255)
        self.brick_list = [[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1]]
        self.brick_length = 70
        self.brick_wide = 20
 
    def brickarrange(self):     
        for i in range(5):
            for j in range(6):
                self.brick_x = j*(self.brick_length+24)
                self.brick_y = i*(self.brick_wide+20)+40
                if self.brick_list[i][j] == 1:
                    #draw blocks 
                    pygame.draw.rect(self.game_window,self.brick_color,(self.brick_x,self.brick_y,self.brick_length,self.brick_wide))                   
                    
                    self.ball_brick()                                       
                    if self.distanceb < self.radius:
                        self.brick_list[i][j] = 0
                        self.score += self.point
        # how to win
        if self.brick_list == [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]:
            self.win = self.win_font.render("You Win",False,(0,0,0))
            self.game_window.blit(self.win,(100,130))
            self.win_sign = 1
 
class Score(object):
    '''score'''
    def __init__(self,*args,**kw):      
        #initial score
        self.score = 0
        #typrface
        self.score_font = pygame.font.SysFont('arial',20)
        
        self.point = 1
        
        self.frequency = 0
 
    def countscore(self):
        #draw player's score         
        my_score = self.score_font.render(str(self.score),False,(218,44,51))
        self.game_window.blit(my_score,(555,15))
 
class GameOver(object):
    '''gameover'''
    def __init__(self,*args,**kw):
        #typrface
        self.over_font = pygame.font.SysFont('arial',80)
        #gameover sign 
        self.over_sign = 0
 
class Win(object):
    '''win'''
    def __init__(self,*args,**kw):
        #typrface
        self.win_font = pygame.font.SysFont('arial',80)
        #sign of win
        self.win_sign = 0
 

class Collision(object):
    '''collision'''
    
    def ball_window(self):
        if self.ball_x <= self.radius or self.ball_x >= (self.window_length-self.radius):
            self.move_x = -self.move_x
        if self.ball_y <= self.radius:
            self.move_y = -self.move_y
 
    #bounce between the ball and the racket
    def ball_rect(self):
        
        self.collision_sign_x = 0
        self.collision_sign_y = 0
 
        if self.ball_x < (self.mouse_x-self.rect_length//2):
            self.closestpoint_x = self.mouse_x-self.rect_length//2
            self.collision_sign_x = 1
        elif self.ball_x > (self.mouse_x+self.rect_length//2):
            self.closestpoint_x = self.mouse_x+self.rect_length//2
            self.collision_sign_x = 2
        else:
            self.closestpoint_x = self.ball_x
            self.collision_sign_x = 3
 
        if self.ball_y < (self.window_wide-self.rect_wide):
            self.closestpoint_y = (self.window_wide-self.rect_wide)
            self.collision_sign_y = 1
        elif self.ball_y > self.window_wide:
            self.closestpoint_y = self.window_wide
            self.collision_sign_y = 2
        else:
            self.closestpoint_y = self.ball_y
            self.collision_sign_y = 3
        
        self.distance = math.sqrt(math.pow(self.closestpoint_x-self.ball_x,2)+math.pow(self.closestpoint_y-self.ball_y,2))
        
        if self.distance < self.radius and self.collision_sign_y == 1 and (self.collision_sign_x == 1 or self.collision_sign_x == 2):
            if self.collision_sign_x == 1 and self.move_x > 0:
                self.move_x = - self.move_x
                self.move_y = - self.move_y
            if self.collision_sign_x == 1 and self.move_x < 0:
                self.move_y = - self.move_y
            if self.collision_sign_x == 2 and self.move_x < 0:
                self.move_x = - self.move_x
                self.move_y = - self.move_y
            if self.collision_sign_x == 2 and self.move_x > 0:
                self.move_y = - self.move_y
        if self.distance < self.radius and self.collision_sign_y == 1 and self.collision_sign_x == 3:
            self.move_y = - self.move_y
        
        if self.distance < self.radius and self.collision_sign_y == 3:
            self.move_x = - self.move_x
 
    #bounce between the ball and blocks
    def ball_brick(self):
        
        self.collision_sign_bx = 0
        self.collision_sign_by = 0
 
        if self.ball_x < self.brick_x:
            self.closestpoint_bx = self.brick_x
            self.collision_sign_bx = 1
        elif self.ball_x > self.brick_x+self.brick_length:
            self.closestpoint_bx = self.brick_x+self.brick_length
            self.collision_sign_bx = 2
        else:
            self.closestpoint_bx = self.ball_x
            self.collision_sign_bx = 3
 
        if self.ball_y < self.brick_y:
            self.closestpoint_by = self.brick_y
            self.collision_sign_by = 1
        elif self.ball_y > self.brick_y+self.brick_wide:
            self.closestpoint_by = self.brick_y+self.brick_wide
            self.collision_sign_by = 2
        else:
            self.closestpoint_by = self.ball_y
            self.collision_sign_by = 3
        
        self.distanceb = math.sqrt(math.pow(self.closestpoint_bx-self.ball_x,2)+math.pow(self.closestpoint_by-self.ball_y,2))
        
        if self.distanceb < self.radius and self.collision_sign_by == 1 and (self.collision_sign_bx == 1 or self.collision_sign_bx == 2):
            if self.collision_sign_bx == 1 and self.move_x > 0:
                self.move_x = - self.move_x
                self.move_y = - self.move_y
            if self.collision_sign_bx == 1 and self.move_x < 0:
                self.move_y = - self.move_y
            if self.collision_sign_bx == 2 and self.move_x < 0:
                self.move_x = - self.move_x
                self.move_y = - self.move_y
            if self.collision_sign_bx == 2 and self.move_x > 0:
                self.move_y = - self.move_y
        if self.distanceb < self.radius and self.collision_sign_by == 1 and self.collision_sign_bx == 3:
            self.move_y = - self.move_y
        
        if self.distanceb < self.radius and self.collision_sign_by == 2 and (self.collision_sign_bx == 1 or self.collision_sign_bx == 2):
            if self.collision_sign_bx == 1 and self.move_x > 0:
                self.move_x = - self.move_x
                self.move_y = - self.move_y
            if self.collision_sign_bx == 1 and self.move_x < 0:
                self.move_y = - self.move_y
            if self.collision_sign_bx == 2 and self.move_x < 0:
                self.move_x = - self.move_x
                self.move_y = - self.move_y
            if self.collision_sign_bx == 2 and self.move_x > 0:
                self.move_y = - self.move_y
        if self.distanceb < self.radius and self.collision_sign_by == 2 and self.collision_sign_bx == 3:
            self.move_y = - self.move_y
        
        if self.distanceb < self.radius and self.collision_sign_by == 3:
            self.move_x = - self.move_x
 
class Main(GameWindow,Rect,Ball,Brick,Collision,Score,Win,GameOver):
    '''main game'''
    def __init__(self,*args,**kw):      
        super(Main,self).__init__(*args,**kw)
        super(GameWindow,self).__init__(*args,**kw)
        super(Rect,self).__init__(*args,**kw)
        super(Ball,self).__init__(*args,**kw)
        super(Brick,self).__init__(*args,**kw)
        super(Collision,self).__init__(*args,**kw)      
        super(Score,self).__init__(*args,**kw)
        super(Win,self).__init__(*args,**kw)
        #sign of the bigning 
        start_sign = 0
 
        while True:         
            self.backgroud()
            self.rectmove()
            self.countscore()           
             
            if self.over_sign == 1 or self.win_sign == 1:
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        start_sign = 1
            if start_sign == 0:
                self.ballready()
            else:
                self.ballmove()
 
            self.brickarrange()
 
            
            pygame.display.update()
            
            time.sleep(0.050)
 
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    catchball = Main()