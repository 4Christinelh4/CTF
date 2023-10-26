import re

def check_list_containing(ls1, ls2):
    for ele in ls1:
        if not ele in ls2:
            return False
    return True

def check_finish_xss(query_insert):
    # <script> alert() </script>
    pattern = r"^<script>.*</script>$"
    return re.match(pattern, query_insert)

def check_topsecret_solved(result_rows):
    print(result_rows)
    if result_rows[0] == ('admin', 'aswd'):
        return True
    return False
