from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from .. import socketio
from app.utils import jwt_functions
from app.decorators import token_required_socket
from app.chat.models import Room, Message

@socketio.on('join', namespace='/chat')
@token_required_socket
def join(message):
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    room = message['room_id']
    user_id = int(payload['user_id'])
    roomObj = Room.query.filter_by(room_id=room).first()
    # check if room exists
    if not roomObj:
        emit('status', {'msg': 'Room does not exist.'})
        disconnect()
        return
    # check if permitted
    if roomObj.seller_id != user_id and roomObj.buyer_id != user_id:
        emit('status', {'msg': 'not allowed'})
        disconnect()
        return
    
    join_room(room)
    emit('status', {'msg': payload['user_id'] + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
@token_required_socket
def text(message):
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    room = int(session.get('room_id'))
    
    Message(room_id=room, sender_id=payload['user_id'], detail=message['detail'], type=message['type']).save()
    emit('message', {'msg': payload['user_id'] + ':' + message['detail']}, room=room)


@socketio.on('left', namespace='/chat')
@token_required_socket
def left(message):
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    room = payload['room_id']
    leave_room(room)
    emit('status', {'msg': payload['user_id'] + ' has left the room.'}, room=room)

