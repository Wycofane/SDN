import initialize
import jsonHelper
from logger import logger
import variable


def jsonGet(url):
    # perform get request
    data = initialize.get_request(url)
    # transform bytes to json object
    obj, data = jsonHelper.byteToJson(data)

    # logging the action for later problem solving (if br0k3n)
    logger("rest-API request: /dataservice/" + url)

    # return both objects
    return obj, data


def addDevicesToGui():
    site = ""

    # ask cisco for the devices then write the json answer to a global variable
    resp, data = jsonGet("device")
    variable.deviceData = data

    logger(data)
    i = 1

    for value in variable.deviceData['data']:
        deviceID = value['deviceId']
        hostname = value['host-name']
        reachable = value['reachability']
        status = value['status']

        # write the informations to the logger (debug)
        logger(deviceID + " " + hostname + " " + reachable + " " + status)

        # change the colors of the border if the cisco device is online
        if status == "normal":
            variable.border = """border-success"""
        else:
            variable.border = """border-danger"""

        # append every device to the site and build it with the variables
        site = site + """
            
            <div class="col-sm">
                <div class="card border """ + variable.border + """ border-4 mb-3">
                      <div class="card-body border border-5">
                            <h5 class="card-title">""" + hostname + """</h5>
                            <p class="card-text">Status: """ + status + """</p>
                            <p class="card-text">Erreichbarkeit: """ + reachable + """</p>
                            <p class="card-text">Device ID: """ + deviceID + """</p>
                            <form action="" method="post">
                                <a href="/controlpanelAction?id=""" + str(i) + """" class="btn btn-primary" type="submit">Neustarten</a>
                            </form>
                      </div>
				</div>
			</div>
        """

        """
        Normalerweise würde der Neustart aufruf funktionieren. Aber Cisco erlaubt in der Always-ON Sandbox keine ändernungen:
        Access forbidden: role not allowed{"error":{"message":"Forbidden","details":"User does not have permission to access this resource","code":"DS0001"}}
        """

        # put the build site in a global context
        variable.site = site

        i = i + 1


# the main building of the site with a frame and the dynamic content
def buildSiteCP():
    variable.controlpanel = """
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    
        <link rel="stylesheet" href="//wycofane.de/static/css/Wycofane.css">
        <link rel="stylesheet" href="file:///C:/Users/Julian/LogInSystem/static/css/Wycofane.css">
    
        <link rel="apple-touch-icon" sizes="57x57" href="//wycofane.de/static/img/pics/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="//wycofane.de/static/img/pics/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="//wycofane.de/static/img/pics/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="//wycofane.de/static/img/pics/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="//wycofane.de/static/img/pics/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="//wycofane.de/static/img/pics/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="//wycofane.de/static/img/pics/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="//wycofane.de/static/img/pics/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="//wycofane.de/static/img/pics/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192"  href="//wycofane.de/static/img/pics/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="//wycofane.de/static/img/pics/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="//wycofane.de/static/img/pics/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="//wycofane.de/static/img/pics/favicon-16x16.png">
        <link rel="manifest" href="//wycofane.de/static/img/pics/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="//wycofane.de/static/img/pics/ms-icon-144x144.png">
        <meta name="theme-color" content="#ffffff">
    
    
        <script src="https://kit.fontawesome.com/8223c4836d.js" crossorigin="anonymous"></script>
    
        <title>Wycofane</title>
      </head>
      <body>
        <nav class="navbar sticky-top navbar-expand-lg navbar-dark" style="background-color: #1A0C2B;">
          <div class="container-fluid">
            <a class="navbar-brand" href="/">
            <img src="//wycofane.de/static/img/wycofane.png" width="50" height="50" class="d-inline-block align-top" alt="wycofane logo" onerror="this.src='img/wycofane.png'">
                Wycofane
            </a>
    
    
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
            </div>
              <form class="d-flex">
                  <a href="/logout" class="btn btn-outline-primary" role="button">Logout</a>
              </form>
          </div>
        </nav>
    
        <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #291344;">
          <div class="container-fluid">
    
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown2" aria-controls="navbarNavDropdown" aria-expanded="false" aria label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
    
            <div class="collapse navbar-collapse" id="navbarNavDropdown2">
              <ul class="navbar-nav">
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
    
                <li class="nav-item">
                      <a class="nav-link" href="/home"><i class="bi bi-controller"></i> Home</a>
                </li>
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                  &nbsp;
                <li class="nav-item">
                      <a class="nav-link" href="/bonus"><i class="bi bi-hdd-stack"></i> Bonus</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        <div class="container-fluid" >
            <div class="container-md">
                &nbsp;
                &nbsp;
                &nbsp;
                <div class="row">
                    """ + variable.site + """  
                </div>
              &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
			  &nbsp;
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
      </body>
    </html>
    """
