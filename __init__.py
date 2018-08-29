import os
import logging
import time
from flask import render_template, jsonify
from CTFd.utils import admins_only, is_admin, ratelimit, override_template
from CTFd.models import db, Challenges, Keys, Awards, Solves, Files, Tags, Teams, WrongKeys, DatabaseError, Unlocks, Tracking
from CTFd import utils
from logging import getLogger, basicConfig,DEBUG,ERROR
from CTFd.plugins import challenges, register_plugin_assets_directory
from CTFd import utils, CTFdFlask
from flask import session, Blueprint, request, redirect
from flask import current_app as app, request, render_template, url_for
from CTFd.plugins.keys import get_key_class
from  passlib.hash import bcrypt_sha256
from CTFd.utils.decorators import authed_only, during_ctf_time_only, viewable_without_authentication
from CTFd.plugins.challenges import get_chal_class
from werkzeug.routing import Rule
from .smartCommand import SmartTable, createSmartCityTableSession

admin_teams = Blueprint('admin_teams', __name__)
auth = Blueprint('auth', __name__)
challenges2 = Blueprint('challenges', __name__)
basicConfig(level=ERROR)
logger = getLogger(__name__)
teamColorList = ['GRREN','BLUE', 'YELLOW','RED','AQUA', 'PURPLE', 'GOLD','TURQUOIS', 'PINK', 'LIMEGREEN']

#app.url_map(Rule('/register', endpoint='register.colors', methods=['GET', 'POST']))

class SmartCityTeam(db.Model):
	_mapper_args__ = {'polymorphic_identity': 'smart_city'}
	#name = db.Column(None, db.ForeignKey('teams.name'), primary_key=Truep
	id = db.Column(db.Integer, primary_key=True)
	#name = db.Column(db.String(128), unique=True)
	#email = db.Column(db.String(124), unique=True)
	teamId = db.Column(db.String(128))
	color = db.Column(db.String(123))
	image = db.Column(db.Integer)
	def __init__(self, teamId, name, color, image):
		#self.name = name
		self.teamId = teamId
		self.name = name
		self.color = color
		self.image = image 



class SmartCityChallenge(Challenges):
	__mapper_args__ = {'polymorphic_identity': 'smart_city'}
	id = db.Column(None, db.ForeignKey('challenges.id'), primary_key=True)
	buildingId = db.Column(db.String(5))

	def __init__(self, name, description, value, category, buildingId, type): 
		self.name = name
		self.description = description
		self.value = value
		self.category = category
		self.type = type
		#smart_city Challenege value
		self.buildingId = buildingId


