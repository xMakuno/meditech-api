from flask import Blueprint, request, jsonify, session
from flask_login import login_user, login_required, current_user
from .models import Subscription

subscriptions = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')


@subscriptions.route('/', methods=['GET'])
def get_all_subscriptions():
    subscriptions_list = Subscription.query.all()
    return jsonify([{
        'id': subscription.id,
        'plan': subscription.plan,
        'start_date': subscription.start_date,
        'active': subscription.active,
        'user_id': subscription.user_id,
        'insurance_id': subscription.insurance_id
    } for subscription in subscriptions_list]), 200


@subscriptions.route('/self', methods=['GET'])
@login_required
def get_all_self_subscriptions():
    user_id = current_user.id
    subscriptions_list = Subscription.query.filter_by(user_id=user_id)
    return jsonify([{
        'id': subscription.id,
        'plan': subscription.plan,
        'start_date': subscription.start_date,
        'active': subscription.active,
        'user_id': subscription.user_id,
        'insurance_id': subscription.insurance_id
    } for subscription in subscriptions_list]), 200
