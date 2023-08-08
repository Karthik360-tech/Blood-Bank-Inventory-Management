import json
from flask import Flask,request,Response
from flask_restful import Api,Resource
from  flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)       #creates flask application where name specifies the root path
api = Api(app)              #routing and request handling 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql24903@localhost/bloodbanks'
db = SQLAlchemy(app)

class bloodbank_app(Resource):
    '''Options : 
        1.Using the name of the donor, we will be able find out his or her blood group, location, and phone number.
        2.Using the blood group, we should be able to get the list of people of that blood group, their age and location.
        3. Summary : 
            a.	How many donors in each blood group
            b.	How many donors of blood group below the age of 30
            c.	Male and female ratio of the donors
    '''
    def get(self,nam) :                 
        sql_query = f"select * from donor where name = {nam}"

        try:
            result = db.engine.execute(sql_query)
            result = result.fetchone()
            print(result)
            if result:
                data = {
                    'id': result[0],
                    'blood_grp' : result[1],
                    'units_donated': result[2],
                    'name': result[3],
                    'Bloodbank_ID': result[4],
                    'Location': result[5],
                    'gender': result[6],
                    'age': result[7],
                    'Phn_no': result[8]
                }
                #return data
                return Response(json.dumps(data), content_type='application/json')
            else:
                return {'message': 'Donor not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
        
class GetID(Resource) : 
     def get(self,id) : 
        sql_query = f"select * from donor where donor_id = {id}"

        try:
            result = db.engine.execute(sql_query)
            result = result.fetchone()
            print(result)
            if result:
                data = {
                    'id': result[0],
                    'blood_grp' : result[1],
                    'units_donated': result[2],
                    'name': result[3],
                    'Bloodbank_ID': result[4],
                    'Location': result[5],
                    'gender': result[6],
                    'age': result[7],
                    'Phn_no': result[8]
                }
                return Response(json.dumps(data), content_type='application/json')
            else:
                return {'message': 'Donor not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

class summary(Resource) :
    def get(self) :
        sql_query = "SELECT count(*) as no_of_donors,blood_grp FROM bloodbanks.donor group by blood_grp;"
        try:
            data = {}
            result1 = db.engine.execute(sql_query)
            result1 = result1.fetchall()
            print(result1)
            if result1:
                blood_grp_data = {}
                for row in result1:
                    blood_grp_data[row[1]] = row[0]
                    print(blood_grp_data)
                data['NO OF DONORS FOR EACH BLOOD GROUP'] = blood_grp_data
                print(data)
            else:
                return {'message': 'Donor not found'}, 404
           
            
            sql_query = "SELECT count(*) as no_of_donors,blood_grp FROM bloodbanks.donor where age<30 group by blood_grp";
            result2 = db.engine.execute(sql_query)
            result2 = result2.fetchall()
            print(result2)
            if result2 : 
                blood_grp_data_age_lt_30 = {}
                for row in result2:
                    blood_grp_data_age_lt_30[row[1]] = row[0]

                data['NO OF DONORS FOR EACH BLOOD GROUP WITH AGE < 30'] = blood_grp_data_age_lt_30
            else:
                return {'message': 'Donor not found'}, 404
            print(data)
            sql_query = "SELECT count(*) as no_of_donors,gender FROM bloodbanks.donor  group by gender;"
            result3 = db.engine.execute(sql_query)
            result3 = result3.fetchall()
            print(result3)
            print("RATIO : ",result3[0][0]/result3[1][0])
            if result3:
                data['RATIO OF MALE AND FEMALE DONORS'] = result3[0][0]/result3[1][0]
            else:
                return {'message': 'Donor not found'}, 404
            return data
            
        except Exception as e:
            return {'error': str(e)}, 500
        
    
api.add_resource(bloodbank_app, "/donordata","/donordata/<string:nam>")     #/<int:name> : used to define the parameters to be passed with the request
api.add_resource(GetID,"/donordata/by_id_custom/<int:id>")
api.add_resource(summary,"/donordata/summary")

if __name__ == "__main__" : 
    app.run(debug = True)