class SmartCity(challenges.BaseChallenge):
	id = "smart_city"
	name = "smart_city"
        

	templates = { # Handlebars template used for each aspect of challenge editing and viewing
                        'create' : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-create.njk',
        		'update' : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-update.njk',
			'modal'  : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-modal.njk',
	}

        scripts = {
                        'create' : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-create.js',
			'update' : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-update.js',
			'modal'  : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-modal.js',
        }
	
	@staticmethod
	def create(request):
		"""
		This method is used to process the challege creation request.
		
		:param request:
		:return:
		"""
		
		files = request.files.getlist('files[]')
	
		chal = SmartCityChallenge(
			name= request.form['name'],
			category = request.form['category'],
			description = request.form['description'],
			value = request.form['value'],
			buildingId = request.form['buildingId'],
			type=request.form['chaltype']
		
		)
                
		if 'hidden' in request.form:
			chal.hidden = True
		else:
			chal.hidden = False

		max_attempts = request.form.get('max_attempts')
		if max_attempts and max_attempts.isdigit():
			chal.max_attempts = int(max_attempts)



		logger.debug("Genereted buildingId " + chal.buildingId + " for challenge " + chal.name)
		
		db.session.add(chal)
		db.session.commit() 

		flag = Keys(chal.id, request.form['key'], request.form['key_type[0]'])
		if request.form.get('keydata'):
			flag.data = request.form.get('keydata')
		
		db.session.add(flag)
		db.session.commit()

		for f in files:
			utils.upload_file(file=f, chalid=chal.id)

		db.session.commit()

		print(chal.buildingId)
	
	@staticmethod
	def read(challenge):
		
		challenge = SmartCityChallenge.query.filter_by(id=challenge.id).first()	 
		data = {
			'id': challenge.id,
			'name': challenge.name,
			'value': challenge.value,
			'description': challenge.description,
			'category': challenge.category,
			'hidden': challenge.hidden,
			'max_attempts': challenge.max_attempts,
			'buildingId': challenge.buildingId,
			'type': challenge.type,
			'type_data': {
				'id': SmartCity.id,
				'name': SmartCity.name,
				'templates': SmartCity.templates,
				'scripts': SmartCity.scripts,
			}
		
		}
		return challenge, data

	@staticmethod
	def delete(challenge):
		"""
        	This method is used to delete the resources used by a challenge.

        	:param challenge:
        	:return:
       		 """
        	WrongKeys.query.filter_by(chalid=challenge.id).delete()
        	Solves.query.filter_by(chalid=challenge.id).delete()
        	Keys.query.filter_by(chal=challenge.id).delete()
        	files = Files.query.filter_by(chal=challenge.id).all()
        	for f in files:
            		utils.delete_file(f.id)
        	Files.query.filter_by(chal=challenge.id).delete()
        	Tags.query.filter_by(chal=challenge.id).delete()
        	SmartCityChallenge.query.filter_by(id=challenge.id).delete()
        	Challenges.query.filter_by(id=challenge.id).delete()
        	db.session.commit()


	@staticmethod
    	def attempt(chal, request):
        	"""
        	This method is used to check whether a given input is right or wrong. It does not make any changes and should
        	return a boolean for correctness and a string to be shown to the user. It is also in charge of parsing the
        	user's input from the request itself.

        	:param chal: The Challenge object from the database
        	:param request: The request the user submitted
        	:return: (boolean, string)
        	"""
        	provided_key = request.form['key'].strip()
        	chal_keys = Keys.query.filter_by(chal=chal.id).all() 
        	for chal_key in chal_keys:
			print(chal_key)
            		if get_key_class(chal_key.type).compare(chal_key, provided_key):
                		return True, 'Correct'
        	return False, 'Incorrect'

    	@staticmethod
    	def solve(team, chal, request):
        	"""
        	This method is used to insert Solves into the database in order to mark a challenge as solved.

        	:param team: The Team object from the database
        	:param chal: The Challenge object from the database
        	:param request: The request the user submitted
        	:return:
        	"""
        	chal = SmartCityChallenge.query.filter_by(id=chal.id).first()

        	solve_count = Solves.query.join(Teams, Solves.teamid == Teams.id).filter(Solves.chalid==chal.id, Teams.banned==False).count()

        	#value = (((chal.minimum - chal.initial)/(chal.decay**2)) * (solve_count**2)) + chal.initial
        	#value = math.ceil(value)

        	#if value < chal.minimum:
            	#	value = chal.minimum

        	#chal.value = value

        	provided_key = request.form['key'].strip()
        	solve = Solves(teamid=team.id, chalid=chal.id, ip=utils.get_ip(req=request), flag=provided_key)
        	db.session.add(solve)

        	db.session.commit()
        	db.session.close()

    	@staticmethod
    	def fail(team, chal, request):
        	"""
        	This method is used to insert WrongKeys into the database in order to mark an answer incorrect.

        	:param team: The Team object from the database
        	:param chal: The Challenge object from the database
        	:param request: The request the user submitted
        	:return:
        	"""
        	provided_key = request.form['key'].strip()
        	wrong = WrongKeys(teamid=team.id, chalid=chal.id, ip=utils.get_ip(request), flag=provided_key)
        	db.session.add(wrong)
        	db.session.commit()
        	db.session.close()


	@staticmethod
	def update(challenge, request):
		"""
        	This method is used to update the information associated with a challenge. This should be kept strictly to the
       		 Challenges table and any child tables.
        	:param challenge:
        	:param request:
        	:return:
        	"""
		challenge = SmartCityChallenge.query.filter_by(id=challenge.id).first()
		   
		challenge.name = request.form['name']
		challenge.description = request.form['description']
		challenge.value = int(request.form.get('value', 0)) if request.form.get('value', 0) else 0
        	challenge.max_attempts = int(request.form.get('max_attempts', 0)) if request.form.get('max_attempts', 0) else 0
        	challenge.category = request.form['category']
		challenge.hidden = 'hidden' in request.form

		challenge.buildingId = request.form['buildingId']

		db.session.commit()
		db.session.close()

	@staticmethod
	def getBuildingId(chal):
		chal = SmartCityChallenge.query.filter_by(id=chal.id).first()
		return str(chal.buildingId)	


