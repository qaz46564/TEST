import tkinter as tk
import random, math, time

# Chiikawa-inspired desktop companion. Standard-library prototype for Windows.
# Build into a standalone EXE using build_exe.bat (requires internet once to install PyInstaller).

W, H = 190, 205
KEY = "#ff00ff"
INK = "#292326"
WHITE = "#fffdfb"
PINK = "#f5a7ba"
BLUE = "#8edbe9"
CREAM = "#fff5e9"

class ChiikawaPet:
    def __init__(self, root):
        self.root = root
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg=KEY)
        try: root.wm_attributes("-transparentcolor", KEY)
        except tk.TclError: pass
        self.sw, self.sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.x, self.y = max(0, self.sw//2-90), max(0, self.sh-280)
        root.geometry(f"{W}x{H}+{self.x}+{self.y}")
        self.c = tk.Canvas(root, width=W, height=H, bg=KEY, highlightthickness=0, bd=0)
        self.c.pack()
        self.state = "walk"
        self.frame = 0
        self.dx = random.choice([-1.8, 1.8])
        self.drag_origin = None
        self.drag_start = None
        self.state_since = time.time()
        self.msg = ""
        self.msg_until = 0
        self.edge_side = "left"
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="쓰다듬기", command=self.pet)
        self.menu.add_command(label="기뻐하기", command=lambda: self.set_state("happy"))
        self.menu.add_command(label="울기", command=lambda: self.set_state("cry"))
        self.menu.add_command(label="그루밍", command=lambda: self.set_state("groom"))
        self.menu.add_command(label="잠자기", command=lambda: self.set_state("sleep"))
        self.menu.add_command(label="다시 걷기", command=lambda: self.set_state("walk"))
        self.menu.add_separator()
        self.menu.add_command(label="종료 (Esc)", command=root.destroy)
        self.c.bind("<ButtonPress-1>", self.press)
        self.c.bind("<B1-Motion>", self.drag)
        self.c.bind("<ButtonRelease-1>", self.release)
        self.c.bind("<Button-3>", self.popup)
        root.bind("<Escape>", lambda e: root.destroy())
        self.draw()
        self.tick()

    def oval(self, box, fill, outline=INK, width=2):
        return self.c.create_oval(*box, fill=fill, outline=outline, width=width)
    def line(self, pts, width=3, fill=INK, smooth=False):
        return self.c.create_line(*pts, fill=fill, width=width, capstyle=tk.ROUND,
                                  joinstyle=tk.ROUND, smooth=smooth)
    def poly(self, pts, fill, outline=INK, width=2, smooth=True):
        return self.c.create_polygon(*pts, fill=fill, outline=outline, width=width, smooth=smooth)

    def draw(self):
        c = self.c; c.delete("all")
        f = self.frame
        bob = math.sin(f*.42)*2.2 if self.state in ("walk","happy","edge") else (math.sin(f*.13)*1.0 if self.state=="sleep" else 0)
        # speech bubble
        if time.time() < self.msg_until and self.msg:
            c.create_oval(16, 1, 126, 34, fill="#fffdfb", outline="#d8c8cb", width=1)
            c.create_text(71, 17, text=self.msg, fill=INK, font=("Malgun Gothic", 10, "bold"))
        # shadow
        self.oval((48,177,143,190), "#d8d0d0", "#d8d0d0", 1)
        # tiny ears / round head silhouette
        self.poly([48,51+bob,43,28+bob,53,19+bob,66,28+bob,73,47+bob], WHITE, INK, 3)
        self.poly([117,47+bob,126,28+bob,139,20+bob,148,30+bob,140,55+bob], WHITE, INK, 3)
        # body/head as a unified chubby shape
        self.poly([47,48+bob,62,37+bob,82,33+bob,105,35+bob,128,43+bob,
                   145,62+bob,151,88+bob,147,117+bob,140,137+bob,
                   143,153+bob,132,161+bob,116,155+bob,108,177+bob,
                   91,183+bob,76,178+bob,69,158+bob,52,164+bob,
                   42,155+bob,47,137+bob,35,120+bob,31,95+bob,36,70+bob],
                  WHITE, INK, 3)
        # little feet and arms
        self.oval((59,155+bob,83,185+bob), WHITE, INK, 3)
        self.oval((103,155+bob,127,185+bob), WHITE, INK, 3)
        self.poly([39,119+bob,27,124+bob,25,134+bob,35,139+bob,45,133+bob], WHITE, INK, 2)
        self.poly([143,118+bob,155,122+bob,158,132+bob,148,138+bob,139,131+bob], WHITE, INK, 2)
        # cheeks
        self.oval((42,100+bob,68,119+bob), PINK, PINK, 1)
        self.oval((119,100+bob,145,119+bob), PINK, PINK, 1)
        # cheek hatch marks
        for x in (49,56,63): self.line([x,106+bob,x-3,113+bob],2,INK)
        for x in (126,133,140): self.line([x,106+bob,x-3,113+bob],2,INK)
        # state-specific face
        if self.state == "sleep":
            self.line([71,82+bob,78,85+bob,85,82+bob],3)
            self.line([104,82+bob,111,85+bob,118,82+bob],3)
            self.line([89,103+bob,95,106+bob,101,103+bob],2)
            c.create_text(142,57,text="z",fill="#7caac3",font=("Arial",14,"bold"))
            c.create_text(154,43,text="z",fill="#7caac3",font=("Arial",10,"bold"))
        elif self.state == "cry":
            self.line([69,81+bob,77,85+bob,85,81+bob],3)
            self.line([103,81+bob,111,85+bob,119,81+bob],3)
            self.oval((76,87+bob,84,108+bob), BLUE, BLUE, 1)
            self.oval((105,87+bob,113,108+bob), BLUE, BLUE, 1)
            self.oval((88,102+bob,101,113+bob), INK, INK, 1)
        elif self.state == "happy":
            self.line([70,81+bob,77,75+bob,84,81+bob],3)
            self.line([104,81+bob,111,75+bob,118,81+bob],3)
            self.poly([86,96+bob,91,92+bob,96,96+bob,101,92+bob,106,96+bob,100,107+bob,93,107+bob], INK, INK, 1)
            c.create_text(29,61,text="♪",fill=PINK,font=("Arial",14,"bold"))
        elif self.state == "groom":
            self.oval((72,78+bob,81,87+bob),INK,INK,1)
            self.oval((106,78+bob,115,87+bob),INK,INK,1)
            self.oval((89,98+bob,101,106+bob),PINK,INK,1)
            self.oval((104,121+bob,122,139+bob),WHITE,INK,2)
            self.line([91,111+bob,97,114+bob],2)
        elif self.state == "edge":
            self.oval((72,78+bob,81,87+bob),INK,INK,1)
            self.oval((106,78+bob,115,87+bob),INK,INK,1)
            self.line([87,99+bob,93,102+bob,99,99+bob],2)
            self.line([38,126+bob,28,120+bob],3)
            self.line([146,126+bob,157,120+bob],3)
        else:
            # expressive neutral / walking face
            self.oval((72,78+bob,81,87+bob), INK, INK, 1)
            self.oval((106,78+bob,115,87+bob), INK, INK, 1)
            self.line([86,99+bob,91,103+bob,96,99+bob,101,103+bob,106,99+bob],2)
            # eyebrows
            self.line([69,68+bob,80,65+bob],2)
            self.line([106,65+bob,117,68+bob],2)
        # little walk marks
        if self.state == "walk" and f % 10 < 4:
            self.line([22,146,14,149],2,"#8b7b7e")
            self.line([160,146,168,149],2,"#8b7b7e")
        if self.state == "edge":
            c.create_text(95,198,text="꼬옥!",fill=INK,font=("Malgun Gothic",8,"bold"))

    def say(self, text, duration=1.6):
        self.msg=text; self.msg_until=time.time()+duration; self.draw()
    def set_state(self, s):
        self.state=s; self.state_since=time.time(); self.draw()
    def pet(self):
        self.set_state("happy")
        self.say(random.choice(["헤헤!","우웅!","좋아!","와아!","고마워!"]))
        self.root.after(1500, lambda: self.set_state("walk") if self.state=="happy" else None)
    def press(self, e):
        self.drag_origin=(e.x,e.y); self.drag_start=(self.x,self.y)
    def drag(self, e):
        if self.drag_origin is None: return
        dx=e.x-self.drag_origin[0]; dy=e.y-self.drag_origin[1]
        if abs(dx)+abs(dy)>3:
            self.x=max(0,min(self.sw-W,self.drag_start[0]+dx))
            self.y=max(0,min(self.sh-H,self.drag_start[1]+dy))
            self.root.geometry(f"+{int(round(self.x))}+{int(round(self.y))}")
            self.state="idle"; self.draw()
    def release(self, e):
        if self.drag_origin is None: return
        moved=abs(e.x-self.drag_origin[0])+abs(e.y-self.drag_origin[1])>5
        self.drag_origin=None; self.drag_start=None
        if not moved: self.pet()
        else:
            if self.x < 8 or self.x > self.sw-W-8:
                self.state="edge"; self.edge_side="left" if self.x<self.sw/2 else "right"
            else: self.state="idle"
            self.state_since=time.time()
    def popup(self, e):
        try: self.menu.tk_popup(e.x_root,e.y_root)
        finally: self.menu.grab_release()

    def tick(self):
        if not self.root.winfo_exists(): return
        now=time.time(); self.frame+=1
        if self.drag_origin is None:
            if self.state == "walk":
                self.x += self.dx
                if self.x < 0 or self.x > self.sw-W:
                    self.dx *= -1
                    self.x=max(0,min(self.sw-W,self.x))
                    self.state="edge"; self.edge_side="left" if self.x==0 else "right"; self.state_since=now
                self.root.geometry(f"+{int(round(self.x))}+{int(round(self.y))}")
                if random.random()<0.0018:
                    self.set_state(random.choice(["sleep","groom","idle","happy"]))
            elif self.state in ("sleep","groom","idle","happy","cry"):
                limit={"sleep":5.5,"groom":3.2,"idle":2.2,"happy":1.5,"cry":2.8}.get(self.state,3)
                if now-self.state_since>limit:
                    self.state="walk"; self.state_since=now
            elif self.state=="edge":
                # cling for a moment, then shuffle away from the edge
                if now-self.state_since>3:
                    self.dx=1.8 if self.edge_side=="left" else -1.8
                    self.state="walk"; self.state_since=now
        self.draw()
        self.root.after(90,self.tick)

if __name__ == "__main__":
    root=tk.Tk()
    app=ChiikawaPet(root)
    root.mainloop()
