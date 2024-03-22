import os


def assign_value(rule: dict, text):
    return rule[text]


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def actu_list(lista, nv):
    try:
        l_nv = lista.index(nv)
    except:
        lista.append(nv)
    return lista


def text_to_list(text, **kwargs):
    number_type = kwargs.get('ntype',int)
    l = text.split(',')
    for i in range(len(l)):
        try:
            l[i] = number_type(l[i])
        except:
            l[i] = l[i]
    return l


