# utils/localization.py

from dataclasses import dataclass
from typing import Dict

@dataclass
class Localization:
    start_message: str
    processing_file_message: str
    check_saved_message: str
    check_request: str
    fio_request: str
    example_fio: str
    region_request: str
    example_region: str
    city_request: str
    example_city: str
    address_request: str
    example_address: str
    phone_request: str
    example_phone: str
    success_message: str
    file_error: str
    cloud_upload_error: str
    processing_data_message: str
    language_selection_prompt: str
    language_set_confirmation: str
    contract_sent_message: str
    file_send_error: str
    file_not_found: str
    database_save_error: str
    google_sheets_error: str
    count_of_orders: str
    example_count_of_orders: str
    error_no_amount_line: str
    error_no_qr_code: str
    error_invalid_amount: str
    error_minimum_amount: str
    error_check_repeat: str
    receipt_verified_message: str

LOCALIZATIONS: Dict[str, Localization] = {
    'kk': Localization(
        start_message=(
            "👋 <b>Қош келдіңіз!</b>\n\n"
            "📤 Өтінемін, <b>чекті</b> <i>фото</i> немесе <i>құжат</i> түрінде жіберіңіз, "
            "және біз тапсырысты рәсімдеуді бастаймыз.\n\n"
        ),
        processing_file_message="📥 <i>Файлыңыз өңделуде...</i>",
        check_saved_message="✅ Чек сақталды!",
        check_request="📤 Жаңа <b>чекті</b> фото немесе құжат түрінде жіберіңіз:",
        fio_request="3/5 Өтінемін, <b>Аты-жөніңізді</b> енгізіңіз 👤:",
        example_fio="<i>Мысалы: Иванов Иван Иванович</i>",
        region_request="🏠 4/5 Өтінемін, <b>жеткізу облысын</b> енгізіңіз 📍:",
        example_region="<i>Мысалы: Алматы облысы</i>",
        city_request="🏠 4/5 Өтінемін, <b>жеткізу қаласын</b> енгізіңіз 📍:",
        example_city="<i>Мысалы: Алматы</i>",
        address_request="🏠 4/5 Өтінемін, <b>жеткізу мекенжайын</b> енгізіңіз 📍:",
        example_address="<i>Мысалы: Панфилов к-сі, 12, 34 кв.</i>",
        phone_request="📞 5/5 <b>Телефон нөмірін</b> көрсетіңіз ☎️:",
        example_phone="<i>Мысалы: +7 777 123 45 67</i>",
        success_message=(
            "🎉 <b>Барлығы дайын!</b>\n\n"
            "Сіздің деректеріңіз сәтті сақталды:\n"
            "📄 <b>Чек:</b> {check_link}  \n"
            "👤 <b>Аты-жөніңіз:</b> {fio}\n"
            "🏠 <b>Мекенжай:</b> {address}\n"
            "📞 <b>Телефон:</b> {phone}\n\n"
            "🚀 <i>Жақын арада сізбен хабарласамыз!</i> 😊\n\n"
            "🎟 <b>Ұтысқа қатысу үшін сіздің бірегей нөміріңіз:</b> <code>{user_id}</code>\n\n"
        ),
        file_error="❗ <b>Қате:</b> Өтінемін, <u>чек</u> құжатын pdf форматында жіберіңіз.",
        cloud_upload_error="❗ Бұлтты жүйеге файлды жүктеу кезінде қате орын алды. Қайта көріңіз.",
        processing_data_message="✍️ <i>Деректеріңізді жазып жатырмыз...</i>",
        language_selection_prompt="Өтінемін, қалаған тіліңізді таңдаңыз:",
        language_set_confirmation="Тіл таңдалды: {language}",
        contract_sent_message="📄 <b>Договор</b> жіберілді. Өтінемін, оны қарап шығыңыз.",
        file_send_error="❗ Договорды жіберу кезінде қате орын алды.",
        file_not_found="❗ Серверде договор файлы табылмады.",
        database_save_error="❗ Деректеріңізді сақтау кезінде қате орын алды. Қайта көріңіз.",
        google_sheets_error="❗ Google Sheets-ке деректерді жазу кезінде қате орын алды.",
        count_of_orders=" 🛍️ Қанша тауар сатып алдыңыз?",
        example_count_of_orders="<i>Мысалы: 3</i>",
        error_no_amount_line="❌ Соманы анықтайтын жол табылған жоқ. Чекті pdf-форматта қайта жіберіңіз.",
        error_no_qr_code="❌ QR-код табылған жоқ. Чекті қайта жіберіңіз.",
        error_invalid_amount="❌ Чектегі сома дұрыс емес. Чекті қайта жіберіңіз.",
        error_minimum_amount="❌ Ең төменгі сома {minimum} ₸ болуы керек.",
        error_check_repeat="❌ Осындай QR коды бар чек жіберілді!. Басқа чекті жіберіңіз.",
        receipt_verified_message="✅ Чек сәтті тексерілді. Сома: {amount} ₸. Тауар саны: {count_of_orders}"
    ),
    'ru': Localization(
        start_message=(
            "👋 <b>Добро пожаловать!</b>\n\n"
            "📤 Пожалуйста, отправьте <b>чек</b> в виде <i>фото</i> или <i>документа</i>, "
            "и мы начнем оформление.\n\n"
        ),
        processing_file_message="📥 <i>Обработка вашего файла...</i>",
        check_saved_message="✅ Чек сохранен!",
        check_request="📤 Отправьте новый <b>чек</b> в виде pdf документа:",
        fio_request="3/5 Введите, пожалуйста, <b>ваше ФИО</b> 👤:",
        example_fio="<i>Например: Иванов Иван Иванович</i>",
        region_request="🏠 4/5 Введите, пожалуйста, <b>область доставки</b> 📍:",
        example_region="<i>Например: Алматинская область</i>",
        city_request="🏠 4/5 Введите, пожалуйста, <b>город доставки</b> 📍:",
        example_city="<i>Например: Алматы</i>",
        address_request="🏠 4/5 Введите, пожалуйста, <b>адрес доставки</b> 📍:",
        example_address="<i>Например: ул. Панфилова, д. 12, кв. 34</i>",
        phone_request="📞 5/5 Укажите <b>номер телефона</b> ☎️:",
        example_phone="<i>Например: +7 777 123 45 67</i>",
        success_message=(
            "🎉 <b>Все готово!</b>\n\n"
            "Ваши данные успешно сохранены:\n"
            "📄 <b>Чек:</b> {check_link}  \n"
            "👤 <b>ФИО:</b> {fio}\n"
            "🏠 <b>Адрес:</b> {address}\n"
            "📞 <b>Телефон:</b> {phone}\n\n"
            "🚀 <i>Мы свяжемся с вами в ближайшее время!</i> 😊\n\n"
            "🎟 <b>Ваш уникальный номер для розыгрыша:</b> <code>{user_id}</code>\n\n"
        ),
        file_error="❗ <b>Ошибка:</b> Пожалуйста, отправьте <u>документ</u> с чеком в pdf формате.",
        cloud_upload_error="❗ Произошла ошибка при загрузке файла в облако. Попробуйте еще раз.",
        processing_data_message="✍️ <i>Записываем ваши данные...</i>",
        language_selection_prompt="Пожалуйста, выберите ваш предпочитаемый язык:",
        language_set_confirmation="Язык установлен: {language}",
        contract_sent_message="📄 <b>Договор</b> отправлен. Пожалуйста, ознакомьтесь с ним.",
        file_send_error="❗ Произошла ошибка при отправке договора.",
        file_not_found="❗ Файл договора не найден на сервере.",
        database_save_error="❗ Произошла ошибка при сохранении ваших данных. Пожалуйста, попробуйте позже.",
        google_sheets_error="❗ Произошла ошибка при записи данных в Google Sheets.",
        count_of_orders="2/5 🛍️ Сколько товаров вы хотите купить?",
        example_count_of_orders="<i>Например: 3</i>",
        error_no_amount_line="❌ Строка с суммой не найдена. Пожалуйста, отправьте чек в формате pdf снова.",
        error_no_qr_code="❌ QR-код не найден. Пожалуйста, отправьте чек снова.",
        error_invalid_amount="❌ Сумма в чеке некорректна. Пожалуйста, отправьте чек снова.",
        error_minimum_amount="❌ Минимальная сумма должна быть {minimum} ₸.",\
        error_check_repeat="❌ Чек с таким QR кодом уже отправлен!. Пожалуйста, отправьте другой чек.",
        receipt_verified_message="✅ Чек успешно проверен. Сумма: {amount} ₸. Количество товаров: {count_of_orders}"
    ),
    'en': Localization(
        start_message=(
            "👋 <b>Welcome!</b>\n\n"
            "📤 Please send a <b>receipt</b> as a <i>photo</i> or <i>document</i>, "
            "and we'll start processing your order.\n\n"
        ),
        processing_file_message="📥 <i>Processing your file...</i>",
        check_saved_message="✅ Check saved!",
        check_request="📤 Send a new <b>receipt</b> as a document:",
        fio_request="3/5 Please enter your <b>Full Name</b> 👤:",
        example_fio="<i>Example: John Doe</i>",
        region_request="🏠 4/5 Please enter the <b>delivery region</b> 📍:",
        example_region="<i>Example: Almaty Region</i>",
        city_request="🏠 4/5 Please enter the <b>delivery city</b> 📍:",
        example_city="<i>Example: Almaty</i>",
        address_request="🏠 4/5 Please enter the <b>delivery address</b> 📍:",
        example_address="<i>Example: 12 Panfilov St., Apt. 34</i>",
        phone_request="📞 5/5 Provide your <b>phone number</b> ☎️:",
        example_phone="<i>Example: +7 777 123 45 67</i>",
        success_message=(
            "🎉 <b>All Done!</b>\n\n"
            "Your data has been successfully saved:\n"
            "📄 <b>Receipt:</b> {check_link}  \n"
            "👤 <b>Full Name:</b> {fio}\n"
            "🏠 <b>Address:</b> {address}\n"
            "📞 <b>Phone:</b> {phone}\n\n"
            "🚀 <i>We'll contact you soon!</i> 😊\n\n"
            "🎟 <b>Your unique number for the giveaway:</b> <code>{user_id}</code>\n\n"
        ),
        file_error="❗ <b>Error:</b> Please send a <u>photo</u> or <u>document</u> with the receipt.",
        cloud_upload_error="❗ An error occurred while uploading the file to the cloud. Please try again.",
        processing_data_message="✍️ <i>Saving your data...</i>",
        language_selection_prompt="Please select your preferred language:",
        language_set_confirmation="Language set to: {language}",
        contract_sent_message="📄 <b>Contract</b> has been sent. Please review it.",
        file_send_error="❗ An error occurred while sending the contract.",
        file_not_found="❗ Contract file not found on the server.",
        database_save_error="❗ An error occurred while saving your data. Please try again later.",
        google_sheets_error="❗ An error occurred while writing data to Google Sheets.",
        count_of_orders="2/5 🛍️ How many items would you like to purchase?",
        example_count_of_orders="<i>Example: 3</i>",
        error_no_amount_line="❌ The line with the amount could not be found. Please resend the receipt in the pdf format.",
        error_no_qr_code="❌ QR code not found. Please resend the receipt.",
        error_invalid_amount="❌ The amount in the receipt is invalid. Please resend the receipt.",
        error_minimum_amount="❌ The minimum amount must be {minimum} ₸.",
        error_check_repeat="❌ A check with this QR code has already been sent!. Please send another check.",
        receipt_verified_message="✅ The receipt has been successfully verified. Amount: {amount} ₸. Number of items: {count_of_orders}"
    )
}