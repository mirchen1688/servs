import sys
import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services import UserService, AppService, init_db  # 正常导入

class AppStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Store 管理端")

        # 用户数据列表
        self.user_listbox = tk.Listbox(root)
        self.user_listbox.pack(pady=10)
        self.load_users()

        # 应用管理
        self.app_frame = tk.Frame(root)
        self.app_frame.pack(pady=10)

        tk.Label(self.app_frame, text="应用名称:").grid(row=0, column=0)
        self.app_name_entry = tk.Entry(self.app_frame)
        self.app_name_entry.grid(row=0, column=1)

        tk.Label(self.app_frame, text="应用描述:").grid(row=1, column=0)
        self.app_description_entry = tk.Entry(self.app_frame)
        self.app_description_entry.grid(row=1, column=1)

        tk.Label(self.app_frame, text="下载链接:").grid(row=2, column=0)
        self.app_url_entry = tk.Entry(self.app_frame)
        self.app_url_entry.grid(row=2, column=1)

        tk.Label(self.app_frame, text="应用图标:").grid(row=3, column=0)
        self.icon_url_entry = tk.Entry(self.app_frame)
        self.icon_url_entry.grid(row=3, column=1)
        tk.Button(self.app_frame, text="选择图标", command=self.select_icon).grid(row=3, column=2)

        tk.Label(self.app_frame, text="应用截图:").grid(row=4, column=0)
        self.screenshots_entry = tk.Entry(self.app_frame)
        self.screenshots_entry.grid(row=4, column=1)
        tk.Button(self.app_frame, text="选择截图", command=self.select_screenshots).grid(row=4, column=2)

        tk.Label(self.app_frame, text="所需积分:").grid(row=5, column=0)
        self.points_required_entry = tk.Entry(self.app_frame)
        self.points_required_entry.grid(row=5, column=1)

        tk.Button(self.app_frame, text="添加应用", command=self.add_app).grid(row=6, column=0)
        tk.Button(self.app_frame, text="删除应用", command=self.delete_app).grid(row=6, column=1)

        # 应用列表
        self.app_listbox = tk.Listbox(root)
        self.app_listbox.pack(pady=10)
        self.load_apps()

    def select_icon(self):
        """选择应用图标"""
        file_path = filedialog.askopenfilename(title="选择应用图标", filetypes=[("图片文件", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.icon_url_entry.delete(0, tk.END)
            self.icon_url_entry.insert(0, file_path)

    def select_screenshots(self):
        """选择应用截图"""
        file_paths = filedialog.askopenfilenames(title="选择应用截图", filetypes=[("图片文件", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            self.screenshots_entry.delete(0, tk.END)
            self.screenshots_entry.insert(0, json.dumps(file_paths))  # 将截图路径列表转为 JSON 字符串

    def add_app(self):
        """添加应用"""
        name = self.app_name_entry.get()
        description = self.app_description_entry.get()
        url = self.app_url_entry.get()
        icon_url = self.icon_url_entry.get()
        screenshots = json.loads(self.screenshots_entry.get()) if self.screenshots_entry.get() else []
        points_required = int(self.points_required_entry.get()) if self.points_required_entry.get() else 10
        if name and description and url and icon_url and screenshots:
            AppService.add_app(name, description, url, icon_url, screenshots, points_required)
            self.load_apps()
            messagebox.showinfo("成功", "应用添加成功")
        else:
            messagebox.showerror("错误", "请填写完整信息")

    def delete_app(self):
        """删除应用"""
        selection = self.app_listbox.curselection()
        if selection:
            app_id = int(self.app_listbox.get(selection[0]).split(",")[0].split(": ")[1])
            AppService.delete_app(app_id)
            self.load_apps()
            messagebox.showinfo("成功", "应用删除成功")
        else:
            messagebox.showerror("错误", "请选择一个应用")

    def load_users(self):
        """加载用户数据"""
        users = UserService.get_all_users()
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, f"ID: {user['user_id']}, 用户名: {user['username']}, 积分: {user['points']}")

    def load_apps(self):
        """加载应用数据"""
        apps = AppService.get_all_apps()
        self.app_listbox.delete(0, tk.END)
        for app in apps:
            self.app_listbox.insert(tk.END, f"ID: {app['app_id']}, 名称: {app['name']}, 描述: {app['description']}, 所需积分: {app['points_required']}")

if __name__ == "__main__":
    try:
        init_db()  # 初始化数据库
        root = tk.Tk()
        app = AppStoreApp(root)
        root.mainloop()
    except Exception as e:
        print(f"程序崩溃: {str(e)}")