#  -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------
# author: 散落于云海
# QQ学习群: 651689292
# github: https://github.com/jiangwu007
# Facebook: https://www.facebook.com/profile.php?id=100012379458432
# 知乎: https://www.zhihu.com/people/san-luo-yu-yun-hai-96
# 一些重要的小知识,参考过的一些贴子
# https://github.com/bsamek/Tetris
# https://blog.csdn.net/qq_21264377/article/details/119900475
# https://blog.csdn.net/wosind/article/details/106406870
# https://ask.csdn.net/questions/7471494
# https://stackoverflow.com/questions/17747904/continuous-calls-of-the-configure-event-in-tkinter
# https://stackoverflow.com/questions/64683696/tkinter-difference-between-event-and-event
# https://stackoverflow.com/questions/45183914/tkinter-detecting-a-window-drag-event
# https://www.cnpython.com/qa/94279
# https://segmentfault.com/q/1010000008579491
# --------------------------------------------------------------------------------------
import ctypes
from sys import path
import ttkbootstrap as tk
from random import choice
from datetime import datetime
from ttkbootstrap.dialogs import Messagebox
from typing import List, Tuple, Set, Deque, Dict, Counter


class AttrGame:
    BOX_SIZE: int = 45
    LOCAL_PATH: str = path[0]
    SCORES: Tuple[int, int, int, int, int] = (0, 2, 5, 9, 20)
    SPEED_GRADES: Dict = {
        1: 500, 2: 450, 3: 400, 4: 350, 5: 300, 6: 250,
        7: 200, 8: 170, 9: 140, 10: 120,
        11: 500, 12: 450, 13: 400, 14: 350, 15: 300, 16: 250,
        17: 200, 18: 170, 19: 140, 20: 120}

    @classmethod
    def set_box_size(cls, value: int) -> None:
        with open(rf"{AttrGame.LOCAL_PATH}\tetris", mode='w') as f:
            f.write(str(value))
        cls.BOX_SIZE = value

    @classmethod
    def get_width(cls) -> int:
        return cls.BOX_SIZE * 10

    @classmethod
    def get_height(cls) -> int:
        return cls.BOX_SIZE * 20


