from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required

from ..extensions import db
from ..forms import CreatePackForm
from ..models.packs import Packs

pack = Blueprint('pack', __name__)


@pack.route('/pack/list', methods=['GET'])
@login_required
def all():
    return render_template('pack/all.html',
                           packs=Packs.query.order_by(Packs.pack_name).all())


@pack.route('/pack/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePackForm()
    if form.validate_on_submit():
        new_pack = Packs(pack_name=form.name.data,
                         description=form.description.data)
        try:
            db.session.add(new_pack)
            db.session.commit()
            flash(f"Pack created", "success")
        except Exception as e:
            print(str(e))
            flash(f"Pack creation failed", "danger")

    return render_template('pack/create.html', form=form)


@pack.route('/pack/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    pack = Packs.query.get(id)
    if request.method == 'POST':
        pack.pack_name = request.form.get('pack_name')
        pack.description = request.form.get('description')
        try:
            db.session.commit()
            return redirect('pack/list')
        except Exception as e:
            print(str(e))
            flash(f"Pack update failed", "danger")
    else:
        return render_template('pack/update.html', pack=pack)


@pack.route('/pack/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    pack = Packs.query.get(id)
    try:
        db.session.delete(pack)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(str(e))
        flash(f"Pack deletion failed", "danger")
        db.session.rollback()

