# -*- coding: utf-8 -*-

import dialogando.models as md
import codecs

def get_person_email(person_id):
    person = md.Person.query.filter(md.Person.id == person_id)[0]
    if ';' in person.email:
        email = person.email.split(';')[0]
    elif '/' in person.email:
        email = person.email.split('/')[0]
    else:
        email = person.email
    
    email =  email.strip().lstrip().rstrip().encode('utf8')
    
    msg_file = codecs.open('tools/mail.html', 'r', encoding='utf-8').read()
    senh = u'Senhor' if person.sex[0] == 'M' else 'Senhora'
    nome_urna = person.urn_name
    candidato = u'Caro Candidato' if person.sex[0] == 'M' else 'Cara Candidata'
    cargo = person.candidature
    partido = person.party
    url = u'<a href="http://dialogando.org/responder/0?u={}">http://dialogando.org/responder/0?u={}</a>'.format(person.slug, person.slug)
    msg_file = msg_file.format(senh=senh, nome_urna=nome_urna, candidato=candidato, cargo=cargo, partido=partido, url=url)
    
    return msg_file
