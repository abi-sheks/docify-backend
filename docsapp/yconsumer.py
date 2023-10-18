import y_py as Y
from docsapp.models.editable import Editable
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from ypy_websocket.django_channels_consumer import YjsConsumer
from ypy_websocket.yutils import create_update_message


class EditableConsumer(YjsConsumer):
    def make_room_name(self) -> str:
        # modify the room name here
        return self.scope["url_route"]["kwargs"]["id"]

    async def make_ydoc(self) -> Y.YDoc:
        doc = Y.YDoc()
        init_state = await database_sync_to_async(self.fetch_doc)()
        print(f"The init state is {init_state}")
        if init_state != b'':
            print("Entering")
            # init_update = Y.encode_state_as_update(doc, init_state_vec)
            # print(f"The init update is {init_update}")
            Y.apply_update(doc, init_state)
        # fill doc with data from DB here
        doc.observe_after_transaction(self.on_update_event)
        return doc

    async def connect(self):
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        print(f"data from client is {bytes_data}")
        await super(EditableConsumer, self).receive(text_data, bytes_data)
        await database_sync_to_async(self.update_doc)(Y.encode_state_as_update(self.ydoc))

    def on_update_event(self, event):
        # process event here
        ...
        # print(event.get_update())
        # database_sync_to_async(self.update_doc)(event.after_state)

    async def doc_update(self, update_wrapper):
        update = update_wrapper["update"]
        print(update)
        Y.apply_update(self.ydoc, update)
        await self.group_send_message(create_update_message(update))

    def update_doc(self, update):
        if update is not None: 
            doc = Editable.objects.get(id=self.room_name)
            doc.content = update
            doc.save()
            print("Happening?")

    def fetch_doc(self):
        print(f"The room name is {self.room_name}")
        cont = Editable.objects.get(id=self.room_name).content
        print(f"the cont is {cont}")
        return cont

def send_doc_update(room_name, update):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(room_name, {"type": "doc_update", "update": update})