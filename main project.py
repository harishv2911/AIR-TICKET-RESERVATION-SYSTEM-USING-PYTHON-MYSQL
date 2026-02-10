
#IMPORTING THE REQUIRED MODULES
import random
import time
import mysql.connector as sql

#ESTABLISHING CONNECTION BETWEEN PYTHON AND MYSQL DATABASE
db=sql.connect(
host='localhost',
user='root',
password='rootroot',
database='airline_management_system')
cur=db.cursor()

def home_page():
    print()
    print("=============AIRLINES MANAGEMENT SYSTEM==============")
    print()
    time.sleep(0.5)
    print("HOME PAGE")
    print()
    time.sleep(0.5)
    print("1.ADMIN")
    print("2.USERS")
    print("Press any other key to exit this application:")
    sd=input("Who are you ? [1/2] .....")
    if sd=='1':
        admin()
    elif sd=='2':
        user_welcome()
        
    else:
        print("Do you want to exit this application?")
        s=int(input("If yes press 1 :"))
        if s==1:
            exit_()
        else:
            print()
            home_page()
def user_welcome(): 
    print()
    u=input("New user(N) or Existing user(E):")
    print()
    if u=='N' or u=='n':
        new_user()
    elif u=='E' or u=='e':
        existing_user()
    else:
        print("ENTER VALID INPUT")
        print('\n')
        user_welcome()
def new_user():
    print("=============NEW USER CREATION PORTAL=============")
    time.sleep(0.5)
    #GETTING USER'S DATA
    uname1=input("Enter a username:")
    name=input("Enter your name:")
    phno=input("Enter your mobile number:")
    email=input("Enter your mail id:")
    dob=input("Enter your date of birth  [YYYY-MM-DD] :")
    pwd1=int(input("Enter a 4 digit pin :"))
    pw1=int(input("Re enter your pin:"))
    if pwd1==pw1:
        #INSERTING USER DETAILS INTO THE DATABASE
        q1="INSERT INTO USERS VALUES('{}','{}','{}','{}','{}',{})".format(uname1,name,phno,email,dob,pwd1)
        cur.execute(q1)
        db.commit()
        print('\n')
        existing_user()
    else:
        print("PINS DO NOT MATCH !!!!")
        print('\n')
        user_welcome()
def existing_user():
    print("=============EXISTING USER LOGIN PORTAL=============")
    uname2=input("Enter your username:")
    pwd2=int(input("Enter your pin:"))
    df=(uname2,pwd2)
    #MATCHING USERNAME AND PASSWORD
    q2="SELECT USER_NAME,PASS_WORD FROM USERS"
    cur.execute(q2)
    data=cur.fetchall()
    for rec in data:
        if rec==df:
            print("ACCESS GRANTED")
            home()
    else:
        print("ENTERED PIN IS INCORRECT !!!!")
        print('\n')
        print("TRY AGAIN")
        print("Not  an existing user ?")
        er=int(input("Press 1 to register yourself as a new user : "))
        if er==1:
            time.sleep(0.5)
            new_user()
        else:
            time.sleep(0.5)
            existing_user()
def home():
    print("WELCOME")
    print()
    time.sleep(0.25)
    #DISPLAYING MENU
    print("What's your plan today?")
    print("1.VIEW FLIGHTS")
    print("2.BOOK TICKETS")
    print("3.VIEW MY TRIPS")
    print("4.CANCEL TICKETS")
    print("5.ACCOUNT USER INFO")
    print("6.LOGOUT")
    print()
    ch=int(input("Enter your choice:"))
    if ch==1:
        view_flights()
    elif ch==2:
        book_tickets()
    elif ch==3:
        view_tickets()
    elif ch==4:
        cancel_tickets()
    elif ch==5:
        user_info()
    elif ch==6:
        logout()
