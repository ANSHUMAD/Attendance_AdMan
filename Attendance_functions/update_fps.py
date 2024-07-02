import time

def update_fps(self):
       now = time.time()
       # Refresh fps per second
       if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
           self.fps_show = self.fps
       self.start_time = now
       self.frame_time = now - self.frame_start_time
       self.fps = 1.0 / self.frame_time
       self.frame_start_time = now