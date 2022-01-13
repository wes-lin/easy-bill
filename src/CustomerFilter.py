import arrow

def datetimeformat (date,format="YYYY-MM-DD"):
    val = arrow.get(date).format(format)
    return val