def view_flights():
    #SEARCHING FOR FLIGHTS 
    ori=input("Enter place of origin:")
    dest=input("Enter place of destination:")
    tdate=input("Enter date of travel:")
    time.sleep(0.3)
    print("=============LIST OF FLIGHTS=============")
    view="SELECT * FROM FLIGHT_DETAILS WHERE ORIGIN='{}' AND DESTINATION='{}' and FLIGHT_DATE='{}'".format(ori,dest,tdate)
    cur.execute(view)
    flights=cur.fetchall()
    #PRINTING THE LIST OF FLIGHTS
    if len(flights)>0:
        for rec in flights:
            time.sleep(2)
            print()
            print("ORIGIN:",rec[2])
            print("DESTINATION:",rec[3])
            print("DATE :",rec[4])
            print("TIME:",rec[5])
            print("AIRLINES:",rec[1])
            print("FLIGHT NUMBER:",rec[0])
            print("=============")
    else:
        print("No flights found")
    input("REDIRECTING TO THE MAIN PAGE  .......")
    home()
def book_tickets():
    print("TICKET BOOKING")
    fare=0.0
    add=0.0
    tid=random.randint(10000,99999)
    print()
    fno=int(input("FLIGHT NUMBER:"))
    cur.execute("SELECT * FROM FLIGHT_DETAILS WHERE FLIGHT_NUMBER={};".format(fno))
    data=cur.fetchall()
    if len(data)>0:
        for rec in data:
            dep=rec[2]
            arr=rec[3]
            tdate=rec[4]
            fno=rec[0]
    else:
        print("Entered Flight Number is incorrect")
        book_tickets()
        
    no=int(input("How many passengers?"))
    print()
    for i in range(no):
        name=input("Enter passenger's name:")
        print()
        #SELECTING SEAT CLASS
        dict_seat_class1={1:2000,2:2500,3:4000,4:6500}
        dict_seat_class2={1:"ECONOMY",2:"ECONOMY PLUS",3:"BUSINESS CLASS",4:"FIRST CLASS"}
        print("1.ECONOMY --------------$2000")
        print("2.ECONOMY PLUS ---------$2500")
        print("3.BUSINESS CLASS--------------$4000")
        print("4.FIRST CLASS ------------$6500")
        cl=int(input("Enter seat class:"))
        fare+=dict_seat_class1[cl]
        print()
        #SELECTING SEAT TYPE
        dict_seat_type1={1:0,2:250,3:500,4:1000}
        dict_seat_type2={1:"REGULAR",2:"ACCESSIBLE",3:"EMERGENCY EXIT",4:"EXTRA LEG ROOM"}
        print("1.REGULAR --------------------$0")
        print("2.ACCESSIBLE -----------------$250")
        print("3.EMERGENCY EXIT ------------$500")
        print("4.EXTRA LEG ROOM ------------$1000")
        st=int(input("Select desired seat type:"))
        add+=dict_seat_type1[st]
        print()
        querry_booking="INSERT INTO TICKET_BOOKING VALUES('{}',{},'{}','{}','{}',{},'{}','{}')".format(
        name,tid,dep,arr,tdate,fno,dict_seat_class2[cl],dict_seat_type2[st])
        cur.execute(querry_booking)
        db.commit()
    # FOOD ORDERING    
    op=input("Do you want to order food? ........[Y/N]")
    fcharge=0.0
    if op=="Y" or op=="y":
        print()
        fcharge=food(tid)
        print()
    elif op=="N" or op=="n":
        print()
    else:
        print()
        #PRINTING AMOUNT TO BE PAID
    print("FARE:",fare,     "ADDITIONAL CHARGES:",add,      "FOOD:",fcharge)
    total=fare+add+fcharge
    print()
    pay(tid,total)
    qp="INSERT INTO COSTS VALUES('{}',{})".format(tid,total)
    cur.execute(qp)
    db.commit()
    cur.execute("UPDATE FLIGHT_DETAILS SET SEATS=SEATS-{} WHERE FLIGHT_NUMBER={}".format(no,fno))
    db.commit()
    print()
    print("YOUR TICKETS HAVE BEEN BOOKED")
    print("Your TICKET ID is",tid,".")
    print()
    print("Contact 9587496874 or airlines@gmail.com for any queries....")
    print("The e-tickets are sent to your registered phone number via SMS")
    print("THANK YOU FOR CHOOSING AMS")
    print()
    time.sleep(5)
    home()
