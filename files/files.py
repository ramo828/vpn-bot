class FileModel:
    def __init__(self, name, path, type):
        self.name = name
        self.path = path
        self.type = type

files = {
    FileModel(name="SampleVideo1280x7201mb.mp4", path="files/videos/", type="video"),
    FileModel(name="SampleVideo1280x7202mb.mp4", path="files/videos/", type="video"),
    FileModel(name="SampleVideo1280x7205mb.mp4", path="files/videos/", type="video"),
    FileModel(name="SampleJPGImage50kbmb.jpg", path="files/images/", type="image"),
    FileModel(name="SampleJPGImage100kbmb.jpg", path="files/images/", type="image"),
    FileModel(name="SampleJPGImage200kbmb.jpg", path="files/images/", type="image"),
    FileModel(name="SampleJPGImage500kbmb.jpg", path="files/images/", type="image"),
    FileModel(name="SamplePDFFile5mb.pdf", path="files/documents/", type="doc"),
}

file_lang = {
    "az": {
        "Images": "Şəkillər",
        "Videos": "Videolar",
        "Documents": "Sənədlər",
        "load": "göndərilir...",
        "unsupport": "Bu fayl növü dəstəklənmir.",
        "file_not_found": "Fayl tapılmadı, xahiş edirik fayl yolunu yoxlayın.",
        "error": "Fayl göndərilərkən xəta baş verdi"
    },
    "ru": {
        "Images": "Изображения",
        "Videos": "Видео",
        "Documents": "Документы",
        "load": "отправляется...",
        "unsupport": "Этот тип файла не поддерживается.",
        "file_not_found": "Файл не найден, пожалуйста, проверьте путь к файлу.",
        "error": "Ошибка при отправке файла"
    },
    "en": {
        "Images": "Images",
        "Videos": "Videos",
        "Documents": "Documents",
        "load": "sending...",
        "unsupport": "This file type is not supported.",
        "file_not_found": "File not found, please check the file path.",
        "error": "Error while sending the file"
    },
    "tr": {
        "Images": "Görüntüler",
        "Videos": "Videolar",
        "Documents": "Belgeler",
        "load":"gönderiliyor...",
        "unsupport":"Bu dosya türü desteklenmiyor.",
        "file_not_found":"Dosya bulunamadı, lütfen dosya yolunu kontrol edin.",
        "error":"Dosya gönderilirken hata",
    }
}