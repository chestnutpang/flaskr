from flask import Blueprint, request, g
import datetime
from flaskr import comm, model
from flaskr.err_code import ErrorCode
from flaskr.exception import NormalError
from sqlalchemy import func

bp = Blueprint('bill', __name__)


@bp.route('/record', methods=['POST'])
@comm.login_required
def record_bill():
    """记账"""
    params = request.get_json()
    record_type = params.get('record_type')
    content = params.get('content')
    amount = params.get('amount')
    record_time = params.get('time')
    user_id = g.user._id
    if record_time is None:
        now = datetime.datetime.now().timetuple()[:3]
    else:
        now = check_time(record_time)
    bk = model.Bill(record_type, amount, content, user_id, now)
    bk.save()
    return {}


@bp.route('/list', methods=['GET'])
@comm.login_required
def query_bill_list_year():
    """记账列表，年、月、日波动统计 （类别）"""
    params = request.args
    group_by = params.get('group', None)
    record_type = params.get('type', None)
    user_id = g.user._id
    bill_query = model.Bill.query.filter(model.Bill.user_id == user_id)\
        .order_by(model.Bill.record_time, model.Bill.createdAt)
    args = [model.Bill.id, func.sum(model.Bill.amount)]

    if record_type is not None:
        bill_query = bill_query.filter(model.Bill.record_type == record_type)
    if group_by == 'year':
        args.extend([model.Bill.year])
        bill_query = bill_query.group_by(model.Bill.year).with_entities(*args)
        record_time = ''
    elif group_by == 'month':
        year = int(params.get('year', 0))
        args.extend([model.Bill.month])
        bill_query = bill_query.filter(model.Bill.year == year).group_by(model.Bill.month).with_entities(*args)
        record_time = f'{year}'
    elif group_by == 'day':
        year = int(params.get('year', 0))
        month = int(params.get('month', 0))
        args.extend([model.Bill.day])
        bill_query = bill_query.filter(model.Bill.year == year, model.Bill.month == month)\
            .group_by(model.Bill.day).with_entities(*args)
        record_time = f'{year}-{month}'
    else:
        raise NormalError(ErrorCode.COMM_ERROR)
    bill_list = bill_query.all()
    res = []
    for bill in bill_list:
        data = {
            'bill': bill[0],
            'amount': bill[1],
            'time': f'{record_time}-{bill[2]}',
        }
        res.append(data)
    return {
        'list': res
    }


@bp.route('/delete', methods=['POST'])
@comm.login_required
def bill_delete():
    """删除某次账单"""
    params = request.get_json()
    bill_id = params.get('bill')
    user_id = g.user._id
    bill = model.Bill.query.get(bill_id)
    if bill.user_id != user_id:
        raise NormalError(ErrorCode.COMM_ERROR)
    model.Bill.remove(bill)
    return {}


@bp.route('/update', methods=['POST'])
@comm.login_required
def bill_update():
    """更新某次账单"""
    params = request.get_json()
    bill_id = params.get('bill')

    record_type = params.get('record_type')
    alias = params.get('alias')
    try:
        amount = int(params.get('amount'), 0)
    except AttributeError:
        raise NormalError(ErrorCode.COMM_ERROR)
    record_time = params.get('time')

    key_list = ['record_type', 'alias', 'amount']
    attr_list = [record_type, alias, amount]

    user_id = g.user._id
    bill = model.Bill.query.get(bill_id)
    if bill.user_id != user_id:
        raise NormalError(ErrorCode.COMM_ERROR)
    change = False

    for index in range(len(key_list)):
        if key_list[index] is not None:
            if bill.get(key_list[index]) != attr_list[index]:
                bill.set(key_list[index], attr_list[index])
                change = True

    if record_time is not None:
        new_record_time = check_time(record_time)
        if bill.record_time != new_record_time:
            bill.update_time(*new_record_time)
            change = True

    if change is True:
        bill.save()
    return {}


def check_time(record_time):
    try:
        now = comm.ltimesf_str_to_datetime(record_time, '%Y/%m/%d').timetuple()[:3]
    except:
        raise NormalError(ErrorCode.COMM_ERROR)
    return now
