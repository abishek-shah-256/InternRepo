"""
CRUD operation with CSV file
=====================================
To use this module, Follow the steps:
1. Inherit the 'CSV_Saver' parent class.
    and put the snippets inside that class:
        def __init__(self, **kwargs):
        super().__init__(**kwargs)

2. Create an instance of the base class and pass the parameter with null values to
    create the Column Name and create the CSV file

3. Call the write() method to write data on the CSV file. Use pass the data in the parameter of the write() method

4. Call the read() method to read the data from the CSV file.

5. Call the delete() method and pass the interger id as parameter that you want to delete like:
    delete(3)

6. Call the update() method and pass the id and new data as parameter that you want to update like:
    update(2,new_data)
    The data should be passed in the form of dictionary with key and values pairs.
"""


class CSV_Saver:

    def __init__(self):

        # self.fields = list(kwargs.keys())
        self.filename = self.__class__.__name__
        keys = list(self.__dict__.keys())[:-1]
        self.values = list(self.__dict__.values())[:-1]

        # print(self.values)

        try:
            file = open(f'{self.filename}.csv', "r")
            file.close()

        except IOError:
            with open(f'{self.filename}.csv', 'a+') as file:
                data = ','.join(keys)
                file.write(data + "\n")
                file.close()
            print("File does not exist. creating new file")

    def write(self):

        # list_data = []
        # print("Writing the data to the csv....")
        # for k in self.fields:
        #     for j in data:
        #         list_data.append(j[k])
        #
        # same_dataype = [i if isinstance(i, str) else str(i) for i in list_data]

        try:
            file = open(f'{self.filename}.csv', 'r')
            lines = file.readlines()
            file.close()

            if len(lines) <= 1:
                with open(f'{self.filename}.csv', 'a+') as file:
                    dat = ','.join(self.values)
                    file.write(dat + "\n")
                    file.close()

            elif len(lines) >= 2:

            #------------Now restrict the use of same id to append or write the data
            # ------------retrieving the data in the form of list of dictionary from the csv file
                with open(f'{self.filename}.csv', 'r') as file:
                    lines = file.readlines()
                column_names = lines[0].strip().split(",")


                data_list = []
                for line in lines[1:]:
                    values = line.strip().split(",")

                    data_dict = {}
                    for i in range(len(column_names)):
                        data_dict[column_names[i]] = values[i]
                    data_list.append(data_dict)

                #iterating through the list of dictionaries to check for the 'id' and comparing it with the writing
                # so that no duplication of id occurs

                duplicate_flag = False
                for item in data_list:
                    if item['id'] == self.values[0]:
                        duplicate_flag = True
                        raise Exception("Same id detected!..Use different id")
                        # break

                    elif item['id'] != self.values[0]:
                        duplicate_flag = False

                if duplicate_flag == False:
                    with open(f'{self.filename}.csv', 'a+') as file:
                        dat = ','.join(self.values)
                        file.write(dat + "\n")
                        file.close()


            else:
                 raise Exception("Does not have a record data to retrieve")

        except IOError:
            print("File does not exist")

    @classmethod
    def read(cls):
        filename = cls.__name__
        print("Reading the data from the csv....:-)")
        # with open(f'{filename}.csv', 'r') as file:
        #     lines = file.readlines()
        #     print(f"The data of the '{self.filename}'.csv are: =\n")

        # ------------retrieving the data in the form of list of dictionary from the csv file
        with open(f'{filename}.csv', 'r') as file:
            lines = file.readlines()

            column_names = lines[0].strip().split(",")
            data_list = []
            for line in lines[1:]:
                values = line.strip().split(",")
                # print(column_names)
                # print(data_list)

                data_dict = {}
                for i in range(len(column_names)):
                    data_dict[column_names[i]] = values[i]
                data_list.append(cls(**data_dict))

            file.close()

        return data_list


    def read_retrieve(self, id):
        print("Reading the data from the csv....:-)")

        # ------------retrieving the data in the form of list of dictionary from the csv file
        with open(f'{self.filename}.csv', 'r') as file:
            lines = file.readlines()

        column_names = lines[0].strip().split(",")
        data_list = []
        for line in lines[1:]:
            values = line.strip().split(",")

            data_dict = {}
            for i in range(len(column_names)):
                data_dict[column_names[i]] = values[i]
            data_list.append(data_dict)

        # print(data_list)
        # ------------->>>Retrieving the data from the records
        final_records = [record for record in data_list if record['id'] == str(id)]

        return  final_records

    def delete(self):
        print(f"Deleting the data with id = {self.id}from the csv....")

        try:
            file = open(f'{self.filename}.csv', 'r')
            lines = file.readlines()
            file.close()
            if len(lines) >= 2:
                # second_line = lines[1]
                # print(second_line)

                #------------retrieving the data in the form of list of dictionary from the csv file
                with open(f'{self.filename}.csv', 'r') as file:
                    lines = file.readlines()

                column_names = lines[0].strip().split(",")
                data_list = []
                for line in lines[1:]:
                    values = line.strip().split(",")

                    data_dict = {}
                    for i in range(len(column_names)):
                        data_dict[column_names[i]] = values[i]
                    data_list.append(data_dict)

                # print(data_list)
                #------------->>>deleting the data from the records
                final_records = [record for record in data_list if record['id'] != str(self.id)]

                # print(final_records)

                #--------writing the new data into csv file i.e. ignoring the deleted data
                data_lines = []
                for data_dict in final_records:
                    values = [str(data_dict.get(key, "")) for key in column_names]
                    line = ",".join(values)
                    data_lines.append(line)

                with open(f'{self.filename}.csv', "w") as file:
                    header_line = ','.join(column_names)
                    file.write(header_line + "\n")
                    file.writelines("\n".join(data_lines) + "\n")

            else:
                print("Does not have a record data to delete")

        except IOError:
            print("File does not exist")

    def update(self, new_data):
        print(f"Updating the data with id = {self.id} into the csv....")

        # ------retrieving the data
        with open(f'{self.filename}.csv', 'r') as file:
            lines = file.readlines()

        column_names = lines[0].strip().split(",")
        #-------packaging the data into list of dictionaries
        data_list = []
        for line in lines[1:]:
            values = line.strip().split(",")

            data_dict = {}
            for i in range(len(column_names)):
                data_dict[column_names[i]] = values[i]
            data_list.append(data_dict)
        # print(data_list)

        #--------updating the data in the list of dictionaries
        for row in data_list:
            # print(type(id))
            if row['id'] == str(self.id):
                row.update(new_data)

        # print(data_list)

        #-------writing the updated list of dictionary in the new file
        data_lines = []
        for data_dict in data_list:
            values = [str(data_dict.get(key, "")) for key in column_names]
            line = ",".join(values)
            data_lines.append(line)

        with open(f'{self.filename}.csv', "w") as file:
            header_line = ','.join(column_names)
            file.write(header_line + "\n")
            file.writelines("\n".join(data_lines))

class User(CSV_Saver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Product(CSV_Saver):
    def __init__(self, id, category, price):
        self.id = id
        self.category = category
        self.price = price

        super().__init__()


if __name__ == '__main__':

    p1 = Product(id="1", category="electronic", price="500")
    # p.write()
    p2 = Product(id="2", category="electronic", price="500")
    # p2.write()
    p3 = Product(id="3", category="electronic", price="500")
    # p3.write()
    p4 = Product(id="2", category="electronic", price="500")



    data = Product.read()

    for u in data:
        print(u.id)

    # p.delete()
    # p2.delete()

    # new_data = {'price': 2600}
    # p.update(new_data)

    # data = p.read_retrieve(2)
    # print(data)
