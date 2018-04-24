'''
Module DOCSTRING: Helps define Payloads
'''
import payload_def
ParamLocation = payload_def.ParamLocation

PKG_TEMPLATE = { # PAYLOAD NAME: Give_a_name_HERE
    # Define Host here
    'host': 'a',
    # Define endpoint here
    'endpoint': 'b',
    # Define Headers Here
    'method': 'POST',
    # Define Headers Here as a dict of header names to array of
    #  value at 0th position and its meta-extensions
    'hdrs': {
        'Content-Type': [
            'application/json',
            {
                '_meta': {
                    'enabled': True
                }
            }
        ]
    },
    # Define Body here if custom body
    'body': '',
    # Other payload settings
    '_meta': {
        # Define parameters as a dict of param names to array of
        #  value at its 0th position and its meta-extensions
        'params': {
            'refresh_token': [
                '',
                {
                    '_meta': {
                        'enabled': True,
                        'param_loc': ParamLocation.Param_Nowhere
                    }
                }
            ]
        },
    }
}

PKG_GOOGLE_DEV_AUTH = { # PAYLOAD NAME: Device Auth Request for Google Cal
    # Define Host here
    'host': 'https://accounts.google.com',
    # Define endpoint here
    'endpoint': '/o/oauth2/device/code',
    # Define Headers Here
    'method': 'POST',
    # Define Headers Here as a dict of header names to array of
    #  value at 0th position and its meta-extensions
    'hdrs': {
        'Content-Type': [
            'application/x-www-form-urlencoded',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'User-Agent': [
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ]
    },
    # Define Body here if custom body
    'body': '',
    # Other payload settings
    '_meta': {
        # Define parameters as a dict of param names to array of
        #  value at its 0th position and its meta-extensions
        'params': {
            'client_id': [
                '324547397668-3734hug20g3utckov1d61uc9lokftorg' +\
                '.apps.googleusercontent.com',
                {
                    '_meta': {
                        'enabled': True,
                        'param_loc': ParamLocation.Param_Body_Form
                    }
                }
            ],
            'scope': [
                'email https://www.googleapis.com/auth/calendar',
                {
                    '_meta': {
                        'enabled': True,
                        'param_loc': ParamLocation.Param_Body_Form
                    }
                }
            ]
        },
    }
}

GOOGLE_DOT_COM = { # PAYLOAD NAME: Google Request
    # Define Host here
    'host': 'https://www.google.com',
    # Define endpoint here
    'endpoint': '/',
    # Define Headers Here
    'method': 'GET',
    # Define Headers Here as a dict of header names to array of
    #  value at 0th position and its meta-extensions
    'hdrs': {
        'User-Agent': [
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ]
    },
    # Define Body here if custom body
    'body': '',
    # Other payload settings
    '_meta': {
        # Define parameters as a dict of param names to array of
        #  value at its 0th position and its meta-extensions
        'params': {
        },
    }
}

GOOGLE_DEV_AUTH_CHECK = { # PAYLOAD NAME: Give_a_name_HERE
    # Define Host here
    'host': 'a',
    # Define endpoint here
    'endpoint': 'b',
    # Define Headers Here
    'method': 'POST',
    # Define Headers Here as a dict of header names to array of
    #  value at 0th position and its meta-extensions
    'hdrs': {
        'Content-Type': [
            'application/json',
            {
                '_meta': {
                    'enabled': True
                }
            }
        ]
    },
    # Define Body here if custom body
    'body': '',
    # Other payload settings
    '_meta': {
        # Define parameters as a dict of param names to array of
        #  value at its 0th position and its meta-extensions
        'params': {
            'refresh_token': [
                '',
                {
                    '_meta': {
                        'enabled': True,
                        'param_loc': ParamLocation.Param_Nowhere
                    }
                }
            ]
        },
    }
}

TRIPADVISOR_DOT_COM = { # PAYLOAD NAME: Google Request
    # Define Host here
    'host': 'http://www.tripadvisor.com',
    # Define endpoint here
    'endpoint': '/',
    # Define Headers Here
    'method': 'GET',
    # Define Headers Here as a dict of header names to array of
    #  value at 0th position and its meta-extensions
    'hdrs': {
        'User-Agent': [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'Accept': [
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'Accept-Language': [
            'en-US,en;q=0.5',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'Accept-Encoding': [
            'gzip, deflate, br',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'DNT': [
            '1',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'Connection': [
            'keep-alive',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ],
        'Upgrade-Insecure-Requests': [
            '1',
            {
                '_meta':{
                    'enabled': True
                }
            }
        ]
    },
    # Define Body here if custom body
    'body': '',
    # Other payload settings
    '_meta': {
        # Define parameters as a dict of param names to array of
        #  value at its 0th position and its meta-extensions
        'params': {
        },
    }
}
