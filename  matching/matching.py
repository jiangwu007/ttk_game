#  -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------
# author: 散落于云海
# QQ学习群: 651689292
# github: https://github.com/jiangwu007
# Facebook: https://www.facebook.com/profile.php?id=100012379458432
# 知乎: https://www.zhihu.com/people/san-luo-yu-yun-hai-96
# https://coderslegacy.com/python/problem-solving/improve-tkinter-resolution/
# https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-
# disabled-programmatically-on-a-per-session-basis
# --------------------------------------------------------------------------------------
import ctypes
from sys import path
import ttkbootstrap as tk
from random import shuffle
from datetime import datetime
from typing import Dict, List
from PIL import ImageTk, Image
from PIL.ImageFile import ImageFile
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import dialogs
from ttkbootstrap.dialogs import Messagebox


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class AttrGame:
    BOX_SIZE: int = 80
    SECRET: bool = False
    LOCAL_PATH: str = path[0]
    CRY_HELP: bool = False

    def __init__(self) -> None:
        self.image: ImageFile = Image.open(rf'{AttrGame.LOCAL_PATH}\tk\images\animal.bmp')
        self.tit_img: ImageFile = Image.open(rf'{AttrGame.LOCAL_PATH}\tk\images\lian.bmp')

    def create_map(self, row: int, column: int) -> List[int]:
        self.row: int = row
        self.column: int = column
        images: List[ImageTk.PhotoImage] = [ImageTk.PhotoImage(self.image.crop(
            (0, i * 39, 39, (i + 1) * 39)).resize((AttrGame.BOX_SIZE - 1, AttrGame.BOX_SIZE - 1
                                                   ), Image.Resampling.LANCZOS)) for i in range(42)]
        temps: List[int] = [j for _ in range(4) for j in range(self.row * self.column // 4)]
        shuffle(images)
        images = images[:self.row * self.column // 4]
        shuffle(images)
        self.dict_pic: Dict[int, ImageTk.PhotoImage] = dict(zip(range(42), images))
        shuffle(temps)
        return temps

    @classmethod
    def set_box_size(cls, value: int) -> None:
        with open(rf"{AttrGame.LOCAL_PATH}\size", mode='w') as f:
            f.write(str(value))
        cls.BOX_SIZE = value

    @classmethod
    def set_cry_help(cls, mybool=bool) -> None:
        print(mybool)
        cls.CRY_HELP = mybool


class Game(tk.Frame):
    def __init__(self, parent: tk.Window, title: str) -> None:
        tk.Frame.__init__(self, parent)
        self.line_id: List[int] = []
        self.title: str = title
        self.scale_num: str = ''
        self.first_selected_block: int = -1
        self.frist_selected_bool: bool = False
        self.second_selected_block: int = -1
        self.first_find_block: int = -1
        self.second_find_block: int = -1
        self._attr: AttrGame = AttrGame()
        self.create_new_game: bool = False
        self.line_points: List[Point] = []
        self.skin: tk.BooleanVar = tk.BooleanVar()
        width, edge, size = self._attr.BOX_SIZE * 11, 10, self._attr.BOX_SIZE
        self.game_init(width, edge, size)

    def game_init(self, width: int, edge: int, size: int) -> None:
        self.frame1: tk.Frame = tk.Frame(self, border=1, relief=tk.SUNKEN, height=width)
        self.canvas1: tk.Canvas = tk.Canvas(self.frame1, height=width, width=width)
        self.title_img: Image.PhotoImage = ImageTk.PhotoImage(
            self._attr.tit_img.resize((size * 10, size * 5), Image.Resampling.LANCZOS))
        self.canvas1.create_image((size * 11 // 2, size * 11 // 2),
                                  image=self.title_img, tags='title_img', anchor='center')
        self.canvas1.bind('<Double-Button-1>', self.fault_tolerant)
        self.canvas1.bind('<Button-1>', self.click_link)
        self.canvas1.bind('<Button-3>', self.find_block)
        self.frame2: tk.Frame = tk.Frame(self)
        self.combobox: tk.Combobox = tk.Combobox(self.frame2, values=(
            '10 * 10', '12 * 12', '09 * 16', '10 * 14', '10 * 16'), width=8, state='readonly')
        self.combobox.current(0)
        self.lab_name: tk.Label = tk.Label(self.frame2, text='00:00:00')
        self.button: tk.Button = tk.Button(self.frame2, text='开始游戏', command=self.click_start)
        self.lab_save: tk.Button = tk.Button(self.frame2, text='保存设置', command=self.click_save)
        self.scale: tk.Scale = tk.Scale(self.frame2, orient=tk.HORIZONTAL, to=130, from_=30,
                                        length=150, value=size, command=self.click_block)
        self.block: tk.Label = tk.Label(self.frame2, text=str(size), padding=(edge, 0, 0, 0))
        self.tip: ToolTip = ToolTip(self.scale, text=str(size))
        self.frame2.pack(side=tk.TOP, pady=edge, expand=tk.YES, fill=tk.BOTH)
        self.frame1.pack(side=tk.TOP)
        self.canvas1.pack(padx=self._attr.BOX_SIZE // 4, pady=self._attr.BOX_SIZE // 4)
        self.combobox.grid(row=0, column=0, padx=edge)
        self.lab_name.grid(row=0, column=1, padx=edge)
        self.button.grid(row=0, column=2, padx=edge, ipadx=edge)
        self.lab_save.grid(row=0, column=3, padx=edge, ipadx=edge)
        self.block.grid(row=0, column=4)
        self.scale.grid(row=0, column=5, padx=edge)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.frame2.columnconfigure(2, weight=1)
        self.frame2.columnconfigure(3, weight=1)
        self.frame2.columnconfigure(4, weight=1)
        self.frame2.columnconfigure(5, weight=1)

    def click_start(self) -> None:
        if self.button['text'] == '开始游戏':
            self.h, self.w = self.combobox.get().split(' * ')
            self.canvas1.configure(width=(int(self.w) + 1) * self._attr.BOX_SIZE,
                                   height=(int(self.h) + 1) * self._attr.BOX_SIZE)
            self.m_map: List[int] = self._attr.create_map(int(self.h), int(self.w))
            self.print_map()
            self.button.configure(text='结束游戏')
            self.timer = datetime.now()
            self.after(1000, self.computing_time)
            self.canvas1.delete('title_img')
        elif self.button['text'] == '结束游戏':
            top: tk.Window = self.nametowidget(self.winfo_parent())
            abc = Messagebox.yesno(r"你需要结束游戏吗?", self.title, False, self,
                                   padding=(150, 75), anchor='center',
                                   position=(top.winfo_x() + top.winfo_width() // 2 - 150 - 75,
                                             top.winfo_y() + top.winfo_height() // 2 - 75 - 75 // 2))
            if abc == NAME:
                s = self._attr.BOX_SIZE
                self.canvas1.delete(tk.ALL)
                self.button.configure(text='开始游戏')
                self.lab_name.configure(text='00:00:00')
                self.first_find_block = self.second_find_block = -1
                self.title_img: Image.PhotoImage = ImageTk.PhotoImage(self._attr.tit_img.resize((
                    s * int(self.w), s * int(self.w) // 2), Image.Resampling.LANCZOS))
                self.canvas1.create_image(((int(self.w) + 1) * s // 2, (int(self.h) + 1) * s // 2),
                                          image=self.title_img, tags='title_img', anchor='center')

    def click_block(self, *args) -> None:
        if not self.scale_num == '':
            self.after_cancel(self.scale_num)
        self.scale_num = self.after(50, self._scale_ok)

    def click_link(self, event) -> None:
        if self.button['text'] == '结束游戏':
            x: int = (event.x - self._attr.BOX_SIZE // 2) // self._attr.BOX_SIZE
            y: int = (event.y - self._attr.BOX_SIZE // 2) // self._attr.BOX_SIZE
            if x == -1 or x == self._attr.column or y == -1 or y == self._attr.column:
                return None
            try:
                if self.m_map[y * self._attr.column + x] != -10:
                    s: int = self._attr.BOX_SIZE
                    if not self.frist_selected_bool:
                        self.p1: Point = Point(x, y)
                        self.first_selected_block = self.canvas1.create_rectangle(
                            x * s + s // 2, y * s + s // 2, x * s + s + s // 2,
                            y * s + s + s // 2, outline='red', width=2)
                        self.frist_selected_bool = True
                    else:
                        self.p2: Point = Point(x, y)
                        if self.p1.x == self.p2.x and self.p1.y == self.p2.y:
                            return None
                        self.second_selected_block = self.canvas1.create_rectangle(
                            x * s + s // 2, y * s + s // 2, x * s + s + s // 2,
                            y * s + s + s // 2, outline='red', width=2)
                        if self._attr.CRY_HELP:
                            if self.is_same_block(self.p1, self.p2):
                                self.frist_selected_bool = False
                                self._attr.set_cry_help(False)
                                return self.after(300, self.delay_run)
                        if self.is_same_block(self.p1, self.p2) and self.is_link(self.p1, self.p2):
                            self.frist_selected_bool = False
                            self.draw_link_line(self.p1, self.p2)
                            self.after(300, self.delay_run)
                        else:
                            self.canvas1.delete(self.first_selected_block)
                            self.canvas1.delete(self.second_selected_block)
                            self.first_selected_block = -1
                            self.second_selected_block = -1
                            self.frist_selected_bool = False
            except IndexError:
                print(y * self._attr.column + x)

    def _scale_ok(self) -> None:
        abc = str(int(self.scale.get()))
        self.block.configure(text=abc if len(abc) == 3 else '  ' + abc)
        self.tip.text = abc
        self.scale_num = ''

    def click_save(self) -> None:
        if self.button['text'] == '开始游戏':
            size = int(self.tip.text)
            h, w = self.combobox.get().split(' * ')
            self._attr.set_box_size(size)
            self.canvas1.configure(width=(int(w) + 1) * size, height=(int(h) + 1) * size)
            self.title_img: Image.PhotoImage = ImageTk.PhotoImage(self._attr.tit_img.resize((
                size * int(w), size * int(w) // 2), Image.Resampling.LANCZOS))
            self.canvas1.create_image(((int(w) + 1) * size // 2, (int(h) + 1) * size // 2),
                                      image=self.title_img, tags='title_img', anchor='center')

    def is_link(self, p1: Point, p2: Point) -> bool:
        if self.straight_link(p1, p2):
            return True
        if self.one_corner_link(p1, p2):
            return True
        if self.two_corner_link(p1, p2):
            return True
        return False

    def straight_link(self, p1: Point, p2: Point) -> bool:
        abs_distance: int = 0
        space_count: int = 0
        if p1.x == p2.x or p1.y == p2.y:
            if p1.x == p2.x and p1.y != p2.y:
                abs_distance = abs(p1.y - p2.y) - 1
                zf: int = -1 if p1.y - p2.y > 0 else 1
                for i in range(1, abs_distance + 1):
                    if self.m_map[(p1.y + i * zf) * self._attr.column + p1.x] == -10:
                        space_count += 1
                    else:
                        break
            elif p1.y == p2.y and p1.x != p2.x:
                abs_distance = abs(p1.x - p2.x) - 1
                zf: int = -1 if p1.x - p2.x > 0 else 1
                for i in range(1, abs_distance + 1):
                    if self.m_map[p1.y * self._attr.column + p1.x + i * zf] == -10:
                        space_count += 1
                    else:
                        break
            if space_count == abs_distance:
                return True
        return False

    def one_corner_link(self, p1: Point, p2: Point) -> bool:
        check_p1: Point = Point(p1.x, p2.y)
        check_p2: Point = Point(p2.x, p1.y)
        if self.m_map[check_p1.y * self._attr.column + check_p1.x] == -10:
            if self.straight_link(p1, check_p1) and self.straight_link(check_p1, p2):
                self.line_points.append(check_p1)
                return True
        if self.m_map[check_p2.y * self._attr.column + check_p2.x] == -10:
            if self.straight_link(p1, check_p2) and self.straight_link(check_p2, p2):
                self.line_points.append(check_p2)
                return True
        return False

    def two_corner_link(self, p1: Point, p2: Point) -> bool:
        for i in range(4):
            check_p1: Point = Point(p1.x, p1.y)
            if i == 3:
                check_p1.y += 1
                while (check_p1.y < self._attr.row
                       and self.m_map[check_p1.y * self._attr.column + check_p1.x] == -10):
                    self.line_points.append(check_p1)
                    if self.one_corner_link(check_p1, p2):
                        return True
                    else:
                        self.line_points.pop()
                    check_p1.y += 1
                if check_p1.y == self._attr.row:
                    if p2.y == self._attr.row - 1:
                        # print(check_p1.x, check_p1.y, '向下探测边界=>1型')
                        self.line_points.append(Point(p1.x, self._attr.row))
                        self.line_points.append(Point(p2.x, self._attr.row))
                        return True
                    check_p2: Point = Point(p2.x, self._attr.row - 1)
                    if (self.m_map[check_p2.y * self._attr.column + check_p2.x] == -10
                            and self.straight_link(check_p2, p2)):
                        self.line_points.append(Point(p1.x, self._attr.row))
                        self.line_points.append(Point(p2.x, self._attr.row))
                        return True
            elif i == 2:
                check_p1.x += 1
                while (check_p1.x < self._attr.column
                       and self.m_map[check_p1.y * self._attr.column + check_p1.x] == -10):
                    self.line_points.append(check_p1)
                    if self.one_corner_link(check_p1, p2):
                        return True
                    else:
                        self.line_points.pop()
                    check_p1.x += 1
                if check_p1.x == self._attr.column:
                    if p2.x == self._attr.column - 1:
                        # print(check_p1.x, check_p1.y, '向右探测边界=>1型')
                        self.line_points.append(Point(self._attr.column, p1.y))
                        self.line_points.append(Point(self._attr.column, p2.y))
                        return True
                    check_p2: Point = Point(self._attr.column - 1, p2.y)
                    if (self.m_map[check_p2.y * self._attr.column + check_p2.x] == -10
                            and self.straight_link(check_p2, p2)):
                        self.line_points.append(Point(self._attr.column, p1.y))
                        self.line_points.append(Point(self._attr.column, p2.y))
                        return True
            elif i == 1:
                check_p1.x -= 1
                while (check_p1.x >= 0
                       and self.m_map[check_p1.y * self._attr.column + check_p1.x] == -10):
                    self.line_points.append(check_p1)
                    if self.one_corner_link(check_p1, p2):
                        return True
                    else:
                        self.line_points.pop()
                    check_p1.x -= 1
                if check_p1.x == -1:
                    if p2.x == 0:
                        # print(check_p1.x, check_p1.y, '向左探测边界=>1型')
                        self.line_points.append(Point(-1, p1.y))
                        self.line_points.append(Point(-1, p2.y))
                        return True
                    check_p2: Point = Point(0, p2.y)
                    if (self.m_map[check_p2.y * self._attr.column + check_p2.x] == -10
                            and self.straight_link(check_p2, p2)):
                        self.line_points.append(Point(-1, p1.y))
                        self.line_points.append(Point(-1, p2.y))
                        return True
            else:
                check_p1.y -= 1
                while (check_p1.y >= 0
                       and self.m_map[check_p1.y * self._attr.column + check_p1.x] == -10):
                    self.line_points.append(check_p1)
                    if self.one_corner_link(check_p1, p2):
                        return True
                    else:
                        self.line_points.pop()
                    check_p1.y -= 1
                if check_p1.y == -1:
                    if p2.y == 0:
                        # print(check_p1.x, check_p1.y, '向上探测边界=>1型')
                        self.line_points.append(Point(p1.x, -1))
                        self.line_points.append(Point(p2.x, -1))
                        return True
                    check_p2: Point = Point(p2.x, 0)
                    if (self.m_map[check_p2.y * self._attr.column + check_p2.x] == -10
                            and self.straight_link(check_p2, p2)):
                        self.line_points.append(Point(p1.x, -1))
                        self.line_points.append(Point(p2.x, -1))
                        return True
        return False

    def fault_tolerant(self, event) -> None:
        pass

    def find_block(self, event) -> None:
        if self._attr.SECRET:
            if self.button['text'] == '结束游戏' and self.first_find_block == -1:
                b_fond: bool = False
                for i in range(len(self.m_map)):
                    if b_fond:
                        break
                    x = i % self._attr.column
                    y = i // self._attr.column
                    p1 = Point(x, y)
                    if self.m_map[y * self._attr.column + x] == -10:
                        continue
                    for j in range(i + 1, len(self.m_map)):
                        x2 = j % self._attr.column
                        y2 = j // self._attr.column
                        p2 = Point(x2, y2)
                        if (self.m_map[y2 * self._attr.column + x2] != -10
                                and self.is_same_block(p1, p2)):
                            if self.is_link(p1, p2):
                                b_fond = True
                                break
                if b_fond:
                    s = self._attr.BOX_SIZE
                    self.first_find_block = self.canvas1.create_rectangle(
                        p1.x * s + s // 2, p1.y * s + s // 2, p1.x * s + s + s // 2,
                        p1.y * s + s + s // 2, outline='orange', width=3)
                    self.second_find_block = self.canvas1.create_rectangle(
                        p2.x * s + s // 2, p2.y * s + s // 2, p2.x * s + s + s // 2,
                        p2.y * s + s + s // 2, outline='orange', width=3)
                    self.line_points.clear()

    def is_same_block(self, p1: Point, p2: Point) -> bool:
        if (self.m_map[p1.y * self._attr.column + p1.x]
                == self.m_map[p2.y * self._attr.column + p2.x]):
            return True
        return False

    def print_map(self) -> None:
        s: int = self._attr.BOX_SIZE
        for x in range(self._attr.column):
            for y in range(self._attr.row):
                if self.m_map[y * self._attr.column + x] != -10:
                    my_id = self.m_map[y * self._attr.column + x]
                    self.canvas1.create_image((x * s + s // 2, y * s + s // 2),
                                              image=self._attr.dict_pic[my_id],
                                              anchor='nw', tags='%02d-%02d' % (x, y))

    def draw_link_line(self, p1: Point, p2: Point) -> None:
        if len(self.line_points) == 0:
            return self.line_id.append(self.draw_line(p1, p2))
        if len(self.line_points) == 1:
            z: Point = self.line_points.pop()
            self.line_id.append(self.draw_line(p1, z))
            self.line_id.append(self.draw_line(p2, z))
        if len(self.line_points) == 2:
            z1: Point = self.line_points.pop()
            self.line_id.append(self.draw_line(p2, z1))
            z2: Point = self.line_points.pop()
            self.line_id.append(self.draw_line(z1, z2))
            self.line_id.append(self.draw_line(p1, z2))

    def draw_line(self, p1: Point, p2: Point) -> int:
        s = self._attr.BOX_SIZE
        return self.canvas1.create_line(p1.x * s + s, p1.y * s + s,
                                        p2.x * s + s, p2.y * s + s,
                                        width=2, fill='red')

    def delay_run(self) -> None:
        self.canvas1.delete(self.first_selected_block)
        self.canvas1.delete(self.second_selected_block)
        self.m_map[self.p1.y * self._attr.column + self.p1.x] = -10
        self.m_map[self.p2.y * self._attr.column + self.p2.x] = -10
        self.canvas1.delete('%02d-%02d' % (self.p1.x, self.p1.y))
        self.canvas1.delete('%02d-%02d' % (self.p2.x, self.p2.y))
        if self.first_find_block != -1:
            self.canvas1.delete(self.first_find_block)
            self.canvas1.delete(self.second_find_block)
            self.first_find_block = self.second_find_block = -1
        self.frist_selected_bool = False
        while self.line_id:
            self.canvas1.delete(self.line_id.pop())
        if all(map(lambda x: x == -10, self.m_map)):
            s = self._attr.BOX_SIZE
            self.title_img: Image.PhotoImage = ImageTk.PhotoImage(self._attr.tit_img.resize((
                s * int(self.w), s * int(self.w) // 2), Image.Resampling.LANCZOS))
            self.canvas1.create_image(((int(self.w) + 1) * s // 2, (int(self.h) + 1) * s // 2),
                                      image=self.title_img, tags='title_img', anchor='center')
            self.button.configure(text='开始游戏')

    def _cal_time(self, myfloat: float) -> str:
        m, s = divmod(myfloat, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def computing_time(self) -> None:
        if self.button['text'] == '结束游戏':
            second = datetime.now() - self.timer
            second = self._cal_time(second.seconds)
            self.lab_name.configure(text=second)
            self.after(1000, self.computing_time)


def theme_skin(theme_name: str, root: tk.Window) -> None:
    root.style.theme_use(theme_name)


def game_secret(root: tk.window) -> None:
    if dialogs.Querybox.get_string(
            prompt='请输入密码,将获取右键提示功能!\n密码1: 1314\n密码2: 9527\n密码3: 520',
            title="QQ学习群651689292", parent=root, initialvalue='9527', padding=(70, 35),
            position=(root.winfo_x() + root.winfo_width() // 2 - 150 - 75,
                      root.winfo_y() + root.winfo_height() // 2 - 75 - 75 // 2)) == '9527':
        AttrGame.SECRET = True


def resolution_power(resolv: int, root: tk.Window) -> None:
    abc = Messagebox.yesno(f"调整{resolv}%分辨率后,\n要关闭再打开游戏.\n您需要这么做吗?",
                           "连连看--by:散落于云海", False, root,
                           padding=(150, 75), anchor='center',
                           position=(root.winfo_x() + root.winfo_width() // 2 - 150 - 75,
                                     root.winfo_y() + root.winfo_height() // 2 - 75 - 75 // 2))
    if abc == NAME:
        with open(rf"{AttrGame.LOCAL_PATH}\resolution", mode='w') as f:
            f.write(str(resolv))


def game_cry_help(root: tk.Window) -> None:
    abc = Messagebox.yesno("当游戏无法通过时,\n可以消除1组相同方块.\n您需要这么做吗?",
                           "连连看--by:散落于云海", False, root,
                           padding=(150, 75), anchor='center',
                           position=(root.winfo_x() + root.winfo_width() // 2 - 150 - 75,
                                     root.winfo_y() + root.winfo_height() // 2 - 75 - 75 // 2))
    if abc == NAME:
        AttrGame.set_cry_help(True)
    else:
        AttrGame.set_cry_help(False)


def main(*args) -> None:
    global NAME
    NAME = args[1]
    try:
        with open(rf"{AttrGame.LOCAL_PATH}\size", mode='r') as f:
            AttrGame.set_box_size(int(f.read()))
    except FileNotFoundError:
        with open(rf"{AttrGame.LOCAL_PATH}\size", mode='w') as f:
            f.write(str(AttrGame.BOX_SIZE))

    root: tk.Window = tk.Window(args[0], themename='superhero')
    try:
        with open(rf"{AttrGame.LOCAL_PATH}\resolution", mode='r') as f:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            root.tk.call('tk', 'scaling', ScaleFactor / int(f.read()))
    except FileNotFoundError:
        pass
    menu: tk.Menu = tk.Menu(root)
    game_menu: tk.Menu = tk.Menu(menu)
    help_menu: tk.Menu = tk.Menu(menu)
    theme_menu: tk.Menu = tk.Menu(game_menu)
    resolution_menu: tk.Menu = tk.Menu(game_menu)
    menu.add_cascade(label='游戏设置', menu=game_menu, underline=1)
    menu.add_cascade(label='游戏帮助', menu=help_menu, underline=1)
    game_menu.add_cascade(label='皮肤主题', menu=theme_menu)
    game_menu.add_cascade(label='分辨率调整', menu=resolution_menu)
    help_menu.add_command(label='游戏密技', command=lambda: game_secret(root))
    help_menu.add_command(label='游戏求救', command=lambda: game_cry_help(root))
    game: Game = Game(root, args[0])
    game.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)
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


if __name__ == '__main__':
    # 英语环环境下,用'Yes',中文环境下用'确认'
    # Use 'yes' in English environment and'确认'in Chinese environment
    main("连连看", '确认')
