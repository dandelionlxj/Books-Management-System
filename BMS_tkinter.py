# -*- coding=utf-8 -*-
import mysql.connector
import datetime
from tkinter import *
from tkinter import messagebox

db = None


def connectdb():
    '''
    连接数据库
    '''
    print('connect to mysql...')
    try:

        # 打开数据库连接
        global db
        db = mysql.connector.connect(user="root", passwd="980507", database="library", use_unicode=True)
        print('Connect successfully!')
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        sys.exit()
    return db


def addbook():
    '''
    增加书籍
    '''
    add_book_window = Toplevel(manager_gui)
    add_book_window.title('Add Book')
    add_book_window.geometry('500x300')

    Label(add_book_window, text='书名:').place(x=50, y=50)
    Label(add_book_window, text='书类型:').place(x=50, y=90)

    name_input = StringVar()
    type_input = StringVar()
    Entry(add_book_window, textvariable=name_input).place(x=160, y=50)
    Entry(add_book_window, textvariable=type_input).place(x=160, y=90)

    def handle():
        name = name_input.get()
        type = type_input.get()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql1 = "SELECT * FROM books"
        # 执行SQL语句
        cursor.execute(sql1)
        n = len(cursor.fetchall())
        sql1 = 'select id from books; '
        cursor.execute(sql1)
        s = cursor.fetchall()
        sql = 'select name from books where name="%s";' % (name)
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0 and result[0][0] == name:
            messagebox.showerror(message='该书已存在')
        else:
            # SQL 插入语句
            sql = 'INSERT INTO books(id,name,type,status,borrowtimes)VALUES ("%d","%s","%s","未借出","%d");' % (
                s[n - 1][0] + 1, name, type, 0)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            messagebox.showinfo(message='添加书籍成功')
            add_book_window.destroy()

    Button(add_book_window, text='提交', command=handle).place(x=170, y=130)

    add_book_window.mainloop()


def borrowbook():
    '''
    借书
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    borrowbook_window = Toplevel(reader)
    borrowbook_window.title('Borrow book')
    borrowbook_window.geometry('500x300')

    Label(borrowbook_window, text='借的书名:').place(x=50, y=50)
    Label(borrowbook_window, text='姓名:').place(x=50, y=90)
    Label(borrowbook_window, text='性别：:').place(x=50, y=130)
    Label(borrowbook_window, text='专业:').place(x=50, y=170)

    var_bookname = StringVar()
    Entry(borrowbook_window, textvariable=var_bookname).place(x=160, y=50)
    var_name = StringVar()
    Entry(borrowbook_window, textvariable=var_name).place(x=160, y=90)
    var_sex = StringVar()
    Entry(borrowbook_window, textvariable=var_sex).place(x=160, y=130)
    var_sp = StringVar()
    Entry(borrowbook_window, textvariable=var_sp).place(x=160, y=170)

    def confirm():
        name = var_bookname.get()
        sql = 'select status,borrowtimes,borrowtime,id from books where name="%s";' % (name)
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            messagebox.showerror(message='没有该书籍')
        elif result[0][0] == '已借出':
            messagebox.showerror(message='该书已借出')
        else:
            rname = var_name.get()
            rsex = var_sex.get()
            rspeciality = var_sp.get()
            sql = 'insert into readers(name,sex,speciality,id,bookname,borrowtime) values ("%s","%s","%s","%d","%s","%s");' % (
                rname, rsex, rspeciality, result[0][3], name, datetime.date.today())
            cursor.execute(sql)
            sql1 = 'update books set status="%s",borrowtimes="%d",borrowtime="%s" where name="%s";' % (
                '已借出', result[0][1] + 1, datetime.date.today(), name)
            cursor.execute(sql1)
            db.commit()
            messagebox.showinfo(message='成功借书')
            borrowbook_window.destroy()

    Button(borrowbook_window, text='借书', command=confirm).place(x=170, y=210)
    borrowbook_window.mainloop()


def returnbook():
    '''
    还书
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    returnbook_window = Toplevel(reader)
    returnbook_window.title('Return Book')
    returnbook_window.geometry('500x300')

    Label(returnbook_window, text='书名:').place(x=50, y=50)

    var_name = StringVar()
    Entry(returnbook_window, textvariable=var_name).place(x=160, y=50)

    def return_confirm():
        name = var_name.get()
        sql = 'select status from books where name="%s";' % (name)
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            messagebox.showerror(message='这里没有这本书，你还错地方了')
        elif result[0][0] == '未借出':
            messagebox.showerror(message='无人借该书，你还错地方了')
        else:
            sql1 = 'update readers set returntime="%s" where bookname="%s";' % (datetime.date.today(), name)
            cursor.execute(sql1)
            sql = 'update books set status="%s" where name="%s";' % ('未借出', name)
            cursor.execute(sql)
            db.commit()
            messagebox.showinfo(message='成功还书')
            returnbook_window.destroy()

    Button(returnbook_window, command=return_confirm, text='还书').place(x=170, y=130)
    returnbook_window.mainloop()


