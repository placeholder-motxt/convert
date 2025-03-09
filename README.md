# MoTxT - Convert UML Diagrams to Django Code

MoTxT is a developer tool to help generate code in Django Framework from UML Diagrams, which are UML Class Diagram and UML Sequence Diagram.

MoTxT reads UML Diagrams in .jet format that is based on JSON and parses it in a certain transformation rule. Transformation rule helps MoTxT to identify what UML elements will be generated into.

## UML Class Diagram
There are few UML elements that will be transformed from the .jet file:
- *diagram*
    - 'diagram' will define the type of UML Diagram given
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

## UML Sequence Diagram
There are few UML elements that will be transformed from the .jet file:
- *diagrams*
    - 'diagrams' will define the type of the UML diagram given, the value has to be "SequenceDiagram"
- *nodes*'
    - There are two types of node defined by .jet for Sequence Diagram, which are (Note that all node have 'id' as the identifier!):
        - ImplicitParameterNode
            - ImplicitParameterNode contains information of the class name and also the children it has. 
            - For the classname first, there is specifically one class that will always be in EVERY Sequence Diagram, which is :views that acts as the Controller Method and will be transformed into ControllerMethodObject. For the rest of the class, it will be transformed into ClassObject later on.
            - ImplicitParameterNode also has children, which will later be discussed further more in the 'edges' section since it will hardly rely into each other.
        - CallNode
            - CallNode just tells that there is a function call, but again, it will be discussed in the 'edges' section.
            - In the ImplicitParameterNode, you have already noticed that there are 'children' key, the 'children' are list of CallNode id!
- *edges*
    - 'edges' is used to describe the CallNode. 'edges' value is Array that consists of edges with the property:
        - middleLabel -> describes the method name
        - start -> describe the request class source
        - end -> describe the request class target
        - type -> there are ConstructorEdge (used to create an instance of a class), CallEdge (used for a method call), and ReturnEdge (used to return a value)
    - What special about the information of 'start' and 'end' is that you can RECOGNIZE if a method is called in a method! For example:
    ```
    {
      "middleLabel": "[not hasTanggunganResult] prosesPeminjamanTidakMemilikiTanggungan()",
      "start": 9,
      "end": 10,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "«create»",
      "start": 10,
      "end": 18,
      "type": "ConstructorEdge",
      "signal": false
    },
    {
      "middleLabel": "borrow(isbn)",
      "start": 10,
      "end": 20,
      "type": "CallEdge",
      "signal": false
    },
    ```  
    The method strcture would be like:
    ```
    prosesPeminjamanTidakMemilikiTanggungan():
        create()
        borrow(isbn)
    ```
    - The method that is called inside a method will be transformed into MethodCallObject.
        - If the main method is from views, then it will be ControllerMethodCallObject
        - If the main method is from class, then it will be ClassMethodCallObject

