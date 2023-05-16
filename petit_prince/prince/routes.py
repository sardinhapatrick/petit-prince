# from flask import render_template, url_for, request
from flask import *
from prince import app, db
from prince.models import *
from multiprocessing import Value
import random
import time

d = {}

def computeLang():
    global d
    if d == {}:
        # rel = Relation.query.all()
        dict_lang = {}
        list_grp = []
        # all language which parent is root
        root_child = Relation.query.filter_by(parent = 1)
        for k in range(root_child.count()-1): # -1 car dernier = Doublon langue caucasienne (grp 81)
            key_grp = Group.query.filter_by(i = root_child[k].child)[0].grp
            id_grp = Group.query.filter_by(i = root_child[k].child)[0].i
            dict_lang[key_grp] = []
            tmp_parent = [root_child[k].child]
            tmp_child = []
            grp_child = Relation.query.filter_by(parent = id_grp) # compute child second layer
            test = []
            save = []
            save_temp = []
            visited = []
            while (dict_lang[key_grp] == []):
                for kk in range(grp_child.count()): # if no child don't come here
                    if (grp_child[kk].child not in tmp_child and grp_child[kk].child not in visited):
                        tmp_child.append(grp_child[kk].child)
                for e in tmp_child:
                    try:
                        for l in range(len(Language.query.filter_by(grp = e).all())):
                            test.append((Language.query.filter_by(grp = e).all())[l].french) # try if it's a language
                        save.append(e)
                    except:
                        continue
                for ee in tmp_parent:
                    try:
                        test.append(Language.query.filter_by(grp = ee).first().french) # also try if it's a language (big language) (can be only uniq)
                        save.append(ee)
                    except:
                        continue
                if (test != []):
                    for i in range(len(test)):
                        if test[i] not in save_temp:
                            save_temp.append(test[i])
                if tmp_child == []:
                    dict_lang[key_grp] = save_temp
                    save_temp = []
                    visited = []
                else:
                    grp_child = Relation.query.filter_by(parent = tmp_child[0])
                    visited.append(tmp_child[0])
                    tmp_child.remove(tmp_child[0])
        d = dict_lang

@app.route('/')
@app.route('/home')
def home():
    computeLang()
    prince_language = Language.query.filter_by(actif=1)
    sounds = Sound.query.all()
    return render_template('home.html', title='Petit Prince', prince_language = prince_language, sounds = sounds)

@app.route('/liste_langues')
def liste_langues():
    prince_language = Language.query.filter_by(actif=1)
    sounds = Sound.query.all()
    return render_template('liste_langues.html', title='Liste des langues', prince_language = prince_language, sounds = sounds)

@app.route('/langue/<lang>')
def langue(lang):
    langue_complet = Language.query.filter_by(french = lang).first()
    sounds = Sound.query.filter_by(language = langue_complet.iso)
    return render_template('langue.html', langue=langue_complet, title=lang, sounds = sounds)

@app.route('/carte')
def carte():
    french = Language.french
    prince_language = Language.query.filter_by(actif=1)
    sounds = Sound.query.all()
    return render_template('carte.html', title='Carte', prince_language=prince_language, sounds = sounds)

@app.route('/enregistrement')
def enregistrement():
    return render_template('enregistrement.html', title='Enregistrer un audio')

@app.route('/about')
def about():
    prince_language = Language.query.filter_by(actif=1)
    return render_template('about.html', title='À propos', prince_language = prince_language)

@app.route('/quiz_home')
def quiz_home():
    return render_template('quiz_home.html')

