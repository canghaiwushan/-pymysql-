from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymysql
from PIL import Image,ImageTk

#添加logo为背景图
page = 0	#全局变量page用于存储当前显示信息的页码
who = 0		#全局变量who用于区别身份

def button2_clicked():
	global who
	who = 1
	page = 0
	display_current_page()
 
data_in = None

#用于显示所有信息
def display(i,data):
	global data_in
	data_in = data
	listbox1.delete(0,END)
	listbox2.delete(0,END)
	listbox3.delete(0,END)
	listbox4.delete(0,END)
	listbox5.delete(0,END)
	listbox6.delete(0,END)
	for d in data:
		if i==1:
			listbox1.insert(END,'员工')
		else:
			listbox1.insert(END,'经理')
		listbox2.insert(END, d[0])
		listbox3.insert(END, d[1])
		listbox4.insert(END, d[2])
		listbox5.insert(END, d[3])
		listbox6.insert(END, d[4])

#用于显示下一页的信息	
def display_next_page():
	global page, who, mode
	if mode == 1:
		tkinter.messagebox.showwarning(title='warning',message='已经是最后一页！')
		return None
	page+= 1
	if who == 1:
		cursor.execute("select * from employee limit %d,%d" % (page*20, page*20+20))
		data = cursor.fetchall()
		display(who, data)
	else:
		cursor.execute("select * from manager limit %d,%d" % (page*20, page*20+20))
		data = cursor.fetchall()
		display(who, data)
 
def button_next_page_clicked():
	display_next_page()

#用于显示前一页的信息
def display_previous_page():
	global page, who, mode
	if mode == 1:
		tkinter.messagebox.showwarning(title='warning',message='已经是第一页！')
		return None
	page -= 1
	page = max(page, 0)
	if who == 1:
		cursor.execute("select * from employee limit %d,%d" % (page*20, page*20+20))
		data = cursor.fetchall()
		display(who, data)
	else:
		cursor.execute("select * from manager limit %d,%d" % (page*20, page*20+20))
		data = cursor.fetchall()
		display(who, data)

#用于选择显示何种信息(employee/manager)
def display_current_page():
	global page, who, mode , using_name
	page = page
	if mode == 0:
		if who == 1:
			cursor.execute("select * from employee limit %d,%d" % (page*20, page*20+20))
			data = cursor.fetchall()
			display(who, data)
		else:
			cursor.execute("select * from manager limit %d,%d" % (page*20, page*20+20))
			data = cursor.fetchall()
			display(who, data)
	elif mode == 1:
		cursor.execute('select dept from manager where id ={}'.format(int(using_name)))
		manager_dept=cursor.fetchall()
		real_dept=str(manager_dept[0][0])
		#print('select * from employee where dept = "%s"'%(real_dept))
		cursor.execute('select * from employee where dept = "%s"'%(real_dept))
		data=cursor.fetchall()
		display(who,data)
		#cursor.execute()
      

def button_manager_clicked():
	global who, page
	who = 0
	page = 0
	display_current_page()
 
#listbox为空格数目
#实现删除功能
def button_delete_clicked():
	indexs1 = listbox1.curselection()
	indexs2 = listbox2.curselection()
	indexs3 = listbox3.curselection()
	indexs4 = listbox4.curselection()
	indexs5 = listbox5.curselection()
	indexs6 = listbox6.curselection()
	
	index = -1
	if len(indexs1) > 0:
		index = indexs1[0]
	elif len(indexs2) > 0:
		index = indexs2[0]
	elif len(indexs3) > 0:
		index = indexs3[0]
	elif len(indexs4) > 0:
		index = indexs4[0]
	elif len(indexs5) > 0:
		index = indexs5[0]
	elif len(indexs6) > 0:
		index = indexs6[0]
 
	if index == -1:
		tkinter.messagebox.showerror("Error","未选择要删除的数据")
 
	delete_id = listbox2.get(index,index)
	delete_who = listbox1.get(index,index)
	if delete_who[0] == "员工":
		cursor.execute("delete from employee where id = %d" % int(delete_id[0]))
		database.commit()
		display_current_page()
	else:
		cursor.execute("delete from manager where id = %d" % int(delete_id[0]))
		database.commit()
		display_current_page()
	#print(delete_id)	