def deletebook():
    '''
    删书
    '''
    deletebook_window = Toplevel()
    deletebook_window.title('Deletebook')
    deletebook_window.geometry('500x300')

    Label(deletebook_window, text='删除的书名:').place(x=50, y=50)

    var_name = StringVar()
    Entry(deletebook_window, textvariable=var_name).place(x=160, y=50)

    def delete_confirm():

        def delete():
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            name = var_name.get()
            sql = 'select name from books where name="%s";' % (name)
            cursor.execute(sql)
            s = cursor.fetchall()
            if len(s) == 0:
                messagebox.showerror(message='没有此书')
            else:
                sql = 'select status from books where name="%s";' % (name)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result[0][0] == '已借出':
                    messagebox.showerror(message='该书已借出,不能删除')
                else:
                    sql1 = 'delete from books where name="%s";' % (name)
                    cursor.execute(sql1)
                    db.commit()
                    messagebox.showinfo(message='成功删除该书籍')
                    deletebook_window.destroy()

        confirm = messagebox.askyesno(title='confirm', message='确定删除这本书吗？')
        if confirm:
            delete()

    Button(deletebook_window, command=delete_confirm, text='删除').place(x=170, y=130)
    deletebook_window.mainloop()


def searchreader():
    '''
    查询读者
    '''
    cursor = db.cursor()

    searchreader_window = Toplevel(manager_gui)
    searchreader_window.title('search reader_info')
    searchreader_window.geometry('500x300')

    Label(searchreader_window, text='姓名:').place(x=50, y=50)
    Label(searchreader_window, text='专业:').place(x=50, y=90)

    var_name = StringVar()
    Entry(searchreader_window, textvariable=var_name).place(x=160, y=50)

    var_speciality = StringVar()
    Entry(searchreader_window, textvariable=var_speciality, ).place(x=160, y=90)

    def search():
        name = var_name.get()
        speciality = var_speciality.get()
        sql = 'select * from readers where name ="%s" and speciality="%s";' % (name, speciality)
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            messagebox.showerror(message='该读者没有借阅任何书')
        else:
            printreaders(result)

    Button(searchreader_window, text='查询', command=search).place(x=170, y=130)
    searchreader_window.mainloop()


def deletereader():
    '''
    删除读者
    '''
    cursor = db.cursor()
    deletereader_window = Toplevel(manager_gui)
    deletereader_window.title('Delete Reader')
    deletereader_window.geometry('500x300')

    Label(deletereader_window, text='读者名:').place(x=50, y=50)
    Label(deletereader_window, text='专业:').place(x=50, y=90)

    name_input = StringVar()
    sepicality_input = StringVar()
    Entry(deletereader_window, textvariable=name_input).place(x=160, y=50)
    Entry(deletereader_window, textvariable=sepicality_input).place(x=160, y=90)

    def delete_confirm():

        def delete():
            name = name_input.get()
            speciality = sepicality_input.get()
            sql1 = 'select returntime from readers where name="%s" and speciality="%s";' % (name, speciality)
            cursor.execute(sql1)
            result = cursor.fetchall()
            returntime = []
            s = 0
            if len(result) == 0:
                messagebox.showerror(message='没有该读者的信息')
            else:
                for row in result:
                    returntime.append(row[0])
                for i in range(len(returntime)):
                    if returntime[i] == None:  # 如果没有归还时间，证明有书还没还
                        s += 1
                if s == 0:  # 所有书都还了，可以删除该读者
                    sql = 'delete from readers where name="%s";' % (name)
                    cursor.execute(sql)
                    db.commit()
                    messagebox.showinfo(message='删除成功')
                    deletereader_window.destroy()
                else:
                    messagebox.showerror(message='该读者还有书没还，不能删除')

        confirm = messagebox.askyesno(title='confirm', message='确定删除该读者的信息吗？')
        if confirm:
            delete()

    Button(deletereader_window, command=delete_confirm, text='删除').place(x=170, y=130)
    deletereader_window.mainloop()


