import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class App:
    def __init__(self, master):
        self.notebook = ttk.Notebook(master)
        self.frame1 = tk.Frame(master)
        self.frame2 = tk.Frame(master)
        self.bu1 = tk.Button(self.frame1, text='添加数据', command=self.add_row)
        self.bu1.grid(row=0, column=0)
        self.bu2 = tk.Button(self.frame1, text='读取数据', command=self.read_csv)
        self.bu2.grid(row=0, column=1)
        self.bu3 = tk.Button(self.frame1, text='删除数据', command=self.delete_row)
        self.bu3.grid(row=0, column=2)
        self.bu4 = tk.Button(self.frame1, text='修改数据', command=self.update_row)
        self.bu4.grid(row=0, column=3)
        self.bu5 = tk.Button(self.frame1, text='保存数据', command=self.save_csv)
        self.bu5.grid(row=0, column=4)
        self.buttonlist = []
        self.table = ttk.Treeview(self.frame1, columns=[ '姓名', '英语', '数学', '物理'])
        self.table.grid(rowspan=5, column=2, columnspan=3)
        self.entrylist = []
        for i, col in enumerate([ '姓名', '英语', '数学', '物理']):
            self.table.column(f"{i}", width=120, minwidth=50)
            self.table.heading(f"{i}", text=col, anchor=tk.W)
            self.label = tk.Label(self.frame1, text=col)
            self.label.grid(row=i + 1, column=0, columnspan=1)
            self.entry = tk.Entry(self.frame1)
            self.entry.grid(row=i + 1, column=1, columnspan=1)
            self.entrylist.append(self.entry)
        self.bu6 = tk.Button(self.frame2, text='绘制', command=self.draw_bar)
        self.bu6.grid()
        self.notebook.add(self.frame1, text='子窗体1')
        self.notebook.add(self.frame2, text='子窗体2')
        self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.sortbutton =  tk.Button(self.frame1, text='总分排序', command=self.sort)
        self.sortbutton.grid(row=0, column=5)

    def sort(self):
        if not hasattr(self, 'df'):
            return
        self.newdf = self.df.copy()
        self.newdf['总分'] = self.newdf['英语'] + self.newdf['数学'] + self.newdf['物理']
        self.newdf = self.newdf.sort_values(by='总分', ascending=False)
        self.newdf.to_csv('total.csv', index=False, encoding='utf-8-sig')

    def add_row(self):
        if not hasattr(self, 'df'):
            return
        valuelist = []
        for item in self.entrylist:
            valuelist.append(item.get())
        count = len(self.table.get_children())
        self.table.insert("", count, text=count, values=valuelist)
        self.df.loc[count] = valuelist
        print(self.df)

    def save_csv(self):
        if not hasattr(self, 'df'):
            return
        self.df.reset_index().to_csv('score.csv', index=False, encoding='utf-8-sig')

    def read_csv(self):
        self.df = pd.read_csv('score.csv',index_col=0, encoding='utf-8-sig')
        self.show_table()

    def show_table(self):
        if not hasattr(self, 'df'):
            return
        for children in self.table.get_children():
            self.table.delete(children)
        for i, line in self.df.iterrows():
            self.table.insert("", i, text=i, values=(line['姓名'], line['英语'], line['数学'], line['物理']))

    def delete_row(self):
        if not hasattr(self, 'df'):
            return
        for item in self.table.selection():
            self.df = self.df.drop(self.table.item(item)['text']).reset_index(drop=True)
            self.df['英语'] = self.df['英语'].astype(float)
            self.df['数学'] = self.df['数学'].astype(float)
            self.df['物理'] = self.df['物理'].astype(float)
            self.table.delete(item)
        self.show_table()

    def update_row(self):
        if not hasattr(self, 'df'):
            return
        for item in self.table.selection():
            valuelist = []
            for i, entry in enumerate(self.entrylist):
                if i == 0:
                    valuelist.append(entry.get())
                else:
                    valuelist.append(float(entry.get()))
            self.table.item(item, values=valuelist)
            self.df.loc[self.table.item(item)['text']] = valuelist
            self.df['英语'] = self.df['英语'].astype(float)
            self.df['数学'] = self.df['数学'].astype(float)
            self.df['物理'] = self.df['物理'].astype(float)

    def draw_bar(self):
        if not hasattr(self, 'df'):
            return
        drawPic = Figure(figsize=(5, 4), dpi=100)
        drawPic_canvas = FigureCanvasTkAgg(drawPic, master=self.frame2)
        drawPic_canvas.get_tk_widget().grid(row=1, columns=1, columnspan=5,rowspan=5)
        drawPic_a = drawPic.add_subplot(111)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.data = self.df.set_index('姓名', drop=True).mean(axis=1)
        drawPic_a.bar(self.data.index, self.data.astype(float))
        drawPic_canvas.draw()



if __name__ == '__main__':
    root = tk.Tk()
    root.title('notebook_test')
    # root.iconbitmap('fa.ico') #设置左上角小图标
    root.geometry('1200x600+400+300')
    App(root)
    root.mainloop()