#实现添加信息功能
def button_add_clicked():
	global mode,using_name
	index = combobox_2.current()
	if index < 0:
		tkinter.messagebox.showerror("Error","请选择身份")
		return None
	
	add_id = entry4.get().strip()
	if len(add_id)<=0:
		tkinter.messagebox.showerror("Error","请输入工号")
		return None
	try:
		add_id = int(add_id)
	except Exception as e:
		tkinter.messagebox.showerror("Error","输入工号错误")
		return None
 
	add_name = entry5.get().strip()
	if len(add_name)<=0:
		tkinter.messagebox.showerror("Error","请输入名字")
		return None
 
	add_gender = combobox_3.current()
	if add_gender < 0:
		tkinter.messagebox.showerror("Error","请选择性别")
		return None
 
	add_age = entry7.get().strip()
	if len(add_age)<=0:
		tkinter.messagebox.showerror("Error","请输入年龄")
		return None
	try:
		add_age = int(add_age)
	except Exception as e:
		tkinter.messagebox.showerror("Error","年龄输入错误")
		return None
 
	add_dept = entry8.get().strip()
	if mode == 1:
		cursor.execute('select dept from manager where id ={}'.format(int(using_name)))
		manager_dept=cursor.fetchall()
		real_dept=str(manager_dept[0][0])
		if real_dept != add_dept:
			tkinter.messagebox.showerror("Error","抱歉，您没有该部门的操作权限！")
			return None
	if len(add_dept)<=0:
		tkinter.messagebox.showerror("Error","请输入部门")
		return None
	if index == 0:
		cursor.execute('select * from employee where id = %d' % add_id)
		data = cursor.fetchall()
		if len(data) > 0:
			tkinter.messagebox.showerror("Error","该id已存在")
			return None
		cursor.execute('insert into employee(id,name,gender,age,dept) values(%d,"%s","%s",%d,"%s")' % (add_id, add_name, "男" if add_gender == 0 else "女", add_age, add_dept))
		database.commit()
		display_current_page()
	else:
		cursor.execute('select * from manager where id = %d' % add_id)
		data = cursor.fetchall()
		if len(data) > 0:
			tkinter.messagebox.showerror("Error","该id已存在")
			return None
		cursor.execute('insert into manager(id,name,gender,age,dept) values(%d,"%s","%s",%d,"%s")' % (add_id, add_name, "男" if add_gender == 0 else "女", add_age, add_dept))
		database.commit()
		display_current_page()

'''_____________________________________________________________________________'''
 
#连接database，解决编码问题
#程序执行后在mysql中进行查询会发现中文无法正常显示，这是因为在安装mysql时未选择Ｍysql Server Instance Config Wizard，而机房电脑可以显示正常
database = pymysql.connect(host='localhost', user='root',password='123456',database='employee_system',charset='gb2312')
cursor = database.cursor()
if database.open == False:
	raise Exception("数据库未连接，请检查数据库服务是否启动")
cursor.execute('use employee_system')
 
