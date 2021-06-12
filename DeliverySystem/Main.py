# James Lett Student ID: #001550735

import csv
import datetime
#Graph to store all the distance values between addresses
class AddressGraph:
    def __init__(self):
        self.address_distances = {}
    
    def __str__(self):
        string = ""
        for item in self.address_distances:
           string += str(item)
           string += " : "
           string += str(self.address_distances[item])
           string += "\n"
        return string
#add a directed edge to the graph          
    def add_directed(self,vertex1,vertex2,weight = 1):
        self.address_distances[vertex1,vertex2] = float(weight)
#add undirected address edge to graph   
    def add_undirected(self,vertex1,vertex2,weight = 1):
        self.add_directed(vertex1,vertex2,weight)
        self.add_directed(vertex2,vertex1,weight)
#returns the dictionary for the graph  
    def get_address_distances(self):
        return self.address_distances
#Looks up the distance between two addresses should be O(1)
    def lookup_distance(self,address1,address2):
        return self.address_distances[address1,address2]

#Hash table to store the packages self adjusting for bucket size
class PackageHashTable:
    def __init__(self,buckets = 10):
        self.table = []
        for bucket in range(buckets):
            self.table.append([])

    def __str__(self):
        string = ""
        for item in self.table:
           
            for package in item:

                string += str(package)
      
           
        return string
#Inserts a package into the hash table
    def insert_package(self,package_id,address,city,zip,weight,status = "At Hub",delivery_deadline = None):
         package = Package(package_id,address,city,zip,weight,status,delivery_deadline)
         bucket = package.package_id % len(self.table)
         self.table[bucket].append(package)
#removes a package from the hash table O(N) worse case
    def remove_package(self,package):
        bucket = package.package_id % len(self.table)
        self.table[bucket].remove(package)
#returns a package from the hash table O(N) worse case

    def get_package(self,package_id):
        bucket = package_id % len(self.table)
        for package in self.table[bucket]:
            if package.package_id == package_id:
                return package
        return False

#returns a list of all items in the hash table O(N)
    def all_packages(self):
        temp_list = []
        for bucket in self.table:
            for item in bucket:
                temp_list.append(item)
        return temp_list




#Package class to store package info
class Package:
    def __init__(self,package_id,address,city,zip,weight,status = "At Hub",delivery_deadline = None):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.delivery_deadline = delivery_deadline
        self.delivered = False
        self.status = status
        self.truck_number = None
        self.delivery_time = None
        self.loaded_time = None
        self.zip = zip
        self.weight = weight
    def __str__(self):
        string = ""
        string += "Package ID: " + str(self.package_id) + "\n"
        string += "Delivery Address: "  + str(self.address) + "\n"
        string += "Truck Number : " + str(self.truck_number) + "\n"
        string += "Loaded at : " + str(self.loaded_time) + "\n"
        string += "Status: " + str(self.status)
        if(self.delivered):
            string += " at " + str(self.delivery_time) + "\n"
        else:

            string += "\n"
        return string
#Takes a time and prints the status of the package at that time
    def print_status(self,time):
        if time >= self.delivery_time:
            print(str(self))
        elif time >= self.loaded_time:
            string = ""
            string += "Package ID: " + str(self.package_id) + "\n"
            string += "Delivery Address: "  + str(self.address) + "\n"
            string += "On Truck Number : " + str(self.truck_number) + "\n"
            string += "Loaded at : " + str(self.loaded_time) + "\n"
            string += "Status: En Route"  +"\n"
            print(string)
        else:
            string = ""
            string += "Package ID: " + str(self.package_id) + "\n"
            string += "Delivery Address: "  + str(self.address) + "\n"
            string += "Status: At Hub" +"\n"
            print(string)

            

#Setters and getters
    def get_status(self):
        return self.status
    def set_status(self,status):
        self.status = status
    def set_delivery_time(self,time):
        self.delivery_time = time
    def set_delivered(self):
        self.delivered = True
    def get_address(self):
        return self.address




#Basic class for the truck, stores the speed,location and time
class Truck:
    def __init__(self, truck_id,start_time):
        self.truck_id = truck_id
        self.packages = []
        self.speed = 18
        self.current_location = "Hub"
        self.next_location = None
        self.start_time = start_time
        self.current_time = start_time
        self.max_packages = 16
        self.miles_traveled = 0
        self.packages_delivered = 0
#returns a bool if the truck is full or not
    def is_full(self):
        return bool(len(self.packages)>= self.max_packages)
#Adds a package to the truck and sets package to enroute
    def add_package(self,package):
        package.status = "En Route"
        package.loaded_time = self.current_time
        package.truck_number = self.truck_id
        self.packages.append(package)
#Returns all packages currently on the truck
    def get_packages(self):
        return self.packages

#The core algorithm for the delivery takes all of the packages on the truck and finds the one that is closest to the trucks current location.
#The function then uses the graph to find the distance between the current location and the next location.
#After that it calculates the time it will take to travel the distance and adds that to the trucks current time.
#The function then sets the current location to the location of the delivery and removes the package that was delivered
#The time complexity of this function should be O(N) however,delivering all of the packages will be O(N^2)
    def deliver_package(self,distances):
        distance = 0;
        selected_package = None

        if len(self.packages)> 0:
            self.next_location = self.packages[0].get_address()
            for package in self.packages:
                if (distances.lookup_distance(self.current_location,package.get_address()) 
     <= distances.lookup_distance(self.current_location,self.next_location)):
                    self.next_location = package.get_address()
                    selected_package = package
            distance = distances.get_address_distances()[self.current_location,self.next_location]
            print(str(distance) + " Distance")
            print(self.current_time)
            self.current_time = self.current_time + datetime.timedelta(hours = distance/ self.speed)
            selected_package.set_status("Delivered")
            selected_package.set_delivered()
            selected_package.set_delivery_time(self.current_time)
            self.current_location = self.next_location
            self.packages.remove(selected_package)
            self.miles_traveled += distance
            self.packages_delivered += 1
            print(str(selected_package))
            print(str(self.miles_traveled))
