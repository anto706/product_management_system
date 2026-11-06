
from mysql import connector


class DbConnect:

    def get_connection(self):
        try:
            self.connection = connector.connect(
                host="localhost",
                user="root",
                password="root123#",
                database="product_db"
            )

            return self.connection

        except Exception as e:
            print(e)
            return None


class ProductManager(DbConnect):

    def get_object(self, id=None):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = "SELECT * FROM product WHERE id=%s"
            values = (id,)

            self.cursor.execute(query, values)

            records = self.cursor.fetchone()

            return records

        except Exception as e:
            print(e)

    def get(self):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = "SELECT * FROM product"
            self.cursor.execute(query)

            records = self.cursor.fetchall()
            return records

        except Exception as e:
            print(e)
            return []

    def post(self, **kwargs):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = """
            INSERT INTO product
            (name, category, price, quantity)
            VALUES (%s, %s, %s, %s)
            """

            values = [
                kwargs.get(k)
                for k in ["name", "category", "price", "quantity"]
            ]

            self.cursor.execute(query, values)

            self.connect.commit()

            print("New product added successfully")

        except Exception as e:
            print(e)


    def retrieve(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is None:
                print("Product not found")
            else:
                print(record)

        except Exception as e:
            print(e)


    def delete(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is not None:

                query = "DELETE FROM product WHERE id=%s"
                values = (id,)

                self.cursor.execute(query, values)

                self.connect.commit()

                print("Product deleted successfully")

            else:
                print("Product not found")

        except Exception as e:
            print(e)


    def put(self, id=None, **kwargs):
        try:
            record = self.get_object(id=id)

            if record is not None:

                allowed_fields = [
                    "name", "category", "price", "quantity"
                ]

                if not kwargs or not all(k in allowed_fields for k in kwargs):
                    print("Invalid or empty update fields")
                    return

                placeholder = ""

                for k in kwargs.keys():
                    placeholder += k + "=%s,"

                placeholder = placeholder.rstrip(",")

                query = f"UPDATE product SET {placeholder} WHERE id=%s"

                values = list(kwargs.values())
                values.append(id)

                self.cursor.execute(query, values)

                self.connect.commit()

                print("Product updated successfully")

            else:
                print("Product not found")

        except Exception as e:
            print(e)


# Object creation
product_instance = ProductManager()

# POST
product_instance.post(
    name="Laptop",
    category="Electronics",
    price=55000,
    quantity=10
)

# GET
product_instance.get()

# RETRIEVE
# product_instance.retrieve(1)

# PUT
# product_instance.put(1, price=60000, quantity=15)

# DELETE
# product_instance.delete(1)