mode = -1
#实现登录功能
using_name=""
def button_login_clicked():
	global mode
	global using_name
	index = combobox_login.current()
	username_input = entry1.get().strip()
	using_name=username_input
	password_input = entry2.get().strip()
	print(index, username_input, password_input)
	if index == -1:
		tkinter.messagebox.showerror("错误","请选择你的登陆身份")
	elif len(username_input) == 0 or len(password_input) == 0:
		tkinter.messagebox.showerror("错误","请输入用户名和密码")
	else:
		if index == 0:
			cursor.execute('select * from admin where user_name = "%s" and password = "%s"' % (username_input,password_input))
			if (len(cursor.fetchall()) > 0):
				print("已成功登录")
				myWindow.destroy()
				mode = 0
    
			else:
				tkinter.messagebox.showerror("错误","用户名或密码错误")
		if index == 1:
			cursor.execute('select * from manager_login where user_name = "%s" and password = "%s"' % (username_input,password_input))
			if (len(cursor.fetchall()) > 0):
				print("已成功登录")
				myWindow.destroy()
				mode = 1
			else:
				tkinter.messagebox.showerror("错误","用户名或密码错误")
		if index == 2:
			cursor.execute('select * from employee_login where user_name = "%s" and password = "%s"' % (username_input,password_input))
			if (len(cursor.fetchall()) > 0):
				print("已成功登录")
				myWindow.destroy()
				mode = 2
			else:
				tkinter.messagebox.showerror("错误","用户名或密码错误")
 

#实现修改功能
def button_change_clicked():
	indexs1 = listbox1.curselection()
	indexs2 = listbox2.curselection()
	indexs3 = listbox3.curselection()
	indexs4 = listbox4.curselection()
	indexs5 = listbox5.curselection()
	indexs6 = listbox6.curselection()
	print(indexs1,indexs2,indexs3,indexs4,indexs5,indexs6)
	index = -1
	if len(indexs1) > 0:
		index = indexs1[0]
	elif len(indexs2) > 0:
		index = indexs2[0]
	elif len(indexs3) > 0:
		index = indexs3[0]
	elif len(indexs4) > 0:
		index = indexs4[0]
	elif len(indexs5) > 0:
		index = indexs5[0]
	elif len(indexs6) > 0:
		index = indexs6[0]
	if index == -1:
		tkinter.messagebox.showerror("错误","请选择要修改的数据")
	change_id = listbox2.get(index,index)[0]
	change_who = listbox1.get(index,index)[0]
 
	change_name = entry11.get().strip()
	change_age = entry22.get().strip()
	change_grade = entry33.get().strip()
	index = combobox_22.current()
 
	if len(change_name) > 0:
		if (change_who == "员工"):
			try:
				change_id = int(change_id)
			except Exception as e:
				tkinter.messagebox.showerror("错误","输入错误")
				return None
			cursor.execute('update employee set name = "%s" where id = %d' % (change_name, change_id))
			database.commit()
			display_current_page()
		else:
			try:
				change_id = int(change_id)
			except Exception as e:
				tkinter.messagebox.showerror("错误","输入错误")
				return None
			cursor.execute('update manager set name = "%s" where id = %d' % (change_name, change_id))
			database.commit()	
			display_current_page()
 
	if len(change_age) > 0:
		if (change_who == "员工"):
			try:
				change_age = int(change_age)
			except Exception as e:
				tkinter.messagebox.showerror("错误","输入错误")
				return None
			cursor.execute('update employee set age = "%s" where id = %d' % (int(change_age), int(change_id)))
			database.commit()
			display_current_page()
		else:
			try:
				change_age = int(change_age)
			except Exception as e:
				tkinter.messagebox.showerror("错误","输入错误")
				return None
			cursor.execute('update manager set age = "%s" where id = %d' % (int(change_age), int(change_id)))
			database.commit()	
			display_current_page()
	if len(change_grade) > 0:
		if (change_who == "员工"):
			try:
				change_grade = change_grade
			except Exception as e:
				tkinter.messagebox.showerror("错误","输入错误")
				return None
			cursor.execute('update employee set dept = "%s" where id = %d' % (change_grade, int(change_id)))
			database.commit()
			display_current_page()
		else:
			try:
				change_grade = change_grade
			except Exception as e:
				tkinter.messagebox.showerror("错误","输入错误")
				return None
 
			cursor.execute('update manager set dept = "%s" where id = %d' % (change_grade, int(change_id)))
			database.commit()	
			display_current_page()
	if index != -1:
		if (change_who == "员工"):
			cursor.execute('update employee set gender = "%s" where id = %d' % ("男" if index==0 else "女", int(change_id)))
			database.commit()
			display_current_page()
		else:
			cursor.execute('update manager set gender = "%s" where id = %d' % ("男" if index==0 else "女", int(change_id)))
			database.commit()	
			display_current_page()
 

