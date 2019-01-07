# -*- coding=utf-8 -*-
import mysql.connector
import datetime

def connectdb():
    '''
    连接数据库
    '''
    #print('连接到mysql服务器...')
    # 打开数据库连接
    db = mysql.connector.connect(user="root", passwd="980507", database="library", use_unicode=True)
    #print('连接上了!')
    return db

def addbook(db):
    '''
    增加书籍
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    sql1 = "SELECT * FROM books"
    # 执行SQL语句
    cursor.execute(sql1)
    n=len(cursor.fetchall())
    name=input('书名:')
    sql='select name from books where name="%s";'%(name)
    cursor.execute(sql)
    result=cursor.fetchall()
    if len(result)!=0 and result[0][0] == name:
        print('该书已存在')
    else:
        type=input('书类型:')
        # SQL 插入语句
        sql = 'INSERT INTO books(id,name,type,status,borrowtimes)VALUES ("%d","%s","%s","未借出","%d");'%(n+1,name,type,0)
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

def borrowbook(db):
    '''
    借书
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    name=input('借的书名:')
    sql='select name from books where name="%s";'%(name)
    cursor.execute(sql)
    s=cursor.fetchall()
    if len(s)==0:
        print('该书不存在')
    else:
        sql='select status,borrowtimes,borrowtime,id from books where name="%s";'%(name)
        cursor.execute(sql)
        result=cursor.fetchall()
        if result[0][0] == '已借出':
            print('该书已借出')
        else:
            rname=input('姓名:')
            rsex=input('性别:')
            rspeciality=input('专业：')
            sql='insert into readers(name,sex,speciality,id,bookname,borrowtime) values ("%s","%s","%s","%d","%s","%s");'%(rname,rsex,rspeciality,result[0][3],name,datetime.date.today())
            cursor.execute(sql)
            sql1='update books set status="%s",borrowtimes="%d",borrowtime="%s" where name="%s";'%('已借出',result[0][1]+1,datetime.date.today(),name)
            cursor.execute(sql1)
            db.commit()
            print('成功借书')

