from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from str_for_search import phone_number, check_str, country_index, provider_kod, except_country_index, TLD, abnormal_phone_form
from PIL import Image
import img2pdf
import cv2
import pytesseract
import fitz
import os
import asyncio
import numpy as np

project_path = os.getcwd()

def search_files(folder_path, extension):

    found_files = []

    try:

        for file in os.listdir(folder_path):

            if file.endswith(extension):

                found_files.append(file)
    except Exception:
        print(f"Ошибка при поиске файлов: ")

    return found_files

def convert_png_to_pdf(png_files, output_pdf_path):

    with open(output_pdf_path, "wb") as pdf_file:

        pdf_file.write(img2pdf.convert(png_files))

async def photo_searcher(name_extracrtedPage, config, file_name):

    global x_paste
    global y_paste
    global ko_vo_of_founded_elems_2

    ko_vo_of_founded_elems_1 = 0
    ko_vo_of_founded_elems_2 = 0

    hid_and_area_list = []

    scaleFactor = 2

    while True:

        x_paste = 0
        y_paste = 0

        img = cv2.imread(f'IMG/INPUT/{name_extracrtedPage}')

        faces = cv2.CascadeClassifier('faces.xml')
        file_path = os.path.join('IMG/AREA/', f'{file_name}.png')

        result = faces.detectMultiScale(img, scaleFactor=scaleFactor, minNeighbors=3)

        if not os.path.exists(file_path):

            try:

                for (x, y, w, h) in result:

                    x_paste = x
                    y_paste = y
                    image_width = w
                    image_heigh = h
                    area = img[y:y + h, x:x + w]

                    cv2.imwrite(f'IMG/AREA/{name_extracrtedPage}', area)
                    cv2.imwrite(f'IMG/NEW/{name_extracrtedPage}', img)

                    img_2 = cv2.imread(f'IMG/AREA/{name_extracrtedPage}')

                    cartoon_image = cv2.stylization(img_2, sigma_s=10, sigma_r=0.5)

                    cv2.imwrite(f'IMG/AREA/{name_extracrtedPage}', cartoon_image)

                    background_path = f'IMG/NEW/{file_name}.png'
                    overlay_path = f'IMG/AREA/{file_name}.png'
                    output_path = f'IMG/HID&AREA/{file_name}.png'

                    background = Image.open(background_path)
                    overlay = Image.open(overlay_path)

                    overlay = overlay.convert("RGBA")
                    overlay_mask = overlay.split()[3]  # Извлечение альфа-канала в маску

                    background.paste(overlay, (x_paste, y_paste), overlay_mask)
                    background.save(output_path)

                    hid_and_area_list.append(output_path)

                    return hid_and_area_list

            except:

                scaleFactor += 1
                continue

        if scaleFactor == 20:

            break

        else:

            scaleFactor += 1