@auth.route('register', methods=['POST', 'GET'])
@ratelimit(method="POST", limit=10, interval=5)
def register_smart():
    logger = logging.getLogger('regs')
    if not utils.can_register():
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        errors = []
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
	color = request.form['color']
	#school = request.form['school']
	image = request.form['image']
	
	print("Color is " + color) 

        name_len = len(name) == 0
        names = Teams.query.add_columns('name', 'id').filter_by(name=name).first()
        emails = Teams.query.add_columns('email', 'id').filter_by(email=email).first()
        smart_colors = SmartCityTeam.query.add_columns('color').filter_by(color=color).first()
	smart_image = SmartCityTeam.query.add_columns('image').filter_by(image=image).first()
	#challenge = SmartCityChallenge.query.filter_by(id=challenge.id).first()
	pass_short = len(password) == 0
        pass_long = len(password) > 128
        valid_email = utils.check_email_format(request.form['email'])
        team_name_email_check = utils.check_email_format(name)


        if not valid_email:
            errors.append("Please enter a valid email address")
        if names:
            errors.append('That team name is already taken')
        if team_name_email_check is True:
            errors.append('Your team name cannot be an email address')
        if emails:
            errors.append('That email has already been used')
        if pass_short:
            errors.append('Pick a longer password')
        if pass_long:
            errors.append('Pick a shorter password')
        if name_len:
            errors.append('Pick a longer team name')
	if smart_colors:
            errors.append('The following colors are available:  \n' + getAvailableColors())
	if smart_image:
            errors.append('That image is already taken')

        if len(errors) > 0:
            return render_template('register.html', errors=errors, name=request.form['name'], email=request.form['email'], password=request.form['password'])
        else:
            with app.app_context():
                team = Teams(name, email.lower(), password)
                db.session.add(team)
                db.session.commit()
                db.session.flush()
	
		
	
		smart_team = SmartCityTeam(team.id ,team.name, color, image)
		db.session.add(smart_team)
		db.session.commit()
		db.session.flush()

                session['username'] = team.name
                session['id'] = team.id
                session['admin'] = team.admin
                session['nonce'] = utils.sha512(os.urandom(10))

                if utils.can_send_mail() and utils.get_config('verify_emails'):  # Confirming users is enabled and we can send email.
                    logger = logging.getLogger('regs')
                    logger.warn("[{date}] {ip} - {username} registered (UNCONFIRMED) with {email}".format(
                        date=time.strftime("%m/%d/%Y %X"),
                        ip=utils.get_ip(),
                        username=request.form['name'].encode('utf-8'),
                        email=request.form['email'].encode('utf-8')
                    ))
                    utils.verify_email(team.email)
                    db.session.close()
                    return redirect(url_for('auth.confirm_user'))
                else:  # Don't care about confirming users
                    if utils.can_send_mail():  # We want to notify the user that they have registered.
                        utils.sendmail(request.form['email'], "You've successfully registered for {}".format(utils.get_config('ctf_name')))

        logger.warn("[{date}] {ip} - {username} registered with {email}".format(
            date=time.strftime("%m/%d/%Y %X"),
            ip=utils.get_ip(),
            username=request.form['name'].encode('utf-8'),
            email=request.form['email'].encode('utf-8')
        ))
        db.session.close()
        return redirect(url_for('challenges.challenges_view'))
    else:
	return render_template('register.html')