def searchbook():
    cursor = db.cursor()
    try:
        now = manager_gui
        searchbook_window = Toplevel(now)
    except:
        now = reader
        searchbook_window = Toplevel(now)
    finally:
        searchbook_window.title('searchbook_window')
        searchbook_window.geometry('500x300')

        def use_name():
            use_name_gui = Toplevel(now)
            use_name_gui.title('use name to search')
            use_name_gui.geometry('500x300')

            Label(use_name_gui, text='书名:').place(x=50, y=50)

            var_name = StringVar()
            Entry(use_name_gui, textvariable=var_name).place(x=160, y=50)

            def search():
                name = var_name.get()
                sql = 'select * from books where name="%s";' % (name)
                cursor.execute(sql)
                a = cursor.fetchall()
                if len(a) == 0:
                    messagebox.showerror(message='该书不存在')
                else:
                    printbooks(a)

            Button(use_name_gui, command=search, text='查找').place(x=170, y=130)
            use_name_gui.mainloop()

        def use_type():
            use_type_gui = Toplevel(now)
            use_type_gui.title('use type to search')
            use_type_gui.geometry('500x300')

            Label(use_type_gui, text='书类型名:').place(x=50, y=50)

            var_type = StringVar()
            Entry(use_type_gui, textvariable=var_type).place(x=160, y=50)

            def search():
                type = var_type.get()
                sql = 'select * from books where type="%s";' % (type)
                cursor.execute(sql)
                b = cursor.fetchall()
                if len(b) == 0:
                    messagebox.showerror(message='没有该类型')
                else:
                    printbooks(b)

            Button(use_type_gui, command=search, text='查找').place(x=170, y=130)
            use_type_gui.mainloop()

        def use_isborrow():

            sql = 'select * from books where status="未借出";'
            cursor.execute(sql)
            c = cursor.fetchall()
            if len(c) == 0:
                messagebox.showerror(message='所有的书都被借出了')
            else:
                printbooks(c)

        Button(searchbook_window, text='书名查找', command=use_name).place(x=100, y=150)
        Button(searchbook_window, text='类型查找', command=use_type).place(x=200, y=150)
        Button(searchbook_window, text='未借出', command=use_isborrow).place(x=300, y=150)

        searchbook_window.mainloop()


def printbooks(s):
    '''
    打印书本信息
    '''
    try:
        now = manager_gui
        print_books_window = Toplevel(now)
    except:
        now = reader
        print_books_window = Toplevel(now)
    finally:
        print_books_window.geometry('600x1000')
        print_books_window.title('All books')

        Label(print_books_window, text='ID').place(x=10, y=10)
        Label(print_books_window, text='Name').place(x=60, y=10)
        Label(print_books_window, text='Type').place(x=170, y=10)
        Label(print_books_window, text='status').place(x=230, y=10)
        Label(print_books_window, text='borrow_times').place(x=300, y=10)
        Label(print_books_window, text='time ').place(x=400, y=10)

        # 遍历所有书籍，i用作位置点
        i = 0
        for row in s:
            i += 1
            var_id = StringVar()
            var_name = StringVar()
            var_type = StringVar()
            var_status = StringVar()
            var_bt = StringVar()
            var_time = StringVar()
            id = row[0]
            name = row[1]
            type = row[2]
            status = row[3]
            borrowtimes = row[4]
            time = row[5]
            Entry(print_books_window, textvariable=var_id).place(x=10, y=40 * i)
            var_id.set(id)
            Entry(print_books_window, textvariable=var_name).place(x=60, y=40 * i)
            var_name.set(name)
            Entry(print_books_window, textvariable=var_type).place(x=170, y=40 * i)
            var_type.set(type)
            Entry(print_books_window, textvariable=var_status).place(x=230, y=40 * i)
            var_status.set(status)
            Entry(print_books_window, textvariable=var_bt).place(x=300, y=40 * i)
            var_bt.set(borrowtimes)
            Entry(print_books_window, textvariable=var_time).place(x=400, y=40 * i)
            var_time.set(time)

            #     # 打印结果
            # print("ID: %s, Name: %s, type: %s, status:%s, borrowtimes:%d, borrowtime=%s" % (
            #     id, name, type, status, borrowtimes, time))
        # print('------------------------------------------------------------------------------------------------------')
        # print('\n')
        print_books_window.mainloop()


