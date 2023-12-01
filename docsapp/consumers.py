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
        if init_state.content != b'':
            Y.apply_update(doc, init_state.content)
        doc.observe_after_transaction(self.on_update_event)
        return doc

    async def connect(self):
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        await super(EditableConsumer, self).receive(text_data, bytes_data)
        #Bad solution?
        curr_db_state = await database_sync_to_async(self.fetch_doc)()
        if curr_db_state.content != Y.encode_state_as_update(self.ydoc) and curr_db_state.content != b'':
            Y.apply_update(self.ydoc, curr_db_state.content)
        content_as_text = self.ydoc.get_text("quill").__str__()
        curr_db_state.contenttext = content_as_text
        await database_sync_to_async(curr_db_state.save)();
        await database_sync_to_async(self.update_doc)(Y.encode_state_as_update(self.ydoc))
    
    async def disconnect(self, code):
        update = Y.encode_state_as_update(self.ydoc)
        content_as_text = self.ydoc.get_text("quill").__str__()
        print(content_as_text)
        #primitive solution for es searching
        doc = await database_sync_to_async(self.fetch_doc)();
        doc.contenttext = content_as_text
        await database_sync_to_async(doc.save)();
        await database_sync_to_async(self.update_doc)(update)
        await self.group_send_message(create_update_message(update))
        await super().disconnect(code)

    def on_update_event(self, event):
        # process event here
        ...

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
        content = Editable.objects.get(id=self.room_name)
        return content

def send_doc_update(room_name, update):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(room_name, {"type": "doc_update", "update": update})