async def text_searcher(HID_AREA, HID, name_extracrtedPage, config, file_name):

    global img

    hid_and_area_list = await photo_searcher(name_extracrtedPage, config, file_name)

    ko_vo_of_founded_elems = 0
    country_index_kol_vo = 0
    provider_kod_kol_vo = 0
    phone_number_elems_kol_vo = 0
    kol_vo_of_phone_number_elems = 0
    linkeDin_founded = 0
    telegram_founded = 0
    facebook_founded = 0
    telegram_letter_list = []
    telegram_letter_list_kol_vo = 0
    telegram_letter_list_kol_vo_2 = 0
    searching_potential = 0
    same_linked = ''
    elem_index = 0
    e_mail = 0

    try:

        if HID_AREA in hid_and_area_list:

            img = cv2.imread(HID_AREA)

        if HID_AREA not in hid_and_area_list:

            img = cv2.imread(HID)

    except:

        img = cv2.imread(f'IMG/INPUT/{name_extracrtedPage}')

    data = pytesseract.image_to_data(img, config=config, lang='eng')

    for i, el in enumerate(data.splitlines()):

        if i == 0:
            continue

        el = el.split()

        try:

            if file_name == '17227490':

                print(el[11])
                print(searching_potential, provider_kod_kol_vo, country_index_kol_vo)

            elem_index += 1
            searching_potential -= 1
            phone_number_elems_kol_vo -= 1

            if 'e-mail' in el[11].lower() or 'email' in el[11].lower():

                e_mail += 1

            if 'telegram' in el[11].lower():

                telegram_founded += 1

            """if 'linkedin' in el[11].lower() and 'www' not in el[11] and '.com' not in el[11]:

                linkeDin_founded += 1"""

            if 'facebook' in el[11].lower():

                facebook_founded += 1

            if e_mail > 0:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                e_mail = 0

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            """if linkeDin_founded > 0:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                if el[11][-1] != '.':

                    linkeDin_founded = 0

                else:

                    pass

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass"""

            if facebook_founded > 0:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                if el[11][-1] != '.':

                    facebook_founded = 0

                else:

                    pass

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            if '@' in el[11] and telegram_founded > 0:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                for letter in el[11].lower():

                    telegram_letter_list.append(letter)

                cv2.imwrite(HID, img)

                for elem in el[11].lower():

                    if elem in telegram_letter_list:
                        telegram_letter_list_kol_vo_2 += 1

                    if telegram_letter_list_kol_vo == telegram_letter_list_kol_vo_2:

                        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                        cv2.imwrite(HID, img)

                        try:

                            if HID_AREA in hid_and_area_list:
                                cv2.imwrite(HID_AREA, img)
                                cv2.imwrite(HID, img)

                            if HID_AREA not in hid_and_area_list:
                                cv2.imwrite(HID, img)

                        except:

                            pass

                try:

                    if HID_AREA in hid_and_area_list:

                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:

                        cv2.imwrite(HID, img)

                except:

                    pass

            if "@" in el[11] and (TLD[0] in el[11].lower() or TLD[1] in el[11].lower() or TLD[2] in el[11].lower() or TLD[3] in el[11].lower()):

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                ko_vo_of_founded_elems += 1
                searching_potential = 20

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:

                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:

                        cv2.imwrite(HID, img)

                except:

                    pass

            if el[11] in country_index and el[11] not in except_country_index:

                provider_kod_kol_vo = 0

                if searching_potential > 0:

                    x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                    country_index_kol_vo += 1
                    provider_kod_kol_vo = 0
                    searching_potential += 4

                    cv2.imwrite(HID, img)

                if country_index_kol_vo == 0:

                    x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                    country_index_kol_vo += 1
                    provider_kod_kol_vo = 0
                    searching_potential = 2

                    cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            if ('www.linkedin' in el[11] or'linkedin.com' in el[11] or 'inkedin.com' in el[11]):

                provider_kod_kol_vo = 1

                if linkeDin_founded == 0:

                    x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                    country_index_kol_vo += 1
                    linkeDin_founded += 1
                    same_linked = el[11]

                    cv2.imwrite(HID, img)

                if same_linked in el[11] and linkeDin_founded > 0:

                    x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                    cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            if el[11] in provider_kod and searching_potential > 0 and provider_kod_kol_vo == 0 and country_index_kol_vo > 0:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                provider_kod_kol_vo += 1
                ko_vo_of_founded_elems += 1
                searching_potential = 5
                country_index_kol_vo = 0
                phone_number_elems_kol_vo = 2

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            if el[11] in phone_number and provider_kod_kol_vo > 0 and searching_potential > 0 and phone_number_elems_kol_vo > 0:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                kol_vo_of_phone_number_elems += 1
                phone_number_elems_kol_vo += 1
                searching_potential = 5

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            if '+' in el[11] and len(el[11]) > 7:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                ko_vo_of_founded_elems += 1

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            if el[11][-5:] in abnormal_phone_form and len(el[11][:-5]) >= 5:

                x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=cv2.FILLED)

                ko_vo_of_founded_elems += 1

                cv2.imwrite(HID, img)

                try:

                    if HID_AREA in hid_and_area_list:
                        cv2.imwrite(HID_AREA, img)
                        cv2.imwrite(HID, img)

                    if HID_AREA not in hid_and_area_list:
                        cv2.imwrite(HID, img)

                except:

                    pass

            #print(el)

        except IndexError:

            elem_index += 1
            searching_potential -= 1

    folder_path = 'IMG/HID'
    extension = '.png'

    found_files = search_files(folder_path, extension)

    if name_extracrtedPage in found_files:

        pass

    else:

        cv2.imwrite(HID, img)