def returnbook(db):
    '''
    还书
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    name=input('还的书名:')
    sql='select name from books where name="%s";'%(name)
    cursor.execute(sql)
    s=cursor.fetchall()
    if len(s)==0:
        print('这里没有这本书，你还错地方了')
    else:
        sql='select status from books where name="%s";'%(name)
        cursor.execute(sql)
        result=cursor.fetchall()
        if result[0][0]=='未借出':
            print('无人借该书，你还错地方了')
        else:
            sql1='update readers set returntime="%s" where bookname="%s";'%(datetime.date.today(),name)
            cursor.execute(sql1)
            sql='update books set status="%s" where name="%s";'%('未借出',name)
            cursor.execute(sql)
            db.commit()
            print('成功还书')

def deletebook(db):
    '''
    删书
    '''
    # 使用cursor()方法获取操作游标 
    cursor=db.cursor()
    name=input('删除的书名:')
    sql='select name from books where name="%s";'%(name)
    cursor.execute(sql)
    s=cursor.fetchall()
    if len(s)==0:
        print('这里没有这本书')
    else:
        sql='select status,borrowtimes,borrowtime,id from books where name="%s";'%(name)
        cursor.execute(sql)
        result=cursor.fetchall()
        if result[0][0] == '已借出':
            print('该书已借出,不能删除')
        else:
            sql1='delete from books where name="%s";'%(name)
            cursor.execute(sql1)
            db.commit()
            print('成功删除该书籍')
            

def searchreader(db):
    '''
    查询读者
    '''
    cursor=db.cursor()
    name=input('请输入查询的读者名:')
    speciality=input('专业:')
    sql='select * from readers where name ="%s" and speciality="%s";'%(name,speciality)
    cursor.execute(sql)
    result=cursor.fetchall()
    if len(result)==0:
        print('没有该读者的信息')
    else:
        printreaders(result)

def deletereader(db):
    cursor=db.cursor()
    name =input('请输入要删除的读者名：')
    speciality=input('专业:')
    sql1='select returntime from readers where name="%s" and speciality="%s";'%(name,speciality)
    cursor.execute(sql1)
    result=cursor.fetchall()
    returntime=[]
    s=0
    if len(result)==0:
        print('没有该读者的信息') 
    else:
        for row in result: 
            returntime.append(row[0]) 
        for i in range(len(returntime)):
            if returntime[i]==None:#如果没有归还时间，证明有书还没还
                s+=1
        if s==0:#所有书都还了，可以删除该读者
            sql='delete from readers where name="%s";'%(name)
            cursor.execute(sql)
            db.commit()
            print('删除成功')
        else:
            print('该读者还有书没还，不能删除')
            
def searchbook(db):
    cursor=db.cursor()
    print('1.书名查找，2类型查找，3还未借出')
    choice=input('请选择:')
    if choice=='1':
        name=input('请输入书名：')
        sql='select * from books where name="%s";'%(name)
        cursor.execute(sql)
        a=cursor.fetchall()
        if len(a)==0:
            print('该书不存在')
        else:
            printbooks(a)
    elif choice=='2':
        type=input('请输入类型：')
        sql='select * from books where type="%s";'%(type)
        cursor.execute(sql)
        b=cursor.fetchall()
        if len(b)==0:
            print('没有该类型')
        else:
            printbooks(b)
    elif choice=='3':
        sql='select * from books where status="未借出";'
        cursor.execute(sql)
        c=cursor.fetchall()
        if len(c)==0:
            print('所有的书都被借出了')
        else:
            printbooks(c)
    else:
        print('输入错误，请重新输入')
        print('\n')

def printbooks(s):
    '''
    打印书本信息
    '''
    print('------------------------------------------------------------------------------------------------------')
    for row in s:
        id = row[0]
        name = row[1]
        type = row[2]
        status=row[3]
        borrowtimes=row[4]
        time=row[5]
        # 打印结果
        print ("ID: %s, Name: %s, type: %s, status:%s, borrowtimes:%d, borrowtime=%s" % (id,name,type,status,borrowtimes,time))
    print('------------------------------------------------------------------------------------------------------')
    print('\n')

def printreaders(s):
    '''
    打印读者信息
    '''
    print('------------------------------------------------------------------------------------------------------')
    for row in s:
        name=row[0]
        sex=row[1]
        speciality=row[2]
        id=row[3]
        bookname=row[4]
        borrowtime=row[5]
        returntime=row[6]
        print("name:%s, sex:%s, speciality:%s, id:%d, bookname:%s, borrowtime:%s, returntime:%s"%(name,sex,speciality,id,bookname,borrowtime,returntime))
    print('------------------------------------------------------------------------------------------------------')
    print('\n')

def querydb(db):
    '''
    从数据库获取数据并返回
    '''
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 查询语句
    #sql = "SELECT * FROM Student \
    #    WHERE Grade > '%d'" % (80)
    sql = "SELECT * FROM books"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    printbooks(results)

def borrowlist(db):
    '''
    借阅情况
    '''
    cursor=db.cursor()
    sql='select * from readers'
    cursor.execute(sql)
    results=cursor.fetchall()
    printreaders(results)
    

if __name__ == '__main__': 
    while True:
        db = connectdb()
        user=input('请选择登录身份，1代表管理员，2代表读者,3退出:')
        if user== '1':              
            password=input('管理员密码：') #如果以管理员身份登入需要输入密码
            if password == '123456':
                print('欢迎回来')
                while(True):
                    print('**********************图书管理系统******************************')
                    print('                     1.查询所有书籍                             ')
                    print('                     2.查询指定书籍                             ')
                    print('                     3.增加书籍                                ')
                    print('                     4.借还情况                                ')
                    print('                     5.删除书籍                                ')
                    print('                     6.查询读者                                ')
                    print('                     7.删除读者                                ')
                    print('                     8.退出系统                                ')
                    print('***************************************************************')
                    choice = input("请选择:")
                    if choice == '1':
                        querydb(db)
                    elif choice == '2':
                        searchbook(db)
                    elif choice == '3':
                        addbook(db)
                    elif choice == '4':
                        borrowlist(db)
                    elif choice == '5':
                        deletebook(db)
                    elif choice == '6':
                        searchreader(db)
                    elif choice == '7':
                        deletereader(db)
                    elif choice == '8':
                        print ("谢谢使用")
                        print('\n')
                        db.close()
                        break
                    else:
                        print('输入错误，请重新输入')
                        print('\n')
            else:
                print('密码错误')
                print('\n')
                continue
        elif user=='2':
            print('欢迎光临') #以读者身份登入不需要密码
            while True:
                print('***********************读者系统********************************')
                print('                     1.查询所有书籍                             ')
                print('                     2.借出书籍                                ')
                print('                     3.归还书籍                                ')
                print('                     4.退出系统                                ')
                print('***************************************************************')
                choice = input("请选择:")
                if choice == '1':
                    querydb(db)
                elif choice == '2':
                    borrowbook(db)
                elif choice == '3':
                    returnbook(db)
                elif choice == '4':
                    print ("谢谢使用")
                    print('\n')
                    db.close()
                    break
                else:
                    print('输入错误，请重新输入')
                    print('\n')
                    
        elif user=='3':
            print ("谢谢使用")
            break
        else:
            print('输入错误，请重新输入')
            print('\n')