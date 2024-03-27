# plants watering control with Azure

* Azure IoT architecture
<center>
<img src="images/iot-refarch.PNG" alt="" > 
</center>

<br>


* demos
    - with cli to send commands [link](https://www.youtube.com/watch?v=tQTMoHhKo98)

    - with serverless [link](https://www.youtube.com/watch?v=WdupkN_S0Lg)

* Azure services
    - Azure IoT hub
    - Azure serverless
    - Azure Functions (IoT Hub event trigger)
    - Azurite
    - Azure Storage

* Tools
    - python programming language
    - counterfit (virtual devices)
    - X.509 certificates to Secure IoT devices
* to run the code :

    ### you have two folders in this project soil-moisutre-sensor and soil-moisutre-trigger. each folder have `requirements.txt`

    ### -->>> open `soil-moisutre-sensor folder` with any ide and do these steps to install packages
    ```sh
    python3 -m venv .venv
    ```
    ```sh
    .venv\Scripts\activate.bat
    ```
    ```sh
    pip install -r requirements.txt
    ```
    --> to run virtual sensors
    ```sh
    counterfit
    ```
    go to http://localhost:5000/ and add `soil moisture sensor and relay`

    ## to connect the device to the cloud:

    ### 1- install the Azure CLI from here [ Azure CLI documentation](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?WT.mc_id=academic-17441-jabenn)

    ### 2- Install the IoT extension by running

    ```sh
    az extension add --name azure-iot
    ```
    ### 3- log in to your Azure subscription from the Azure CLI
    ```sh
    az login
    ```
    the output will be like that
    ```output
    ➜  ~ az account list --output table
    Name                    CloudName    SubscriptionId                        State    IsDefault
    ----------------------  -----------  ------------------------------------  -------  -----------
    School-subscription     AzureCloud   cb30cde9-814a-42f0-a111-754cb788e4e1  Enabled  True
    Azure for Students      AzureCloud   fa51c31b-162c-4599-add6-781def2e1fbf  Enabled  False
    ```
    ### 4- select the subscription you want to use, Replace `<SubscriptionId>` with the Id of the subscription you want to use
    ```sh
    az account set --subscription <SubscriptionId>
    ```
    ### 5- create a resource group
    ```sh
    az account list-locations --output table
    ```
    You will see a list of locations
    ```output
        ➜  ~ az account list-locations --output table
    DisplayName               Name                 RegionalDisplayName
    ------------------------  -------------------  -------------------------------------
    East US                   eastus               (US) East US
    East US 2                 eastus2              (US) East US 2
    South Central US          southcentralus       (US) South Central US
    ...
    ```
    ```sh
    az group create --name <resourceGroupName> --location <location>
    ```
    resourceGroupName have to be unique in your subscription.

    Replace `<location>` with the location you selected in the previous step.
    
    ### 6- create an IoT Hub
    ```sh
    az iot hub create --resource-group <resourceGroupName> --sku F1 --partition-count 2 --name <hub_name>
    ```
    Replace `<hub_name>` with a name for your hub. This name needs to be globally unique - that is no other IoT Hub created by anyone can have the same name. This name is used in a URL that points to the hub, so needs to be unique.
    ### 7- register your IoT device
    ```sh
    az iot hub device-identity create --device-id <deviceID> --hub-name <hub_name>
    ```
    set `<deviceID>` as you want

    Run the following command to get the connection string:
    ```sh
    az iot hub device-identity connection-string show --device-id <deviceID> --output table --hub-name <hub_name>
    ```
    Store the connection string that is shown in the output as you will need it later.
    ### 8- run the `app.py` file in soil-moisture-sensor->virtual-device folder, but Replace `connection_string` with you get in the previous step.

    ### 9- monitor events
    Run the following command in your command prompt or terminal
    ```sh
    az iot hub monitor-events --hub-name <hub_name>
    ```
    ### 10-  control your IoT device
    ```sh
    az iot hub invoke-device-method --device-id <deviceID> --method-name relay_on --method-payload '{}' --hub-name <hub_name>
    ```
    Repeat the above step, but set the --method-name to relay_off. 
    ### 11- for `secure` connection and data

    1- go to folder virtual-device-secure
    ```sh
    cd virtual-device-secure
    ```
    2- create a device identity using an X.509 certificate
    ```sh
    az iot hub device-identity create --device-id <deviceIDWithx509> --am x509_thumbprint --output-dir . --hub-name <hub_name>
    ```
    3- run app.py file in soil-moisture-sensor->`virtual-device-secure folder`, but Replace `host_name and device_id` with your.

    * your code should work as this demo [link](https://www.youtube.com/watch?v=tQTMoHhKo98)

    ## to upload server code and use serverless service

    ### -->>> open `soil-moisutre-trigger folder` with any ide and do these steps to install packages
    ```sh
    python3 -m venv .venv
    ```
    ```sh
    .venv\Scripts\activate.bat
    ```
    ### 1- install the Azure Functions core tools by following the instructions on the [Azure Functions Core Tools documentation](https://docs.microsoft.com/azure/azure-functions/functions-run-local?WT.mc_id=academic-17441-jabenn)

    ### 2- Run the following command to create a Functions app 
     ```sh
    func init --worker-runtime python soil-moisture-trigger
    ```
    This will create three files inside the current folder
    `host.json`, `local.settings.json`,  `requirements.txt`
    ### 3- Install the necessary Pip packages
    ```sh
    pip install -r requirements.txt
    ```
    ### 4- get the Event Hub compatible endpoint connection string
     ```sh
    az iot hub connection-string show --default-eventhub --output table --hub-name <hub_name>
    ```
    ### 5- open the `local.settings.json` file. Add the following additional value inside the `Values` section:
    ```json
    "IOT_HUB_CONNECTION_STRING": "<connection string>"
    ```
     Replace `<connection string>` with the value from the previous step.

     ### 6- create an event trigger
     * first delete this file `function_app.py`
     ```sh
    func new --name <any Name> --template "Azure Event Hub trigger"
    ```
    This will create a folder inside the soil-moisture-trigger folder called `<any Name>` that contains `__init__.py`and  `function.json`
    ### 7- Update these fields in `function.json`
    ```json
    "connection": "IOT_HUB_CONNECTION_STRING",
    ```
     ```json
    "eventHubName": "",
    ```
    ### 8- replace `__init__.py` code with `__init__.py` code in `iot-hub-trigger` folder

    ### 9- get the Registry Manager connection string
     ```sh
    az iot hub connection-string show --policy-name service --output table --hub-name <hub_name>
    ```
    open the `local.settings.json` file. Add the following additional value inside the `Values` section:

    ```json
    "REGISTRY_MANAGER_CONNECTION_STRING": "<connection string>"
    ```
    Replace <connection string> with the value from the previous command step
    ### 10- Create a storage account:

    ```sh
    az storage account create --resource-group <resourceGroupName> --sku Standard_LRS --name <storage_name> 
    ```
    ### 11- create a Function App:

    ```sh
    az functionapp create --resource-group <resourceGroupName> --runtime python --functions-version 3 --os-type Linux --consumption-plan-location <location> --storage-account <storage_name> --name <functions_app_name>
    ```
    set the `IOT_HUB_CONNECTION_STRING` setting in the Functions App Application Settings:

    ```sh
    az functionapp config appsettings set --resource-group <resourceGroupName> --name <functions_app_name> --settings "IOT_HUB_CONNECTION_STRING=<connection string>"
    ```
    Replace <connection string> with the value of IOT_HUB_CONNECTION_STRING from your local.settings.json file.
    
    ```sh
    az functionapp config appsettings set --resource-group <resourceGroupName> --name <functions_app_name> --settings "REGISTRY_MANAGER_CONNECTION_STRING=<connection string>"
    ```
    set the value of `REGISTRY_MANAGER_CONNECTION_STRING` to the corresponding value from your `local.settings.json` file.

    ### 12-  deploy your Functions App to the cloud
    before deploy you should test your function locally 
    
    so we will use azurite as locall storage

    install it and you should have node js installed at your machine 
    ```sh
    npm install -g azurite
    ```
    ```sh
    azurite --location azurite
    ```
    it will create folder named azurite

    ### -->> noe you can run your function and test it
    ```sh
    func start
    ```
    after testing your function deploy it to cloud
    ```sh
    func azure functionapp publish <functions_app_name>
    ```
    There will be a lot of console output, ending in confirmation of the deployment and a list of the functions deployed
    ```output
    Deployment successful.
    Remote build succeeded!
    Syncing triggers...
    Functions in <resourceGroupName>:
    <trigger Name> - [eventHubTrigger]
    ```
    * your code should work as this demo [link](https://www.youtube.com/watch?v=WdupkN_S0Lg)

    ## after finish you should remove resource group from your account 
    ```sh 
    az group delete --name <resource-group-name>
    ```
    ```sh
    Are you sure you want to perform this operation? (y/n): 
    ```
    Enter <b>y</b> to confirm and delete the Resource Group. It will take a while to delete all the services.