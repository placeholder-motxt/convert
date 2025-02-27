import json
from app.element_objects import *

class ParseJsonToObject:
    def __init__(self,data):
        self.__json = data
    
    def parse_methods(self):
        pass

    def parse_relationships(self, classes, uml_json):
        edges = uml_json['edges']
        for edge in edges :
            class_from_id = classes[edge['start']]
            class_to_id = classes[edge['end']]

            if 'type' in edge.keys() and edge['type'] =='GeneralizationEdge':
                class_from_id.set_parent(class_to_id)
                continue

            self.__validate_amount(edge['startLabel'])
            self.__validate_amount(edge['endLabel'])

            ro = None
            if (('*' in edge['startLabel'] or '.' in edge['startLabel'] or self.__is_number_greater_than(edge['startLabel']))\
                and ('*' in edge['endLabel'] or '.' in edge['endLabel'] or self.__is_number_greater_than(edge['endLabel']))):
                
                ro = ManyToManyRelationshipObject()
                print(edge['startLabel'], "many to many", edge['endLabel'])

            elif (('*' in edge['startLabel'] or '.' in edge['startLabel'] or self.__is_number_greater_than(edge['startLabel']))\
                or ('*' in edge['endLabel'] or '.' in edge['endLabel'] or self.__is_number_greater_than(edge['endLabel']))):
                
                ro = ManyToOneRelationshipObject()
                print(edge['startLabel'], "many to one", edge['endLabel'])
                
                if '*' in edge['startLabel'] or '.' in edge['startLabel'] or self.__is_number_greater_than(edge['startLabel']) :
                    ro.setSourceClassOwnAmount(edge['startLabel'])
                    ro.setTargetClassOwnAmount(edge['endLabel'])

                    class_from_id.add_relationship(ro)
                else:
                    ro.setSourceClassOwnAmount(edge['endLabel'])
                    ro.setTargetClassOwnAmount(edge['startLabel'])

                    class_to_id.add_relationship(ro)
                continue
            else:
                print(edge['startLabel'], "one to one", edge['endLabel'])
                ro = OneToOneRelationshipObject()

            ro.setSourceClass(class_from_id)
            ro.setTargetClass(class_to_id)

            ro.setSourceClassOwnAmount(edge['startLabel'])
            ro.setTargetClassOwnAmount(edge['endLabel'])
            class_from_id.add_relationship(ro)
        return classes

    def __validate_amount(self, amount_str):
        if not amount_str:
            raise Exception("Association multiplicity cannot be empty")

        # Kalo bentuknya bukan * atau N..*
        if '*' in amount_str and '*'!=amount_str[len(amount_str)-1]:
            raise Exception("Invalid use of * in multiplicity")
        
        # Amount hanya angka
        if amount_str.isnumeric() or amount_str=='*':
            return "amount_str"
        else:
            # validate minimum and maximum amount
            end_minimum = False
            start_max = False
            has_min_number = False
            minimum_amount = 0
            maximum_amount = 0
            titik_count = 0
            for i, ch in enumerate(amount_str):
                if ch.isdigit() and not end_minimum:
                    has_min_number = True
                    minimum_amount*=10
                    minimum_amount+=int(ch)
                elif has_min_number and ch=='.':
                    end_minimum = True
                    titik_count+=1
                elif end_minimum and ch.isdigit():
                    start_max = True
                    maximum_amount+=int(ch)
                elif end_minimum and ch=='*' and i==len(amount_str)-1:
                    start_max = True
                elif start_max and ch.isdigit():
                    maximum_amount*=10 
                    maximum_amount+=int(ch)
                else:
                    raise Exception("Invalid multiplicity in a relationship")
            if (end_minimum and not start_max) or titik_count!=2:
                raise Exception("Invalid multiplicity in a relationship")
            
            return amount_str
        
    def __is_number_greater_than(self, amount_str, compared_to=1):
        if amount_str.isnumeric():
            return int(amount_str) > compared_to
        return False