async def fifth_page(project_path, file_name, pdf_list):

    input_pdf_path = f"IMG/INPUT_PDF/{file_name}.pdf"
    output_pdf_path = f"IMG/RESULT/{file_name}.pdf"
    save_png = f"IMG/INPUT/{file_name}5.png"
    name_extracrtedPage = f"{file_name}5.png"
    text_to_add = f"{file_name}@example.com"
    HID_AREA = f'IMG/HID&AREA/{file_name}5.png'
    HID = f'IMG/HID/{file_name}5.png'
    save_await = 0

    images = convert_from_path(input_pdf_path, first_page=0, last_page=6,
                               poppler_path=f'{project_path}/poppler-23.11.0/Library/bin')

    image = images[4]

    try:

        if images[5]:

            print(images[5])

    except:

        pdf_list.append(HID)
        save_await += 1

    image.save(save_png, "PNG")

    pytesseract.pytesseract.tesseract_cmd = f'{project_path}/Tesseract-OCR/tesseract.exe'
    config = 'r--oem 4 --psm 6'

    global x_paste
    global y_paste
    global ko_vo_of_founded_elems_2

    await asyncio.sleep(2)

    await text_searcher(HID_AREA, HID, name_extracrtedPage, config, file_name)

    if save_await > 0:

        convert_png_to_pdf(pdf_list, output_pdf_path)

async def fourth_page(project_path, file_name, pdf_list):

    input_pdf_path = f"IMG/INPUT_PDF/{file_name}.pdf"
    output_pdf_path = f"IMG/RESULT/{file_name}.pdf"
    save_png = f"IMG/INPUT/{file_name}4.png"
    name_extracrtedPage = f"{file_name}4.png"
    text_to_add = f"{file_name}@example.com"
    HID_AREA = f'IMG/HID&AREA/{file_name}4.png'
    HID = f'IMG/HID/{file_name}4.png'
    save_await = 0

    images = convert_from_path(input_pdf_path, first_page=0, last_page=6,
                               poppler_path=f'{project_path}/poppler-23.11.0/Library/bin')

    image = images[3]

    try:

        if images[4]:

            await fifth_page(project_path, file_name, pdf_list)

    except:

        pdf_list.append(HID)
        save_await += 1

    image.save(save_png, "PNG")

    pytesseract.pytesseract.tesseract_cmd = f'{project_path}/Tesseract-OCR/tesseract.exe'
    config = 'r--oem 4 --psm 6'

    global x_paste
    global y_paste
    global ko_vo_of_founded_elems_2

    await asyncio.sleep(2)

    await text_searcher(HID_AREA, HID, name_extracrtedPage, config, file_name)

    if save_await > 0:

        convert_png_to_pdf(pdf_list, output_pdf_path)

async def third_page(project_path, file_name, pdf_list):

    input_pdf_path = f"IMG/INPUT_PDF/{file_name}.pdf"
    output_pdf_path = f"IMG/RESULT/{file_name}.pdf"
    save_png = f"IMG/INPUT/{file_name}3.png"
    name_extracrtedPage = f"{file_name}3.png"
    text_to_add = f"{file_name}@example.com"
    HID_AREA = f'IMG/HID&AREA/{file_name}3.png'
    HID = f'IMG/HID/{file_name}3.png'
    save_await = 0

    images = convert_from_path(input_pdf_path, first_page=0, last_page=6,
                               poppler_path=f'{project_path}/poppler-23.11.0/Library/bin')

    image = images[2]

    try:

        if images[3]:

            await fourth_page(project_path, file_name, pdf_list)

    except:

        pdf_list.append(HID)
        save_await += 1

    image.save(save_png, "PNG")

    pytesseract.pytesseract.tesseract_cmd = f'{project_path}/Tesseract-OCR/tesseract.exe'
    config = 'r--oem 4 --psm 6'

    global x_paste
    global y_paste
    global ko_vo_of_founded_elems_2

    await asyncio.sleep(2)

    await text_searcher(HID_AREA, HID, name_extracrtedPage, config, file_name)

    if save_await > 0:

        convert_png_to_pdf(pdf_list, output_pdf_path)

