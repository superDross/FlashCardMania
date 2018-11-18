''' Transforms QuerySets into HTML tables. Pilfered from the internet.

Limited utility and very inefficient. Do replace in the near future.

'''
from django.utils.html import escape
from django.utils.safestring import mark_safe


def result_as_table(queryset, fieldnames=None):
    ''' Take a resultdata queryset and return it as a HTML table.
        Columns will be returned in the order they are declared
        in the model.

        Optionally, provide a list of fieldnames, which will be
        used to limit the output.
    '''

    dictlist = queryset.values()
    output = '<table class="ui celled table"><thead>\n'
    output_keys = []
    if fieldnames:
        names = fieldnames
    else:
        names = dictlist[0].keys()
    for name in names:
        if not name.endswith("_id"):
            output_keys.append(name)
            th = "<th>%s</th>\n" % escape(name.replace("_", " ").capitalize())
            output = "".join((output, th))
    "".join((output, '</thead>'))
    for rddict in dictlist:
        output = "".join((output, "<tr>\n"))
        for key in output_keys:
            val = rddict[key]
            if not key.endswith("_id"):
                display_func = get_display_method(rddict, queryset, key)
                if display_func:
                    output = "".join((output, "<td>%s</td>\n" %
                                      escape(display_func())))
                else:
                    # adds links to the id values
                    new_val = escape(val)
                    if key == 'id':
                        href = f'/card/{val}'
                        td = f'<td><a href={href}>{new_val}</a></td>\n'
                        output = "".join((output, td))
                    else:
                        output = "".join(
                            (output, "<td>%s</td>\n" % escape(val)))
        output = "".join((output, "</tr>\n"))
    return mark_safe("".join((output, "</table>\n")))


def get_display_method(rddict, queryset, key):
    ''' Re-implementation of inspect.getmembers(rddict,inspect.ismethod)
        and a test to see if this is a get_field_status method.  Had to
        reimplement inspect because it was bombing on the object - expecting
        some property that is not present.
    '''

    rdobj = queryset[0].__class__.objects.filter(
        id=rddict.get("id")).get()
    targetname = "get_%s_display" % key
    display_func = False

    for name in dir(rdobj):
        if name == targetname:
            try:
                display_func = getattr(rdobj, name)
                break
            except Exception as e:
                print(e)

    return display_func
