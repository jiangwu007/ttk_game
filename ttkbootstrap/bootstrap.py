# -*- coding:utf-8 -*-
import ttkbootstrap as tk
from ttkbootstrap.dialogs import Messagebox
from typing import List, Union, Tuple, Optional
from ttkbootstrap.scrolled import ScrolledText

# 参考
# https://stackoverflow.com/questions/2922295/why-does-the-calculated-width-and-height-in-pixel-of-a-string-in-tkinter-differ
# https://stackoverflow.com/questions/7591294/how-to-create-a-self-resizing-grid-of-buttons-in-tkinter


class Ui(tk.Frame):
    def __init__(self, root: tk.Window, content: str) -> None:
        super().__init__(root, padding=10)
        self.bool_gaugeing: bool = False
        self.style: tk.Style = tk.Style()
        self.theme_names: List[str] = self.style.theme_names()

        self.theme_selection: tk.Frame = tk.Frame(
            self, padding=(10, 10, 10, 0))
        self.theme_selection.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)
        self.theme_selected: tk.Label = tk.Label(
            self.theme_selection, text='cyborg', font='-size 24 -weight bold')
        self.theme_selected.pack(side=tk.LEFT)
        self.lbl_theme: tk.Label = tk.Label(self.theme_selection, text='选择主题')
        self.cbo_theme: tk.Combobox = tk.Combobox(
            self.theme_selection, values=self.theme_names, textvariable=self.style.theme.name)
        self.cbo_theme.current(self.theme_names.index(self.style.theme.name))
        self.cbo_theme.pack(side=tk.RIGHT, padx=10)
        self.lbl_theme.pack(side=tk.RIGHT)
        self.cbo_theme.bind('<<ComboboxSelected>>', self.change_theme)
        tk.Separator(self).pack(fill=tk.X, pady=10, padx=10, expand=tk.NO)

        self.frame2: tk.Frame = tk.Frame(self, padding=5)
        # self.frame3: tk.Frame = tk.Frame(self, padding=5)
        self.frame3: tk.Panedwindow = tk.Panedwindow(self)
        self.frame3.pack(side=tk.LEFT, fill=tk.Y, pady=(5, 0))
        self.frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

        self.color_group: tk.Labelframe = tk.Labelframe(
            self.frame2, text='按钮颜色选项', padding=10)
        self.color_group.pack(fill=tk.X, side=tk.TOP)

        self.button_list: List[tk.Button] = []
        for x, color in enumerate(self.style.colors):
            cb: tk.Button = tk.Button(
                self.color_group, text=color, bootstyle=color)
            cb.grid(row=0, column=x, padx=5, sticky="we")
            self.button_list.append(cb)
        max_width = max(map(lambda x: x.winfo_reqwidth(), self.button_list))
        for x, _ in enumerate(self.button_list):
            self.color_group.columnconfigure(x, weight=1, minsize=max_width)

        self.rb_group: tk.Labelframe = tk.Labelframe(
            self.frame2, text='复选按钮与单选按钮', padding=10)
        self.rb_group.pack(fill=tk.X, pady=10, side=tk.TOP)
        self.button_list2: List[Union[tk.Checkbutton, tk.Radiobutton]] = []
        for i in range(8):
            if i < 4:
                abc = tk.Checkbutton(
                    self.rb_group, text=''.join(('多项选择', str(i + 1))))
                abc.grid(row=0, column=i, padx=5, sticky='we')
                if i <= 1:
                    abc.invoke()
                elif i == 3:
                    abc.configure(state=tk.DISABLED)
            else:
                abc = tk.Radiobutton(self.rb_group, text=''.join(
                    ('单选择', str(i - 3))), value=i - 3)
                abc.grid(row=0, column=i, padx=5, sticky='we')
                if i == 7:
                    abc.configure(state=tk.DISABLED)
                elif i == 4:
                    abc.invoke()
            self.rb_group.columnconfigure(i, weight=1)
            self.button_list2.append(abc)

        self.ttr_frame: tk.Frame = tk.Frame(self.frame2)
        # self.ttr_frame = tk.Panedwindow(self.frame2, orient=tk.HORIZONTAL)
        self.ttr_frame.pack(side=tk.TOP, pady=5, fill=tk.X, expand=tk.NO)
        table_data: List[Tuple[str, int]] = [
            ('中华人民共和国', 1),
            ('美利坚合众国', 2),
            ('越南社会主义共和国', 3),
            ('法兰西共和国', 4),
            ('希腊共和国', 5)
        ]
        self.tv: tk.Treeview = tk.Treeview(
            self.ttr_frame, columns=[0, 1], show=tk.HEADINGS, height=5)
        for row in table_data:
            self.tv.insert('', tk.END, values=row)
        self.tv.selection_set('I003')
        self.tv.heading(0, text='国家')
        self.tv.heading(1, text='人口排名')
        self.tv.column(0, width=250)
        self.tv.column(1, width=120, anchor=tk.CENTER)
        self.tv.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        # self.ttr_frame.add(self.tv)
        self.nb = tk.Notebook(self.ttr_frame)
        self.nb.pack(side=tk.LEFT, padx=(10, 0), fill=tk.BOTH, expand=tk.YES)
        # self.ttr_frame.add(self.nb)
        nb_text = '最是那一低头的温柔.\n像一朵水莲花不胜凉风的娇羞.\n道一声珍重，道一声珍重,\n那一声珍重里有蜜甜的忧愁——沙扬娜拉.'
        self.nb.add(tk.Label(self.nb, text=nb_text), text='选项卡1', sticky='nw')
        nb_text = '我是天空里的一片云.\n偶尔投影在你的波心.\n你不必惊异,更无须欢喜.\n在转瞬间就不见踪影.'
        self.nb.add(tk.Label(self.nb, text=nb_text), text='选项卡2')
        nb_text = '你我相逢在黑夜的海上.\n你有你的,我有我的方向.\n你记得也好,最好是忘掉,\n你我交汇时互放的光亮.'
        self.nb.add(tk.Label(self.nb, text=nb_text), text='选项卡3')

        self.pande: tk.Panedwindow = tk.Panedwindow(
            self.frame2, orient=tk.HORIZONTAL)
        self.txt: ScrolledText = ScrolledText(
            self.pande, height=5, width=50, autohide=True)
        self.txt.insert(tk.END, content)
        self.pande.add(self.txt)
        self.pande.pack(fill=tk.BOTH, expand=tk.YES)

        self.frame_inner = tk.Frame(self.pande)
        self.pande.add(self.frame_inner)
        self.scale: tk.Scale = tk.Scale(
            self.frame_inner, orient=tk.HORIZONTAL, value=75, from_=0, to=100)
        self.progress = tk.Progressbar(
            self.frame_inner, orient=tk.HORIZONTAL, mode='indeterminate')
        self.progress2 = tk.Progressbar(
            self.frame_inner, orient=tk.HORIZONTAL, value=75, bootstyle=(tk.SUCCESS, tk.STRIPED))
        self.meter = tk.Meter(
            self.frame_inner, metersize=150, amountused=66.6,
            subtext="圆环图表", bootstyle=tk.DANGER, interactive=True, stripethickness=10)
        self.sb = tk.Scrollbar(self.frame_inner, orient=tk.HORIZONTAL)
        self.sb.set(0.1, 0.9)
        self.sb2 = tk.Scrollbar(
            self.frame_inner, orient=tk.HORIZONTAL, bootstyle=(tk.INFO, tk.ROUND))
        self.sb2.set(0.1, 0.9)
        self.scale.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, pady=7, padx=20)
        self.progress.pack(side=tk.TOP, fill=tk.X,
                           expand=tk.YES, pady=7, padx=20)
        self.progress2.pack(side=tk.TOP, fill=tk.X,
                            expand=tk.YES, pady=7, padx=20)
        self.meter.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, pady=7, padx=20)
        self.sb.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, pady=7, padx=20)
        self.sb2.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, pady=7, padx=20)

        self.input_group = tk.Labelframe(
            self.frame3, text='信息输入控件', padding=(10, 5))
        self.frame3.add(self.input_group)
        # self.input_group.pack(fill=tk.X, side=tk.TOP)
        self.entry = tk.Entry(self.input_group)
        self.entry.pack(fill=tk.X, side=tk.TOP, ipadx=10, pady=5)
        self.entry.insert(tk.END, '请输入居民身份证')
        self.entry2 = tk.Entry(self.input_group)
        self.entry2.pack(fill=tk.X, ipadx=10, pady=5)
        self.entry2.insert(0, '请输入核酸检测数据')
        self.entry3 = tk.Entry(self.input_group, show="•")
        self.entry3.pack(fill=tk.X, ipadx=10, pady=5)
        self.entry3.insert(0, 'paasword95271314')
        self.spinbox = tk.Spinbox(self.input_group, from_=0, to=100)
        self.spinbox.pack(fill=tk.X, ipadx=10, pady=5)
        self.spinbox.set(66)
        self.date = tk.DateEntry(self.input_group)
        self.date.pack(fill=tk.X, ipadx=10, pady=5)
        self.gauge = tk.Floodgauge(
            self.input_group, mask='已经加载{}%', bootstyle=tk.DANGER)
        self.gauge.pack(pady=5, fill=tk.X)
        self.gauge.configure(value=35)

        self.btn_group = tk.Labelframe(self.frame3, text='按钮控件组')
        self.frame3.add(self.btn_group)
        # self.btn_group.pack(fill=tk.BOTH, pady=(10, 0), expand=tk.YES)
        self.btn1 = tk.Button(self.btn_group, text='点击开始',
                              command=self.gauge_start, bootstyle=tk.INSIDE)
        self.btn1.pack(fill=tk.X, pady=10, padx=10)
        self.btn1.focus_set()
        self.btn2 = tk.Button(self.btn_group, text='确定按钮',
                              bootstyle=tk.OUTLINE, command=self.open_from)
        self.btn2.pack(fill=tk.X, pady=10, padx=10)
        self.btn3 = tk.Button(self.btn_group, text='变色按钮',
                              bootstyle=tk.TOOLBUTTON, command=self.begin_1)
        self.btn3.pack(fill=tk.X, pady=10, padx=10)
        self.btn4 = tk.Button(self.btn_group, text='无色按钮',
                              bootstyle=(tk.LINK), command=self.begin_2)
        self.btn4.pack(fill=tk.X, pady=10, padx=10)
        self.btn5 = tk.Button(self.btn_group, text='复核按钮',
                              bootstyle=(tk.LINK), command=self.begin_3)
        self.btn5.pack(fill=tk.X, pady=10, padx=10)
        self.cb1 = tk.Checkbutton(self.btn_group, text="圆形按钮",
                                  bootstyle=(tk.SUCCESS, tk.ROUND, tk.TOGGLE))
        self.cb2 = tk.Checkbutton(
            master=self.btn_group, text="方形按钮", bootstyle=(tk.SQUARE, tk.TOGGLE))
        self.cb1.invoke()
        self.cb2.invoke()
        self.cb1.pack(anchor='se', side=tk.RIGHT, fill=tk.X, pady=5, padx=15)
        self.cb2.pack(anchor='sw', side=tk.LEFT, fill=tk.X, pady=5, padx=15)

    def gauge_start(self) -> None:
        if not self.bool_gaugeing:
            self.bool_gaugeing = True
            self.gauge.configure(value=0)
            self.after(100, self._gaugeing, 1)

    def _gaugeing(self, interval: int) -> None:
        if interval < 100:
            interval += 1
            self.gauge.configure(value=interval)
            return self.after(100, self._gaugeing, interval)
        self.gauge.configure(value=35)
        self.bool_gaugeing = False

    def change_theme(self, event) -> None:
        self.style.theme_use(self.cbo_theme.get())
        self.theme_selected.configure(text=self.cbo_theme.get())
        self.cbo_theme.selection_clear()

    def open_from(self) -> None:
        root = self.nametowidget(self.winfo_parent())
        top: tk.Toplevel = tk.Toplevel(root, resizable=(False, False))
        frame = tk.Frame(top)
        frame.pack()
        top.attributes('-topmost', True)
        lab_block: tk.Label = tk.Label(frame, text='身份证')
        entry_block: tk.Entry = tk.Entry(frame)
        entry_block.insert(0, '110101199003074979')
        lab_w: tk.Label = tk.Label(frame, text='体重')
        entry_w: tk.Entry = tk.Entry(frame)
        entry_w.insert(0, '132')
        lab_h: tk.Label = tk.Label(frame, text='身高')
        entry_h: tk.Entry = tk.Entry(frame)
        but_yes: tk.Button = tk.Button(top, text='确定', command=lambda: self.top_yes(
            top, entry_block.get(), entry_h.get(), entry_w.get()))
        but_no: tk.Button = tk.Button(
            top, text='取消', command=lambda: self.top_close(top))
        lab_block.grid(column=0, row=0, padx=10, pady=(15, 5))
        entry_block.grid(column=1, row=0, padx=10, pady=(15, 5))
        lab_w.grid(column=0, row=1, padx=10, pady=5)
        entry_w.grid(column=1, row=1, padx=10, pady=5)
        lab_h.grid(column=0, row=2, padx=10, pady=5)
        entry_h.grid(column=1, row=2, padx=10, pady=5)
        but_no.pack(side=tk.RIGHT, padx=35, pady=15, fill=tk.X, ipadx=15)
        but_yes.pack(side=tk.LEFT, padx=35, pady=15, fill=tk.X, ipadx=15)
        # top.place_window_center()

        top.update()
        x1, y1 = top.winfo_width(), top.winfo_height()
        w, h = root.winfo_width() // 2, root.winfo_height() // 2
        x, y = root.winfo_x() + w - x1 // 2, root.winfo_y() + h - y1 // 2
        top.geometry(f'+{x}+{y}')

    def top_close(self, top: tk.Toplevel) -> None:
        top.destroy()

    def top_yes(self, top: tk.Toplevel, s: Optional[str], w: Optional[str], h: Optional[str]) -> None:
        try:
            x, y, z = int(w), int(h), int(s)
            print(x, y, z)
            top.destroy()
        except ValueError:
            pass

    def begin_1(self):
        if self.btn3['text'] == '变色按钮':
            self.progress.start()
            self.btn3.configure(text='变色铵钮')
        else:
            self.progress.stop()
            self.btn3.configure(text='变色按钮')

    def begin_2(self):
        if self.btn4['text'] == '无色按钮':
            self.progress2.start()
            self.btn4.configure(text='无色铵钮')
        else:
            self.progress2.stop()
            self.btn4.configure(text='无色按钮')
            self.progress2.configure(value=75)

    def begin_3(self) -> None:
        top: tk.Window = self.nametowidget(self.winfo_parent())
        Messagebox.ok('核酸检查完毕。您的身体非常健康。\n请再接再厉，定期检查！',
                      'Tkinter示例', True, self,
                      position=(top.winfo_x() + top.winfo_width() // 2 - 143,
                                top.winfo_y() + top.winfo_height() // 2 - 90),
                      anchor='s'
                      )


def main(*args) -> None:
    content = '''优美胜于丑陋。
显式胜于隐式。
简单胜于复杂。
复杂胜于难懂。
扁平胜于嵌套。
间隔胜于紧凑。
可读性应当被重视。
尽管实用性会打败纯粹性，特例也不能凌驾于规则之上。
除非明确地使其沉默，错误永远不应该默默地溜走。
面对不明确的定义，拒绝猜测的诱惑。
用一种方法，最好只有一种方法来做一件事。
虽然一开始这种方法并不是显而易见的，但谁叫你不是Python之父呢。
做比不做好，但立马去做有时还不如不做。
如果实现很难说明，那它是个坏想法。
如果实现容易解释，那它有可能是个好想法。
命名空间是个绝妙的想法，让我们多多地使用它们吧！
'''
    root: tk.Window = tk.Window(title=args[0], themename='cyborg')
    app: Ui = Ui(root, content)
    app.pack(fill=tk.BOTH, expand=tk.YES)
    root.place_window_center()
    root.mainloop()


if __name__ == '__main__':
    # pip install ttkbootstrap
    main('Tkinter示例--by:散落于云海')