@challenges2.route('/chal/<int:chalid>', methods=['POST'])
@during_ctf_time_only
@viewable_without_authentication()
def chal_custom(chalid):
    if utils.ctf_paused():
        return jsonify({
            'status': 3,
            'message': '{} is paused'.format(utils.ctf_name())
        })
    if (utils.authed() and utils.is_verified() and (utils.ctf_started() or utils.view_after_ctf())) or utils.is_admin():
        team = Teams.query.filter_by(id=session['id']).first()
        fails = WrongKeys.query.filter_by(teamid=session['id'], chalid=chalid).count()
        logger = logging.getLogger('keys')
        data = (time.strftime("%m/%d/%Y %X"), session['username'].encode('utf-8'), request.form['key'].encode('utf-8'), utils.get_kpm(session['id']))
        print("[{0}] {1} submitted {2} with kpm {3}".format(*data))

        chal = Challenges.query.filter_by(id=chalid).first_or_404()
        if chal.hidden:
            abort(404)
        chal_class = get_chal_class(chal.type)

        # Anti-bruteforce / submitting keys too quickly
        if utils.get_kpm(session['id']) > 10:
            if utils.ctftime():
                chal_class.fail(team=team, chal=chal, request=request)
            logger.warn("[{0}] {1} submitted {2} with kpm {3} [TOO FAST]".format(*data))
            # return '3' # Submitting too fast
            return jsonify({'status': 3, 'message': "You're submitting keys too fast. Slow down."})

        solves = Solves.query.filter_by(teamid=session['id'], chalid=chalid).first()

        # Challange not solved yet
        if not solves:
            provided_key = request.form['key'].strip()
            saved_keys = Keys.query.filter_by(chal=chal.id).all()

            # Hit max attempts
            max_tries = chal.max_attempts
            if max_tries and fails >= max_tries > 0:
                return jsonify({
                    'status': 0,
                    'message': "You have 0 tries remaining"
                })

            status, message = chal_class.attempt(chal, request)
            if status:  # The challenge plugin says the input is right
                if utils.ctftime() or utils.is_admin():
                    chal_class.solve(team=team, chal=chal, request=request)
                logger.info("[{0}] {1} submitted {2} with kpm {3} [CORRECT]".format(*data))
		
		if not utils.is_admin():
			smart_color = SmartCityTeam.query.filter_by(id=session['id']).first().color
			smart_buildingId = SmartCityChallenge.query.filter_by(id=chalid).first().buildingId
			smart_image = SmartCityTeam.query.filter_by(id=session['id']).first().image
			smartSession = SmartTable(smart_buildingId, smart_color, smart_image)
                	createSmartCityTableSession(smartSession)

                return jsonify({'status': 1, 'message': message})
            else:  # The challenge plugin says the input is wrong
                if utils.ctftime() or utils.is_admin():
                    chal_class.fail(team=team, chal=chal, request=request)
                logger.info("[{0}] {1} submitted {2} with kpm {3} [WRONG]".format(*data))
                # return '0' # key was wrong
                if max_tries:
                    attempts_left = max_tries - fails - 1  # Off by one since fails has changed since it was gotten
                    tries_str = 'tries'
                    if attempts_left == 1:
                        tries_str = 'try'
                    if message[-1] not in '!().;?[]\{\}':  # Add a punctuation mark if there isn't one
                        message = message + '.'
                    return jsonify({'status': 0, 'message': '{} You have {} {} remaining.'.format(message, attempts_left, tries_str)})
                else:
                    return jsonify({'status': 0, 'message': message})

        # Challenge already solved
        else:
            logger.info("{0} submitted {1} with kpm {2} [ALREADY SOLVED]".format(*data))
            # return '2' # challenge was already solved
            return jsonify({'status': 2, 'message': 'You already solved this'})
    else:
        return jsonify({
            'status': -1,
            'message': "You must be logged in to solve a challenge"
        })


