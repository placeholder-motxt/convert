# MoTxT - Convert UML Diagrams to Django Code

MoTxT is a developer tool to help generate code in Django Framework from UML Diagrams, which are UML Class Diagram and UML Sequence Diagram.

MoTxT reads UML Diagrams in .jet format that is based on JSON and parses it in a certain transformation rule. Transformation rule helps MoTxT to identify what UML elements will be generated into.

## UML Class Diagram
There are few UML elements that will be transformed from the .jet file:
- *diagram*
    - 'diagram' will define the name of Django Project that will be generated
- *nodes*
    - 'nodes' has value of list of all class object defined in the Class Diagram. Each class object will be parsed into ClassObject. There are few elements in the 'nodes':
        - *methods*
            - 'methods' is used to define all methods that the class has. The value of methods is written in this format:
            ```
            [modifier] [method name ([parameter name]: [data type])]: [data type]
            ```
            - If there are more than one method define, it is separated using \n
            - 'methods' will be transformed into ClassMethodObject by iterating each method by splitting the separator first, which is \n, then get the information of the method name and the return data type.
            - If a method contains parameters, then it will be parsed into ParameterObject to store information about the parameter name and the data type.
        - *name*
            - 'name' is used to define the class name. The variable name of the ClassObject will be set as 'name'.
        - *attributes*
            - 'attributes' is used to define all the attributes that the class has. The value of attributes is written in this format:
            ```
            [modifier] [attribute name]: [data type]
            ```
            - If there are more than one attributes, it is separated using \n
            - 'attributes' will be transformed into FieldObject by iterating each method by splitting the separator first, which is \n, then get the information of the attribute name and data type.
        - *id*
            - 'id' is used to define a ClassObject's id (can be said as Primary Key)
- *edges*
    - 'edges' has value of list of all relationships between classes in order to know which class is associated to. Each relationship will be transformed into either ManyToOneRelationshipObject,  ManyToManyRelationshipObject, or OneToOneRelationShipObject, which depends on the relationship. There are few elements in the 'edges':
        - *startLabel*
            -  'startLabel' will be parsed to get information about the cardinality of the source ClassObject
        - *endLabel*
            - 'endLabel' will be parsed to get the information about the cardinality of the targetClassObject
        - *start*
            - 'start' will be parsed to get the information about the source ClassObject's id
        - *end*
            - 'end' will be parsed to get the information about the target ClassObject's id
        ```
        Note that by knowing the cardinality, we can defined its relationship, whether it is ManyToMany, ManyToOne, or OneToOne! Also, we can know which class will be the foreign key of a class too!
        ```