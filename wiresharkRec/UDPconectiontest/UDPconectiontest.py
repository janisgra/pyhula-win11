import pyhula

api = pyhula.UserApi()
print("Connecting to drone...")

api.connect()
print("Connected to drone!")

api.single_fly_takeoff()
print("Drone taking off...")

exit()