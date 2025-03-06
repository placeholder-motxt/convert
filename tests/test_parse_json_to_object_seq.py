import unittest

from app.parse_json_to_object_seq import ParseJsonToObjectSeq


class TestParseJsonToObjectSeq(unittest.TestCase):
    def test_set_valid_json(self):
        json_data = """
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
"""
        self.assertEqual("Success", ParseJsonToObjectSeq().set_json(json_data))

    def test_negative_set_invalid_json(self):
        json_data = """
{
  "diagram": "ClassDiagram",
  "nodes": [
    {
      "id": 0,
      "type": "UnknownNode",
      "name": "InvalidNode",
      "x": 100,
      "y": 200
    },
    {
      "id": 1,
      "type": "CallNode",
      "name": "ValidNode"
    }
  ],
  "edges": [
    {
      "start": 1,
      "end": 999,
      "type": "CallEdge",
      "middleLabel": "Invalid Edge",
      "signal": true
    }
  ],
  "version": "3.8"
}
"""
        with self.assertRaises(Exception) as context:
            ParseJsonToObjectSeq().set_json(json_data)

        self.assertEqual(str(context.exception), "Given .jet is not valid!")

    def test_negative_set_empty_json(self):
        with self.assertRaises(Exception) as context:
            ParseJsonToObjectSeq().set_json("")

        self.assertEqual(str(context.exception), "Given .jet is not valid!")

    def test_positive_parse_views(self):
        json_data = """
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
      "middleLabel": "[POST] login (username, password)",
      "start": 25,
      "end": 14,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "HalamanPemrosesanPeminjaman ()",
      "start": 25,
      "end": 5,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "LihatDetailBuku (isbn)",
      "start": 25,
      "end": 6,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "getBuku (isbn)",
      "start": 6,
      "end": 3,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "FormProsesPeminjaman (isbn)",
      "start": 25,
      "end": 7,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[POST] SubmitProsesPeminjaman (isbn)",
      "start": 25,
      "end": 8,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isValid (dataAnggota)",
      "start": 8,
      "end": 27,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[isValid] prosesPeminjamanValidKeanggotaan ()",
      "start": 8,
      "end": 9,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan (peminjam)",
      "start": 9,
      "end": 28,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan ()",
      "start": 28,
      "end": 23,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not hasTanggunganResult] prosesPeminjamanTidakMemilikiTanggungan ()",
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
      "middleLabel": "borrow (isbn)",
      "start": 10,
      "end": 20,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "findCopyBuku (isbn) -> copyBuku",
      "start": 20,
      "end": 21,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isBorrowed ()",
      "start": 20,
      "end": 16,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "showNotifikasiBerhasilPinjam ()",
      "start": 10,
      "end": 11,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[hasTanggungan] showNotifikasiGagalPinjam ()",
      "start": 9,
      "end": 12,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not isValid] showNotifikasiDataTidakValid ()",
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
      "middleLabel": "getDetailBuku ()",
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
"""

        parser = ParseJsonToObjectSeq()
        parser.set_json(json_data)
        parser.parse()

        parsed_value = parser.get_controller_method()

        self.assertEqual(len(parsed_value), 10)

        self.assertEqual(parsed_value[0].get_name(), "login")
        self.assertEqual(len(parsed_value[0].get_parameters()), 2)
        self.assertEqual(parsed_value[0].get_parameters()[0].get_name(), "username")
        self.assertEqual(parsed_value[0].get_parameters()[1].get_name(), "password")

        self.assertEqual(parsed_value[1].get_name(), "HalamanPemrosesanPeminjaman")
        self.assertEqual(len(parsed_value[1].get_parameters()), 0)

        self.assertEqual(parsed_value[2].get_name(), "LihatDetailBuku")
        self.assertEqual(len(parsed_value[2].get_parameters()), 1)
        self.assertEqual(parsed_value[2].get_parameters()[0].get_name(), "isbn")

        self.assertEqual(parsed_value[3].get_name(), "FormProsesPeminjaman")
        self.assertEqual(len(parsed_value[3].get_parameters()), 1)
        self.assertEqual(parsed_value[3].get_parameters()[0].get_name(), "isbn")

        self.assertEqual(parsed_value[4].get_name(), "SubmitProsesPeminjaman")
        self.assertEqual(len(parsed_value[4].get_parameters()), 1)
        self.assertEqual(parsed_value[4].get_parameters()[0].get_name(), "isbn")

        self.assertEqual(parsed_value[5].get_name(), "prosesPeminjamanValidKeanggotaan")
        self.assertEqual(len(parsed_value[5].get_parameters()), 0)

        self.assertEqual(
            parsed_value[6].get_name(), "prosesPeminjamanTidakMemilikiTanggungan"
        )
        self.assertEqual(len(parsed_value[6].get_parameters()), 0)

        self.assertEqual(parsed_value[7].get_name(), "showNotifikasiBerhasilPinjam")
        self.assertEqual(len(parsed_value[7].get_parameters()), 0)

        self.assertEqual(parsed_value[8].get_name(), "showNotifikasiGagalPinjam")
        self.assertEqual(len(parsed_value[8].get_parameters()), 0)

        self.assertEqual(parsed_value[9].get_name(), "showNotifikasiDataTidakValid")
        self.assertEqual(len(parsed_value[9].get_parameters()), 0)

    def test_edge_duplicate_class_name(self):
        json_data = """
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
      "name": "buku2:Buku",
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
      "middleLabel": "[POST] login (username, password)",
      "start": 25,
      "end": 14,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "HalamanPemrosesanPeminjaman ()",
      "start": 25,
      "end": 5,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "LihatDetailBuku (isbn)",
      "start": 25,
      "end": 6,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "getBuku (isbn)",
      "start": 6,
      "end": 3,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "FormProsesPeminjaman (isbn)",
      "start": 25,
      "end": 7,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[POST] SubmitProsesPeminjaman (isbn)",
      "start": 25,
      "end": 8,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isValid (dataAnggota)",
      "start": 8,
      "end": 27,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[isValid] prosesPeminjamanValidKeanggotaan ()",
      "start": 8,
      "end": 9,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan (peminjam)",
      "start": 9,
      "end": 28,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan ()",
      "start": 28,
      "end": 23,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not hasTanggunganResult] prosesPeminjamanTidakMemilikiTanggungan ()",
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
      "middleLabel": "borrow (isbn)",
      "start": 10,
      "end": 20,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "findCopyBuku (isbn) -> copyBuku",
      "start": 20,
      "end": 21,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isBorrowed ()",
      "start": 20,
      "end": 16,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "showNotifikasiBerhasilPinjam ()",
      "start": 10,
      "end": 11,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[hasTanggungan] showNotifikasiGagalPinjam ()",
      "start": 9,
      "end": 12,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not isValid] showNotifikasiDataTidakValid ()",
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
      "middleLabel": "getDetailBuku ()",
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
"""
        with self.assertRaises(Exception) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(str(context.exception), "Duplicate class name!")

    def test_edge_duplicate_method_name(self):
        json_data = """
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
      "name": "listbuku:ListBuku",
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
      "middleLabel": "[POST] login (username, password)",
      "start": 25,
      "end": 14,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "login ()",
      "start": 25,
      "end": 5,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "LihatDetailBuku (isbn)",
      "start": 25,
      "end": 6,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "getBuku (isbn)",
      "start": 6,
      "end": 3,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "FormProsesPeminjaman (isbn)",
      "start": 25,
      "end": 7,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[POST] SubmitProsesPeminjaman (isbn)",
      "start": 25,
      "end": 8,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isValid (dataAnggota)",
      "start": 8,
      "end": 27,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[isValid] prosesPeminjamanValidKeanggotaan ()",
      "start": 8,
      "end": 9,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan (peminjam)",
      "start": 9,
      "end": 28,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan ()",
      "start": 28,
      "end": 23,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not hasTanggunganResult] prosesPeminjamanTidakMemilikiTanggungan ()",
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
      "middleLabel": "borrow (isbn)",
      "start": 10,
      "end": 20,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "findCopyBuku (isbn) -> copyBuku",
      "start": 20,
      "end": 21,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isBorrowed ()",
      "start": 20,
      "end": 16,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "showNotifikasiBerhasilPinjam ()",
      "start": 10,
      "end": 11,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[hasTanggungan] showNotifikasiGagalPinjam ()",
      "start": 9,
      "end": 12,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not isValid] showNotifikasiDataTidakValid ()",
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
      "middleLabel": "getDetailBuku ()",
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
"""
        with self.assertRaises(Exception) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(str(context.exception), "Duplicate method!")

    def test_edge_duplicate_attribute(self):
        json_data = """
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
      "middleLabel": "[POST] login (username, username)",
      "start": 25,
      "end": 14,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "HalamanPemrosesanPeminjaman ()",
      "start": 25,
      "end": 5,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "LihatDetailBuku (isbn)",
      "start": 25,
      "end": 6,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "getBuku (isbn)",
      "start": 6,
      "end": 3,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "FormProsesPeminjaman (isbn)",
      "start": 25,
      "end": 7,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[POST] SubmitProsesPeminjaman (isbn)",
      "start": 25,
      "end": 8,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isValid (dataAnggota)",
      "start": 8,
      "end": 27,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[isValid] prosesPeminjamanValidKeanggotaan ()",
      "start": 8,
      "end": 9,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan (peminjam)",
      "start": 9,
      "end": 28,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "hasTanggungan ()",
      "start": 28,
      "end": 23,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not hasTanggunganResult] prosesPeminjamanTidakMemilikiTanggungan ()",
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
      "middleLabel": "borrow (isbn)",
      "start": 10,
      "end": 20,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "findCopyBuku (isbn) -> copyBuku",
      "start": 20,
      "end": 21,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "isBorrowed ()",
      "start": 20,
      "end": 16,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "showNotifikasiBerhasilPinjam ()",
      "start": 10,
      "end": 11,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[hasTanggungan] showNotifikasiGagalPinjam ()",
      "start": 9,
      "end": 12,
      "type": "CallEdge",
      "signal": false
    },
    {
      "middleLabel": "[not isValid] showNotifikasiDataTidakValid ()",
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
      "middleLabel": "getDetailBuku ()",
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
"""
        with self.assertRaises(Exception) as context:
            parser = ParseJsonToObjectSeq()
            parser.set_json(json_data)
            parser.parse()
        self.assertEqual(str(context.exception), "Duplicate attribute!")
