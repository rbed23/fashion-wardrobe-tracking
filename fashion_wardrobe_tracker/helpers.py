from fashion_wardrobe_tracker import db

def generate_selection(SelectionClass, selector):
    select_objs = db.session.query(SelectionClass)
    selections = [(getattr(x, selector), getattr(x, selector).title()) 
                  for x in select_objs] if not SelectionClass == 'Size' else\
                        [(getattr(x, selector), getattr(x, selector)) 
                        for x in select_objs]
    return selections