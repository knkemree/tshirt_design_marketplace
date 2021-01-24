import json
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from orders.models import OrderItem
from django.utils.translation import gettext

# will be triggered every time a LogEntry is saved i.e. every time an action is made.
@receiver(post_save, sender=LogEntry)
def ready_to_ship_changed(instance, **kwargs):
    print(instance.change_message)
    try:
        change_message = json.loads(instance.change_message)
        for each in change_message[0]['changed']['fields']:
            if each == 'Ready to ship':
                item = OrderItem.objects.get(id=instance.object_id)
                if item.ready_to_ship:
                    item.log_entry = 'Marked RTS:',instance.user.get_full_name()
                    item.save()
                    print('Marked RTS:',instance.user.get_full_name())
                else:
                    item.log_entry = 'Unmarked RTS:',instance.user.get_full_name()
                    item.save()
                    print('Unmarked RTS:',instance.user.get_full_name())
    except:
        pass
    # print(instance.ready_to_ship)
    # if instance.ready_to_ship:
    #     logs = LogEntry.objects.filter(object_id=instance)[0]
    #     print
    #     instance.log_entry = "Marked"
        
    # else:
    #     instance.log_entry = "Unmarked"
        
    # print('heyyyy')
    # ready_to_ship_changes = LogEntry.objects.filter(content_type_id__model = 'orderitem', action_flag = 2)
    # print(ready_to_ship_changes)
    # for action in ready_to_ship_changes:
    #     try:
    #         change_message = json.loads(action.change_message)
    #         for each in change_message[0]['changed']['fields']:
    #             if each == 'Ready to ship':
    #                 item = OrderItem.objects.get(id=action.object.id)
    #                 item.log_entry = 'Ready to ship changed by ',action.user, action.object_id
    #                 item.save()
    #                 print('Ready to ship changed by ',action.user, action.object_id)
    #     except:
    #         pass