async def second_page(project_path, file_name, pdf_list):

    input_pdf_path = f"IMG/INPUT_PDF/{file_name}.pdf"
    output_pdf_path = f"IMG/RESULT/{file_name}.pdf"
    save_png = f"IMG/INPUT/{file_name}2.png"
    name_extracrtedPage = f"{file_name}2.png"
    text_to_add = f"{file_name}@example.com"
    HID_AREA = f'IMG/HID&AREA/{file_name}2.png'
    HID = f'IMG/HID/{file_name}2.png'
    save_await = 0

    images = convert_from_path(input_pdf_path, first_page=0, last_page=6,
                               poppler_path=f'{project_path}/poppler-23.11.0/Library/bin')

    image = images[1]

    try:

        if images[2]:

            pdf_list.append(HID)

            await third_page(project_path, file_name, pdf_list)

    except:

        pdf_list.append(HID)
        save_await += 1

    image.save(save_png, "PNG")

    pytesseract.pytesseract.tesseract_cmd = f'{project_path}/Tesseract-OCR/tesseract.exe'
    config = 'r--oem 4 --psm 6'

    global x_paste
    global y_paste
    global ko_vo_of_founded_elems_2

    await asyncio.sleep(2)

    await text_searcher(HID_AREA, HID, name_extracrtedPage, config, file_name)

    if save_await > 0:

        convert_png_to_pdf(pdf_list, output_pdf_path)

async def first_page(project_path, file_name):

    print(file_name)

    input_pdf_path = f"IMG/INPUT_PDF/{file_name}.pdf"
    output_pdf_path = f"IMG/RESULT/{file_name}.pdf"
    save_png = f"IMG/INPUT/{file_name}.png"
    name_extracrtedPage = f"{file_name}.png"
    text_to_add = f"{file_name}@example.com"
    HID_AREA = f'IMG/HID&AREA/{name_extracrtedPage}'
    HID = f'IMG/HID/{name_extracrtedPage}'
    png_list = []
    save_await = 0

    hid_and_area_list = []
    hid_and_area_list.append(name_extracrtedPage)

    images = convert_from_path(input_pdf_path, first_page=0, last_page=6,
                               poppler_path=f'{project_path}/poppler-23.11.0/Library/bin')

    image = images[0]  # Получаем только первое изображение

    try:

        if images[1]:

            png_list.append(HID)

            await second_page(project_path, file_name, png_list)

    except:

        png_list.append(HID)
        save_await += 1

    image.save(save_png, "PNG")

    pytesseract.pytesseract.tesseract_cmd = f'{project_path}/Tesseract-OCR/tesseract.exe'
    config = 'r--oem 4 --psm 6'

    global x_paste
    global y_paste
    global ko_vo_of_founded_elems_2

    await asyncio.sleep(2)

    await text_searcher(HID_AREA, HID, name_extracrtedPage, config, file_name)

    if save_await > 0:

        convert_png_to_pdf(png_list, output_pdf_path)

folder_path = 'IMG/INPUT_PDF'
file_extension = '.pdf'

result = search_files(folder_path, file_extension)

async def main():

    if result:

        tasks = []

        print("Найденные файлы:")
        for found_file_name in result:

            file_name = found_file_name[:-4]

            task = first_page(project_path, file_name)

            tasks.append(task)

        while len(tasks) != 0:

            if len(tasks) % 10 == 0 or (len(tasks) % 10 != 0 and len(tasks) > 10):

                await asyncio.gather(*tasks[:10])
                del tasks[:10]

            if len(tasks) == 9:

                await asyncio.gather(*tasks[:9])
                del tasks[:9]

            if len(tasks) == 8:
                await asyncio.gather(*tasks[:8])
                del tasks[:8]

            if len(tasks) == 7:
                await asyncio.gather(*tasks[:7])
                del tasks[:7]

            if len(tasks) == 6:
                await asyncio.gather(*tasks[:6])
                del tasks[:6]

            if len(tasks) == 5:
                await asyncio.gather(*tasks[:5])
                del tasks[:5]

            if len(tasks) == 4:
                await asyncio.gather(*tasks[:4])
                del tasks[:4]

            if len(tasks) == 3:
                await asyncio.gather(*tasks[:3])
                del tasks[:3]

            if len(tasks) == 2:
                await asyncio.gather(*tasks[:2])
                del tasks[:2]

            if len(tasks) == 1:
                await asyncio.gather(*tasks[:1])
                del tasks[:1]

            if len(tasks) == 0:

                break

        print(len(tasks))

    else:
        print("Файлы не найдены.")

if __name__ == '__main__':

    asyncio.run(main())

    files = os.listdir('IMG/AREA/')

    for file_name in files:

        file_path = os.path.join('IMG/AREA/', file_name)

        if os.path.isfile(file_path):

            os.remove(file_path)

            print(f"Файл '{file_name}' удален.")
