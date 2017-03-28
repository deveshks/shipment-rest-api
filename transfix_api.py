from flask import Flask, jsonify,request
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields,ValidationError
import os

app = Flask(__name__)
api = Api(app,catch_all_404s=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


'''Shipment Object
 @param shipment_name : Name of the shipment
 @param total_price : Total price of the shipment
 @param segment_distances : List of segment distances for the shipment
 @param cost_breakdown : Cost per segment
 '''
class Shipment(object):
    def __init__(self, shipment_name, total_price,segment_distances,cost_breakdown):
        self.shipment_name = shipment_name
        self.total_price = total_price
        self.segment_distances = segment_distances
        self.cost_breakdown = cost_breakdown

'''Shipment Object Database Model'''
class ShipmentModel(db.Model):
    shipment_name = db.Column(db.String, primary_key=True)
    total_price = db.Column(db.Float)
    segment_distances = db.Column(db.PickleType)
    cost_breakdown = db.Column(db.PickleType)

    def __init__(self, shipment_name, total_price,segment_distances,cost_breakdown):
        self.shipment_name = shipment_name
        self.total_price = total_price
        self.segment_distances = segment_distances
        self.cost_breakdown = cost_breakdown

'''Shipment Object Schema'''
class ShipmentSchema(Schema):

    #Validation for total price and distances
    def validate_total_price(n):
        val = float(n)
        if(val<=0):
            raise ValidationError("Total price must be greater than 0")    

    def validate_distance(n):
        val = float(n)
        if(val<=0):
            raise ValidationError("Distances must be a greater than 0")

  
    shipment_name = fields.Str(required=True)
    total_price = fields.Float(required=True,validate=validate_total_price)
    segment_distances = fields.List(fields.Float(validate=validate_distance, error_messages={'invalid': 'Distances must be a float'}),required=True)
    cost_breakdown = fields.List(fields.Float())

class ShipmentAPI(Resource):

    '''GET /shipment/<shipment_name>: Returns the Shipment Object given a shipment name'''
    def get(self,shipment_name):
        try:
            shipment_data = ShipmentModel.query.filter_by(shipment_name=shipment_name).first()
            if not shipment_data:
                return returnJSON("GET","Error",shipment_name)
            schema = ShipmentSchema()
            shipment = schema.dump(shipment_data)
            data = shipment.data
            return data
        except Exception as e:
            print e

    '''POST /shipment: Creates a new Shipment Object given shipment details'''
    def post(self):
        try:
            shipment_data = request.get_json(force=True)
            schema = ShipmentSchema()
            result,errors = schema.load(shipment_data)
            if errors:
                return errors
            shipment_name = result['shipment_name']
            segment_distances = result['segment_distances']
            total_price = result['total_price']
            shipment_data = ShipmentModel.query.filter_by(shipment_name=shipment_name).first()
            if shipment_data:
                return returnJSON("POST","Error",shipment_name)
            cost_breakdown = splitcost(total_price,segment_distances)
            shipment = ShipmentModel(result['shipment_name'],result['total_price'],result['segment_distances'],cost_breakdown)
            db.session.add(shipment)
            db.session.commit() 
            return returnJSON("POST","Success",shipment_name)
        except Exception as e:
            print e 

    '''PUT /shipment: Updates an existing Shipment Object given shipment details'''
    def put(self):
        try:
            shipment_data = request.get_json(force=True)
            schema = ShipmentSchema()
            result,errors = schema.load(shipment_data)
            if errors:
                return errors
            shipment_name = result['shipment_name']
            segment_distances = result['segment_distances']
            total_price = result['total_price']
            shipment_data = ShipmentModel.query.filter_by(shipment_name=shipment_name).first()
            if not shipment_data:
                return returnJSON("PUT","Error",shipment_name)
            cost_breakdown = splitcost(total_price,segment_distances)
            shipment_data.total_price = total_price
            shipment_data.segment_distances = segment_distances
            shipment_data.cost_breakdown = cost_breakdown
            db.session.commit() 
            return returnJSON("PUT","Success",shipment_name)
        except Exception as e:
            print e 

    '''DELETE/shipment: Deletes all shipment objects from the database
       DELETE/shipment/<shipment_name>: Deletes the shipment object for the given shipment name 
        '''
    def delete(self,shipment_name=None):
        try:
            if shipment_name is None:
                ShipmentModel.query.delete()
                db.session.commit()
                return returnJSON("DELETE","Success")
            else:
                shipment_data = ShipmentModel.query.filter_by(shipment_name=shipment_name).first()
                if not shipment_data:
                    return returnJSON("DELETE","Error",shipment_name)
                db.session.delete(shipment_data)
                db.session.commit() 
                return returnJSON("DELETE","Success",shipment_name)
        except Exception as e:
            print e

'''Method to split cost among segment distances
@param cost : Total cost of shipment
@param distances: List of segment distances
@return distributed_costs: Lists of costs proportionally distributed by segment distances'''
def splitcost(cost, distances):
    distributed_costs = []
    total_distance = sum(distances)
    for distance in distances:
        distance = float(distance)
        p = distance / total_distance
        distributed_cost = round(p * cost,2)
        distributed_costs.append(distributed_cost)
        total_distance -= distance
        cost -= distributed_cost
    return distributed_costs


'''Method to form appropriate JSON return response
@param reqtype : Type of Request
@param rettype: Type of response Requested
@param shipment_name: Name of shipment
@return response: JSON return response'''
def returnJSON(reqtype,rettype,shipment_name=None):
    response = {}
    successfullyDeletedAllStr = 'All Shipments successfully deleted'
    if shipment_name is not None:
        prefixStr = 'Shipment with name '+shipment_name
        doesNotExistsStr = prefixStr + ' does not exist'
        alreadyExistsStr = prefixStr + ' already exists'
        successfullyCreatedStr = prefixStr + ' successfully created'
        successfullyUpdatedStr = prefixStr + ' successfully updated'
        successfullyDeletedStr = prefixStr + ' successfully deleted'
    if reqtype == "GET":
        if rettype == "Error":
            response[rettype] = doesNotExistsStr
    elif reqtype == "POST":
        if rettype == "Success":
            response[rettype] = successfullyCreatedStr
        elif rettype == "Error":
            response[rettype] = alreadyExistsStr
    elif reqtype == "PUT":
        if rettype == "Success":
            response[rettype] = successfullyUpdatedStr
        elif rettype == "Error":
            response[rettype] = doesNotExistsStr
    elif reqtype == "DELETE":
        if rettype == "Success":
            if shipment_name is None:
                response[rettype] = successfullyDeletedAllStr
            else:
                response[rettype] = successfullyDeletedStr
        elif rettype == "Error":
            response[rettype] = doesNotExistsStr
    return jsonify(response)

#API Endpoints for the Shipping API
api.add_resource(ShipmentAPI, '/shipment',endpoint='postshipment')
api.add_resource(ShipmentAPI, '/shipment',endpoint='putshipment')
api.add_resource(ShipmentAPI, '/shipment/<shipment_name>',endpoint='getshipment')
api.add_resource(ShipmentAPI,'/shipment/<shipment_name>',endpoint='deleteshipment')

if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port ,debug=True)	