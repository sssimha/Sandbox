'''
*******************************************************************************
Module DOCSTRING: Tries to run a delayed action
'''
import time
import urllib
import json
import dicttoxml
import requests as req

from payload_def import ParamLocation

urlencode = urllib.parse.urlencode
PARAMS = {}

def main():
    """ Tries to run a delayed action """
    # global pkg
    for i in range(1, 5):
        time.sleep(0.6)
        try_it(i)
    # print(type(pkg))

def try_it(i):
    print('this is the %dth attempt', i)

def run_request(request_compl_dict):
    s = req.Session()

    url_params = strip_vars(request_compl_dict['_meta']['params'], \
                                True, url_param_meta_parser)
    url_params_string = urlencode(url_params)
    rqst = req.Request(request_compl_dict['method'], \
                        request_compl_dict['host'] + \
                        request_compl_dict['endpoint'] +\
                        ('' if url_params_string == '' else '?') +\
                        url_params_string)
    prepd_reqst = s.prepare_request(rqst)

    hdrs = strip_vars(request_compl_dict['hdrs'])
    prepd_reqst.prepare_headers(hdrs)

    body_json_params = strip_vars(request_compl_dict['_meta']['params'], \
                                    True, \
                                    body_json_param_meta_parser)
    body_json_params_string = json.dumps(body_json_params)
    
    xml_coll_name = lambda x: x[:-1]
    body_form_params_string = ''
    body_json_params_string = ''
    body_xml_params_string = ''
    body_xml_params = strip_vars(request_compl_dict['_meta']['params'], \
                                    True, \
                                    body_xml_param_meta_parser)
    body_xml_params_string = dicttoxml.dicttoxml(body_xml_params, \
                                        attr_type=False, \
                                        root=False, \
                                        item_func=xml_coll_name).decode('ascii')

    body_form_params = strip_vars(request_compl_dict['_meta']['params'], \
                                    True, \
                                    body_form_param_meta_parser)
    body_form_params_string = urlencode(body_form_params)

    num_bodies = (0 if body_form_params_string == '' else 1) +\
                    (0 if body_json_params_string == '' else 1) +\
                    (0 if body_xml_params_string == '' else 1)
    data = '' if num_bodies > 1 else body_json_params_string +\
                                        body_form_params_string +\
                                        body_xml_params_string
    files = {'json_file':('json_file',\
                        body_json_params_string, 'application/json', None), \
            'xml_file':('xml_file',
                        body_xml_params_string, 'application/xml', None), \
            'form_file':('form_file', body_form_params_string,\
                        'application/x-www-form-urlencoded', None)}
    print('')
    if num_bodies > 1:
        prepd_reqst.prepare_body(data=None, files=files)
    else:
        prepd_reqst.prepare_body(data=data, files=None)
    
    start_time = time.gmtime()
    responses = s.send(prepd_reqst)
    end_time = time.gmtime()
    
    line1_txt = prepd_reqst.method + ' ' + request_compl_dict['endpoint'] +\
            ('' if url_params_string == '' else '?') + \
            url_params_string + ' HTTP/1.1'
    line2_txt = 'HOST: ' + request_compl_dict['host']
    line1_lim = 66 if len(line1_txt) > 66 else len(line1_txt)
    line2_lim = 66 if len(line2_txt) > 66 else len(line2_txt)
    
    print(time.strftime("> %Y-%m-%d %H:%M:%S GMT", start_time))
    
    print('> ' + '\n>   [contd.] '.join(\
        [line1_txt[i:i+line1_lim] for i in range(0, \
                len(line1_txt), line1_lim)]))
    print('> ' + '\n>   [contd.] '.join(\
        [line2_txt[i:i+line2_lim] for i in range(0, \
                len(line2_txt), line2_lim)]))
    
    for h in prepd_reqst.headers:
        hline_txt = h + ': ' + prepd_reqst.headers[h]
        hline_lim = 66 if len(hline_txt) > 66 else len(hline_txt)
        print('> ' + '\n>   [contd.] '.join(\
            [hline_txt[i:i+hline_lim] for i in range(0, \
                len(hline_txt), hline_lim)]))
    print('> ')
    body_lines = prepd_reqst.body.decode('ascii') if \
                type(prepd_reqst.body) == bytes else str(prepd_reqst.body)
    body_line_split = body_lines.replace('\r\n','\n').split('\n')
    for body_txt in body_line_split:
        body_lim = 66 if len(body_txt) > 66 else len(body_txt)
        print('> ' + '\n>   [contd.] '.join(\
            [body_txt[i:i+body_lim] \
            for i in range(0,len(body_txt), body_lim)]))
    
    resp_list = []
    
    if responses.history:
        resp_list.extend(responses.history)
    else:
        resp_list.append(responses)
    
    for resp in resp_list:
        line3_txt = 'HTTP/1.1 ' + str(resp.status_code) + ' ' + \
            'OK' if resp.ok else resp.reason
        line3_lim = 66 if len(line3_txt) > 66 else len(line3_txt)
        
        print('')
        print(time.strftime("< %Y-%m-%d %H:%M:%S GMT", end_time))
        print('< ' + '\n<   [contd.] '.join(\
            [line3_txt[i:i+line3_lim] \
            for i in range(0,len(line3_txt),line3_lim)
            ]))
        for h in resp.headers:
            hline_txt = h + ': ' + resp.headers[h]
            hline_lim = 66 if len(hline_txt) > 66 else len(hline_txt)
            print('< ' + '\n<   [contd.] '.join(\
                [hline_txt[i:i+hline_lim] for i in range(0, \
                    len(hline_txt), hline_lim)] ))
        print('<')
        body_lines = resp.text.decode('ascii') if \
                    type(resp.text) == bytes else str(resp.text)
        body_line_split = body_lines.replace('\r\n','\n').split('\n')
        for body_txt in body_line_split:
            body_lim = 66 if len(body_txt) > 66 else len(body_txt)
            print('< ' + '\n<   [contd.] '.join(\
                [body_txt[i:i+body_lim] \
                for i in range(0,len(body_txt), body_lim)]))

def strip_vars(param_compl_dict, meta_passed_only=True, meta_parser=None):
    res = {}
    def basic_meta_parser(m):
        return m['enabled']
    if (meta_parser is None):
        meta_parser = basic_meta_parser
    for key in param_compl_dict:
        if (meta_parser(param_compl_dict[key][1]['_meta']) \
            or (not meta_passed_only)):
            res[key] = param_compl_dict[key][0]
    return res

def url_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Url_Form) and \
                m['enabled'])

def body_form_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Body_Form) and \
                m['enabled'])

def body_json_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Body_Json) and \
                m['enabled'])

def body_xml_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Body_Xml) and \
                m['enabled'])
