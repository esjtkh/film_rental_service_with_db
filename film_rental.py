import mysql.connector
from datetime import date
import time

class film_rent :
    
      username =""
      password = ""
      shop1 =""
      shop2 =""
      active_shop = ""
      role=""
      def __init__(self):
            
            self.film_rent_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="esjkhademi8095",
            database="film_rent"
            )
            self.mycursor = self.film_rent_db.cursor()
            # sql = f"INSERT INTO man_shop (username,shop1) VALUES ('hello', 'jpjo')"
            # mycursor.execute(sql)
            # film_rent_db.commit()


      def handle_valid_command(self):
          answer = input("Enter s for sign-up and l for login :")

          if answer =='l' or answer == 's':
                  return answer
          else :
                  print("Invalid Command!\n")
                  return answer


      def retrieve_shop_name(self): 
            sql = f"select shop1,shop2 from man_shop where username ='{self.username}'"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.shop1 = result[0][0]
            self.shop2 = result[0][1]


      def handle_login(self):
          while True :
                answer = input("Enter m for manager and c for customer :")
                if not answer == 'm' and not answer == 'c':
                      print("Invalid Command!")
                      continue 
                username = input("Enter username : ")
                password = input("Enter password : ")
                status = self.check_user_pass(username,password,answer,"login")
                if status :
                      print("You are logged in successfully!")
                      self.username = username
                      self.password = password
                      if answer == "m":
                           self.role = 'manager'
                      else :
                           self.role = "customer"
                      break
                else :
                      print("Login failed!")
                      continue



      def handle_signup(self):
          while True:
            answer = input("Enter m for manager and c for customer : ")
            if not answer == 'm' and not answer == 'c':
                  print("Invalid command!")
                  continue

            username = input("please enter your username : ")
            password = input("please enter your password : ")
            if answer == 'm' :
                  shop1 = input("Enter name of your first shop: ")
                  shop2 = input("Enter name of your second shop: ")
                  status = self.check_user_pass(username,password,answer,'signup')

                  if status:
                        status = self.check_shop_name(shop1,shop2)
                        if status :
                              self.enter_man_user_pass(username,password,answer,shop1,shop2)
                              print("registration successfully done!")
                              return True
                        else :
                         continue
                  else :
                        continue
            elif answer == 'c':
                  age = input("Enter your age : ")
                  gender = input("Enter your gender : ")
                  status = self.check_user_pass(username,password,answer,'signup')
                  if status:
                        self.enter_cstmr_user_pass(username,password,age,gender)
                        print("registration successfully done!")
                        return True
                  else :
                        continue




      def check_user_pass (self , username,password,answer , l_or_s):
        if answer == 'm':
              table = 'man_login'
        else :
              table = 'customer_login'

        sql = f"select username,pass from {table} where username = '{username}'"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()

        if len(result) == 0 and l_or_s == "signup":
              return True
        
        elif len(result) == 0 and l_or_s == "login":

            print("username not found!")
            return False
        
        elif not len(result) == 0 and l_or_s == "login":
              
              for i in range(len(result)):
                      if result[0][0]==username:
                            if result[0][1] == password:
                                 return True
              print("Not found!")
              return False

        else :
              print("Invalid username!")
              return False
        

      def check_shop_name(self,shop1,shop2 = None):
          
          sql = f"select shop1,shop2 from man_shop where shop1 = '{shop1}' or shop2 = '{shop1}'"
          self.mycursor.execute(sql)
          result = self.mycursor.fetchall()
          if len(result) == 0:
            if shop2:
               sql = f"select shop1,shop2 from man_shop where shop1 = '{shop2}' or shop2 = '{shop2}'"
               self.mycursor.execute(sql)
               result = self.mycursor.fetchall()
               if len(result) == 0:
                    return True
               else :
                    print("Shop2 name is in use")
                    return False
            else :
                 return True
          
          print("Shop1 name is in use")
          return False


      def enter_man_user_pass(self,username,password,answer,shop1=None,shop2=None):
          if answer == "m":
            table = "man_login"
            self.shop1 = shop1
            self.shop2 = shop2
            if shop2 == "":
                 shop2 ="NULL"
            sql = f"insert into man_shop values('{username}','{shop1}',{shop2})"
            self.mycursor.execute(sql)
            self.film_rent_db.commit()

          else :
                table = "customer_login"
               
          sql = f"insert into {table} values ('{username}','{password}')"

          self.mycursor.execute(sql)
          self.film_rent_db.commit()
          


      def enter_cstmr_user_pass(self,username,password,age,gender):
            sql = f"insert into customer_login(username,pass,age,gender) values('{username}','{password}',{age},'{gender}')"
            self.mycursor.execute(sql)
            self.film_rent_db.commit()



      def check_movie_presence(self,name,lang,year):
          
          sql = f"select film_name from film_info,shop_film where film_info.film_name = '{name}' and film_info.lang = '{lang}' and film_info.product_year = '{year}' and shop_film.shop_name = '{self.active_shop}'"
          self.mycursor.execute(sql)
          result = self.mycursor.fetchall()
          if len(result) == 0 :
                return 0
          else :
                return 1


      def handle_add_movie(self):
        
        name , genre ,year, lang , film_number = input("Enter movie name , genre , production year , language , film_number (seperate by ,) : ").split(',')
        actors = []
        
        while True:
            acname = input("Enter movie actors (Press Enter to finish): ")
            if not acname:
                  break
            actors.append(acname)


        status = self.check_movie_presence(name,lang,year)

        if status == 0:

            sql = f"insert into film_info (film_name,genre,product_year,lang) values('{name}','{genre}','{year}','{lang}')"
            self.mycursor.execute(sql)
            self.film_rent_db.commit() 
            sql = f"select film_id from film_info where film_name = '{name}' and genre = '{genre}' and lang = '{lang}' and product_year = {year}"
            self.mycursor.execute(sql)
            film_id = self.mycursor.fetchall()
            sql = f"insert into shop_film (shop_name,film_id,film_num) values('{self.active_shop}',{film_id[0][0]},{film_number})"
            self.mycursor.execute(sql)
            self.film_rent_db.commit()

            for x in actors:
                  # sql = "insert into actor(name) values(%s)"
                  # self.mycursor.executemany(sql,actors)
                  sql = f"insert into actor(name) value('{x}')"
                  self.mycursor.execute(sql)
                  self.film_rent_db.commit()

            for x in actors :
                 
                  sql = f"select actor_id from actor where name = '{x}'"
                  self.mycursor.execute(sql)
                  actor_id = self.mycursor.fetchall()

                  sql = f"insert into film_actor values({film_id[0][0]},{actor_id[0][0]})"
                  self.mycursor.execute(sql)
                  self.film_rent_db.commit() 
            print("movie successfully added.")

        else :
              print("This movie is already in your shop")



      def handle_customer_info(self):
           sql = f"select c.username,c.age,c.gender ,f.film_name from active_rental as a inner join film_info as f on a.film_id = f.film_id inner join customer_login as c on c.customer_id = a.customer_id"
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()

           for x in result:
                print (x)


      def handle_view_reservations(self):
           sql = f"select cl.customer_id,cl.username,cr.film_id,fi.film_name,sf.film_num,cr.rental_days from customer_reserve as cr inner join customer_login as cl on cr.customer_id = cl.customer_id inner join film_info as fi on cr.film_id = fi.film_id inner join shop_film as sf on sf.shop_name = cr.shop_name where  cr.shop_name = '{self.active_shop}'"
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()

           for i in range(len(result)):
                print(result[i])

           while True: #reservation approval
                  movie_name , username = input("Enter name of movie and related username you want to accept (seperate by ',') or 'E,E' to Exit: ").split(',')
           
                  if movie_name =="E" and username == "E":
                        return True
                  
                  customer_id = result[0][0]
                  film_id = result[0][2]
                  rental_days = result[0][5]
                  rental_date = date.today()
                  rental_date = rental_date.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
                  film_num = result[0][4]
                  #insert to active rental
                  sql = f"insert into active_rental values('{self.active_shop}',{film_id},{customer_id},'{rental_date}',{rental_days},1)"
                  self.mycursor.execute(sql)
                  self.film_rent_db.commit()
                  #delete from reserve table 
                  sql = f"delete from customer_reserve where customer_id = {customer_id} and film_id = {film_id} and shop_name = '{self.active_shop}'"
                  self.mycursor.execute(sql)
                  self.film_rent_db.commit()
                  #decrease number of films               
                  film_num = film_num - 1                       
                  sql = f"update shop_film set film_num ={film_num} where film_id = {film_id} and shop_name = '{self.active_shop}'"
                  self.mycursor.execute(sql)
                  self.film_rent_db.commit()
                  print("successfully gave to customer.")
                  return True
      
      def is_Delay(self,rental_date,give_back_date,rental_days,customer_id,film_id):
           #difference = give_back_date - rental_date
           timestamp1 = time.mktime(time.strptime(str(rental_date), "%Y-%m-%d"))
           timestamp2 = time.mktime(time.strptime(str(give_back_date), "%Y-%m-%d"))
           # Calculate the difference in seconds and convert to days
           difference_in_seconds = timestamp2 - timestamp1
           difference = difference_in_seconds / 86400 #86400 seconds a day

           if difference > rental_days:
                diff = difference -rental_days
                
                #Enter to delay table
                sql = f"insert into customer_delay values({customer_id},{self.active_shop},{film_id},'{rental_date}','{give_back_date}',{diff})"
                self.mycursor.execute(sql)
                self.film_rent_db.commit()

                p =int(rental_days)*2 + diff*3 
                print(f"total cost : {p} dollars")
             

           else :
                p =int(rental_days) * 2
                print (f"total cost : {p} dollars" ) 

           return(p)



      def handle_give_back_confirmation(self):
           #show all requests:
           sql = f"select ar.customer_id,fi.film_id,fi.film_name,cl.username,ar.rental_date,ar.rental_days,ar.status from active_rental as ar inner join customer_login as cl on ar.customer_id = cl.customer_id inner join film_info as fi on fi.film_id = ar.film_id where ar.shop_name = '{self.active_shop}' and ar.status = -1"
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()

           for x in result :
                print(x)

            #accept request 
           username,film_name =input("Enter username and film name you want to accept (seperate by ',') or E,E for Exit :").split(",")
                  
           if username == "E" and film_name == "E":
                return True
           
            #add to rental_history
           for x in result:
                  if x[3]==username and x[2] == film_name:
                       customer_id = x[0]
                       film_id = x[1]
                       rental_date = x[4]

                       give_back_date = date.today()
                       give_back_date = give_back_date.strftime("%Y-%m-%d")
                       rental_days = result[0][5]

                       payment_cost = self.is_Delay(rental_date,give_back_date,rental_days,customer_id,film_id)

                       sql = f"insert into rental_history(shop_name,customer_id,film_id,payment_cost,rental_date,give_back_date) values('{self.active_shop}',{customer_id},{film_id},{payment_cost},'{rental_date}','{give_back_date}')"
                       self.mycursor.execute(sql)
                       self.film_rent_db.commit()

                        #increase film number
                       sql = f"select film_num from shop_film where shop_name ='{self.active_shop}' and film_id={film_id}"
                       self.mycursor.execute(sql)
                       film_num = self.mycursor.fetchall()
                       film_num = film_num[0][0] + 1
                       sql = f"update shop_film set film_num = {film_num} where shop_name ='{self.active_shop}' and film_id = {film_id}"    
                       self.mycursor.execute(sql)
                       self.film_rent_db.commit()

                       # delete from active_rental table
                       sql = f"delete from active_rental where customer_id = {x[0]} and film_id = {x[1]} and shop_name ='{self.active_shop}'"
                       self.mycursor.execute(sql)
                       self.film_rent_db.commit()
                       print("Successfully done.")
            
     
     
      def manager_dashboard(self):
          
          self.retrieve_shop_name()
        
          print(f"\n\t---------------------------- Welcome to Dashboard -------------------------------------\n Your Shop :{self.shop1} {self.shop2}")
          while True:
                  answer = input("Choose Your Active Shop :")
                  if answer ==self.shop1 or self.shop2:   
                        self.active_shop = answer
                        break 
                  else :      
                        print("invalid shop name!")
                        continue
          while True :
                  print("Enter proper key ....")
                  print("Adding Movie to Shop <am> :")
                  print("Your customers info <ci> :")
                  print("View Reservations <vr>: ")
                  print("View Active Rents <va>:")
                  print("Give Back Confirmation <gc>:")


                  answer = input()
                  if answer == "exit":
                       return True
                  if answer =='am':
                        self.handle_add_movie()
                  elif answer =='ci':
                        self.handle_customer_info()
                  elif answer == 'vr' :
                       self.handle_view_reservations()
                  elif answer == "va" :
                       self.handle_view_active_rent()      
                  elif answer == "gc" :
                       self.handle_give_back_confirmation()            

      
      def handle_visit_shops(self):
           
            #check if customer has delay for more than 10 times 
           sql = f"select * from customer_delay as cd inner join customer_login as cl on cd.customer_id = cl.customer_id where cl.username ='{self.username}'"
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()
           if len(result) > 10:
                print("Your account is banned _ maximum delay limit reached")
                return True
           

           sql = "select shop1,shop2 from man_shop "
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()
           for x in range(len(result)) :
                if result[x][0]:
                  print(result[x][0])
                  if result[x][1]:
                       print[x][1]
            
           while True:
                answer = input("Enter name of shop you want to visit:")
                 
                for x in result :
                  if answer == x[0] or answer == x[1]:

                        # check if rent movies are 3:
                        sql = f"select * from active_rental as ar inner join customer_login as cl on ar.customer_id = cl.customer_id where ar.shop_name  = '{answer}' and  cl.username = '{self.username}'"
                        self.mycursor.execute(sql)
                        result = self.mycursor.fetchall()

                        if len(result) ==3 :
                             print("You have reached maximum limit of rent")
                             return True
                        
                        sql = f"select sf.film_id,sf.shop_name,fi.film_name,fi.genre,fi.product_year,fi.lang,sf.film_num from film_info as fi inner join shop_film as sf on fi.film_id = sf.film_id where sf.shop_name ='{answer}'"   
                        self.mycursor.execute(sql)
                        result = self.mycursor.fetchall()

                        for x in result :
                              print(x)
                        
                        while True:
                              answer = input("Enter name of movie you want to reserve: ")
                              #while True:
                              rental_days = int(input("How many days do you wanna to reserve (max =14 , min=1) : "))
                              if rental_days<=14 and rental_days>1:
                                          print(f"rental cost = {rental_days*2} dollars")
                                          for x in result:
                                           if answer ==x[2]:
                                                if x[6]>0:
                                                      
                                                      sql = f"select customer_id from customer_login where username = '{self.username}'"
                                                      self.mycursor.execute(sql)
                                                      customer_id = self.mycursor.fetchall()
                                                      sql = f"insert into customer_reserve (customer_id,shop_name,film_id,rental_days) values({customer_id[0][0]},'{x[1]}',{x[0]},{rental_days})"   
                                                      self.mycursor.execute(sql)
                                                      self.film_rent_db.commit()
                                                      print("movie successfully reserved!")
                                                      return True
                                                else:
                                                      print("sold out!")
                                                      continue
                                   
                                          print("not found!")
                              else :
                                         print("invalid rental days")
                                         continue
                  else :
                        continue


      
      def handle_view_active_rent(self):
           sql = f"select fi.film_name,cl.username,ar.rental_date,ar.rental_days from film_info as fi inner join active_rental as ar on fi.film_id = ar.film_id inner join customer_login as cl on cl.customer_id =ar.customer_id where ar.shop_name = '{self.active_shop}'"
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()

           for x in result :
                print(x)

           print("\n")
           


      def handle_give_back(self):
           #show customer`s active rents
            sql = f"select ar.film_id,ar.customer_id,ar.shop_name,fi.film_name,ar.rental_date,ar.rental_days from active_rental as ar inner join customer_login as cl on ar.customer_id = cl.customer_id inner join film_info as fi on fi.film_id = ar.film_id where cl.username='{self.username}'"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()

            print("Your Active Rents : ")
            for x in result :
                 print(x)

            shop_name,film_name = input("Enter shop_name and film_name you want to give back (seperate by ',') (E,E to Exit): ").split(",")
            if shop_name =="E" and film_name =="E":
                 return True
            
            for x in result :
                 if x[2] == shop_name and x[3]==film_name:
                        film_id = x[0]
                        customer_id = x[1]

                        sql = f"update active_rental set status = -1 where film_id = {film_id} and customer_id = {customer_id} and shop_name = '{shop_name}'"
                        self.mycursor.execute(sql)
                        self.film_rent_db.commit()

                        # give score to film
                        while True:
                              score = int(input("Enetr score of movie you give <out of 10>: "))

                              if score >10 or score <0:
                                   continue

                              sql = f"insert into film_score values ({film_id},'{shop_name}',{customer_id},{score})"
                              self.mycursor.execute(sql)
                              self.film_rent_db.commit()

                              break

                        print("Your request is recorded successfully!")




      def handle_edit_profile(self):
           sql = f"select * from customer_login where username = '{self.username}' "
           self.mycursor.execute(sql)
           result = self.mycursor.fetchall()

           for x in result:
                print(x)

           username ,password,age,gender= input("Enter your new profile info seperated by ',': ").split(",")

           sql = f"UPDATE customer_login SET username = '{username}', pass= '{password}' , age ={age},gender = '{gender}' WHERE customer_id ={result[0][0]} "      
           self.mycursor.execute(sql)
           self.film_rent_db.commit()



      def customer_dashboard(self):
           print("\n\t--------------------- WELCOME TO DASHBOARD -------------------------")
           while True :
                  print("Enter proper key ....")
                  print("Visit Shops and Reservation <vs> :")
                  print("Edit Profile <ep> :")
                  print("Give Back Movie <gb>:")
                  answer = input()
                  if answer == "exit":
                       return True
                  elif answer == "vs":
                       self.handle_visit_shops()
                  elif answer == "gb":
                        self.handle_give_back()
                  elif answer == "ep":
                       self.handle_edit_profile()

                

################################      MAIN      ########################################

obj = film_rent()


while True:
      answer = obj.handle_valid_command()
      if answer == 's':
            obj.handle_signup()
      elif answer == 'l':
            obj.handle_login()
            if obj.role == "manager" :
                  obj.manager_dashboard()
            else :
                  obj.customer_dashboard()

        


