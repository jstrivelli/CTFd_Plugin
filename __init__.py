from flask import render_template
from CTFd.utils import admins_only, is_admin
from CTFd.models import db, Challenges, Keys, Awards, Solves, Files, Tags, Teams, WrongKeys
from CTFd import utils
from logging import getLogger, basicConfig,DEBUG,ERROR
from CTFd.plugins import challenges, register_plugin_assets_directory
from CTFd import utils, CTFdFlask
from flask import session
from CTFd.plugins.keys import get_key_class



basicConfig(level=ERROR)
logger = getLogger(__name__)

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

def load(app):
    """load overrides for smart_city to work properly"""
    logger.setLevel(app.logger.getEffectiveLevel())
    app.db.create_all()
    register_plugin_assets_directory(app, base_path='/plugins/CTFd_SmartCity/assets')
    challenges.CHALLENGE_CLASSES['smart_city'] = SmartCity   
     
    

    #challenges.CHALLENGE_CLASSES["smart_city"] = SmartCity
    #def view_challenges():
        #return render_template('page.html', content="<h1>Challenges are currently closed</h1>")

    # The format used by the view_functions dictionary is blueprint.view_function_name
    #app.view_functions['challenges.challenges_view'] = view_challenges
