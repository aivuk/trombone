from sqlalchemy import func, and_, or_
import dialogando.models as md
from flask import request, flash, redirect, render_template
import random

def root():
    return render_template('soon.html')

def about():
    return render_template('about.html')

def themes():
    return render_template('themes.html')

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
                    rs += [(r.dissertative_1, r)]
                elif rint == 0:
                    rs += [(r.dissertative_2, r)]
                elif r.dissertative_2 != '':
                    rs += [(r.dissertative_2, r)]
                else:
                    rs += [(r.dissertative_1, r)]

                rs_ids.add(r.person.id)
 
                if len(rs) == 3:
                    break
        if len(rs) == 3:
            break
    
    return render_template('root.html', random_answers=rs)

def answers(person_id, question_id=None):
    person = md.db.session.query(md.Person).get(person_id)
    topics = md.db.session.query(md.Topic).all()
    all_questions = md.db.session.query(md.SimpleQuestion).all()
    selected_question_id = question_id if question_id else 1
    person_answer = filter(lambda x: x.simple_question_id == selected_question_id, person.answers)

    if person_answer:
        answer = person_answer[0]
    else:
        answer = None

    try:
        question = filter(lambda x: x.id == selected_question_id, all_questions)[0]
    except:
        return redirect('/')

    return render_template('answers.html', topics=topics, questions=all_questions, question=question, answer=answer, person=person, selected_question_id=selected_question_id)
