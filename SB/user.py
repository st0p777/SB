from .models import Ticket, Queue, KBCategory, KBItem
from .settings import settings as helpdesk_settings


def huser_from_request(req):
    return HelpdeskUser(req.user)


class HelpdeskUser:
    def __init__(self, user):
        self.user = user

    def get_queues(self):
        user = self.user
        all_queues = Queue.objects.all()
        public_ids = [q.pk for q in
                      Queue.objects.filter(allow_public_submission=True)]
        limit_queues_by_user = \
            helpdesk_settings.HELPDESK_ENABLE_PER_QUEUE_STAFF_PERMISSION \
            and not user.is_superuser
        if limit_queues_by_user:
            id_list = [q.pk for q in all_queues if user.has_perm(q.permission_name)]
            id_list += public_ids
            return all_queues.filter(pk__in=id_list)
        else:
            return all_queues

    def get_allowed_kb_categories(self):
        categories = []
        for cat in KBCategory.objects.all():
            if self.can_access_kbcategory(cat):
                categories.append(cat)
        return categories

    def get_assigned_kb_items(self):
        kbitems = []
        for item in KBItem.objects.all():
            if item.get_team() and item.get_team().is_member(self.user):
                kbitems.append(item)
        return kbitems

    def get_tickets_in_queues(self):
        return Ticket.objects.filter(queue__in=self.get_queues())

    def has_full_access(self):
        return self.user.is_superuser or self.user.is_staff \
            or helpdesk_settings.HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE

    def can_access_queue(self, queue):
        if self.has_full_access():
            return True
        else:
            return (
                helpdesk_settings.HELPDESK_ENABLE_PER_QUEUE_STAFF_PERMISSION
                and
                self.user.has_perm(queue.permission_name)
            )

    def can_access_ticket(self, ticket):
        user = self.user
        if self.can_access_queue(ticket.queue):
            return True
        elif self.has_full_access() or \
                (ticket.assigned_to and user.id == ticket.assigned_to.id):
            return True
        else:
            return False

    def can_access_kbcategory(self, category):
        if category.public:
            return True
        return self.has_full_access() or (category.queue and self.can_access_queue(category.queue))
