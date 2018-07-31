from flask import render_template
from CTFd.utils import admins_only, is_admin
from CTFd.models import db, Challenges, Keys, Awards, Solves, Files, Tags, Teams
from CTFd import utils
from logging import getLogger, basicConfig,DEBUG,ERROR
from CTFd.plugins import challenges, register_plugin_assets_directory
from CTFd import utils, CTFdFlask
from flask import session




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
			'modal'  : '/plugins/CTFd_SmartCity/assets/smartcity-challenge-model.njk',
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

		files = request.files.getlist('files[]')
		for f in files:
			utils.upload_file(file=f, chalid=chal.id)


		logger.debug("Genereted buildingId " + chal.buildingId + " for challenge " + chal.name)
		
		db.session.add(chal)
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
