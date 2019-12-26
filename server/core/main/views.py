"""
views.py -> Verwaltet Seiten
"""
from flask import Blueprint, render_template, url_for, abort, redirect, request, send_file
from flask_login import current_user, login_user, logout_user, login_required

from core import db, bcrypt, logger
from core.models import User
from core.main.forms import LoginForm, StockSelect

from core.packages.plots import candlestick
from core.packages.data import get_data
from core.packages.logger import init_logger
from core.packages.algorithms.linear import run

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login Seite
    
    Returns:
        response: Login Seite
    """
    if current_user.is_authenticated:

        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=False)
            logger.info('Logged in as: {}'.format(form.username.data))

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:

            logger.info('Failed to login as: {}'.format(form.username.data))

    return render_template('login.html', title='Login', form=form)


@main.route('/home')
@login_required
def home():
    """Home Seite
    
    Returns:
        response: Home Seite
    """
    return render_template('home.html', title='Home')


@main.route('/stocks', methods=['GET', 'POST'])
@login_required
def stocks():
    """Aktien Seite
    
    Returns:
        response: Aktien Seite
    """
    form = StockSelect()

    if form.validate_on_submit():

        stock = form.stock.data.upper()

        try:
            logger.info('Plotting stock: {}'.format(stock))
            data = get_data(stock)
            prediction = run(data, stock)

            return render_template('graph.html', title=stock, plot=candlestick(data, stock), data=prediction)

        except Exception as e:

            return abort(404, 'Unknown stock ticker: %s' % stock)

    return render_template('stocks.html', title='Stocks', form=form)


@main.route('/documentation')
@login_required
def documentation():
    """Dokumentation
    
    Returns:
        response: Dokumentation
    """
    return send_file('.\\static\\documentation.pdf')


@main.route('/logout')
@login_required
def logout():
    """Logout Seite
    
    Returns:
        response: Logout Seite
    """
    if current_user.is_authenticated:

        logout_user()

        return redirect(url_for('main.login'))

