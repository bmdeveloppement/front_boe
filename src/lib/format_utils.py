# -*- coding: utf-8 -*-
import dateutil.parser


def view_formatter(type, data, suffix=False):
    """Format data from type"""
    if repr(data) == 'Undefined':
        return ''
    try:
        if type == 'date':
            date = dateutil.parser.parse(data)
            data = date.strftime('%m/%d/%Y')
        elif type == 'integer':
            data = u'{0:,}'.format(int(float(data)))
        elif type == 'float':
            data = "{0:.2f}".format(round(data, 5))
        elif type == 'percent' and suffix is False:
            data = u"%0.2f %%" % (round(float(data) * 100, 2))
        elif type == 'percent':
            data = round(float(data), 2)
        elif type == 'money' and suffix is False:
            data = u'{0:,} €'.format(round(float(data), 2))
        elif type == 'money':
            data = round(float(data), 2)
        elif type == 'money_w/o_comma':
            data = u'{0:,} €'.format(int(float(data)))
        elif type == 'string' and data == '-1':
            data = DEFAULT_TITLE
    except:
        logging.exception('Error while dashboard format')
    return data