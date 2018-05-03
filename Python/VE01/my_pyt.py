'''
*******************************************************************************
Module DOCSTRING: Tries to run a delayed action
*******************************************************************************
'''
import time
import datetime as dt
import urllib
import urllib.parse as pr
import json
import dicttoxml
import requests as req

from payload_def import ParamLocation

urlencode = urllib.parse.urlencode
dt1 = dt.datetime
strftime = dt1.strftime
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


def run_request(request_compl_dict, print_response_always=False):
    '''Run a request'''
    # Define session
    s = req.Session()

    # Prepare URL query string
    url_params = strip_vars(request_compl_dict['_meta']['params'],
                            True, url_param_meta_parser)
    url_params_string = urlencode(url_params)
    rqst = req.Request(request_compl_dict['method'],
                       request_compl_dict['host']
                       + request_compl_dict['endpoint']
                       + ('' if url_params_string == '' else '?')
                       + url_params_string)
    prepd_reqst = s.prepare_request(rqst)

    # Prepare headers
    hdrs = strip_vars(request_compl_dict['hdrs'])
    prepd_reqst.prepare_headers(hdrs)

    # Initialize Body strings
    body_form_params_string = ''
    body_json_params_string = ''
    body_xml_params_string = ''

    # Prepare JSON Body
    body_json_params = strip_vars(request_compl_dict['_meta']['params'],
                                  True, body_json_param_meta_parser)
    body_json_params_string = json.dumps(body_json_params)
    body_json_params_string = '' if body_json_params_string == "{}" else\
                                    body_json_params_string

    # Prepare XML Body
    xml_coll_name = lambda x: x[:-1]
    body_xml_params = strip_vars(request_compl_dict['_meta']['params'],
                                True,
                                body_xml_param_meta_parser)
    body_xml_params_string = dicttoxml.dicttoxml(body_xml_params,
                                        attr_type=False,
                                        root=False,
                                        item_func=xml_coll_name).decode(
                                        'ascii')

    # Prepare Form Body
    body_form_params = strip_vars(request_compl_dict['_meta']['params'],
                                    True,
                                    body_form_param_meta_parser)
    body_form_params_string = urlencode(body_form_params)

    # Prepare final body (multi-part if needed)
    num_bodies = (0 if body_form_params_string == '' else 1) +\
                    (0 if body_json_params_string == '' else 1) +\
                    (0 if body_xml_params_string == '' else 1)
    data = '' if num_bodies > 1 else body_json_params_string +\
                                        body_form_params_string +\
                                        body_xml_params_string
    files = {'json_file': ('json_file',
                        body_json_params_string, 'application/json', None),
            'xml_file': ('xml_file',
                        body_xml_params_string, 'application/xml', None),
            'form_file': ('form_file', body_form_params_string,
                        'application/x-www-form-urlencoded', None)}
    if num_bodies > 1:
        prepd_reqst.prepare_body(data=None, files=files)
    else:
        prepd_reqst.prepare_body(data=data, files=None)

    # Initialize request/response chain
    req_resp_list = []
    req_ersp_timelog = []
    continue_loop = True
    responses = None

    # Send request till no redirects
    while continue_loop:
        start_time = dt1.utcnow()
        responses = s.send(prepd_reqst, allow_redirects=False)
        end_time = dt1.utcnow()
        # Append request, response tuple to list
        req_resp_list.append((prepd_reqst, responses))
        # Append the appropriate start and end time tuple into the list
        req_ersp_timelog.append([start_time, end_time])
        # Flags to end/continue loop
        continue_loop = responses.is_redirect
        prepd_reqst = responses.next

    # Initialize counter to process request/response chain
    req_resp_idx = 0

    # Loop to iterate over each request, response pair and print the output
    for (reqst, resp) in req_resp_list:
        # Separate out multiple requests
        if req_resp_idx > 0:
            print('')
        p1 = pr.urlparse(reqst.url)
        # Generate first line of resquest with the method, HTTP version and
        # the resource being sought
        line1_txt = reqst.method + ' ' + p1.path + \
                ('' if p1.params == '' else ';' + p1.params) + \
                ('' if p1.query == '' else '?' + p1.query) + \
                ('' if p1.fragment == '' else '#' + p1.fragment) + \
                ' HTTP/1.1'
        # Generate second line of request with Host name
        line2_txt = 'HOST: ' + ((p1.scheme+':') if p1.scheme != '' else '') + \
                        '//' + p1.netloc
        # Determine if lines need to be split
        line1_lim = 66 if len(line1_txt) > 66 else len(line1_txt)
        line2_lim = 66 if len(line2_txt) > 66 else len(line2_txt)

        # Start printing request details
        # Request send time
        print(strftime(req_ersp_timelog[req_resp_idx][0],
                "> %Y-%m-%d %H:%M:%S.%f GMT"))

        # Print line 1: Method, resource, HTTP version
        print('> ' + '\n>   [contd.] '.join(
            [line1_txt[i:i+line1_lim] for i in range(0,
                    len(line1_txt), line1_lim)]))
        # Print line 2: Hostname
        print('> ' + '\n>   [contd.] '.join(
            [line2_txt[i:i+line2_lim] for i in range(0,
                    len(line2_txt), line2_lim)]))

        # Print Headers
        for h in reqst.headers:
            # Header output is generated as a line
            hline_txt = h + ': ' + reqst.headers[h]
            # Determine if lines need to be split
            hline_lim = 66 if len(hline_txt) > 66 else len(hline_txt)
            # Print Header
            print('> ' + '\n>   [contd.] '.join(
                [hline_txt[i:i+hline_lim] for i in range(0,
                    len(hline_txt), hline_lim)]))
        # Print separator
        print('> ')
        # Generate body lines as ascii text string
        body_lines = reqst.body.decode('ascii') if \
                    type(reqst.body) == bytes else str(reqst.body)
        # Split body by line into a list
        body_line_split = body_lines.replace('\r\n', '\n').split('\n')
        # Print each body line
        for body_txt in body_line_split:
            # Determine if body line needw to be split
            body_lim = 66 if len(body_txt) > 66 else len(body_txt)
            print('> ' + '\n>   [contd.] '.join(
                [body_txt[i:i+body_lim]
                for i in range(0, len(body_txt), body_lim)]))

        # Start preparing response details
        # Determine response HTTP version, status code and text (line 1)
        line3_txt = 'HTTP/' + repr(resp.raw.version/10) +\
            ' ' + str(resp.status_code) + ' ' + resp.reason
        # Determine if line 1 of response needs to be split
        line3_lim = 66 if len(line3_txt) > 66 else len(line3_txt)

        # Print a separator between Request and response
        print('')
        # Print response recd & processed time
        print(strftime(req_ersp_timelog[req_resp_idx][1],
                "< %Y-%m-%d %H:%M:%S.%f GMT"))
        # Print line 1 of response
        print('< ' + '\n<   [contd.] '.join(
            [line3_txt[i:i+line3_lim]
            for i in range(0, len(line3_txt), line3_lim)]))
        # Print response headers
        for h in resp.headers:
            # Prepare response header type and content
            hline_txt = h + ': ' + resp.headers[h]
            # Determine if response header line needs to be split
            hline_lim = 66 if len(hline_txt) > 66 else len(hline_txt)
            print('< ' + '\n<   [contd.] '.join(
                [hline_txt[i:i+hline_lim] for i in range(0,
                    len(hline_txt), hline_lim)]))

        # Only print response body if error OR print_response_always is True
        if not resp.ok or print_response_always:
            # Print blank line before starting body
            print('<')
            # Read body into ascii string
            body_lines = resp.text.decode('ascii') if \
                        type(resp.text) == bytes else str(resp.text)
            # Assign 'None' text to body text. Null response check
            body_lines = 'None' if len(body_lines) == 0 else body_lines
            # Split body into lines as a list of strings
            body_line_split = body_lines.replace('\r\n', '\n').split('\n')
            for body_txt in body_line_split:
                # Secondary NULL response check. Only print body if particular
                # line is not zero-length
                if len(body_txt) > 0:
                    # Determine if body line needs to be split
                    body_lim = 66 if len(body_txt) > 66 else len(body_txt)
                    print('< ' + '\n<   [contd.] '.join(
                        [body_txt[i:i+body_lim]
                        for i in range(0, len(body_txt), body_lim)]))

        # Iterate over next request, response pair
        req_resp_idx = req_resp_idx + 1

    print('')
    # Return the last final response
    return responses


def strip_vars(param_compl_dict, meta_passed_only=True, meta_parser=None):
    res = {}

    def basic_meta_parser(m):
        return m['enabled']
    if (meta_parser is None) or (not callable(meta_parser)):
        meta_parser = basic_meta_parser
    for key in param_compl_dict:
        if (meta_parser(param_compl_dict[key][1]['_meta'])
                or (not meta_passed_only)):
            res[key] = param_compl_dict[key][0]
    return res


def url_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Url_Form)
                 and m['enabled'])


def body_form_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Body_Form)
                and m['enabled'])


def body_json_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Body_Json)
                and m['enabled'])


def body_xml_param_meta_parser(m):
    return ((m['param_loc'] == ParamLocation.Param_Body_Xml)
                and m['enabled'])
