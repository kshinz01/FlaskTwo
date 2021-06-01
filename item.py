from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3

items = [
    {'name': 'chair', 'price': 12.00}
]


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"item": {
                'name': row[0],
                'price':row[1],
            }}

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items values (?, ?)"
        cursor.execute(query,(item['name'],item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))

        connection.commit()
        connection.close()


    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item,201
        return {"message": "There is no item by that name."},500

    # @jwt_required()
    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {'message':"An error occured inserting."},500

        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message':"An error occured inserting."},500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message':"An error occured updating."},500
        return updated_item

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': "Item deleted"}, 200


class ItemList(Resource):
    def get(self):
#        return {'items': items}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()
        return {'items': rows}