#实现搜索功能
def button_search_clicked():
	global using_name
	index = combobox_1.current()
	content = entry1.get().strip()
 
	if index == -1:
		tkinter.messagebox.showerror("错误","请选择搜索依据")
		return None
	if len(content) == 0:
		tkinter.messagebox.showerror("错误","请输入搜索内容")
		return None
	if index == 0:
		try:
			search_id = int(content)
		except Exception as e:
			tkinter.messagebox.showerror("Error","请输入正确id")
			return None
		if mode == 0 :
			cursor.execute('select * from employee where id = %d' % search_id)
			data1 = cursor.fetchall()
			cursor.execute('select * from manager where id = %d' % search_id)
			data2 = cursor.fetchall()
		else:
			cursor.execute('select dept from manager where id ={}'.format(int(using_name)))
			manager_dept=cursor.fetchall()
			real_dept=str(manager_dept[0][0])
			cursor.execute('select * from (select * from employee where dept = "%s") as new_emp where new_emp.id = %d'%(real_dept,search_id))
			data1=cursor.fetchall()
			data2=cursor.fetchall()
		
		listbox1.delete(0,END)
		listbox2.delete(0,END)
		listbox3.delete(0,END)
		listbox4.delete(0,END)
		listbox5.delete(0,END)
		listbox6.delete(0,END)
		for d in data1:
			listbox1.insert(END,'员工')
			listbox2.insert(END, d[0])
			listbox3.insert(END, d[1])
			listbox4.insert(END, d[2])
			listbox5.insert(END, d[3])
			listbox6.insert(END, d[4])
 
		for d in data2:
			listbox1.insert(END,'经理')
			listbox2.insert(END, d[0])
			listbox3.insert(END, d[1])
			listbox4.insert(END, d[2])
			listbox5.insert(END, d[3])
			listbox6.insert(END, d[4])
	if index == 1:
		if mode == 0:
			cursor.execute('select * from employee where name = "%s"' % content)
			data1 = cursor.fetchall()
			cursor.execute('select * from manager where name = "%s"' % content)
			data2 = cursor.fetchall()
		else:
			cursor.execute('select dept from manager where id ={}'.format(int(using_name)))
			manager_dept=cursor.fetchall()
			real_dept=str(manager_dept[0][0])
			#必须为嵌套查询的内部表设置别名(as new_emp)
			cursor.execute('select * from (select * from employee where dept = "%s") as new_emp where new_emp.name = "%s"'%(real_dept,content))
			data1=cursor.fetchall()
			data2=cursor.fetchall()
		
		listbox1.delete(0,END)
		listbox2.delete(0,END)
		listbox3.delete(0,END)
		listbox4.delete(0,END)
		listbox5.delete(0,END)
		listbox6.delete(0,END)
		for d in data1:
			listbox1.insert(END,'员工')
			listbox2.insert(END, d[0])
			listbox3.insert(END, d[1])
			listbox4.insert(END, d[2])
			listbox5.insert(END, d[3])
			listbox6.insert(END, d[4])
 
		for d in data2:
			listbox1.insert(END,'经理')
			listbox2.insert(END, d[0])
			listbox3.insert(END, d[1])
			listbox4.insert(END, d[2])
			listbox5.insert(END, d[3])
			listbox6.insert(END, d[4])

def get_image(file_name,width,height):
	im=Image.open(file_name).resize((width,height))
	return ImageTk.PhotoImage(im)

#界面设置
#初始化Tk()
myWindow = Tk()
#设置标题
myWindow.title('员工信息管理系统登陆页面')
myWindow.geometry('1080x600')

