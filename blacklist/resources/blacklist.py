from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from blacklist.models import Blacklist, db

class AddToBlacklist(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data or 'email' not in data or 'app_uuid' not in data:
            return {"message": "Missing required fields 'email' or 'app_uuid'"}, 400

        existing_entry = Blacklist.query.filter_by(email=data['email']).first()
        if existing_entry:
            return {"message": "El email ya está en la lista negra"}, 400

        new_entry = Blacklist(
            email=data['email'],
            app_uuid=data['app_uuid'],
            blocked_reason=data.get('blocked_reason', ''),
            ip_address=request.remote_addr
        )

        db.session.add(new_entry)
        db.session.commit()

        return {"message": "Email added to blacklist"}, 201

    @jwt_required()
    def delete(self, email):
        entry = Blacklist.query.filter_by(email=email).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return {"message": "Email removed from blacklist"}, 200
        return {"message": "Email not found in blacklist"}, 404


class CheckBlacklist(Resource):
    @jwt_required()
    def get(self, email):
        entry = Blacklist.query.filter_by(email=email).first()
        if entry:
            return {
                "is_blacklisted": True,
                "reason": entry.blocked_reason
            }, 200
        return {
            "is_blacklisted": False
        }, 404
