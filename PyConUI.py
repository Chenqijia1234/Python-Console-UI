"""

PyConUI.py
可提供完整的控制台UI体验

"""
import enum
import os
import os.path
import sys

# 屏幕大小
# SCREENSIZE = os.get_terminal_size()  句柄无效
# 工作目录
WORKPATH = os.getcwd()
# 解释器目录
PREFIXPATH = sys.prefix


class UILayout(enum.Enum):
    """
    UI对齐枚举
    LeftLayout:左对齐
    CentralLayout:居中
    RightLayout:右对齐
    """
    LeftLayout = 1
    CentralLayout = 2
    RightLayout = 3


class UIBaseWiget:
    """
    控制台窗体的基类
    add_compent:在窗体中增加组件
    clear_screen:清屏
    output:输出窗体，输出前自动清屏
    get_output_str:从各组件中获取窗体布局
    """
    Widgets = set()

    def __init__(self, width: int, height: int, name) -> None:
        UIBaseWiget.Widgets.add(self)
        self.compents = []
        self.width = width
        self.height = height
        self.name = name
        self.v_split_line = "-"*(self.width+2)

    def add_compent(self, compent: object) -> None:
        self.compents.append(compent)

    def clear_screen(self) -> None:
        os.system("cls")

    def output(self, mode) -> None:
        self.clear_screen()
        output_str: list[str] = self.get_output_str(mode)
        
        print(self.v_split_line)
        for i in output_str:
            print("|"+i+"|")
        print(self.v_split_line)

    def get_output_str(self, mode):
        output_str = []
        for compent in self.compents:
            for text in compent.show():
                if len(text) < self.width:
                    text_len = len(text)
                    white_text = self.width-text_len
                    if mode == None or mode == UILayout.LeftLayout:
                        text = text + " "*(self.width-text_len)
                    elif mode == UILayout.CentralLayout:
                        right_white = (white_text//2)*" "
                        left_white = (white_text-white_text//2)*" "
                        text = right_white+text+left_white
                    elif mode == UILayout.RightLayout:
                        left_white = (self.width-text_len)*" "
                        text = left_white+text
                    else:
                        raise ValueError
                elif len(text) == self.width:
                    pass
                elif len(text) > self.width:
                    text = text[:self.width]
                output_str.append(text)
            output_str.append(self.v_split_line[:-2])
        return output_str


class UIBaseCompent:
    """
    控制台窗体组件的基类

    """
    def __init__(self, parent_widget: UIBaseWiget,height: int, name) -> None:
        self.name = name
        self.parent_widget = parent_widget
        self.width = parent_widget.width
        self.height = height
        self.screen_str: str = ""
        self.screen: list[str] = []
        for i in range(height):
            self.screen.append("")

    def __str__(self):
        return f"{__class__}(name={self.name},parent={self.parent_widget})"

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, __name: str):
        return object.__getattribute__(self.widget, __name)

    def show(self):
        return self.screen

    def set_screen(self, data:list) -> None:
        if len(data)>self.height:
            self.screen = data[:self.height]
        else:
            for i in range(self.height-len(data)):
                data.append("")
            self.screen = data

    def get_screen(self):
        return self.screen

class SimpleTextCompent(UIBaseCompent):
    def __init__(self, parent_widget: UIBaseWiget, height: int, name) -> None:
        super().__init__(parent_widget, height, name)


class MainWindow(UIBaseWiget):
    def __init__(self, width: int, height: int, name,title:str="MainWindow") -> None:
        super().__init__(width, height, name)
        if width-2<len(title):
            raise ValueError
        self.title = title
        self.compents = [
            SimpleTextCompent(self,height-2,"Content"),
            SimpleTextCompent(self,3,"Tip")            
        ]
    def output(self, mode) -> str:
        self.clear_screen()
        output_str: list[str] = self.get_output_str(mode)
        v_split_line = "-"*(self.width+2)
        print(v_split_line)
        left_white = (self.width-len(self.title))//2-1
        right_white = self.width-left_white-len(self.title)
        print(f"|{left_white*' '}{self.title}{right_white*' '}",end="|\n")
        print(v_split_line)
        for i in output_str:
            print("|"+i+"|")
        print(v_split_line)
        return input(">>>")


if __name__ == "__main__":
    mainwindow = MainWindow(90,7,None)
    mainwindow.output(UILayout.CentralLayout)