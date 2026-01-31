import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, make_response
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from models import AdminUsers, ServiceRequest, SecurityLog
from extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def device_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_cookie = request.cookies.get('whiztech_auth_token')
        psst = os.getenv('DK')

        if not psst:
            print("CRITICAL SECURITY ERROR: UI_CONFIG_TOKEN is missing!")
            abort(500)

        if user_cookie != psst:
            try:
                log = SecurityLog(
                    ip_address=request.remote_addr,
                    user_agent=str(request.user_agent),
                    endpoint=request.path,
                    risk_lvl="HIGH",
                    result="BLOCKED",
                    details="Missing device key"
                )
                db.session.add(log)
                db.session.commit()
            except:
                pass
            abort(404)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
@device_key_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AdminUsers.query.filter_by(admin_username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        
        flash('Invalid credentials')

    return render_template('admin/login.html')

@admin_bp.route('dashboard')
@login_required
@device_key_required
def dashboard():
    tickets = ServiceRequest.query.order_by(ServiceRequest.date_created.desc()).all()
    return render_template('admin/dashboard.html', tickets=tickets)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    # 1. Get the ticket from the DB (or 404 if not found)
    ticket = ServiceRequest.query.get_or_404(ticket_id)

    # 2. Handle the "Update" Button Click
    if request.method == 'POST':
        ticket.status = request.form.get('status')
        ticket.admin_notes = request.form.get('admin_notes')
        
        try:
            db.session.commit()
            flash('Ticket updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating ticket: {e}', 'error')
            
        # Refresh the page to show changes
        return redirect(url_for('admin.ticket_detail', ticket_id=ticket.id))

    # 3. Show the Ticket Detail Page
    return render_template('admin/ticket_detail.html', ticket=ticket)