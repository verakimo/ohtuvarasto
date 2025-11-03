import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

class TestVarastoBranches(unittest.TestCase):
    def test_konstruktori_tilavuus_nolla_menee_elseen(self):
        v = Varasto(0, 0)
        self.assertEqual(v.tilavuus, 0)
        self.assertEqual(v.saldo, 0)

    def test_konstruktori_negatiivinen_saldo_nollataan(self):
        v = Varasto(10, -1)
        self.assertEqual(v.tilavuus, 10)
        self.assertEqual(v.saldo, 0)

    def test_konstruktori_saldo_tasan_tilavuus_menee_elif_haaraan(self):
        v = Varasto(10, 10)
        self.assertEqual(v.tilavuus, 10)
        self.assertEqual(v.saldo, 10)

    def test_konstruktori_saldo_yli_tilavuuden_menee_else_haaraan(self):
        v = Varasto(5, 10)
        self.assertEqual(v.tilavuus, 5)
        self.assertEqual(v.saldo, 5)

    # --- lisaa_varastoon: <0, ==mahtuu, >mahtuu ---
    def test_lisays_negatiivinen_ei_muuta(self):
        v = Varasto(10, 2)
        v.lisaa_varastoon(-3)     # maara < 0 -> varhainen return
        self.assertEqual(v.saldo, 2)

    def test_lisays_tasan_mahtuu_menee_true_haaraan(self):
        v = Varasto(10, 8)
        v.lisaa_varastoon(2)      # maara == mahtuu -> if True
        self.assertEqual(v.saldo, 10)
        self.assertEqual(v.paljonko_mahtuu(), 0)

    def test_lisays_yli_mahdollisen_menee_false_haaraan(self):
        v = Varasto(10, 9)
        v.lisaa_varastoon(5)      # maara > mahtuu -> else, saldo=tilavuus
        self.assertEqual(v.saldo, 10)

    def test_lisays_nolla_sallittu_ei_menya_ylitse(self):
        v = Varasto(10, 5)
        v.lisaa_varastoon(0)      # 0 <= mahtuu -> True-haara
        self.assertEqual(v.saldo, 5)

    # --- ota_varastosta: <0, >saldo, ==saldo, 0 ---
    def test_otto_negatiivinen_palauttaa_nolla_eika_muuta(self):
        v = Varasto(10, 4)
        saatu = v.ota_varastosta(-2)  # maara < 0 -> return 0.0
        self.assertEqual(saatu, 0)
        self.assertEqual(v.saldo, 4)

    def test_otto_yli_saldon_tyhjentaa(self):
        v = Varasto(10, 4)
        saatu = v.ota_varastosta(10)  # maara > saldo -> if True
        self.assertEqual(saatu, 4)
        self.assertEqual(v.saldo, 0)

    def test_otto_tasan_saldo_menee_false_haaraan(self):
        v = Varasto(10, 5)
        saatu = v.ota_varastosta(5)   # maara == saldo -> else-haara
        self.assertEqual(saatu, 5)
        self.assertEqual(v.saldo, 0)

    def test_otto_nolla_ei_muuta(self):
        v = Varasto(10, 5)
        saatu = v.ota_varastosta(0)   # 0 > saldo? False -> else
        self.assertEqual(saatu, 0)
        self.assertEqual(v.saldo, 5)

    def test_str_sisaltaa_saldo_ja_tilaa(self):
        v = Varasto(10, 4)
        s = str(v).lower()
        self.assertIn("saldo", s)
        self.assertTrue("tilaa" in s or "vielä" in s or "mahtuu" in s)

def test_ci_breaker():
    assert False, "tarkoituksella rikki"