def pay(tid,amt_pay):
    print("Dear User, your total flight charges are",amt_pay)
    print("1.CREDIT CARD")
    print("2. DEBIT CARD")
    print("3. UPI ")
    mop=int(input("Select the mode of payment:"))
    print()
    if mop==1 or mop==2:
        cno=int(input("Enter 16 digit card number:"))
        noc=input("Enter name on card:")
        cvv=int(input("Enter CVV number:"))
        print("Proceeding for transaction .....")
        pin=int(input("Enter your PIN:"))
        if mop==1:
            x='CREDIT CARD'
        elif mop==2:
            x='DEBIT CARD'
        q5="INSERT INTO TRANSACTIONS_CARD VALUES({},'{}','{}',{},{},'{}')".format(tid,cno,noc,cvv,pin,x)
        cur.execute(q5)
        db.commit()
        print()
    elif mop==3:
        upi=int(input("Enter UPI id:"))
        input("Proceeding for transaction .....")
        pin=int(input("Enter your PIN:"))
        print()
        q5="INSERT INTO TRANSACTIONS_UPI VALUES({},{},{})".format(tid,upi,pin)
        cur.execute(q5)
        db.commit()
    else:
        print("Transaction failed !!")
        print("++++++++++++++++++RETRY++++++++++++++++++")
        pay(fare)
    input()
    print("TRANSACTION SUCCESSFUL !!!!")
    print()
def food(tid):
    fd=0.0
    # ORDERING FOOD
    dict_food_cost={1:99,2:149,3:150,4:199,5:169,6:79}
    dict_food_name={1:"BREAD SANDWICH",2:"BREAD OMELET",3:"ROTI(2) + DAL",4:"PIZZA",5:"VEG BURGER",6:"WATER BOTTLE(1L)"}
    #PRINTING LIST OF FOOD
    print("1.BREAD SANDWICH -------------$99 ")
    print("2.BREAD OMELET ---------------$149")
    print("3.ROTI(2) + DAL --------------$150")
    print("4.PIZZA ----------------------$199")
    print("5.VEG BURGER -----------------$169")
    print("6.WATER BOTTLE(1L) -----------$79 ")
    x=True
    while x:
        order=int(input("Enter the desired food id:"))
        count=int(input("How many?"))
        fd+=dict_food_cost[order]*count
        q4="INSERT INTO FOOD VALUES({},'{}',{},{})".format(tid,dict_food_name[order],count,count*dict_food_cost[order])
        cur.execute(q4)
        db.commit()
        fg=input("Do you want to add more? ......[Y/N]")
        if fg=="N" or fg=="n":
            x=False
    print("The food charges are $",fd)
    return fd
def view_tickets():
    tid=int(input("Enter your TID:"))
    cur.execute("SELECT * FROM TICKET_BOOKING WHERE TICKET_ID={}".format(tid))
    data=cur.fetchall()
    if len(data)==0:
        print("NO TRIPS AVAILABLE")
    else:
        print("Fetching your info  :)  This may take a few moments ")
        #PRINTING TICKET DETAILS
        for rec in data:
            time.sleep(1.5)
            print("NAME:",rec[0])
            print("TICKET_ID:",rec[1])
            print("ORIGIN:",rec[2])
            print("DESTINATION:",rec[3])
            print("TRAVEL_DATE:",rec[4])
            print("FLIGHT_NUMBER:",rec[5])
            print("SEAT CLASS:",rec[6])
            print("SEAT TYPE:",rec[7])
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    home()
def cancel_tickets():
    print("TICKET CANCELLATION")
    print()
    tidc=input("Enter your TICKET_ID:")
    print(" ### ONLY 80% OF THE TOTAL FARE WILL BE REFUNDED ###")
    tc=input("Are you sure you want to cancel your ticket? ......[Y/N]  :")
    if tc=="Y" or tc=="y":
        print()
        #DELETING RECORD FROM DATABASE
        q3="DELETE FROM TICKET_BOOKING WHERE TICKET_ID='{}' ".format(tidc)
        cur.execute(q3)
        db.commit()
        print("TICKET CANCELLATION SUCCESSFUL")
        print()
        home()
    else:
        input("ABORTING FROM TICKET CANCELLATION PORTAL .......")
        print()
        home()
