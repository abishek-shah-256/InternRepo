
class CSV_Saver:

    def __init__(self, **kwargs):

        self.fields = list(kwargs.keys())
        self.filename = self.__class__.__name__

        try:
            file = open(f'{self.filename}.csv', "r")
            file.close()

        except IOError:
            with open(f'{self.filename}.csv', 'a+') as file:
                data = ','.join(self.fields)
                file.write(data + "\n")
                file.close()
            print("File does not exist. creating new file")

    def write(self, data):
        list_data = []
        for k in self.fields:
            for j in data:
                list_data.append(j[k])

        same_dataype = [i if isinstance(i, str) else str(i) for i in list_data]
        # print(same_dataype)

        try:
            file = open(f'{self.filename}.csv', 'r')
            lines = file.readlines()
            file.close()

            if len(lines) <= 1:
                print("Writing the data to the csv....")
                with open(f'{self.filename}.csv', 'a+') as file:
                    dat = ','.join(same_dataype)
                    file.write(dat + "\n")
                    file.close()

            elif len(lines) >= 2:

                # ------------Now restrict the use of same id to append or write the data
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

                # iterating through the list of dictionaries to check for the 'id' and comparing it with the writing
                # so that no duplication of id occurs

                duplicate_flag = False
                for item in data_list:
                    if item['id'] == same_dataype[0]:
                        duplicate_flag = True
                        print("Same id detected!..Use different id")
                        break

                    elif item['id'] != same_dataype[0]:
                        duplicate_flag = False

                if duplicate_flag == False:
                    print("Writing the data to the csv....")
                    with open(f'{self.filename}.csv', 'a+') as file:
                        dat = ','.join(same_dataype)
                        file.write(dat + "\n")
                        file.close()


            else:
                print("Does not have a record data to retrieve")

        except IOError:
            print("File does not exist")

    def read(self):
        print("Reading the data from the csv....:-)")
        with open(f'{self.filename}.csv', 'r') as file:
            lines = file.readlines()
            print(f"The data of the '{self.filename}'.csv are: =\n")
            for line in lines:
                row = line.strip().split(",")
                print(row)
            file.close()

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

    def delete(self, id):
        print(f"Deleting the data with id = {id} from the csv....")

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
                final_records = [record for record in data_list if record['id'] != str(id)]

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

    def update(self, id, new_data):
        print(f"Updating the data with id = {id} into the csv....")

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
            if row['id'] == str(id):
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == '__main__':

    p = Product(id="", category="", price="")
    # p.write([{'id': 2, 'category':"electronics", 'price':1500}])
    # p.write([{'id': 4, 'category':"electronics", 'price':7500}])
    # p.write([{'id': 8, 'category': "vehicle", 'price': 7500}])
    # p.read()
    # p.delete(4)

    new_data = {'price':2600}
    p.update(8, new_data)

    data = p.read_retrieve(8)
    print(data)