#This method delivers all of the packages using the deliver package method which is O(N)
#It calls the deliver_package function until the truck is empty resulting in a time complexity of O(N^2)
#After all packages are delivered it automatically returns to the hub and calculates the distance traveled and new time.
    def deliver_all_packages(self,distances):
        while len(self.packages) > 0:
            self.deliver_package(distances)
        print("Truck ",self.truck_id,"GOING TO HUB")
        self.next_location = "Hub"
        distance = distances.get_address_distances()[self.current_location,self.next_location]
        self.current_time += datetime.timedelta(hours = distance/ self.speed)
        self.miles_traveled += distance
        print("Truck ",self.truck_id," :",self.miles_traveled, " DISTANCE TRAVELED")

            


                
                
#Create the address graph and package hash table

graph = AddressGraph()
hash_table = PackageHashTable()

#Reads all of of the rows in the distances file and adds them to the graph O(N)
with open('distances.csv') as csvfile:
    read = csv.reader(csvfile,delimiter = ',')
    col_labels = []
    row_count = 0
    for row in read:
        if row_count == 0:
           col_labels = row 
        
        else:
            
            for num in range(1,len(row)):
                if(row[num] == ''):
                    break
                else:
                    
                    graph.add_undirected(row[0],col_labels[num],row[num])

            
        row_count += 1
        

#Reads all of the packages into the address hash table O(N)
with open('Packages.csv') as csvfile:
    read = csv.reader(csvfile,delimiter = ",")
    row_count = 0
    for row in read:
        hash_table.insert_package(row[0],row[1],row[2],row[3],row[5],"At Hub",row[4])

        


#Create the trucks

starttime1 = datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,8,0,0)
truck1 = Truck(1,starttime1)
starttime2 = datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,9,5,0)
truck2 = Truck(2,starttime2)
trucks = [truck2,truck1]


packages = hash_table.all_packages()
packages.sort(key = lambda x: x.address)

#Add all the packages with a deadline
truck1.add_package(hash_table.get_package(15))
truck1.add_package(hash_table.get_package(1))
truck1.add_package(hash_table.get_package(13))
truck1.add_package(hash_table.get_package(14))
truck1.add_package(hash_table.get_package(16))
truck1.add_package(hash_table.get_package(20))
truck1.add_package(hash_table.get_package(19))

truck1.add_package(hash_table.get_package(29))
truck1.add_package(hash_table.get_package(30))
truck1.add_package(hash_table.get_package(31))
truck1.add_package(hash_table.get_package(34))
truck1.add_package(hash_table.get_package(37))
truck1.add_package(hash_table.get_package(40))


truck1.deliver_all_packages(graph)

truck1.add_package(hash_table.get_package(25))
truck1.add_package(hash_table.get_package(6))

truck1.deliver_all_packages(graph)

truck1.add_package(hash_table.get_package(9))


truck2.add_package(hash_table.get_package(36))
truck2.add_package(hash_table.get_package(38))
truck2.add_package(hash_table.get_package(3))
truck2.add_package(hash_table.get_package(18))


for package in packages:
    if trucks[0].is_full():
       trucks[0].deliver_all_packages(graph)
       temp = trucks[0]
       trucks[0] = trucks[1]
       trucks[1] = temp
  
    if not package.delivered and package.status != "En Route":
        print(package.status)
        trucks[0].add_package(package)

for truck in trucks:
    truck.deliver_all_packages(graph)



answer = None
while answer != "q":
    print("Type D to see total distance traveled")
    print("Type T to enter a time to see delivery status")
    print("Type A to see all packages and status")
    answer = input("CHOOSE AN OPTION: ").lower()

    if answer[0] == 'd':
        print("TOTAL DISTANCE TRAVELED : ",truck1.miles_traveled+truck2.miles_traveled)
    if answer[0] == 'a':
        packages.sort(key = lambda x: x.package_id)
        for package in packages:
            print(str(package))
    if answer[0] == 't':
        print("Enter the time that you would like to look up package status' or type B to go Back")
        hour = -1
        minute = -1
        while int(hour) <0 or int(minute) < 0 or int(minute) > 59 or int(hour) > 23:
            hour = input("Please enter an hour 0-23: ")
            if hour == 'b' or hour == 'B':
                break
            if not hour.isalpha():
                minute = input("please enter minutes 0-59: ")
            if minute == 'b' or hour == 'B':
                break
            if hour.isalpha() or minute.isalpha():
               hour = -1
               minute = -1
               print("Please enter a valid time")

            if 0 <int(hour) < 24 and 0 < int(minute) < 60: 
                hourstr = str(hour)
                minutestr = str(minute)
                if(int(hour) < 10 ):
                    hourstr = "0"+str(hour)
                if(int(minute) < 10):
                    minutestr = "0"+str(minute)
                print("-------------------------------------------------")
                print("All Packages status at ",hourstr,":",minutestr)
                print("-------------------------------------------------")
                for package in packages:
                    packages.sort(key = lambda x: x.package_id)
                    package.print_status(datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,int(hour),int(minute),0))
            

                

    
    
   


print("Total Packages Delivered : ", truck1.packages_delivered + truck2.packages_delivered)


    
    









