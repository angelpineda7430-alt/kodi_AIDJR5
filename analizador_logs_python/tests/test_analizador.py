import unittest
from analizador import analizar_linea, resumir_eventos


class AnalizadorLogsTests(unittest.TestCase):
    def test_ignora_lineas_vacias(self):
        self.assertIsNone(analizar_linea("   \n", 1))

    def test_evento_valido(self):
        evento = analizar_linea("[INFO] 2025-01-10 Inicio correcto", 1)
        self.assertEqual(evento["nivel"], "INFO")
        self.assertTrue(evento["fecha_valida"])
        self.assertFalse(evento["malformada"])

    def test_fecha_inexistente(self):
        evento = analizar_linea("[ERROR] 2025-02-30 Fecha inválida", 2)
        self.assertFalse(evento["fecha_valida"])
        self.assertTrue(evento["malformada"])

    def test_nivel_desconocido(self):
        evento = analizar_linea("[ALERT] 2025-01-10 Evento", 3)
        self.assertEqual(evento["nivel"], "SIN_CLASIFICAR")
        self.assertTrue(evento["malformada"])

    def test_fecha_con_barras_se_marca_malformada(self):
        evento = analizar_linea("[INFO] 2025/01/10 Wrong date format", 6)
        self.assertTrue(evento["malformada"])
        self.assertIn("fecha ausente o con formato inválido", evento["problemas"])

    def test_resumen(self):
        eventos = [
            analizar_linea("[INFO] 2025-01-10 Inicio", 1),
            analizar_linea("[ERROR] 2025-01-10 Fallo", 2),
        ]
        resumen = resumir_eventos(eventos)
        self.assertEqual(resumen["total"], 2)
        self.assertEqual(resumen["por_nivel"]["INFO"], 1)
        self.assertEqual(resumen["por_nivel"]["ERROR"], 1)


if __name__ == "__main__":
    unittest.main()
