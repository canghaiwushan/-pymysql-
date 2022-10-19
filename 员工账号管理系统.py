#账号管理系统只对管理员开放
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymysql
from PIL import Image,ImageTk

#连接数据库
database=pymysql.connect(host='localhost',user='root',password='123456',database='employee_system',charset='gb2312')
cursor=database.cursor()

def get_image(file_name,width,height):
    im=Image.open(file_name).resize((width,height))
    return ImageTk.PhotoImage(im)

mode=0

def button_admin_login():
    global mode
    username_input = entry1.get().strip()
    password_input = entry2.get().strip()
    cursor.execute('select * from admin where user_name = "%s" and password = "%s"' % (username_input,password_input))
    if (len(cursor.fetchall()) > 0):
        print("已成功登录")
        mynewwin.destroy()
        mode=1
    else:
    	tkinter.messagebox.showerror("错误","用户名或密码错误")

mynewwin=Tk()
mynewwin.title('员工账号管理系统登录页面')
mynewwin.geometry('1080x600')

canvans_myWindow=Canvas(mynewwin,width=720,height=400)
im_root=get_image('D:\数据库课程设计\湖南工程学院员工账号管理系统.png',720,400)
canvans_myWindow.create_image(400,200,image=im_root)
canvans_myWindow.pack()

Label(mynewwin, text="管理员账号:",font=('Arial 12 bold'),width=10,height=1).place(relx = 0.10, rely = 0.75)
Label(mynewwin, text="管理员密码:",font=('Arial 12 bold'),width=10,height=1).place(relx = 0.10, rely = 0.85)

button_login = Button(text = '登陆',relief = 'raised', command = button_admin_login)
button_login.place(relx = 0.5, rely = 0.92)

entry1=Entry(mynewwin)
entry2=Entry(mynewwin,show='*')
entry1.place(relx = 0.45, rely = 0.75)
entry2.place(relx = 0.45, rely = 0.85)
#进入消息循环
mynewwin.mainloop()

def button_insert_account_emp():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('select * from employee_login where user_name ="%s"'%(user_name))
    data=cursor.fetchall()
    if len(data)>0:
        tkinter.messagebox.showerror(title='Error',message='该账号已存在！')
        return None
    cursor.execute('insert into employee_login values("%s","%s")' % (user_name,password))
    database.commit()
    tkinter.messagebox.showinfo(title='新增员工账号密码',message='新增员工账号成功！')

def button_update_account_emp():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('update employee_login set password="%s" where user_name="%s"' % (password,user_name))
    database.commit()
    tkinter.messagebox.showinfo(title='修改员工账号密码',message='修改员工账号密码成功！')

def button_delete_account_emp():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('delete from employee_login where user_name="%s"'%(user_name))
    database.commit()
    tkinter.messagebox.showinfo(title='删除员工账号密码',message='删除员工账号密码成功！')


def button_insert_account_ma():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('select * from manager_login where user_name ="%s"'%(user_name))
    data=cursor.fetchall()
    if len(data)>0:
        tkinter.messagebox.showerror(title='Error',message='该账号已存在！')
        return None
    cursor.execute('insert into manager_login values("%s","%s")'%(user_name,password))
    database.commit()
    tkinter.messagebox.showinfo(title='新增经理账号密码',message='新增经理账号密码成功！')
    
def button_update_account_ma():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('update manager_login set password="%s" where user_name="%s"' % (password,user_name))
    database.commit()
    tkinter.messagebox.showinfo(title='修改经理账号密码',message='修改经理账号密码成功！')

def button_delete_account_ma():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('delete from manager_login where user_name="%s"'%(user_name))
    database.commit()
    tkinter.messagebox.showinfo(title='删除经理账号密码',message='删除经理账号密码成功！')

def button_update_account_my():
    user_name=entry_user.get().strip()
    password=entry_pass.get().strip()
    print(user_name,password)
    cursor.execute('update admin set password="%s" where user_name="%s"' % (password,user_name))
    database.commit()
    tkinter.messagebox.showinfo(title='修改管理员密码',message='修改管理员密码成功，请您牢记新密码！')

if mode==1:
    print("已进入系统")
    mynewwin=Tk()
    mynewwin.title('账号管理系统')
    mynewwin.geometry('720x520')
    
    #各个窗体效果
    Label(mynewwin, text=" ",font=('Arial 12 bold'),width=4,height=1).grid(column = 0, row = 0)
    Label(mynewwin, text="账号：",font=('Arial 12 bold'),width=10,height=1).grid(column=0,row=1)
    entry_user=Entry(mynewwin)
    entry_user.grid(column=1,row=1)


    Label(mynewwin, text="密码：",font=('Arial 12 bold'),width=10,height=1).grid(column=2,row=1)
    entry_pass=Entry(mynewwin)
    entry_pass.grid(column=3,row=1)

    
    #Label(mynewwin, text=" ",font=('Arial 12 bold'),width=4,height=1).grid(column = 0, row = 1)
    
    button_insert_emp=Button(mynewwin,text='新增员工账号密码',relief='raised',command=button_insert_account_emp)
    button_insert_emp.place(relx=0.3,rely=0.2)
    
    button_update_emp=Button(mynewwin,text='修改员工账号密码',relief='raised',command=button_update_account_emp)
    button_update_emp.place(relx=0.5,rely=0.2)
    
    button_delete_emp=Button(mynewwin,text='删除员工账号密码',relief='raised',command=button_delete_account_emp)
    button_delete_emp.place(relx=0.7,rely=0.2)
    
    #Label(mynewwin, text=" ",font=('Arial 12 bold'),width=4,height=1).grid(column = 0, row = 2)
    
    button_insert_ma=Button(mynewwin,text='新增经理账号密码',relief='raised',command=button_insert_account_ma)
    button_insert_ma.place(relx=0.3,rely=0.4)
    
    button_update_ma=Button(mynewwin,text='修改经理账号密码',relief='raised',command=button_update_account_ma)
    button_update_ma.place(relx=0.5,rely=0.4)
    
    button_delete_ma=Button(mynewwin,text='删除经理账号密码',relief='raised',command=button_delete_account_ma)
    button_delete_ma.place(relx=0.7,rely=0.4)

    button_update_my=Button(mynewwin,text='修改管理员密码',relief='raised',command=button_update_account_my)
    button_update_my.place(relx=0.75,rely=0.04)

    mynewwin.mainloop()
    
