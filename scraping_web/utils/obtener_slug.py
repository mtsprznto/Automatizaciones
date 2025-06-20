import re

def obtener_slug(url):
    try:
        match = re.search(r'/groups/(\d+)', url)
        if match:
            grupo_id = match.group(1)
            print(grupo_id)  # Output: 692338427471692
    
        return grupo_id
    except Exception as e:
        print(f"Error al obtener el slug: {e}")
        return None