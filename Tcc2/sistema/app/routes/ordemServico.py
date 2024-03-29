from flask import render_template, url_for, redirect, request, flash, jsonify, Response
from app import app, db
from app.models import OrdemServico, Usuario, TipoBomba
from flask_login import current_user
import datetime, json
from flask_login import login_required

@app.route('/ordemServicoAndamento', methods=['GET', 'POST'])
@login_required
def ordemServicoAndamento():

    usuarios = Usuario.query.all()
    equipamentos = TipoBomba.query.all()
    page = request.args.get('page', 1, type=int)
    ordens = OrdemServico.query.filter_by(situacao=False).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('ordemServicoAndamento', page=ordens.next_num) \
        if ordens.has_next else None
    prev_url = url_for('ordemServicoAndamento', page=ordens.prev_num) \
        if ordens.has_prev else None


    return render_template('ordemServico/lista.html', next_url=next_url, prev_url=prev_url , lista = ordens.items,
                           usuarios=usuarios, equipamentos=equipamentos, title='Ordem de serviço')

@app.route('/novaOrdem', methods=['GET', 'POST'])
def novaOrdem():

    if request.method == 'POST':

        descricao = (request.form.get('descricao'))
        equipamento = (request.form.get('equipamento'))
        executor = (request.form.get('executor'))
        observacao = (request.form.get('observacao'))

        idExecutor = int(executor)

        if descricao and equipamento and executor:

            if idExecutor == current_user.id:

                ordem = OrdemServico(descricao=descricao, equipamento=equipamento, executor=idExecutor, observacao=observacao,
                                     dataHoraInicio=datetime.datetime.now(), situacao=False)

                db.session.add(ordem)
                db.session.commit()

                flash('Inserido com sucesso!', 'info')
                return redirect(url_for('ordemServicoAndamento'))

            flash('O executor não é o mesmo usuário logado!', 'error')

        flash('Não foi possível abrir nova ordem de serviço!', 'error')

    return redirect(url_for('ordemServicoAndamento'))


@app.route("/finalizarOrdem/<int:id>", methods=['GET', 'POST'])
@login_required
def finalizarOrdem(id):

    ordem = OrdemServico.query.filter_by(id = id).first()

    if ordem and ordem.situacao is False:

        executor = int(ordem.executor)

        if executor == current_user.id:

            ordem.situacao = True
            ordem.dataHoraTermino = datetime.datetime.now()

            db.session.commit()

            flash('Finalizado com sucesso!', 'info')
            return redirect(url_for("ordemServicoAndamento"))

        flash('Você não pode finalizar ordem de outros executores!', 'error')
        return redirect(url_for("ordemServicoAndamento"))

    flash('Não foi possível finalizar!', 'error')
    return redirect(url_for("ordemServicoAndamento"))

@app.route('/autocompleteBombas', methods=['GET'])
def autocompleteBombas():

        bombas = TipoBomba.query.all()

        lista = []
        for b in bombas:
                lista.append({'id': b.id, 'tipo': b.tipo})


        return Response(json.dumps(lista), mimetype='application/json')


@app.route('/somenteMinhasOrdensAbertas',  methods=['GET', 'POST'])
def somenteMinhasOrdensAbertas():

    usuarios = Usuario.query.all()
    equipamentos = TipoBomba.query.all()
    user = current_user.id

    page = request.args.get('page', 1, type=int)
    ordens = OrdemServico.query.filter(OrdemServico.executor == user).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('somenteMinhasOrdensAbertas', page=ordens.next_num) \
        if ordens.has_next else None
    prev_url = url_for('somenteMinhasOrdensAbertas', page=ordens.prev_num) \
        if ordens.has_prev else None

    return render_template('ordemServico/lista.html', next_url=next_url, prev_url=prev_url, lista=ordens.items,
                           usuarios=usuarios, equipamentos=equipamentos, title='Ordem de serviço')



@app.route('/ordensFechadas',  methods=['GET', 'POST'])
def ordensFechadas():

    usuarios = Usuario.query.all()
    equipamentos = TipoBomba.query.all()

    page = request.args.get('page', 1, type=int)
    ordens = OrdemServico.query.filter(OrdemServico.situacao==True).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('ordensFechadas', page=ordens.next_num) \
        if ordens.has_next else None
    prev_url = url_for('ordensFechadas', page=ordens.prev_num) \
        if ordens.has_prev else None

    return render_template('ordemServico/lista.html', next_url=next_url, prev_url=prev_url, lista=ordens.items,
                           usuarios=usuarios, equipamentos=equipamentos, title='Ordem de serviço')