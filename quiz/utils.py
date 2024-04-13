from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from io import BytesIO
from jwt import decode
import pandas as pd
import openpyxl

from .models import Question, Quiz


def _import_from_xls(file):
    # Done
    xls_data = pd.read_excel(file)
    data = []
    for idx in range(len(xls_data)):
        row = xls_data.iloc[idx]
        title = row[0]
        if not (1 < row[-1] < 4):
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
    p.drawString(100, 800, "Quiz Export")
    p.setTitle(title=data["title"])
    option_layer = 85
    question_index = 1
    page_height = letter[1]
    if limit is None:
        questions = data["questions"]
    else:
        questions = data["questions"][:limit]
    p.rect(x=15, y=25, width=190 * 3, height=150 * 5)
    p.rect(x=25, y=15, width=190 * 3, height=150 * 5)
    y = 700  # Initial vertical position
    for question in questions:
        print("Parsing: ", question["title"])
        title_lines = question["title"].split(" ")
        split_words = [title_lines[i : i + 13] for i in range(0, len(title_lines), 13)]
        for word_chunk in split_words:
            constructed_word = " ".join(word_chunk)
            p.drawString(70, y, constructed_word)
            y -= 20
        p.drawString(option_layer, y - 15, "_______" * 3)
        p.drawString(option_layer, y - 30, f"1. {question['option_1']}")
        p.drawString(option_layer, y - 45, f"2. {question['option_2']}")
        p.drawString(option_layer, y - 60, f"3. {question['option_3']}")
        p.drawString(option_layer, y - 75, f"4. {question['option_4']}")
        y -= 100
        question_index += 1
        if y < 150:  # Check if content exceeds page height
            p.showPage()  # Create new page
            p.rect(x=15, y=25, width=190 * 3, height=150 * 5)
            p.rect(x=25, y=15, width=190 * 3, height=150 * 5)
            p.setTitle(title=data["title"])
            y = page_height - 100  # Reset vertical position for new page
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