def printreaders(s):
    '''
    打印读者信息
    '''
    print_readers_window = Toplevel(manager_gui)
    print_readers_window.title('Readers message')
    print_readers_window.geometry('600x1000')

    Label(print_readers_window, text='Name').place(x=10, y=10)
    Label(print_readers_window, text='Sex').place(x=60, y=10)
    Label(print_readers_window, text='Speciality').place(x=110, y=10)
    Label(print_readers_window, text='bookname').place(x=190, y=10)
    Label(print_readers_window, text='borrowtimes').place(x=290, y=10)
    Label(print_readers_window, text='returntime').place(x=400, y=10)

    i = 0
    for row in s:
        i += 1
        var_name = StringVar()
        var_sex = StringVar()
        var_specially = StringVar()
        var_bookname = StringVar()
        var_bt = StringVar()
        var_rt = StringVar()
        name = row[0]
        sex = row[1]
        speciality = row[2]
        # id = row[3]
        bookname = row[4]
        borrowtime = row[5]
        returntime = row[6]
        Entry(print_readers_window, textvariable=var_name).place(x=10, y=40 * i)
        var_name.set(name)
        Entry(print_readers_window, textvariable=var_sex).place(x=60, y=40 * i)
        var_sex.set(sex)
        Entry(print_readers_window, textvariable=var_specially).place(x=110, y=40 * i)
        var_specially.set(speciality)
        Entry(print_readers_window, textvariable=var_bookname).place(x=190, y=40 * i)
        var_bookname.set(bookname)
        Entry(print_readers_window, textvariable=var_bt).place(x=290, y=40 * i)
        var_bt.set(borrowtime)
        Entry(print_readers_window, textvariable=var_rt).place(x=400, y=40 * i)
        var_rt.set(returntime)
        # print("name:%s, sex:%s, speciality:%s, id:%d, bookname:%s, borrowtime:%s, returntime:%s" % (
        #     name, sex, speciality, id, bookname, borrowtime, returntime))
    print_readers_window.mainloop()


def querydb():
    '''
    从数据库获取数据并返回
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM books"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    printbooks(results)


def borrowlist():
    '''
    借阅情况
    '''
    cursor = db.cursor()
    sql = 'select * from readers'
    cursor.execute(sql)
    results = cursor.fetchall()
    printreaders(results)


if __name__ == '__main__':
    db = connectdb()
    root = Tk()
    root.title('Weclome to Library System')
    root.geometry('500x300')


    def manager():
        def manager_confirm():
            confirm_pwd = pwd.get()
            if confirm_pwd == '123456':
                manager.destroy()
                global manager_gui
                manager_gui = Tk()
                manager_gui.title('Book Manager System')
                manager_gui.geometry('500x300')

                Button(manager_gui, text='查询所有书籍', command=querydb).place(x=50, y=50)
                Button(manager_gui, text='查询指定书籍', command=searchbook).place(x=150, y=50)
                Button(manager_gui, text='增加书籍', command=addbook).place(x=250, y=50)
                Button(manager_gui, text='借还情况', command=borrowlist).place(x=350, y=50)
                Button(manager_gui, text='删除书籍', command=deletebook).place(x=50, y=150)
                Button(manager_gui, text='查询读者', command=searchreader).place(x=150, y=150)
                Button(manager_gui, text='删除读者', command=deletereader).place(x=250, y=150)
                Button(manager_gui, text='退出系统', command=manager_gui.quit).place(x=350, y=150)

                manager_gui.mainloop()
            else:
                messagebox.showerror(message='password is wrong,try again')

        root.destroy()
        global manager
        manager = Tk()
        manager.title('Weclome back Manager')
        manager.geometry('500x300')

        pwd = StringVar()
        Label(manager, text='管理员密码：').place(x=50, y=50)
        Entry(manager, textvariable=pwd, show='*').place(x=160, y=50)
        Button(manager, text='登录', command=manager_confirm).place(x=150, y=130)

        manager.mainloop()


    def reader():
        root.destroy()
        global reader
        reader = Tk()
        reader.title('Weclome Reader')
        reader.geometry('500x300')

        Button(reader, text='查询所有书籍', command=querydb).place(x=100, y=50)
        Button(reader, text='查询指定书籍', command=searchbook).place(x=220, y=50)
        Button(reader, text='借出书籍', command=borrowbook).place(x=340, y=50)
        Button(reader, text='归还书籍', command=returnbook).place(x=150, y=150)
        Button(reader, text='退出系统', command=reader.quit).place(x=250, y=150)

        reader.mainloop()


    Label(root, text='请选择登录身份').pack()
    Button(root, text='管理员', command=manager).place(x=150, y=150, width=50, height=50)
    Button(root, text='读者', command=reader).place(x=300, y=150, width=50, height=50)
    root.mainloop()
    db.close()