class Game(tk.Frame):
    def __init__(self, parent: tk.Window, title: str) -> None:
        tk.Frame.__init__(self, parent)
        self.grade: int = 1
        self.title: str = title
        self.scale_num: str = ''
        self.suspend: bool = False
        self.running_score: int = 0
        self._attr: AttrGame = AttrGame()
        self.create_new_game: bool = False
        self.skin: tk.BooleanVar = tk.BooleanVar()
        h, w, s = self._attr.get_height(), self._attr.get_width(), self._attr.BOX_SIZE
        self.game_init(s, h, w)

    def game_init(self, size: int, height: int, width: int) -> None:
        self.frame1: tk.Frame = tk.Frame(self, border=1, relief=tk.SUNKEN, height=height)
        self.canvas1: tk.Canvas = tk.Canvas(self.frame1, width=width, height=height)
        self.frame2: tk.Frame = tk.Frame(self, padding=(40, 0, 10, 10))
        self.scored: tk.Label = tk.Label(self.frame2, text='历史最高分')
        self.scored_num: tk.Label = tk.Label(self.frame2, text='0')
        self.score: tk.Label = tk.Label(self.frame2, text='当前分数')
        self.score_num: tk.Label = tk.Label(self.frame2, text='0')
        self.level: tk.Label = tk.Label(self.frame2, text='当前等级')
        self.level_num: tk.Label() = tk.Label(self.frame2, text=' ')
        self.canvas2: tk.Canvas = tk.Canvas(self.frame2, width=size * 4, height=size * 4)
        self.block: tk.Label() = tk.Label(self.frame2, text=' '.join(('积木大小:', str(size))))
        self.scale: tk.Scale = tk.Scale(self.frame2, bootstyle='info', orient=tk.HORIZONTAL, to=80,
                                        from_=25, length=200, value=size, command=self.click_block)
        self.game_save: tk.Button = tk.Button(self.frame2, text='保存设置', command=self.click_save)
        self.game_start: tk.Button = tk.Button(self.frame2, text='开始游戏', command=self.click_start)
        self.game_stop: tk.Button = tk.Button(self.frame2, text='暂停游戏', command=self.click_suspend)
        self.game_reset: tk.Button = tk.Button(self.frame2, text='重置游戏', command=self.click_reset)
        self.rounded: tk.Checkbutton = tk.Checkbutton(self.frame2, padding=(10, 30, 10, 0),
                                                      bootstyle='success-round-toggle',
                                                      variable=self.skin, text='黑夜/白昼')
        self.rounded.bind('<Button-1>', self.click_skin)
        self.frame1.pack(side=tk.LEFT)
        self.canvas1.pack()
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.scored.grid(row=0, column=0, pady=0)
        self.scored_num.grid(row=1, column=0, pady=10)
        self.score.grid(row=2, column=0, pady=5)
        self.score_num.grid(row=3, column=0, pady=10)
        self.level.grid(row=4, column=0, pady=5)
        self.level_num.grid(row=5, column=0, pady=10)
        self.canvas2.grid(row=6, column=0, pady=5, padx=5)
        self.block.grid(row=7, column=0, pady=10)
        self.scale.grid(row=8, column=0, pady=10)
        self.game_save.grid(row=9, column=0, pady=10, ipadx=40)
        self.game_start.grid(row=10, column=0, pady=10, ipadx=40)
        self.game_stop.grid(row=11, column=0, pady=10, ipadx=40)
        self.game_reset.grid(row=12, column=0, pady=10, ipadx=40)
        self.rounded.grid(row=13, column=0, pady=0)
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.rowconfigure(1, weight=1)
        self.frame2.rowconfigure(2, weight=1)
        self.frame2.rowconfigure(3, weight=1)
        self.frame2.rowconfigure(4, weight=1)
        self.frame2.rowconfigure(5, weight=1)
        self.frame2.rowconfigure(6, weight=1)
        self.frame2.rowconfigure(13, weight=1)

    def click_save(self) -> None:
        if not self.create_new_game:
            size = int(self.block['text'].rsplit(' ', 1)[1])
            self._attr.set_box_size(size)
            self.canvas1.configure(width=self._attr.get_width(), height=self._attr.get_height())
            self.canvas2.configure(width=size * 4, height=size * 4)

    def click_start(self) -> None:
        if not self.create_new_game:
            self.timer = datetime.now()
            self.level_num.configure(text='1')
            self.score_num.configure(text='0')
            self.create_new_game = True
            self.current_shape = Current_Shape(self.canvas1, self.canvas2)
            self._bind()
            self._timer()

    def click_suspend(self) -> None:
        if self.game_stop['text'] == '暂停游戏':
            self.game_stop.configure(text='继续游戏')
            self._bind(False)
            self.suspend = True
        else:
            self.game_stop.configure(text='暂停游戏')
            self.suspend = False
            self._bind()
            self.after(200, self._timer)

    def click_reset(self) -> None:
        self.create_new_game = False
        self._bind(False)
        self.canvas1.delete(tk.ALL)
        self.canvas2.delete(tk.ALL)
        self.level_num.configure(text=' ')
        self.score_num.configure(text=' ')
        self.grade, self.running_score = 1, 0
        if self.game_stop['text'] == '继续游戏':
            self.game_stop.configure(text='暂停游戏')
            self.suspend = False

    def click_skin(self, event) -> None:
        top: tk.Window = self.nametowidget(self.winfo_parent())
        if self.skin.get():
            return top.style.theme_use('darkly')
        top.style.theme_use('yeti')

    def click_block(self, *args) -> None:
        if not self.scale_num == '':
            self.after_cancel(self.scale_num)
        self.scale_num = self.after(50, self._scale_ok)

    def _scale_ok(self) -> None:
        self.block.configure(text=' '.join(('积木大小:', str(int(self.scale.get())))))
        self.scale_num = ''

    def _handle_events(self, event) -> None:
        if (a := event.keysym) == 'Up' or a == 'w':
            self.current_shape.rotate()
        elif a == 'Left' or a == 'a':
            self.current_shape.move(-1, 0)
        elif a == 'Right' or a == 'd':
            self.current_shape.move(1, 0)
        elif a == 'Down' or a == 's' or a == 'space':
            self.current_shape.move(0, 1)

    def _timer(self) -> None:
        if self.create_new_game and not self.suspend:
            if not self.current_shape.fall():
                if line := self._remove_complete_lines():
                    self.running_score += self._attr.SCORES[line]
                    self.grade = self.running_score // 100 + 1
                    self.level_num.configure(text=str(self.grade))
                    self.score_num.configure(text=str(self.running_score))
                self.current_shape = Current_Shape(self.canvas1, self.canvas2)
                if self._is_game_over():
                    return self._game_over()
            self.after(self._attr.SPEED_GRADES[self.grade], self._timer)

    def _remove_complete_lines(self) -> int:
        shape_boxes_coords: List[float] = [
            self.canvas1.coords(box)[3] for box in self.current_shape.boxes
        ]
        width, size = self._attr.get_width(), self._attr.BOX_SIZE
        all_boxes: Tuple[int, ...] = self.canvas1.find_all()
        all_boxes_coords: Dict[int:float] = {
            k: v for k, v in zip(all_boxes, [self.canvas1.coords(box)[3] for box in all_boxes])
        }
        lines_to_check: Set[float] = set(shape_boxes_coords)
        boxes_to_check: Dict[int:float] = {
            k: v for k, v in all_boxes_coords.items() if any(v == line for line in lines_to_check)
        }
        counter: Counter = Counter()
        for box in boxes_to_check.values():
            counter[box] += 1
        complete_lines = [k for k, v in counter.items() if v == (width / size)]
        if not complete_lines:
            return 0
        for k, v in boxes_to_check.items():
            if v in complete_lines:
                self.canvas1.delete(k)
                del all_boxes_coords[k]
        for box, coords in all_boxes_coords.items():
            for line in complete_lines:
                if coords < line:
                    self.canvas1.move(box, 0, size)
        return len(complete_lines)

    def _is_game_over(self) -> bool:
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_test(box):
                return True
        return False

    def _game_over(self) -> None:
        self._bind(False)
        _deque.append(choice(Shape.SHAPES))
        second = datetime.now() - self.timer
        top: tk.Window = self.nametowidget(self.winfo_parent())
        Messagebox.ok(f"游戏结束! \n\n游戏用时: {self._cal_time(second.seconds)}",
                      self.title, True, self, padding=(150, 75),
                      position=(top.winfo_x() + top.winfo_width() // 5,
                                top.winfo_y() + top.winfo_height() // 4 + 100))
        if int(self.score_num['text']) > int(self.scored_num['text']):
            with open(rf'{self._attr.LOCAL_PATH}\history.txt', mode='w') as f:
                f.write(self.score_num['text'])
                self.scored_num.configure(text=self.score_num['text'])
        self.canvas1.delete(tk.ALL)
        self.canvas2.delete(tk.ALL)
        self.level_num.configure(text='')
        self.score_num.configure(text='')
        self.grade, self.running_score, self.create_new_game = 1, 0, False

    def _cal_time(self, myfloat: float) -> str:
        m, s = divmod(myfloat, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def _bind(self, mybool: bool = True) -> None:
        top: tk.Window = self.nametowidget(self.winfo_parent())
        if mybool:
            return top.bind('<Key>', self._handle_events)
        top.unbind('<Key>')


ShapeTuple = Tuple[int, list, Tuple[int, int],
                   Tuple[int, int], Tuple[int, int], Tuple[int, int]]


class Shape:
    def __init__(self) -> None:
        self._size = AttrGame()

    @ property
    def BOX_SIZE(self) -> int:
        return self._size.BOX_SIZE

    @ property
    def WIDTH(self) -> int:
        return self._size.get_width()

    @ property
    def HEIGHT(self) -> int:
        return self._size.get_height()

    @ property
    def START_POINT(self) -> int:
        s, w = self._size.BOX_SIZE, self._size.get_width()
        return w / 2 / s * s - s

    COLORS: Dict[int, str] = {
        1: "orange", 2: "Darkkhaki", 3: "SteelBlue",
        4: "DarkSalmon", 5: "IndianRed",
        6: "lightblue", 7: "Plum", }
    __POS: List[list] = [
        [AttrGame.BOX_SIZE, AttrGame.BOX_SIZE],
        [0, AttrGame.BOX_SIZE * 2 - AttrGame.BOX_SIZE // 2],
        [AttrGame.BOX_SIZE * 2 - AttrGame.BOX_SIZE // 2, 0],
        [AttrGame.BOX_SIZE // 1.5, AttrGame.BOX_SIZE // 3],
        [AttrGame.BOX_SIZE // 3, AttrGame.BOX_SIZE // 3],
        [AttrGame.BOX_SIZE // 3, AttrGame.BOX_SIZE],
        [AttrGame.BOX_SIZE, AttrGame.BOX_SIZE // 2], ]
    SHAPES: ShapeTuple = (
        [1, __POS[0], (0, 0), (1, 0), (0, 1), (1, 1)],   # square,第1位是Y轴,第2位是X轴
        [1, __POS[0], (0, 0), (1, 0), (0, 1), (1, 1)],   # 1
        [1, __POS[0], (0, 0), (1, 0), (0, 1), (1, 1)],   # 2
        [2, __POS[1], (0, 0), (1, 0), (2, 0), (3, 0)],   # Horizontal line
        [2, __POS[2], (0, 0), (0, 1), (0, 2), (0, 3)],   # Vertical line
        [3, __POS[4], (2, 0), (0, 1), (1, 1), (2, 1)],   # right F
        [3, __POS[4], (0, 0), (0, 1), (1, 0), (2, 0)],   # 6
        [3, __POS[2], (0, 0), (0, 1), (0, 2), (1, 2)],   # 7
        [3, __POS[3], (0, 0), (1, 0), (1, 1), (1, 2)],   # 8
        [4, __POS[4], (0, 0), (0, 1), (1, 1), (2, 1)],   # left F
        [4, __POS[6], (0, 0), (0, 1), (0, 2), (1, 0)],   # 10
        [4, __POS[0], (0, 0), (1, 0), (2, 0), (2, 1)],   # 11
        [4, __POS[6], (0, 2), (1, 0), (1, 1), (1, 2)],   # 12
        [5, __POS[6], (0, 1), (1, 1), (1, 0), (2, 0)],   # right Z
        [5, __POS[3], (0, 0), (0, 1), (1, 1), (1, 2)],   # 14
        [5, __POS[4], (0, 1), (1, 1), (1, 0), (2, 0)],   # 15
        [6, __POS[6], (0, 0), (1, 0), (1, 1), (2, 1)],   # left Z
        [6, __POS[3], (1, 0), (1, 1), (0, 1), (0, 2)],   # 17
        [6, __POS[3], (0, 0), (1, 0), (1, 1), (2, 1)],   # 18
        [6, __POS[3], (1, 0), (1, 1), (0, 1), (0, 2)],   # 19
        [7, __POS[5], (1, 0), (0, 1), (1, 1), (2, 1)],   # symmetrical T
        [7, __POS[3], (0, 1), (1, 0), (1, 1), (1, 2)],   # 21
        [7, __POS[5], (0, 0), (1, 0), (2, 0), (1, 1)],   # 22
        [7, __POS[2], (0, 0), (0, 1), (1, 1), (0, 2)])   # 23


class Current_Shape(Shape):
    def __init__(self, canvas1: tk.Canvas, canvas2: tk.Canvas) -> None:
        super().__init__()
        self.boxes: List[int] = []
        self.shape: ShapeTuple = _deque.popleft()
        if len(_deque) != 2:
            next_shape: ShapeTuple = _deque[0]
            _deque.append(choice(Shape.SHAPES))
            canvas2.delete(tk.ALL)
            for point in next_shape[2:]:
                canvas2.create_rectangle(
                    point[0] * self.BOX_SIZE + next_shape[1][0],
                    point[1] * self.BOX_SIZE + next_shape[1][1],
                    point[0] * self.BOX_SIZE + self.BOX_SIZE + next_shape[1][0],
                    point[1] * self.BOX_SIZE + self.BOX_SIZE + next_shape[1][1],
                    fill=self.COLORS[next_shape[0]])
        self.canvas: tk.Canvas = canvas1
        for point in self.shape[2:]:
            box = canvas1.create_rectangle(
                point[0] * self.BOX_SIZE + self.START_POINT,
                point[1] * self.BOX_SIZE,
                point[0] * self.BOX_SIZE + self.BOX_SIZE + self.START_POINT,
                point[1] * self.BOX_SIZE + self.BOX_SIZE,
                fill=self.COLORS[self.shape[0]])
            self.boxes.append(box)

    def move(self, x: int, y: int) -> bool:
        if not self._can_move_shape(x, y):
            return False
        for box in self.boxes:
            self.canvas.move(box, x * self.BOX_SIZE, y * self.BOX_SIZE)
        return True

    def can_move_box(self, box: int, x: int, y: int) -> bool:
        x, y = x * self.BOX_SIZE, y * self.BOX_SIZE
        coords: List[float] = self.canvas.coords(box)
        if coords[3] + y > self.HEIGHT:
            return False
        if coords[0] + x < 0:
            return False
        if coords[2] + x > self.WIDTH:
            return False
        overlap: Set[int] = set(self.canvas.find_overlapping(
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y,
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y))
        other_items: Set[int] = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items:
            return False
        return True

    def can_move_test(self, box) -> bool:
        coords = self.canvas.coords(box)
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        test = any(filter(lambda x: x <= self.BOX_SIZE * 2,
                          (self.canvas.coords(box)[3] for box in other_items)))
        if test and coords[3] <= self.BOX_SIZE:
            return False
        return True

    def fall(self) -> bool:
        if not self._can_move_shape(0, 1):
            return False
        for box in self.boxes:
            self.canvas.move(box, 0 * self.BOX_SIZE, 1 * self.BOX_SIZE)
        return True

    def rotate(self) -> bool:
        boxes: List[int] = self.boxes[:]
        pivot, size = boxes.pop(2), self.BOX_SIZE

        def get_move_coords(box) -> Tuple[int, int]:
            box_coords: List[int] = self.canvas.coords(box)
            pivot_coords: List[int] = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            return (- x_diff - y_diff) / size, (x_diff - y_diff) / size
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move):
                return False
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box, x_move * size, y_move * size)
        return True

    def _can_move_shape(self, x: int, y: int) -> bool:
        for box in self.boxes:
            if not self.can_move_box(box, x, y):
                return False
        return True


def resolution_power(resolv: int, root: tk.Window) -> None:
    abc = Messagebox.yesno(f"调整{resolv}%分辨率后,\n要关闭再打开游戏.\n您需要这么做吗?",
                           "连连看--by:散落于云海", False, root,
                           padding=(150, 75), anchor='center',
                           position=(root.winfo_x() + root.winfo_width() // 2 - 150 - 75,
                                     root.winfo_y() + root.winfo_height() // 2 - 75 - 75 // 2))
    if abc == NAME:
        with open(rf"{AttrGame.LOCAL_PATH}\resolution", mode='w') as f:
            f.write(str(resolv))


def game_rese(game: Game) -> None:
    if not game.create_new_game:
        game._attr.set_box_size(40)
        game.canvas1.configure(width=game._attr.get_width(), height=game._attr.get_height())
        game.canvas2.configure(width=40 * 4, height=40 * 4)


def theme_skin(theme_name: str, root: tk.Window) -> None:
    root.style.theme_use(theme_name)


def main(*args) -> None:
    global _deque, NAME
    _deque = Deque(maxlen=2)
    NAME = args[2]
    for _ in range(2):
        _deque.append(choice(Shape.SHAPES))
    try:
        with open(rf"{AttrGame.LOCAL_PATH}\tetris", mode='r') as f:
            AttrGame.set_box_size(int(f.read()))
    except FileNotFoundError:
        with open(rf"{AttrGame.LOCAL_PATH}\tetris", mode='w') as f:
            f.write(str(AttrGame.BOX_SIZE))
    root: tk.Window = tk.Window(args[0], themename='darkly', minsize=(300, 500))
    try:
        with open(rf"{AttrGame.LOCAL_PATH}\resolution", mode='r') as f:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            root.tk.call('tk', 'scaling', ScaleFactor / int(f.read()))
    except FileNotFoundError:
        pass
    menu: tk.Menu = tk.Menu(root)
    game_menu: tk.Menu = tk.Menu(menu)
    theme_menu: tk.Menu = tk.Menu(game_menu)
    menu.add_cascade(label='游戏设置', menu=game_menu, underline=1)
    resolution_menu: tk.Menu = tk.Menu(game_menu)
    game: Game = Game(root, title=args[0])
    game_menu.add_cascade(label='Theme', menu=theme_menu)
    game_menu.add_cascade(label='Zoom', menu=resolution_menu)
    game_menu.add_command(label='Window reset', command=lambda: game_rese(game))
    theme_menu.add_command(label='cosmo', command=lambda: theme_skin('cosmo', root))
    theme_menu.add_command(label='flatly', command=lambda: theme_skin('flatly', root))
    theme_menu.add_command(label='litera', command=lambda: theme_skin('litera', root))
    theme_menu.add_command(label='minty', command=lambda: theme_skin('minty', root))
    theme_menu.add_command(label='lumen', command=lambda: theme_skin('lumen', root))
    theme_menu.add_command(label='sandstone', command=lambda: theme_skin('sandstone', root))
    theme_menu.add_command(label='yeti', command=lambda: theme_skin('yeti', root))
    theme_menu.add_command(label='pulse', command=lambda: theme_skin('pulse', root))
    theme_menu.add_command(label='united', command=lambda: theme_skin('united', root))
    theme_menu.add_command(label='morph', command=lambda: theme_skin('morph', root))
    theme_menu.add_command(label='journal', command=lambda: theme_skin('journal', root))
    theme_menu.add_command(label='darkly', command=lambda: theme_skin('darkly', root))
    theme_menu.add_command(label='superhero', command=lambda: theme_skin('superhero', root))
    theme_menu.add_command(label='solar', command=lambda: theme_skin('solar', root))
    theme_menu.add_command(label='cyborg', command=lambda: theme_skin('cyborg', root))
    theme_menu.add_command(label='simplex', command=lambda: theme_skin('simplex', root))
    theme_menu.add_command(label='vapor', command=lambda: theme_skin('vapor', root))
    theme_menu.add_command(label='cerculean', command=lambda: theme_skin('cerculean', root))
    try:
        with open(rf"{AttrGame.LOCAL_PATH}\history.txt", mode='r') as f:
            content = f.read()
            game.scored_num.configure(text=content)
    except FileNotFoundError:
        with open(rf"{AttrGame.LOCAL_PATH}\history.txt", mode='w') as f:
            f.write('0')
            game.scored_num.configure(text='0')
    game.pack(fill=tk.BOTH, expand=tk.YES, padx=args[1], pady=args[1])
    resolution_menu.add_command(label='25%', command=lambda: resolution_power(25, root))
    resolution_menu.add_command(label='50%', command=lambda: resolution_power(50, root))
    resolution_menu.add_command(label='75%', command=lambda: resolution_power(75, root))
    resolution_menu.add_command(label='100%', command=lambda: resolution_power(100, root))
    resolution_menu.add_command(label='125%', command=lambda: resolution_power(125, root))
    resolution_menu.add_command(label='150%', command=lambda: resolution_power(150, root))
    resolution_menu.add_command(label='175%', command=lambda: resolution_power(175, root))
    resolution_menu.add_command(label='200%', command=lambda: resolution_power(200, root))
    root.configure(menu=menu)
    game.mainloop()


if __name__ == "__main__":
    # 英语环环境下,用'Yes',中文环境下用'确认'
    # Use 'yes' in English environment and'确认'in Chinese environment
    main("俄罗斯方块", 25, '确认')
