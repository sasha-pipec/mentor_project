from photobatle.models import Photo

MAX_NUMBER_OF_COMMENTS_FOR_DETAIL_PHOTO = 3
METADATA = 'Metadata'
RESPONSE = 'Response'
ERROR = 'Error'
STATUS_ERROR = 'Status_error'
ID_OF_USER = 'user_id'
SORT_LIST = ['like_count', 'comment_count', 'updated_at', 'id']
STATUS_LIST = [Photo.ON_DELETION, Photo.ON_MODERATION, Photo.APPROVED, Photo.REJECTED]
DIRECTION_LIST = ['asc', 'desc']
DEFAULT_SORT_VALUE = 'id'
TOKEN = 'Token'
DEFAULT_PHOTO_PATH = '/static/image/default-photo-post.jpeg'
