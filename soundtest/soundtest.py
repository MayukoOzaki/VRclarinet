import pygame
import pygame.midi
import time

pygame.midi.init()

count = pygame.midi.get_count()
print("get_default_output_id:%d" % pygame.midi.get_default_output_id())
for i in range(count):
    print("%d:%s" % (i, pygame.midi.get_device_info(i)))


player = pygame.midi.Output(0)
ch=1
ve=50
while True:
   
    ch+=1
    ve+=1
    player.set_instrument(72,ch%3)
    player.note_on(60, ve,ch%3)
    time.sleep(0.001)
    player.note_off(60,ve-1,(ch-1)%3)
    time.sleep(0.05)
    
   
    ch+=1
    ve+=1
    player.set_instrument(72,ch%3)
    player.note_on(60,ve,ch%3)
    time.sleep(0.001)
    player.note_off(60,ve-1,(ch-1)%3)
    time.sleep(0.05)

  
    ch+=1
    ve+=1
    player.set_instrument(72,ch%3)
    player.note_on(60,ve,ch%3)
    time.sleep(0.001)
    player.note_off(60,ve-1,(ch-1)%3)
    time.sleep(0.05)

    
    ch+=1
    ve+=1
    player.set_instrument(72,ch%3)
    player.note_on(60,ve,ch%3)
    time.sleep(0.001)
    player.note_off(60,ve-1,(ch-1)%3)
    time.sleep(0.05)
    
    


player.close()
pygame.midi.quit()
