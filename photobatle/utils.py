from photobatle.models import *


class DataMixin:

    def all_comments_for_post(self, parent_id=None, photo_id=None):
        # function for getting all the answers under the comment
        comments = Comment.objects.filter(photo_id=photo_id, parent_id=parent_id)
        all_answer_for_comment = []
        if len(comments) != 0:
            for comment in comments:
                all_answer_for_comment.append(comment)
                childs = self.all_comments_for_post(parent_id=comment.pk, photo_id=comment.photo_id, )
                if len(childs) != 0:
                    for child in childs:
                        all_answer_for_comment.append(child)
        else:
            return all_answer_for_comment
        return all_answer_for_comment