def logout():
    lg=input("Do you want to logout of this portal? .......[Y/N]")
    if lg=="Y" or lg=="y":
        time.sleep(1)
        home_page()
    elif lg=="N" or lg=="n":
        print()
        home()
def modify_acc():
    print("ACCOUNT MODIFICATION")
    print()
    print("1.USERNAME")
    print("2.PASSWORD")
    print("3.NAME")
    print("4.DATE OF BIRTH")
    print("5.PHONE NUMBER")
    am=int(input("What do you want to modify? ......"))
    if am==1:
        #UPDATING USERNAME
        u1=input("Enter current username:")
        u2=input("Enter new username:")
        upd_username="UPDATE USERS SET USER_NAME='{}' WHERE USER_NAME='{}'".format(u2,u1)
        cur.execute(upd_username)
        db.commit()
        print("USERNAME UPDATED SUCCESSFULLY")
        home()
    elif am==2:
        #UPDATING PASSWORD
        p1=input("Enter current password:")
        p2=input("Enter new password:")
        upd_password="UPDATE USERS SET PASS_WORD= '{}' WHERE PASS_WORD= '{}'".format(p2,p1)
        cur.execute(upd_password)
        db.commit()
        print("PASSWORD UPDATED SUCCESSFULLY")
        home()
    elif am==3:
        #UPDATING NAME
        n1=input("Enter old name:")
        n2=input("Enter new name:")
        upd_name="UPDATE USERS SET NAME_= '{}' WHERE NAME_= '{}'".format(n2,n1)
        cur.execute(upd_name)
        db.commit()
        print("NAME UPDATED SUCCESSFULLY")
        home()
    elif am==4:
        #UPDATING DATE OF BIRTH
        d1=input("Enter old date of birth [YYYY-MM-DD]: ")
        d2=input("Enter new date of birth [YYYY-MM-DD]: ")
        upd_dob="UPDATE USERS SET DATE_OF_BIRTH= '{}' WHERE DATE_OF_BIRTH= '{}'".format(d2,d1)
        cur.execute(upd_dob)
        db.commit()
        print("DATE OF BIRTH UPDATED SUCCESSFULLY")
        home()
    elif am==5:
        #UPDATING PHONE NUMBER
        ph1=input("Enter old phone number:")
        ph2=input("Enter new phone number:")
        upd_phone_number="UPDATE USERS SET MOBILE_NUMBER= '{}' WHERE MOBILE_NUMBER= '{}'".format(ph2,ph1)
        cur.execute(upd_phone_number)
        db.commit()
        print("PHONE NUMBER UPDATED SUCCESSFULLY")
        home()
    else:
        print("Enter valid input")
        home()
def user_info():
    print("1.VIEW DETAILS")
    print("2.MODIFY ACCOUNT")
    print("3.DELETE ACCOUNT")
    print("4.HOME")
    ui=int(input("Enter your choice:"))
    if ui==1:
        print("ACCOUNT DETAILS")
        uname5=input("Enter your username:")
        acc_="SELECT*FROM USERS WHERE USER_NAME= '{}'".format(uname5)
        cur.execute(acc_)
        ad=cur.fetchall()
        for i in ad:
            print("USERNAME:",i[0])
            print("UNAME:",i[1])
            print("PHONE_NUMBER:",i[2])
            print("DATE_OF_BIRTH:",i[3])
            print("PASSWORD:",i[4])
        input()
        user_info()
    elif ui==2:
        modify_acc()
        input()
        user_info()
    elif ui==3:
        print("ACCOUNT DELETION PORTAL ")
        un=input("Enter the account's username that you want to delete:")
        cur.execute("DELETE FROM USERS WHERE USER_NAME='{}'".format(un))
        db.commit()
        print("ACCOUNT DELETION SUCCESSFUL")
        print()
        user_info()
    elif ui==4:
        print('\n')
        home()
    else:
        print("Enter valid input !!!!")
        user_info()    
