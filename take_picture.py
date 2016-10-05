import mbed_connector_api
from time import sleep

api_token = # Add value here
endpoint = # Add value here


# Initialization
import mbed_connector_api
x = mbed_connector_api.connector(api_token)
x.startLongPolling()

res = x.postResource(endpoint, "/3/0/11002")
while not res.isDone():
    sleep(0.001)

# Use
#x.getEndpoints() # returns a  list of all endpoints on your domain
#x.getResources(endpoint) # returns all resources of an endpoint
res = x.getResourceValue(endpoint, "/3/0/11002") # send the "Value" to the "Resource" over a PUT request
while not res.isDone():
    sleep(0.001)



if not res.error:
    print("Read value")
    with open("image.jpg", "wb") as file_handle:
        file_handle.write(res.result)
else:
    print("Error : %s", res.error.error)

