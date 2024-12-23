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
    region_request: str
    city_request: str
    address_request: str
    phone_request: str
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
        fio_request="2/4 Өтінемін, <b>Аты-жөніңізді</b> енгізіңіз 👤:",
        region_request="🏠 3/4 Өтінемін, <b>жеткізу облысын</b> енгізіңіз 📍:",
        city_request="🏠 3/4 Өтінемін, <b>жеткізу қаласын</b> енгізіңіз 📍:",
        address_request="🏠 3/4 Өтінемін, <b>жеткізу мекенжайын</b> енгізіңіз 📍:",
        phone_request="📞 4/4 <b>Телефон нөмірін</b> көрсетіңіз ☎️:",
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
        file_error="❗ <b>Қате:</b> Өтінемін, <u>фото</u> немесе <u>чек</u> құжатын жіберіңіз.",
        cloud_upload_error="❗ Бұлтты жүйеге файлды жүктеу кезінде қате орын алды. Қайта көріңіз.",
        processing_data_message="✍️ <i>Деректеріңізді жазып жатырмыз...</i>",
        language_selection_prompt="Өтінемін, қалаған тіліңізді таңдаңыз:",
        language_set_confirmation="Тіл таңдалды: {language}",
        contract_sent_message="📄 <b>Договор</b> жіберілді. Өтінемін, оны қарап шығыңыз.",
        file_send_error="❗ Договорды жіберу кезінде қате орын алды.",
        file_not_found="❗ Серверде договор файлы табылмады.",
        database_save_error="❗ Деректеріңізді сақтау кезінде қате орын алды. Қайта көріңіз.",
        google_sheets_error="❗ Google Sheets-ке деректерді жазу кезінде қате орын алды.",
    ),
    'ru': Localization(
        start_message=(
            "👋 <b>Добро пожаловать!</b>\n\n"
            "📤 Пожалуйста, отправьте <b>чек</b> в виде <i>фото</i> или <i>документа</i>, "
            "и мы начнем оформление.\n\n"
        ),
        processing_file_message="📥 <i>Обработка вашего файла...</i>",
        check_saved_message="✅ Чек сохранен!",
        check_request="📤 Отправьте новый <b>чек</b> в виде фото или документа:",
        fio_request="2/4 Введите, пожалуйста, <b>ваше ФИО</b> 👤:",
        region_request="🏠 3/4 Введите, пожалуйста, <b>область доставки</b> 📍:",
        city_request="🏠 3/4 Введите, пожалуйста, <b>город доставки</b> 📍:",
        address_request="🏠 3/4 Введите, пожалуйста, <b>адрес доставки</b> 📍:",
        phone_request="📞 4/4 Укажите <b>номер телефона</b> ☎️:",
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
        file_error="❗ <b>Ошибка:</b> Пожалуйста, отправьте <u>фото</u> или <u>документ</u> с чеком.",
        cloud_upload_error="❗ Произошла ошибка при загрузке файла в облако. Попробуйте еще раз.",
        processing_data_message="✍️ <i>Записываем ваши данные...</i>",
        language_selection_prompt="Пожалуйста, выберите ваш предпочитаемый язык:",
        language_set_confirmation="Язык установлен: {language}",
        contract_sent_message="📄 <b>Договор</b> отправлен. Пожалуйста, ознакомьтесь с ним.",
        file_send_error="❗ Произошла ошибка при отправке договора.",
        file_not_found="❗ Файл договора не найден на сервере.",
        database_save_error="❗ Произошла ошибка при сохранении ваших данных. Пожалуйста, попробуйте позже.",
        google_sheets_error="❗ Произошла ошибка при записи данных в Google Sheets.",
    ),
    'en': Localization(
        start_message=(
            "👋 <b>Welcome!</b>\n\n"
            "📤 Please send a <b>receipt</b> as a <i>photo</i> or <i>document</i>, "
            "and we'll start processing your order.\n\n"
        ),
        processing_file_message="📥 <i>Processing your file...</i>",
        check_saved_message="✅ Check saved!",
        check_request="📤 Send a new <b>receipt</b> as a photo or document:",
        fio_request="2/4 Please enter your <b>Full Name</b> 👤:",
        region_request="🏠 3/4 Please enter the <b>delivery region</b> 📍:",
        city_request="🏠 3/4 Please enter the <b>delivery city</b> 📍:",
        address_request="🏠 3/4 Please enter the <b>delivery address</b> 📍:",
        phone_request="📞 4/4 Provide your <b>phone number</b> ☎️:",
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
    )
}