def getAvailableColors():
	teamColorList = ['GRREN','BLUE', 'YELLOW','RED','AQUA', 'PURPLE', 'GOLD','TURQUOIS', 'PINK', 'LIMEGREEN']
	smart_result = SmartCityTeam.query.with_entities(SmartCityTeam.color).all()
	colorsPickedList = []
	for colorElement in smart_result:
		colorsPickedList.append(colorElement.color)        
	print(str(colorsPickedList))
	availColorList = set(teamColorList) - set(colorsPickedList)
	
	return str(list(availColorList))

@staticmethod
def getTeamColor(teamId):
	smart_team = SmartCityTeam.query.filter_by(id=teamId).first()
	return smart_team.color


@admin_teams.route('/admin/team/new', methods=['POST'])
@admins_only
def admin_create_team_custom():
    name = request.form.get('name', None)
    password = request.form.get('password', None)
    email = request.form.get('email', None)
    color = request.form.get('color', None)
    school = request.form.get('school', None)
    image = request.form.get('image', None)

    admin_user = True if request.form.get('admin', None) == 'on' else False
    verified = True if request.form.get('verified', None) == 'on' else False
    hidden = True if request.form.get('hidden', None) == 'on' else False
    
    smart_color = SmartCityTeam.query.add_columns('color').filter_by(color=color).first()
    smart_image = SmartCityTeam.query.add_columns('image').filter_by(image=image).first() 

    errors = []

    if not name:
        errors.append('The team requires a name')
    elif Teams.query.filter(Teams.name == name).first():
        errors.append('That name is taken')

    if utils.check_email_format(name) is True:
        errors.append('Team name cannot be an email address')

    if not email:
        errors.append('The team requires an email')
    elif Teams.query.filter(Teams.email == email).first():
        errors.append('That email is taken')

    if email:
        valid_email = utils.check_email_format(email)
        if not valid_email:
            errors.append("That email address is invalid")

    if not password:
        errors.append('The team requires a password')

    if smart_color:
	errors.append('Color was already taken. Colors not available: ' +  getAvailableColors())
    if smart_image:
	errors.append('Imagge already taken') 
    if errors:
        db.session.close()
        return jsonify({'data': errors})

    team = Teams(name, email, password)
    team.website = website
    team.affiliation = affiliation
    team.country = country

    team.admin = admin_user
    team.verified = verified
    team.hidden = hidden

    db.session.add(team)
    db.session.commit()
    db.session.close()
    return jsonify({'data': ['success']})


@admin_teams.route('/admin/team/<int:teamid>/delete', methods=['POST'])
@admins_only
def delete_team_custom(teamid):
    try:
        Unlocks.query.filter_by(teamid=teamid).delete()
        Awards.query.filter_by(teamid=teamid).delete()
        WrongKeys.query.filter_by(teamid=teamid).delete()
        Solves.query.filter_by(teamid=teamid).delete()
        Tracking.query.filter_by(team=teamid).delete()
        Teams.query.filter_by(id=teamid).delete()
	SmartCityTeam.query.filter_by(teamId=teamid).delete()
        db.session.commit()
        db.session.close()
    except DatabaseError:
        return '0'
    else:
	return '1'

def load(app):
    """load overrides for smart_city to work properly"""
    logger.setLevel(app.logger.getEffectiveLevel())
    app.db.create_all()
    register_plugin_assets_directory(app, base_path='/plugins/CTFd_SmartCity/assets')
    challenges.CHALLENGE_CLASSES['smart_city'] = SmartCity  


    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'new-register.html')
    override_template('register.html', open(template_path).read())
    template_path = os.path.join(dir_path, 'new-team.html') 
    override_template('admin/teams.html', open(template_path).read())
    app.view_functions['auth.register'] = register_smart 
    app.view_functions['challenges.chal'] = chal_custom
    app.view_functions['admin_teams.delete_team'] = delete_team_custom
    app.view_functions['admin_teams.create_team'] = admin_create_team_custom 