def admin():
    print("================== ADMIN LOGIN PORTAL ================== ")
    aid=input("Enter admin id:")
    apss=int(input("Enter password:"))
    tg=(aid,apss)
    #MATCHING ADMIN ID AND PIN
    cur.execute("SELECT ADMIN_ID,PASS_WORD FROM ADMINS")
    data=cur.fetchall()
    for rec in data:
        if rec==tg:
            print("ACCESS GRANTED ")
            main()
        else:
            print("ADMIN ID AND PASSWORD DO NOT MATCH!!!")
            admin()
def main():
    print('WELCOME TO ADMIN PORTAL')
    print()
    print("What would you like to do now ?")
    print("1.ADD FLIGHTS")
    print("2.MODIFY FLIGHT DETAILS")
    print("3.VIEW FLIGHT DETAILS")
    print("4.PASSENGER DETAILS")
    print("5.ACCOUNTS")
    print("6.STAFFS")
    print("7.LOGOUT")
    ach=int(input("Enter your choice:"))
    if ach==1:
        add_flights()
    elif ach==2:
        mod_flights()
    elif ach==3:
        view_flights_of_admin()
    elif ach==4:
        pass_det()
    elif ach==5:
        acc()
    elif ach==6:
        staffs()
    elif ach==7:
        home_page()
def add_flights():
    print("==================ADD FLIGHTS==================")
    print()
    fno=int(input("Enter Flight number:"))
    aname=input(" Enter Airlines name:")

    ori=input("Enter place of origin:")
    dest=input("Enter place of destination:")

    fdate=input("Enter flight date [YYYY-MM-DD] :")
    ftime=input("Enter flight time [HH:MM:SS] :")
    
    p1name=input("Enter pilot 1 name:")
    p1id=int(input("Enter pilot 1 id:"))
    p1exp=int(input("Enter pilot 1 experience [in yrs] :"))

    p2name=input("Enter pilot 2 name:")
    p2id=int(input("Enter pilot 2 id:"))
    p2exp=int(input("Enter pilot 2 experience [in yrs] :"))

    seats=int(input("How many seats ?"))

    addf="INSERT INTO FLIGHT_DETAILS VALUES ({},'{}','{}','{}','{}','{}','{}',{},{},'{}',{},{},{})".format(
        fno,aname,ori,dest,fdate,ftime,p1name,p1id,p1exp,p2name,p2id,p2exp,seats)
    cur.execute(addf)
    db.commit()
    print("FLIGHT DETAILS ADDED SUCCESSFULLY ")
    print()
    input("Redirecting to the main page .........")
    main()
