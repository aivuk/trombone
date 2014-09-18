from sqlalchemy import func, and_, or_
import dialogando.models as md
from flask import request, flash, redirect, render_template
import random

def root():
    return render_template('soon.html')

def main():
    filter_ids = [1]
    rs = []
    rs_ids = set([1])
    while True:
        random_answers = md.db.session.query(md.SimpleAnswers).filter(and_(or_(md.SimpleAnswers.dissertative_1 != '', md.SimpleAnswers.dissertative_2 != ''), ~md.SimpleAnswers.person_id.in_(rs_ids))).order_by(func.random()).limit(6)
        for r in random_answers:
            if r.person.id not in rs_ids:
                rint = random.randint(0,1)

                if rint == 0 and r.dissertative_1 != '':
                    rs += [(r.dissertative_1, r.person.urn_name)]
                elif rint == 0:
                    rs += [(r.dissertative_2, r.person.urn_name)]
                elif r.dissertative_2 != '':
                    rs += [(r.dissertative_2, r.person.urn_name)]
                else:
                    rs += [(r.dissertative_1, r.person.urn_name)]

                rs_ids.add(r.person.id)
 
                if len(rs) == 3:
                    break
        if len(rs) == 3:
            break
    
    return render_template('root.html', random_answers=rs)

def answers():
    return render_template('answers.html')
