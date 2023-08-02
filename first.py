import mysql.connector 

#MySQL connectivity : 
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "mysql24903",
    database = "bloodbanks"
)

#Creating cursor to execute commands : 
cursor = mydb.cursor()

#Options : 
print("""
    1.Availability Check 
    2.Add Donor
    3.Raise request
""")
option = int(input("Choose option [1/2/3] : "))
if(option == 1) :
    inp_region = input("Enter region : ")
    sql_comm = "select blood_grp,units_avail from blood_stock where bloodbank_id = (select bloodbank_id from blood_bank where region = (%s) )"
    cursor.execute(sql_comm,(inp_region,))
    result = cursor.fetchall()

    if(result == []) : 
        print("No bloodbanks in the specified region")
    for res in result : 
        print(res)

elif(option ==2) : 
    id = int(input("Enter your id : "))
    name = input("Enter your name : ")
    grp = input("Enter your blood group : ")
    unit = int(input("Enter units of blood donated : "))
    reg = input("Enter your region : ")

    #Selecting the ids of donors to check if the donor is already registered in the database
    sql_comm = "select Donor_id from Donor;"
    cursor.execute(sql_comm)
    ids = cursor.fetchall()

    #Retrieving the bbid to update in blood_stock table
    sql_comm = "select bloodbank_id from blood_bank where region = %s"
    cursor.execute(sql_comm,(reg,))
    bbid = cursor.fetchall()[0][0]

    sql_comm = "update blood_stock set units_avail = units_avail + %s where blood_grp = %s and bloodbank_id = %s"
    cursor.execute(sql_comm,(unit,grp,bbid))
    if((id,) in ids) : 
        sql_comm = "update Donor set units = units + %s where Donor_id = %s;"
        cursor.execute(sql_comm,(unit,id))
    else : 
        sql_comm = "insert into Donor(Donor_id,blood_grp,units,name,bloodbank_id,region) values(%s,%s,%s,%s,%s,%s);" 
        cursor.execute(sql_comm,(id,grp,unit,name,bbid,reg))
    
    mydb.commit()

elif(option == 3) :
    id = int(input("Enter the hospital id : "))
    name = input("Enter hospital name name : ")
    grp = input("Enter required blood group : ")
    unit = int(input("Enter required units of blood : "))
    reg = input("Enter the region : ")

    sql_comm = "select hospital_id from hospital;"
    cursor.execute(sql_comm)
    ids = cursor.fetchall()
    sql_comm = "select blood_grp from hospital where hospital_id = %s;"
    cursor.execute(sql_comm,(id,))
    grps = cursor.fetchall()
    check = False
    if((grp,) in grps) : 
        check = True

    sql_comm = "select bloodbank_id from blood_bank where region = %s"
    cursor.execute(sql_comm,(reg,))
    bbid = cursor.fetchall()[0][0]

    sql_comm = "select units_avail from blood_stock where blood_grp = %s and bloodbank_id = %s"
    cursor.execute(sql_comm,(grp,bbid))
    unit_avail = cursor.fetchall()[0][0]
    diff = unit_avail - unit 

    if(unit < unit_avail) : 
        sql_comm = "update blood_stock set units_avail = %s where blood_grp = %s and bloodbank_id = %s"
        cursor.execute(sql_comm,(diff,grp,bbid))
    else : 
        diff = diff + (2*diff)
        print("Not enough blood available, Still ",diff," units required.")
        sql_comm = "update blood_stock set units_avail = 0 where blood_grp = %s and bloodbank_id = %s"
        cursor.execute(sql_comm,(grp,bbid))

    if((id,) in ids and check) : 
        sql_comm = "update hospital set units = units + %s where hospital_id = %s and blood_grp = %s;"
        cursor.execute(sql_comm,(unit,id,grp)) 
    else : 
        sql_comm = "insert into hospital(hospital_id,name,region,blood_grp,units,bloodbank_id) values(%s,%s,%s,%s,%s,%s);" 
        cursor.execute(sql_comm,(id,name,reg,grp,unit,bbid))
    
    mydb.commit()