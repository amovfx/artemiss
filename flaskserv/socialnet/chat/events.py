from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room, send

from ..models import Post
from .. import socketio


@socketio.on('joined', namespace="/chat")
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message['room']
    print(f"Joining room" + session.get('room'))
    session['room'] = message.get('room')
    join_room(message.get('room'))
    emit('status', {'msg': current_user.name + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    print(message)
    room = session.get('room')
    new_post = Post(author_id = current_user,
                    message=message['msg'],
                    tribe=session['TRIBE'],
                    room=room)
    emit('message', {'msg': current_user.name + ':' + message['msg']}, room=room)



@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)