def mod_flights():
    print("================== MODIFY FLIGHT DETAILS ================== ")
    print()
    print("1.FLIGHT NUMBER")
    print("2.AIRLINES NAME")
    print("3.PLACE OF ORIGIN AND DETINATION ")
    print("4.FLIGHT DATE AND TIME")
    print("5.PILOT DETAILS")
    print()
    rt=int(input("What would you like to do ?"))
    if rt==1:
        ofn=int(input("Enter old flight number:"))
        nfn=int(input("Enter new flight number:"))
        cur.execute("UPDATE FLIGHT_DETAILS SET FLIGHT_NUMBER={} WHERE FLIGHT_NUMBER={}".format(nfn,ofn))
        time.sleep(2.5)
        print("UPDATION SUCCESSFULL .....")
        db.commit()
        print()
        main()
    elif rt==2:
        fn=int(input("Enter flight number:"))
        nan=input("Enter new airlines name:")
        cur.execute("UPDATE FLIGHT_DETAILS SET AIRLINES_NAME='{}' WHERE FLIGHT_NUMBER={}".format(nan,fn))
        time.sleep(2.5)
        print("UPDATION SUCCESSFULL .....")
        db.commit()
        print()
        main()
    elif rt==3:
        fn=int(input("Enter flight number:"))
        ori=input("Enter Origin place:")
        dst=input("Enter Destination place:")
        cur.execute("UPDATE FLIGHT_DETAILS SET ORIGIN='{}', DESTINATION='{}' WHERE FLIGHT_NUMBER={}".format(ori,dst,fn))
        time.sleep(2.5)
        print("UPDATION SUCCESSFULL .....")
        db.commit()
        print()
        main()
    elif rt==4:
        fn=int(input("Enter flight number:"))
        dt=input("Enter flight date  [YYYY-MM-DD]:")
        tim=input("Enter flight time [HH:MM:SS]:")
        cur.execute("UPDATE FLIGHT_DETAILS SET FLIGHT_DATE='{}', FLIGHT_TIME ='{}' WHERE FLIGHT_NUMBER={}".format(dt,tim,fn))
        time.sleep(2.5)
        print("UPDATION SUCCESSFULL .....")
        db.commit()
        print()
        main()
    elif rt==5:
        fn=int(input("Enter flight number:"))
        print("1.PILOT 1")
        print("2.PILOT 2")
        pc=int(input("Enter your choice:"))
        print()
        pn=input("Enter pilot name:")
        pid=int(input("Enter pilot id:"))
        pexp=int(input("Enter pilot experience:"))
        if pc==1:
            cur.execute("UPDATE FLIGHT_DETAILS SET PILOT_1_NAME='{}',PILOT_1_ID={},PILOT_1_EXPERIENCE={} WHERE FLIGHT_NUMBER={}".format(
                pn,pid,pexp,fn))
            db.commit()
            time.sleep(2.5)
            print("UPDATION SUCCESSFULL .....")
        elif pc==2:
            cur.execute("UPDATE FLIGHT_DETAILS SET PILOT_2_NAME='{}',PILOT_2_ID={},PILOT_2_EXPERIENCE={} WHERE FLIGHT_NUMBER={}".format(
                pn,pid,pexp,fn))
            db.commit()
            time.sleep(2.5)
            print("UPDATION SUCCESSFULL .....")

        else:
            print("INVALID INPUT")
    else:
        print("INVALID INPUT")
        mod_flights()
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def view_flights_of_admin():
    print("================FLIGHT DETAILS================")
    fo=int(input("Enter flight number to search:"))    
    cur.execute("SELECT * FROM FLIGHT_DETAILS WHERE FLIGHT_NUMBER={} ".format(fo))
    data=cur.fetchall()
    for rec in data:
        print("FLIGHT_NUMBER:",rec[0])
        print("AIRLINES_NAME:",rec[1])
        print("ORIGIN:",rec[2])
        print("DESTINATION:",rec[3])
        print("FLIGHT DATE:",rec[4])
        print("FLIGHT TIME:",rec[5])
        print("PILOT_1_NAME:",rec[6])
        print("PILOT_1_ID:",rec[7])
        print("PILOT_1_EXPERIENCE:",rec[8])
        print("PILOT_2_NAME:",rec[9])
        print("PILOT_2_ID:",rec[10])
        print("PILOT_2_EXPERIENCE:",rec[11])
        print()
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
        print()
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def pass_det():
    print()
    print("PASSENGER DETAILS")          
    print()
    to=int(input("Enter ticket id to search:"))
    cur.execute("SELECT * FROM TICKET_BOOKING WHERE TICKET_ID={}".format(to))
    data=cur.fetchall()
    for rec in data:
        print("PASSENGER_NAME:",rec[0])
        print("TICKET_ID:",rec[1])
        print("ORIGIN:",rec[2])
        print("DESTINATION:",rec[3])
        print("TRAVEL_DATE:",rec[4])
        print("FLIGHT_NUMBER:",rec[5])
        print("SEAT_CLASS:",rec[6])
        print("SEAT_TYPE:",rec[7])
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
        print()
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def acc():
    print("ACCOUNTS")
    print()
    print("1.SEARCH BY YEAR")
    print("2.SEARCH BY MONTH")
    print("3.SEARCH BY DATE")
    ui=int(input("enter your choice:"))
    if ui==1:
        yr=input("Enter year to search   [YYYY] :")
        print()
        q1="SELECT * FROM TICKET_BOOKING WHERE TRAVEL_DATE LIKE '{}-%';".format(yr)
        cur.execute(q1)
        data=cur.fetchall()
    elif ui==2:
        yr=input("Enter which year      [YYYY]? ")
        month=input("Which Month      [MM]? ")
        print()
        q2="SELECT * FROM TICKET_BOOKING WHERE TRAVEL_DATE LIKE '{}-{}-%';".format(yr,month)
        cur.execute(q2)
        data=cur.fetchall()
    elif ui==3:
        date=input("Enter which date [YYYY-MM-DD]:")
        print()
        q2="SELECT * FROM TICKET_BOOKING WHERE TRAVEL_DATE LIKE '{}';".format(date)
        cur.execute(q2)
        data=cur.fetchall()
    if len(data)>0:
        for rec in data:
            time.sleep(0.5)
            print("NAME:",rec[0])
            print("TICKET_ID:",rec[1])
            print("ORIGIN:",rec[2])
            print("DESTINATION:",rec[3])
            print("TRAVEL_DATE:",rec[4])
            print("FLIGHT_NUMBER:",rec[5])
            print("SEAT CLASS:",rec[6])
            print("SEAT TYPE:",rec[7])
            print()
            print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    else:
        print("No details found")
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def staffs():
    print("STAFFS")
    print()
    print("1.ADD STAFFS")
    print("2.VIEW STAFFS")
    print("3.REMOVE STAFFS")
    print("4.BACK")
    we=int(input("Enter your choice:"))
    if we==1:
        add_st()
    elif we==2:
        view_staffs()
    elif we==3:
        rem_staffs()
    elif we==4:
        input("REDIRECTING TO THE MAIN PAGE  .......")
        main()
    else:
        print('INVALID INPUT')
        input("REDIRECTING TO THE MAIN PAGE  .......")
        main()
