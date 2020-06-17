

def generate_selection(SelectionClass, selector):
    select_objs = SelectionClass.query.all()
    selections = [(getattr(x, selector), getattr(x, selector).title()) 
                  for x in select_objs]
    return selections