#插入背景图片
canvans_myWindow=Canvas(myWindow,width=720,height=385)
im_root=get_image('D:\数据库课程设计\湖南工程学院员工信息管理系统.png',720,385)
canvans_myWindow.create_image(400,200,image=im_root)
canvans_myWindow.pack()

#创建一个标签，显示文本
Label(myWindow, text="用户名:",font=('Arial 12 bold'),width=10,height=1).place(relx = 0.10, rely = 0.75)
Label(myWindow, text="密码:",font=('Arial 12 bold'),width=10,height=1).place(relx = 0.10, rely = 0.85)
Label(myWindow, text="登陆身份:",font=('Arial 12 bold'),width=10,height=1).place(relx = 0.10, rely = 0.65)
 
combobox_login = ttk.Combobox(myWindow, values = ['管理员','经理','员工'], width=17)
combobox_login.place(relx = 0.45, rely = 0.65)
 
button_login = Button(text = '登陆',relief = 'raised', command = button_login_clicked)
button_login.place(relx = 0.5, rely = 0.92)

entry1=Entry(myWindow)
entry2=Entry(myWindow,show='*')
entry1.place(relx = 0.45, rely = 0.75)
entry2.place(relx = 0.45, rely = 0.85)
#进入消息循环
myWindow.mainloop()


#设置员工操作页面
def employee_click():
	content = entry111.get()
	if len(content) == 0:
		tkinter.messagebox.showerror("Error","请输入新密码！")
	
	cursor.execute('update employee_login set password= "%s" where user_name="%s"' % (content,using_name))
	database.commit()
	tkinter.messagebox.showinfo(title='修改密码',message="密码修改完成，请牢记新密码！")

#设置经理修改密码功能
def manager_click():
    content= entry_update.get()
    if len(content) == 0:
        tkinter.messagebox.showerror("Error","请输入新密码！")
    
    cursor.execute('update manager_login set password= "%s" where user_name="%s"' % (content,using_name))
    database.commit()
    tkinter.messagebox.showinfo(title='修改密码',message="密码修改完成，请牢记新密码！")
	