@app.route('/quiz_text?<string:level>?<string:sf>?<int:nb_answer>')
def quiz_text(level, sf, nb_answer, score=0, dictLang=d):
    if d == {}:
        computeLang()
    else:
        time.sleep(3)
    list_lang = []
    list_keys = []
    if level == "easy":
        for key in d:
            list_keys.append(key)
        random.shuffle(list_keys)
        f = 0
        while(len(list_lang) != 3):
            l = 0
            random.shuffle(d[list_keys[f]])
            for elem in d[list_keys[f]]:
                iso = Language.query.filter_by(french = d[list_keys[f]][l]).first().iso
                text = Language.query.filter_by(iso=iso).first().text
                if text == "":
                    text = Language.query.filter_by(iso=iso).first().imgtext
                    if text == "":
                        l+=1
                        continue
                    else:
                        if list_lang == []:
                            list_lang.append([d[list_keys[f]][l],1,text,"img"])
                            lang_ok = d[list_keys[f]][l]
                        else:
                            list_lang.append([d[list_keys[f]][l],0,text,"img"])
                        f += 1
                        break
                else:
                    if list_lang == []:
                        list_lang.append([d[list_keys[f]][l],1,text,"text"])
                        lang_ok = d[list_keys[f]][l]
                    else:
                        list_lang.append([d[list_keys[f]][l],0,text,"text"])
                    f += 1
                    break
            f += 1
    if level == "hard":
        for key in d:
            list_keys.append(key)
        random.shuffle(list_keys)
        if sf != "all" and sf != None:
            list_keys.remove(sf)
            list_keys.insert(0, sf)
        f = 0
        while(len(list_lang) != nb_answer):
            is_text = False
            is_correct = False
            l = 0
            while len(d[list_keys[f]]) < nb_answer:
                f += 1
            random.shuffle(d[list_keys[f]])
            for elem in d[list_keys[f]]:
                iso = Language.query.filter_by(french = d[list_keys[f]][l]).first().iso
                text = Language.query.filter_by(iso=iso).first().text
                if text == "":
                    text = Language.query.filter_by(iso=iso).first().imgtext
                    if text == "":
                        if len(list_lang) + 1 < nb_answer or is_text:
                            list_lang.append([d[list_keys[f]][l],0,None])
                        l+=1
                    else:
                        if list_lang == [] or is_correct == False:
                            is_correct = True
                            list_lang.append([d[list_keys[f]][l],1,text,"img"])
                            lang_ok = d[list_keys[f]][l]
                        else:
                            list_lang.append([d[list_keys[f]][l],0,text,"img"])
                        is_text = True
                        l+=1
                else:
                    if list_lang == [] or is_correct == False:
                        is_correct = True
                        list_lang.append([d[list_keys[f]][l],1,text,"text"])
                        lang_ok = d[list_keys[f]][l]
                    else:
                        list_lang.append([d[list_keys[f]][l],0,text,"text"])
                    l+=1
                    is_text = True
                if len(list_lang) == nb_answer:
                    break
            if len(list_lang) != nb_answer:
                list_lang = []
            if (sf == "all" or sf == None):
                f += 1
    random.shuffle(list_lang)
    return render_template('quiz_text.html', text=text, list_lang=list_lang, lang_ok=lang_ok, dict_lang=d)

@app.route('/quiz_audio?<string:level>?<string:sf>?<int:nb_answer>')
def quiz_audio(level, sf, nb_answer, score=0, dictLang=d):
    if d == {}:
        computeLang()
    else:
        time.sleep(3)
    sounds = Sound.query.all()
    list_lang = []
    list_keys = []
    if level == "easy":
        for key in d:
            list_keys.append(key)
        random.shuffle(list_keys)
        f = 0
        while(len(list_lang) != 3):
            l = 0
            random.shuffle(d[list_keys[f]])
            for elem in d[list_keys[f]]:
                try:
                    iso = Language.query.filter_by(french = d[list_keys[f]][l]).first().iso
                    filename = Sound.query.filter_by(language=iso).first().filename
                    if list_lang == []:
                        list_lang.append([d[list_keys[f]][l],1,filename])
                        lang_ok = d[list_keys[f]][l]
                    else:
                        list_lang.append([d[list_keys[f]][l],0,filename])
                    f += 1
                    break
                except:
                    l+=1
                    continue
            f += 1
    if level == "hard":
        for key in d:
            list_keys.append(key)
        random.shuffle(list_keys)
        if sf != "all" and sf != None:
            list_keys.remove(sf)
            list_keys.insert(0, sf)
        f = 0
        while(len(list_lang) != nb_answer):
            is_audio = False
            is_correct = False
            l = 0
            while len(d[list_keys[f]]) < nb_answer:
                f += 1
            random.shuffle(d[list_keys[f]])
            for elem in d[list_keys[f]]:
                try:
                    iso = Language.query.filter_by(french = d[list_keys[f]][l]).first().iso
                    filename = Sound.query.filter_by(language=iso).first().filename
                    if is_correct == False:
                        list_lang.append([d[list_keys[f]][l],1,filename])
                        lang_ok = d[list_keys[f]][l]
                        is_correct = True
                    else:
                        list_lang.append([d[list_keys[f]][l],0,filename])
                    is_audio = True
                    l += 1
                except:
                    if len(list_lang) + 1 < nb_answer or is_audio:
                        list_lang.append([d[list_keys[f]][l],0,None])
                    l+=1
                if len(list_lang) == nb_answer:
                    break
            if len(list_lang) != nb_answer:
                list_lang = []
            if (sf == "all" or sf == None):
                f += 1
    random.shuffle(list_lang)
    return render_template('quiz_audio.html', sounds=sounds, list_lang=list_lang, lang_ok=lang_ok, dict_lang=d)
