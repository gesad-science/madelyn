def clean_string(string : str) -> str:
    return string.replace('\n', '').replace('=', '').replace(',', '').replace('.', '') 
