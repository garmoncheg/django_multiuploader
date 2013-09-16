# Expiration time in seconds, one hour as default

# from django.conf import settings

# TIME_ZONE = settings.TIME_ZONE
# LOGGING_CONFIG = settings.LOGGING_CONFIG


MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600

MULTIUPLOADER_FILES_FOLDER = 'multiuploader'


MULTIUPLOADER_FORMS_SETTINGS = {
    'default': {
        'FILE_TYPES': ['jpg', 'jpeg', 'png', 'txt', 'zip', 'rar', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp', 'rtf'],
        'CONTENT_TYPES': [
                'image/jpeg',
                'image/png',
                'text/plain',
                'application/zip',
                'application/x-rar-compressed',
                'application/octet-stream',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.oasis.opendocument.text',
                'application/vnd.oasis.opendocument.spreadsheet',
                'application/vnd.oasis.opendocument.presentation',
                'text/rtf',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True
    },
    'images': {
        'FILE_TYPES': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'tiff', 'ico'],
        'CONTENT_TYPES': [
            'image/gif',
            'image/jpeg',
            'image/pjpeg',
            'image/png',
            'image/svg+xml',
            'image/tiff',
            'image/vnd.microsoft.icon',
            'image/vnd.wap.wbmp',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True
    },
    'video': {
        'FILE_TYPES': ['flv', 'mpg', 'mpeg', 'mp4' ,'avi', 'mkv', 'ogg', 'wmv', 'mov', 'webm'],
        'CONTENT_TYPES': [
            'video/mpeg',
            'video/mp4',
            'video/ogg',
            'video/quicktime',
            'video/webm',
            'video/x-ms-wmv',
            'video/x-flv',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True
    },
    'audio': {
        'FILE_TYPES': ['mp3', 'mp4', 'ogg', 'wma', 'wax', 'wav', 'webm'],
        'CONTENT_TYPES': [
            'audio/basic',
            'audio/L24',
            'audio/mp4',
            'audio/mpeg',
            'audio/ogg',
            'audio/vorbis',
            'audio/x-ms-wma',
            'audio/x-ms-wax',
            'audio/vnd.rn-realaudio',
            'audio/vnd.wave',
            'audio/webm'
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True
    },
}