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
            # init_update = Y.encode_state_as_update(doc, init_state_vec)
            # print(f"The init update is {init_update}")
            Y.apply_update(doc, init_state)
        # fill doc with data from DB here
        doc.observe_after_transaction(self.on_update_event)
        return doc

    async def connect(self):
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        await super(EditableConsumer, self).receive(text_data, bytes_data)
        print(f"Current state is {Y.encode_state_as_update(self.ydoc)}")
        #Bad solution?
        curr_db_state = await database_sync_to_async(self.fetch_doc)()
        if curr_db_state != Y.encode_state_as_update(self.ydoc):
            Y.apply_update(self.ydoc, curr_db_state)
        await database_sync_to_async(self.update_doc)(Y.encode_state_as_update(self.ydoc))
    
    async def disconnect(self, code):
        update = Y.encode_state_as_update(self.ydoc)
        await database_sync_to_async(self.update_doc)(update)
        await self.group_send_message(create_update_message(update))
        print(f"The update being applied to db is {Y.encode_state_as_update(self.ydoc)}")
        print("Happening on disconnect")
        await super().disconnect(code)

    def on_update_event(self, event):
        # process event here
        ...
        # print(event.get_update())
        # database_sync_to_async(self.update_doc)(event.after_state)

    async def doc_update(self, update_wrapper):
        update = update_wrapper["update"]
        Y.apply_update(self.ydoc, update)
        await self.group_send_message(create_update_message(update))

    def update_doc(self, update):
        if update is not None: 
            doc = Editable.objects.get(id=self.room_name)
            doc.content = update
            doc.save()

    def fetch_doc(self):
        cont = Editable.objects.get(id=self.room_name).content
        return cont

def send_doc_update(room_name, update):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(room_name, {"type": "doc_update", "update": update})