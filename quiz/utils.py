from io import BytesIO
import pandas as pd
from .models import Question, Quiz
from reportlab.pdfgen import canvas


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
            quiz=Quiz.objects.get(id=id),
            title=question,
            option_1=op1,
            option_2=op2,
            option_3=op3,
            option_4=op4,
            answer=ans
        )


def generate_quiz_questions_pdf(quiz):
    # Assuming you have a Quiz model with id and title fields
    questions = Question.objects.filter(quiz=quiz)

    buffer = BytesIO()
    # Create PDF
    pdf = canvas.Canvas(buffer)

    # Set up PDF content
    pdf.drawString(100, 800, f"Quiz: {quiz.title}")
    pdf.drawString(100, 780, "Questions:")

    y_position = 760  # Initial Y position for questions

    for question in questions:
        y_position -= 20  # Move down for each question
        pdf.drawString(100, y_position, f"Savol: {question.title}")
        
        # Add options
        options = [question.option_1, question.option_2, question.option_3, question.option_4]
        for i, option in enumerate(options, 1):
            y_position -= 20  # Move down for each option
            pdf.drawString(120, y_position, f"{i}: {option}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return buffer