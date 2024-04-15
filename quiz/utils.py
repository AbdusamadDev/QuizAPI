from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from io import BytesIO
from jwt import decode
import pandas as pd
import openpyxl

from .models import Question, Quiz
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph


def _import_from_xls(file):
    # Done
    xls_data = pd.read_excel(file)
    data = []
    for idx in range(len(xls_data)):
        row = xls_data.iloc[idx]
        title = row[0]
        if row[-1] not in range(1, 5):
            raise IndexError("Answer index out of range")
        for i in range(1, len(row) - 1, 4):
            question_data = {
                "title": title,
                "options": [row[i], row[i + 1], row[i + 2], row[i + 3]],
                "correct_answer": int(row[-1]),
            }
            data.append(question_data)
    return data


def _export_to_pdf(data, limit):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    page_width = 612
    page_height = 792
    margin_top = page_height * 0.05

    text_x = (page_width - p.stringWidth("Quiz Export")) / 2

    # Calculate Y-coordinate based on margin top and font size (adjust if needed)
    text_y = page_height - margin_top - 14

    # Draw "Quiz Export" centered
    p.drawString(text_x, text_y, data['title'])
    p.drawString(85, text_y-20, f"Umumiy savollar soni: {len(data['questions'])} ta")
    p.drawString(85, text_y-40, f"Ishlash uchun vaxt: {data['solving_time']} daqiqa")
    des = data['description']
    dess = []
    t = ''
    for item in des:
        t+= item
        if len(t) > 80:
            dess.append(t)
            t = ''
    if len(dess) == 0:
        dess.append(des)
    text_y -= 60
    p.drawString(85, text_y, f"Izoh:")
    for d in dess:
        text_y -= 20
        p.drawString(85, text_y, d)

    option_layer = 85
    question_index = 1
    page_height = letter[1]
    if limit is None:
        questions = data["questions"]
    else:
        questions = data["questions"][:limit]
    p.rect(x=15, y=25, width=190 * 3, height=150 * 5)
    p.rect(x=25, y=15, width=190 * 3, height=150 * 5)
    y = text_y-20  # Initial vertical position
    count = 0
    for question in questions:
        count += 1
        title_lines = question["title"].split(" ")
        split_words = [title_lines[i : i + 13] for i in range(0, len(title_lines), 13)]
        for word_chunk in split_words:
            constructed_word = " ".join(word_chunk)
            p.drawString(x=70, y=y, text=f"{count} - Savol: {constructed_word}")
        
        p.drawString(option_layer, y - 30, f"A. {question['option_1']}")
        p.drawString(option_layer, y - 45, f"B. {question['option_2']}")
        p.drawString(option_layer, y - 60, f"C. {question['option_3']}")
        p.drawString(option_layer, y - 75, f"D. {question['option_4']}")
        y -= 100
        question_index += 1
        if y < 150:  # Check if content exceeds page height
            p.showPage()  # Create new page
            p.rect(x=15, y=25, width=190 * 3, height=150 * 5)
            p.rect(x=25, y=15, width=190 * 3, height=150 * 5)
            p.setTitle(title=data["title"])
            y = page_height - 100  # Reset vertical position for new page
    count = 0
    y = 750
    x = 110
    p.showPage()
    p.drawString(70, y, "Savol: ")
    p.drawString(70, y-30, "Javob: ")
    for question in questions:
        if y < 150:  
            p.showPage()
            p.rect(x=15, y=25, width=190 * 3, height=150 * 5)
            p.rect(x=25, y=15, width=190 * 3, height=150 * 5)
            p.setTitle(title=data["title"])
            y = page_height - 100
        count += 1
        p.drawString(x, y, str(count))

        answer = Question.objects.get(id = question['id']).answer
        v = " ABCD" 
        p.drawString(x, y-30, v[answer])
        
        x+= 20
        if x > 500:
            x = 110
            y-= 100
            p.drawString(70, y, "Savol: ")
            p.drawString(70, y-30, "Javob: ")            
        # break


        
    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="quiz_export.pdf"'
    response.write(buffer.read())
    return response


def _export_to_xls(data, limit):
    # Done
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(
        [
            "Question Title",
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
        ]
    )
    for question in data["questions"][:limit]:
        worksheet.append(
            [
                question["title"],
                question["option_1"],
                question["option_2"],
                question["option_3"],
                question["option_4"],
            ]
        )
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer


# def extract_data(id, filename):
#     # df = pd.read_excel(f"media/{filename.name}")
#     df = pd.read_excel(filename)

#     questions = df["Question"]
#     options_1 = df["Option 1"]
#     options_2 = df["Option 2"]
#     options_3 = df["Option 3"]
#     options_4 = df["Option 4"]
#     answers = df["Answer"]

#     for question, op1, op2, op3, op4, ans in zip(
#         questions, options_1, options_2, options_3, options_4, answers
#     ):
#         Question.objects.create(
#             quiz=Quiz.objects.get(id=id),
#             title=question,
#             option_1=op1,
#             option_2=op2,
#             option_3=op3,
#             option_4=op4,
#             answer=ans,
#         )


# def generate_quiz_questions_pdf(quiz):
#     # Assuming you have a Quiz model with id and title fields
#     questions = Question.objects.filter(quiz=quiz)

#     buffer = BytesIO()
#     # Create PDF
#     pdf = canvas.Canvas(buffer)

#     # Set up PDF content
#     pdf.drawString(100, 800, f"Quiz: {quiz.title}")
#     pdf.drawString(100, 780, "Questions:")

#     y_position = 760  # Initial Y position for questions

#     for question in questions:
#         y_position -= 20  # Move down for each question
#         pdf.drawString(100, y_position, f"Savol: {question.title}")

#         # Add options
#         options = [
#             question.option_1,
#             question.option_2,
#             question.option_3,
#             question.option_4,
#         ]
#         for i, option in enumerate(options, 1):
#             y_position -= 20  # Move down for each option
#             pdf.drawString(120, y_position, f"{i}: {option}")

#     pdf.showPage()
#     pdf.save()

#     buffer.seek(0)

#     return buffer


def unhash_token(request_header):
    jwt_token = request_header.get("Authorization", "").split(" ")[1]
    decoded_token = decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
    return decoded_token