#设置管理员操作页面
if mode == 0:
	print("已进入系统")
	page = 0
	who = 1
	#初始化Tk()
	myWindow = Tk()
	#设置标题
	myWindow.title('管理员界面')
	myWindow.geometry('1280x640')
	#创建一个标签，显示文本
	Label(myWindow, text="搜索选项:",font=('Arial 12 bold'),width=10,height=1).grid(column = 0, row = 0)
	combobox_1 = ttk.Combobox(myWindow, values = ['按工号搜索','按姓名搜索'], width=17)
	combobox_1.grid(column = 1, row = 0)
 
	Label(myWindow, text="搜索关键字:",font=('Arial 12 bold'),width=10,height=1).grid(column = 2, row = 0)
	entry1=Entry(myWindow)
	entry1.grid(column = 3, row = 0)
	#将各功能按键与函数绑定
	button1 = Button(text = '搜索',relief = 'raised', command = button_search_clicked)
	button1.grid(column = 4, row = 0)
 
	button2 = Button(text = '显示所有员工信息',relief = 'raised', command = button2_clicked)
	button2.grid(column = 5, row = 0)
 
	button3 = Button(text = '显示所有经理信息',relief = 'raised', command = button_manager_clicked)
	button3.grid(column = 6, row = 0)
 
	Label(myWindow, text=" ",font=('Arial 12 bold'),width=4,height=1).grid(column = 0, row = 1)
 
	Label(myWindow, text="身份",font=('Arial 12 bold'),width=10,height=1).grid(column = 0, row = 2)
	listbox1 = Listbox(myWindow,height=20,selectmode="browse",font=('Arial 12 bold'))
	listbox1.grid(column = 0, row = 3)
 
 
	Label(myWindow, text="工号",font=('Arial 12 bold'),width=10,height=1).grid(column = 1, row = 2)
	listbox2 = Listbox(myWindow,height=20,selectmode="browse",font=('Arial 12 bold'))
	listbox2.grid(column = 1, row = 3)
 
 
	Label(myWindow, text="姓名",font=('Arial 12 bold'),width=10,height=1).grid(column = 2, row = 2)
	listbox3 = Listbox(myWindow,height=20,width = 10,selectmode="browse",font=('Arial 12 bold'))
	listbox3.grid(column = 2, row = 3)
 
 
	Label(myWindow, text="性别",font=('Arial 12 bold'),width=10,height=1).grid(column = 3, row = 2)
	listbox4 = Listbox(myWindow,height=20,width = 5,selectmode="browse",font=('Arial 12 bold'))
	listbox4.grid(column = 3, row = 3)
 
 
	Label(myWindow, text="年龄",font=('Arial 12 bold'),width=10,height=1).grid(column = 4, row = 2)
	listbox5 = Listbox(myWindow,height=20,width = 8,selectmode="browse",font=('Arial 12 bold'))
	listbox5.grid(column = 4, row = 3)
 
 
	Label(myWindow, text="部门",font=('Arial 12 bold'),width=10,height=1).grid(column = 5, row = 2)
	listbox6 = Listbox(myWindow,height=20,width = 8,selectmode="browse",font=('Arial 12 bold'))
	listbox6.grid(column = 5, row = 3)
 
 
	Label(myWindow, text='身份无法修改',font=('Arial 12 bold'),width=10,height=1).grid(column = 0, row = 4)
	Label(myWindow, text='工号无法修改',font=('Arial 12 bold'),width=10,height=1).grid(column = 1, row = 4)
	entry11=Entry(myWindow)
	entry11.grid(column = 2, row = 4)
	combobox_22 = ttk.Combobox(myWindow, values = ['男','女'], width=17)
	combobox_22.grid(column = 3, row = 4)
	entry22=Entry(myWindow)
	entry22.grid(column = 4, row = 4)
	entry33=Entry(myWindow)
	entry33.grid(column = 5, row = 4)
	button4 = Button(text = '修改',relief = 'raised', command = button_change_clicked)
	button4.grid(column = 6, row = 4)
 
 
 
	combobox_2 = ttk.Combobox(myWindow, values = ['员工','经理'], width=17)
	combobox_2.grid(column = 0, row = 5)
 
	entry4=Entry(myWindow)
	entry4.grid(column = 1, row = 5)
	entry5=Entry(myWindow)
	entry5.grid(column = 2, row = 5)
	combobox_3 = ttk.Combobox(myWindow, values = ['男','女'], width=17)
	combobox_3.grid(column = 3, row = 5)
	entry7=Entry(myWindow)
	entry7.grid(column = 4, row = 5)
	entry8=Entry(myWindow)
	entry8.grid(column = 5, row = 5)
 
	button5 = Button(text = '添加',relief = 'raised', command = button_add_clicked)
	button5.grid(column = 6, row = 5)
 
	button6 = Button(text = '删除',relief = 'raised', command = button_delete_clicked)
	button6.grid(column = 6, row = 6)
 
	button7 = Button(text = '上一页',relief = 'raised', command = display_previous_page)
	button7.grid(column = 3, row = 7)
 
	button8 = Button(text = '下一页',relief = 'raised', command = button_next_page_clicked)
	button8.grid(column = 4, row = 7)

	#进入消息循环
	myWindow.mainloop()
 

