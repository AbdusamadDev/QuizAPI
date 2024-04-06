import pandas as pd
from .models import Question, Quiz


def extract_data(id, filename):
    # df = pd.read_excel(f"media/{filename.name}")
    df = pd.read_excel(filename)

    questions = df['Question']
    options_1 = df['Option 1']
    options_2 = df['Option 2']
    options_3 = df['Option 3']
    options_4 = df['Option 4']
    answers = df['Answer']


    for question, op1, op2, op3, op4, ans in zip(questions, options_1, options_2, options_3, options_4, answers):
        Question.objects.create(
            quiz_base=Quiz.objects.get(id=id),
            question=question,
            option_1=op1,
            option_2=op2,
            option_3=op3,
            option_4=op4,
            answer=ans
        )