def add_st():
    print("ADDING NEW STAFFS")
    print()
    sname=input("Enter name:")
    sgen=input("Enter gender  [M/F]:")
    smob=int(input("Enter mobile number:"))
    saddr=input("Enter address:")
    sid=random.randint(100,999)
    cur.execute("INSERT INTO STAFFS VALUES ('{}','{}',{},'{}',{})".format(sname,sgen,smob,saddr,sid))
    db.commit()
    print("The Staff id is",sid)
    print("Details added successfully")
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def view_staffs():
    print("VIEWING STAFF DETAILS")
    print()
    sid=int(input("enter staff id to search:"))
    cur.execute("SELECT * FROM STAFFS WHERE STAFF_ID={}".format(sid))
    data=cur.fetchall()
    for rec in data:
        print("NAME:",rec[0])
        print("GENDER:",rec[1])
        print("MOBILE NUMBER:",rec[2])
        print("ADDRESS:",rec[3])
        print("STAFF ID:",rec[4])
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def rem_staffs():
    print("STAFF REMOVAL PORTAL")
    print()
    sir=int(input("Enter staff id to remove:"))
    cur.execute("DELETE FROM STAFFS WHERE STAFF_ID={}".format(sir))
    db.commit()
    print("Removal Successfully")
    input("REDIRECTING TO THE MAIN PAGE  .......")
    main()
def exit_():
    print("SHUTTING DOWN AIRLINES MANAGEMENT SYSTEM ......")
    exit()

home_page()
