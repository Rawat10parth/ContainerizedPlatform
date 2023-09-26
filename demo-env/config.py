class Config:

    #Mongo db Connection url
    MONGO_DB_CONNECTION = ''

    #API Configs
    API_PATH = '/api/'
    API_VERSION = 'v1'
    BASE_URL = 'http://127.0.0.1:5000'

    #User API Endpoint
    SIGN_IN = API_PATH+API_VERSION+'/sign_in'
    SIGN_UP = API_PATH+API_VERSION+'/sign_up'
    USER_PROFILE = API_PATH+API_VERSION+'/profile/<string:username>'
    