#设置经理操作页面
elif mode == 1:
	print("已成功登录")
	page = 0
	who = 1
	#初始化Tk()
	myWindow = Tk()
	#设置标题
	myWindow.title('经理界面')
	myWindow.geometry('1280x650')
	#创建一个标签，显示文本
	Label(myWindow, text="搜索选项:",font=('Arial 12 bold'),width=10,height=1).grid(column = 0, row = 0)
	combobox_1 = ttk.Combobox(myWindow, values = ['按工号搜索','按姓名搜索'], width=17)
	combobox_1.grid(column = 1, row = 0)
 
	Label(myWindow, text="搜索关键字:",font=('Arial 12 bold'),width=10,height=1).grid(column = 2, row = 0)
	entry1=Entry(myWindow)
	entry1.grid(column = 3, row = 0)
 
	button1 = Button(text = '搜索',relief = 'raised', command = button_search_clicked)
	button1.grid(column = 4, row = 0)
 
	button2 = Button(text = '显示我的部门员工信息',relief = 'raised', command = button2_clicked)
	button2.grid(column = 5, row = 0)
 
 
	Label(myWindow, text=" ",font=('Arial 12 bold'),width=4,height=1).grid(column = 0, row = 1)
 
	Label(myWindow, text="身份",font=('Arial 12 bold'),width=10,height=1).grid(column = 0, row = 2)
	listbox1 = Listbox(myWindow,height=20,selectmode="browse",font=('Arial 12 bold'))
	listbox1.grid(column = 0, row = 3)
 
 
	Label(myWindow, text="工号",font=('Arial 12 bold'),width=10,height=1).grid(column = 1, row = 2)
	listbox2 = Listbox(myWindow,height=20,selectmode="browse",font=('Arial 12 bold'))
	listbox2.grid(column = 1, row = 3)
 
 
	Label(myWindow, text="姓名",font=('Arial 12 bold'),width=10,height=1).grid(column = 2, row = 2)
	listbox3 = Listbox(myWindow,height=20,width = 10,selectmode="browse",font=('Arial 12 bold'))
	listbox3.grid(column = 2, row = 3)
 
 
	Label(myWindow, text="性别",font=('Arial 12 bold'),width=10,height=1).grid(column = 3, row = 2)
	listbox4 = Listbox(myWindow,height=20,width = 5,selectmode="browse",font=('Arial 12 bold'))
	listbox4.grid(column = 3, row = 3)
 
 
	Label(myWindow, text="年龄",font=('Arial 12 bold'),width=10,height=1).grid(column = 4, row = 2)
	listbox5 = Listbox(myWindow,height=20,width = 8,selectmode="browse",font=('Arial 12 bold'))
	listbox5.grid(column = 4, row = 3)
 
 
	Label(myWindow, text="部门",font=('Arial 12 bold'),width=10,height=1).grid(column = 5, row = 2)
	listbox6 = Listbox(myWindow,height=20,width = 8,selectmode="browse",font=('Arial 12 bold'))
	listbox6.grid(column = 5, row = 3)
 
 
	Label(myWindow, text='身份无法修改',font=('Arial 12 bold'),width=10,height=1).grid(column = 0, row = 4)
	Label(myWindow, text='工号无法修改',font=('Arial 12 bold'),width=10,height=1).grid(column = 1, row = 4)
	entry11=Entry(myWindow)
	entry11.grid(column = 2, row = 4)
	combobox_22 = ttk.Combobox(myWindow, values = ['男','女'], width=17)
	combobox_22.grid(column = 3, row = 4)
	entry22=Entry(myWindow)
	entry22.grid(column = 4, row = 4)
	entry33=Entry(myWindow)
	entry33.grid(column = 5, row = 4)
	button4 = Button(text = '修改',relief = 'raised', command = button_change_clicked)
	button4.grid(column = 6, row = 4)
 
 
 
	combobox_2 = ttk.Combobox(myWindow, values = ['员工'], width=17)
	combobox_2.grid(column = 0, row = 5)
 
	entry4=Entry(myWindow)
	entry4.grid(column = 1, row = 5)
	entry5=Entry(myWindow)
	entry5.grid(column = 2, row = 5)
	combobox_3 = ttk.Combobox(myWindow, values = ['男','女'], width=17)
	combobox_3.grid(column = 3, row = 5)
	entry7=Entry(myWindow)
	entry7.grid(column = 4, row = 5)
	entry8=Entry(myWindow)
	entry8.grid(column = 5, row = 5)
 
	button5 = Button(text = '添加',relief = 'raised', command = button_add_clicked)
	button5.grid(column = 6, row = 5)
 
	button6 = Button(text = '删除',relief = 'raised', command = button_delete_clicked)
	button6.grid(column = 6, row = 6)
 
	button7 = Button(text = '上一页',relief = 'raised', command = display_previous_page)
	button7.grid(column = 3, row = 7)
 
	button8 = Button(text = '下一页',relief = 'raised', command = button_next_page_clicked)
	button8.grid(column = 4, row = 7)

	Label(myWindow, text='请输入想更改的新密码：',font=('Arial 12 bold'),height=1).grid(column = 0, row = 7)
	entry_update=Entry(myWindow)
	entry_update.grid(column=1,row=7)
	button_update=Button(text='修改密码',relief='raised',command=manager_click).grid(column=1,row=8)

	cursor.execute("select * from manager where id = %d" % int(using_name))
	data=cursor.fetchall()
	Label(myWindow,text='我的信息如下：',font=('Arial 12 bold'),height=1).place(relx=0.8,rely=0.06)
	myinfo1="工号：%d"%(data[0][0])
	myinfo2="姓名：%s"%(data[0][1])
	myinfo3="性别：%s"%(data[0][2])
	myinfo4="年龄：%d"%(data[0][3])
	myinfo5="职位：%s经理"%(data[0][4])
	Label(myWindow,text=myinfo1,font=('Arial 12 bold'),height=1).place(relx=0.8,rely=0.12)
	Label(myWindow,text=myinfo2,font=('Arial 12 bold'),height=1).place(relx=0.8,rely=0.18)
	Label(myWindow,text=myinfo3,font=('Arial 12 bold'),height=1).place(relx=0.8,rely=0.24)
	Label(myWindow,text=myinfo4,font=('Arial 12 bold'),height=1).place(relx=0.8,rely=0.30)
	Label(myWindow,text=myinfo5,font=('Arial 12 bold'),height=1).place(relx=0.8,rely=0.36)

	#进入消息循环
	myWindow.mainloop()
 


