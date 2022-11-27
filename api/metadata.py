from rest_framework.metadata import BaseMetadata


class DetailPhotoMetadata(BaseMetadata):

    def determine_metadata(self, request, view):
        return {
            'example': 'example_metadata'
        }
