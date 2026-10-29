# TP 1 : Networks and Systems Administration
By : Rym Lemmouchi, M1/G1 Networks and Embedded Systems

---
## Project structure : 
    -- files tree

## Architecture :
    -- mermaid diagram describing how the files/classes relate to each other

### Protocol Definition : 
    characters used : ASCII only
    registration: NAME:<client_name>:<client|sensor>
    sensors register as sensor and send TEMP:<value> or HUM:<value>
    clients send TEMP, HUM, BOTH or EXIT; the server responds with readings or ERROR

### Socket : 
    MESSAGE MessageBuilder(SENDER, RECEIVER, COMMAND, VALUE),
    (SENDER, RECEIVER, COMMAND, VALUE) MessageReceiver(MESSAGE),
    MessageValidityCheck() ?

### Sensors :
    Socket,
    uint RandomReadingGenerator() 


### Server : 


### Client :
    Socket,
    RequestConnexion
    RequestData
    ReceiveData
    DisplayData -- simple console