#设置员工页面
elif mode == 2:
	myWindow = Tk()
	#设置标题
	myWindow.title('员工界面')
	myWindow.geometry('720x580')
 
	#只显示自己的信息
	cursor.execute("select * from employee where id = %d" % int(using_name))
	data = cursor.fetchall()
	#Label(myWindow, text=" ",font=('Arial 12 bold'),width=4,height=1).grid(column = 0, row = 0)
	Label(myWindow,text='我的信息如下：',font=('Arial 12 bold'),height=1).place(relx=0.45,rely=0.23)
	myinfo1="工号：%d"%(data[0][0])
	myinfo2="姓名：%s"%(data[0][1])
	myinfo3="性别：%s"%(data[0][2])
	myinfo4="年龄：%d"%(data[0][3])
	myinfo5="部门：%s"%(data[0][4])
	Label(myWindow,text=myinfo1,font=('Arial 12 bold'),height=1).place(relx=0.45,rely=0.3)
	Label(myWindow,text=myinfo2,font=('Arial 12 bold'),height=1).place(relx=0.45,rely=0.37)
	Label(myWindow,text=myinfo3,font=('Arial 12 bold'),height=1).place(relx=0.45,rely=0.44)
	Label(myWindow,text=myinfo4,font=('Arial 12 bold'),height=1).place(relx=0.45,rely=0.51)
	Label(myWindow,text=myinfo5,font=('Arial 12 bold'),height=1).place(relx=0.45,rely=0.58)
	Label(myWindow, text='请输入想更改的新密码：',font=('Arial 12 bold'),height=1).grid(column = 1, row = 6)
	
	entry111=Entry(myWindow)
	entry111.grid(column = 2, row = 6)
 
	button111 = Button(text = '修改密码',relief = 'raised', command = employee_click)
	button111.grid(column = 2, row = 8)

	myWindow.mainloop()
	
