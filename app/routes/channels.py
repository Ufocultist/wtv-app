from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required

from ..extensions import db
from ..functions import save_picture
from ..forms import CreateChannelForm
from ..models.channels import Channels
from ..models.packs import Packs

channel = Blueprint('channel', __name__)


@channel.route('/channel/list', methods=['GET'])
@login_required
def all():
    channels = Channels.query.order_by(Channels.number).all()
    return render_template('channel/all.html', channels=channels)


@channel.route('/channel/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateChannelForm()
    form.pack.choices = [p.pack_name for p in Packs.query]
    if form.validate_on_submit():
        channel_filename = save_picture(form.logo.data)
        pack_id = Packs.query.filter_by(pack_name=form.pack.data).first().id
        new_channel = Channels(number=form.number.data,
                               channel_name=form.name.data,
                               logo=channel_filename,
                               description=form.description.data,
                               pack=pack_id)
        try:
            db.session.add(new_channel)
            db.session.commit()
            flash(f"Channel created", "success")
            return redirect('/channel/list')
        except Exception as e:
            print(str(e))
            flash(f"Failed to create channel", "danger")

    return render_template('channel/create.html', form=form)


@channel.route('/channel/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    channel = Channels.query.get(id)
    # form = CreateChannelForm()
    # form.pack.data = Channels.query.filter_by(id=channel.pack).first().id
    # form.pack.choices = [p.pack_name for p in Packs.query]
    if request.method == 'POST':
        # for value in channel:
        #     channel.value = request.form.get(value)
        channel.channel_name = request.form.get('channel_name')
        channel.description = request.form.get('description')
        #channel.pack = Packs.query.filter_by(id=channel.pack).first().name
        try:
            db.session.commit()
            return redirect('/channel/list')
        except Exception as e:
            print('Updating Channel Failed', str(e))
            db.session.rollback()
    else:
        return render_template('channel/update.html', channel=channel)


@channel.route('/channel/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    channel = Channels.query.get(id)
    try:
        db.session.delete(channel)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print('Deleting Channel Failed', str(e))
        db.session.rollback()
