# 俄罗斯方块·五年重构  
**从“能跑”到“专业”**  
![tetris.png](https://s2.loli.net/2022/09/08/WFaMpre2dsI9H3D.png)

---

## 📖 项目背景

五年前的作品，当我重新打开这个项目，它依然躺在硬盘角落。这一次，我不只让它跑起来，更要让它专业。

**重构目标**：
- ✅ 彻底解耦 UI 与逻辑  
- ✅ 跨平台标准化配置存储  
- ✅ 消除阻塞，实现流畅动画  
- ✅ 类型注解，提升可维护性  
- ✅ 保留五年前的“数学巧思”——**复数旋转**

---

## 🛠 技术栈

| 领域         | 工具/库                          |
|--------------|----------------------------------|
| 语言         | Python 3.8+                     |
| GUI 框架     | tkinter / ttkbootstrap（皮肤）  |
| 类型检查     | typing, TypeVar, Protocol      |
| 跨平台路径   | os, sys, pathlib               |
| 数据结构     | deque, Counter, List, Dict     |
| 动画驱动     | `after` 分帧                   |

---

## 🎯 核心特性

### 🧩 模块化设计
```
AttrGame         → 全局配置（方块尺寸、速度等级、分数表）
Game             → 主窗口、游戏流程、事件处理
Shape            → 方块数据定义、颜色、预置形状
Current_Shape    → 当前活动方块，继承 Shape，实现移动/旋转/碰撞
```

### 🔄 旋转算法：复数乘法的数学映射
五年前的小聪明，如今依然骄傲：
```python
I = 1j
logic_coords = [complex((c[0]-min_x)/size, (c[1]-min_y)/size) for c in coords]
rotated = [z * I for z in logic_coords]
```
将二维坐标视为复数，乘以 `1j` 即逆时针旋转 90° —— 简洁、优雅、零依赖。

### ⚡ 非阻塞消除行动画（2026 重构核心）
**原罪**：`time.sleep(0.02) + .update()` → 主线程卡死，窗口无法响应。  
**救赎**：`after` 分帧动画，全程零阻塞。

```python
def _remove_complete_lines(self, callback):
    # ... 检测完整行 ...
    self._animating = True
    self.after(20, lambda: self._do_clear(callback, complete_lines))
```
动画期间自动屏蔽键盘输入，动画结束后通过回调更新分数、生成新块。

---

## 📦 跨平台配置存储（2026 重构核心）

五年前：
```python
with open(rf"{path[0]}\tetris", 'w') as f
```
❌ Windows 硬编码，Linux/macOS 直接崩溃。

现在：
```python
def get_appdata_dir(app_name="AFTTetris"):
    if sys.platform == "win32":    return os.path.join(os.environ['APPDATA'], app_name)
    elif sys.platform == "darwin": return os.path.expanduser(f"~/Library/Application Support/{app_name}")
    else:                         return os.path.join(os.environ.get('XDG_CONFIG_HOME', '~/.config'), app_name)
```
✅ 配置文件自动存入：
- Windows: `%APPDATA%\AFTTetris\`
- macOS:   `~/Library/Application Support/AFTTetris/`
- Linux:   `~/.config/AFTTetris/`

**从此告别“在我电脑上能跑”。**

---

## 🧠 类型注解：给 Python 装上安全带

五年后，Python 的类型系统已足够成熟。我为整个项目补全了注解：

```python
class Edge(Generic[V]): ...
class Graph(Generic[V]): ...
ShapeTuple = Tuple[int, list, Tuple[int,int], ...]
```
配合 `mypy` 可静态检查，维护信心大增。

---

## 🚀 如何运行

### 环境要求
- Python 3.8+
- `tkinter`（通常内置）
- `ttkbootstrap`（可选，用于皮肤切换）

```bash
pip install ttkbootstrap
```

### 启动游戏
```bash
python tetris.py
```

### 配置文件位置
首次运行会自动在系统标准目录下创建 `AFTTetris` 文件夹，包含：
- `tetris`      – 存储当前方块大小
- `resolution`  – 存储 DPI 缩放比例
- `history.txt` – 历史最高分

---

## 🔭 未来展望

1. **单元测试**  
   将游戏板状态剥离为纯逻辑类 `TetrisBoard`，用 `pytest` 测试碰撞、消除、得分逻辑。

2. **网格状态数组**  
   抛弃 `canvas.find_overlapping` 的实时查询，改用二维数组维护固定方块，渲染器只做镜像绘制，性能可提升 10 倍以上。

3. **踢墙（Wall Kick）**  
   为旋转加入标准偏移试探，手感向专业级看齐。

4. **音效与动画特效**  
   消除行增加粒子效果，支持自定义皮肤。

---

## 💬 结语

五年，足够让一个青涩的“代码堆砌者”成长为开始思考**架构、可维护性、用户体验**的开发者。  
这个俄罗斯方块，是我编程路上的一个锚点——它提醒我：**能跑不是终点，专业才是。**

感谢你看到这里。  
如果你对这个项目感兴趣，欢迎 **Star / Fork**，一起让经典永不过时。

---

**项目地址**：[GitHub - AFTTetris](https://github.com/jiangwu007/ttk_game)
**授权协议**：MIT

---

*2026 年 2 月 · 重构笔记*