Here is an example of a complete .jet structure for a SequenceDiagram:
```
{
  "diagram": "SequenceDiagram",
  "nodes": [
    {
      "children": [
        1
      ],
      "name": "buku:Buku",
      "x": 510,
      "y": 123,
      "id": 0,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 1,
      "type": "CallNode"
    },
    {
      "children": [
        3
      ],
      "name": "listBuku:ListBuku",
      "x": 370,
      "y": 91,
      "id": 2,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 3,
      "type": "CallNode"
    },
    {
      "children": [
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14
      ],
      "name": ":views",
      "x": 250,
      "y": 52,
      "id": 4,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 5,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 6,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 7,
      "type": "CallNode"
    },
    {
      "x": 890,
      "y": 10,
      "openBottom": false,
      "id": 8,
      "type": "CallNode"
    },
    {
      "x": 335,
      "y": 56,
      "openBottom": false,
      "id": 9,
      "type": "CallNode"
    },
    {
      "x": 29,
      "y": 29,
      "openBottom": false,
      "id": 10,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 11,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 12,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 13,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 14,
      "type": "CallNode"
    },
    {
      "children": [
        16
      ],
      "name": "copyBuku:CopyBuku",
      "x": 1420,
      "y": -8,
      "id": 15,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 16,
      "type": "CallNode"
    },
    {
      "children": [
        18
      ],
      "name": "peminjaman:Peminjaman",
      "x": 840,
      "y": 28,
      "id": 17,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 18,
      "type": "CallNode"
    },
    {
      "children": [
        20,
        21
      ],
      "name": "listCopy:ListCopy",
      "x": 1090,
      "y": 126,
      "id": 19,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 20,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 21,
      "type": "CallNode"
    },
    {
      "children": [
        23
      ],
      "name": "peminjam:Peminjam",
      "x": 800,
      "y": 73,
      "id": 22,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 23,
      "type": "CallNode"
    },
    {
      "children": [
        25
      ],
      "name": ":UI",
      "x": 10,
      "y": 65,
      "id": 24,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 26,
      "y": 18,
      "openBottom": false,
      "id": 25,
      "type": "CallNode"
    },
    {
      "children": [
        27,
        28
      ],
      "name": "listPeminjam:ListPeminjam",
      "x": 620,
      "y": 123,
      "id": 26,
      "type": "ImplicitParameterNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 27,
      "type": "CallNode"
    },
    {
      "x": 0,
      "y": 0,
      "openBottom": false,
      "id": 28,
      "type": "CallNode"
    }
  ],
  "edges": [
    {
      "middleLabel": "[POST] login(username, password)",
      "start": 25,
      "end": 14,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "HalamanPemrosesanPeminjaman()",
      "start": 25,
      "end": 5,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "LihatDetailBuku(isbn)",
      "start": 25,
      "end": 6,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "getBuku(isbn)",
      "start": 6,
      "end": 3,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "FormProsesPeminjaman(isbn)",
      "start": 25,
      "end": 7,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[POST] SubmitProsesPeminjaman(isbn)",
      "start": 25,
      "end": 8,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isValid(dataAnggota)",
      "start": 8,
      "end": 27,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[isValid] prosesPeminjamanValidKeanggotaan()",
      "start": 8,
      "end": 9,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan(peminjam)",
      "start": 9,
      "end": 28,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan()",
      "start": 28,
      "end": 23,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not hasTanggunganResult] prosesPeminjamanTidakMemilikiTanggungan()",
      "start": 9,
      "end": 10,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "«create»",
      "start": 10,
      "end": 18,
      "type": "ConstructorEdge",
      "signal": false
    },
    {
      "middleLabel": "borrow(isbn)",
      "start": 10,
      "end": 20,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "findCopyBuku(isbn) -> copyBuku",
      "start": 20,
      "end": 21,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isBorrowed()",
      "start": 20,
      "end": 16,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "showNotifikasiBerhasilPinjam()",
      "start": 10,
      "end": 11,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[hasTanggungan] showNotifikasiGagalPinjam()",
      "start": 9,
      "end": 12,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not isValid] showNotifikasiDataTidakValid()",
      "start": 8,
      "end": 13,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "buku",
      "start": 3,
      "end": 6,
      "type": "ReturnEdge"
    },
    {
      "middleLabel": "getDetailBuku()",
      "start": 6,
      "end": 1,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "detailBuku",
      "start": 1,
      "end": 6,
      "type": "ReturnEdge"
    },
    {
      "middleLabel": "isValid",
      "start": 27,
      "end": 8,
      "type": "ReturnEdge"
    },
    {
      "middleLabel": "hasTanggunganResult",
      "start": 23,
      "end": 28,
      "type": "ReturnEdge"
    },
    {
      "middleLabel": "hasTanggunganResult",
      "start": 28,
      "end": 9,
      "type": "ReturnEdge"
    }
  ],
  "version": "3.8"
}
```
